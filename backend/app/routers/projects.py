import re
import shutil
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal, get_db
from app.models import Export, Project, Segment
from app.services.cuts import keep_ranges
from app.services.media import MediaError, probe_duration, project_dir, render_cut
from app.services.transcribe import transcribe

router = APIRouter(prefix="/api/projects", tags=["projects"])


class SegmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    idx: int
    start: float
    end: float
    text: str
    deleted: bool


class ProjectSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    duration: float
    created_at: datetime


class ProjectOut(ProjectSummary):
    segments: list[SegmentOut] = []


class SegmentPatch(BaseModel):
    text: str | None = None
    deleted: bool | None = None


class ExportOut(BaseModel):
    status: str
    duration: float | None = None
    error: str | None = None


def _get_project(db: Session, project_id: str) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    return project


@router.get("", response_model=list[ProjectSummary])
def list_projects(db: Session = Depends(get_db)):
    return db.scalars(select(Project).order_by(Project.created_at.desc())).all()


@router.post("", response_model=ProjectOut, status_code=201)
def create_project(
    name: str = Form(..., min_length=1, max_length=200),
    video: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not (video.content_type or "").startswith("video/"):
        raise HTTPException(415, "Please upload a video file")

    project = Project(name=name.strip(), video_path="", duration=0)
    db.add(project)
    db.flush()

    dest = project_dir(project.id) / f"source{Path(video.filename or 'v.mp4').suffix or '.mp4'}"
    limit, written = get_settings().max_upload_mb * 1024 * 1024, 0
    try:
        with dest.open("wb") as fh:
            while chunk := video.file.read(1024 * 1024):
                written += len(chunk)
                if written > limit:
                    raise HTTPException(413, "Video exceeds the maximum upload size")
                fh.write(chunk)
        duration = probe_duration(dest)
        segments = transcribe(dest, duration)
    except MediaError as exc:
        db.rollback()
        shutil.rmtree(dest.parent, ignore_errors=True)
        raise HTTPException(422, str(exc)) from exc
    except Exception:
        db.rollback()
        shutil.rmtree(dest.parent, ignore_errors=True)
        raise

    project.video_path, project.duration = str(dest), duration
    project.segments = [Segment(idx=i, **s) for i, s in enumerate(segments)]
    project.export = Export(status="none")
    db.commit()
    db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: str, db: Session = Depends(get_db)):
    return _get_project(db, project_id)


@router.get("/{project_id}/video")
def stream_source(project_id: str, db: Session = Depends(get_db)):
    project = _get_project(db, project_id)
    return FileResponse(project.video_path, media_type="video/mp4")


@router.patch("/{project_id}/segments/{segment_id}", response_model=SegmentOut)
def patch_segment(project_id: str, segment_id: int, body: SegmentPatch, db: Session = Depends(get_db)):
    seg = db.scalar(select(Segment).where(Segment.id == segment_id, Segment.project_id == project_id))
    if not seg:
        raise HTTPException(404, "Segment not found")
    if body.text is not None:
        seg.text = body.text
    if body.deleted is not None:
        seg.deleted = body.deleted
    db.commit()
    return seg


def _run_cut(project_id: str) -> None:
    with SessionLocal() as db:
        project = db.get(Project, project_id)
        export = project.export
        try:
            out = project_dir(project_id) / "cut.mp4"
            render_cut(Path(project.video_path), keep_ranges(project.segments), out)
            export.output_path, export.duration = str(out), probe_duration(out)
            export.status, export.error = "done", None
        except Exception as exc:  # noqa: BLE001 - surface any failure to the client
            export.status, export.error = "failed", str(exc)[:500]
        db.commit()


@router.post("/{project_id}/cut", response_model=ExportOut, status_code=202)
def start_cut(project_id: str, tasks: BackgroundTasks, db: Session = Depends(get_db)):
    project = _get_project(db, project_id)
    if not keep_ranges(project.segments):
        raise HTTPException(409, "Nothing left to export: every segment is deleted")
    if project.export is None:
        project.export = Export()
    project.export.status, project.export.error = "processing", None
    db.commit()
    tasks.add_task(_run_cut, project_id)
    return ExportOut(status="processing")


@router.get("/{project_id}/export", response_model=ExportOut)
def export_status(project_id: str, db: Session = Depends(get_db)):
    project = _get_project(db, project_id)
    e = project.export
    return ExportOut(status=e.status if e else "none", duration=e.duration if e else None, error=e.error if e else None)


@router.get("/{project_id}/export/download")
def download_export(project_id: str, db: Session = Depends(get_db)):
    project = _get_project(db, project_id)
    if not project.export or project.export.status != "done":
        raise HTTPException(409, "Export is not ready")
    filename = (re.sub(r"[^A-Za-z0-9._-]+", "_", project.name) or "scriptcut") + ".mp4"
    return FileResponse(project.export.output_path, media_type="video/mp4", filename=filename)
