from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import SessionLocal, init_db, ProjectDB

app = FastAPI(title="ScriptCut AI API")

# Инициализация базы данных при старте
@app.on_event("startup")
def startup_event():
    init_db()
    # Сидим базовые данные, если пусто
    db = SessionLocal()
    if not db.query(ProjectDB).filter(ProjectDB.id == "proj-1").first():
        sample = ProjectDB(
            id="proj-1",
            title="Sample Podcast Episode",
            transcript="Hello and welcome to our podcast. Today we talk about AI video editing."
        )
        db.add(sample)
        db.commit()
    db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProjectResponse(BaseModel):
    id: str
    title: str
    transcript: str

    class Config:
        orm_mode = True

@app.get("/")
def read_root():
    return {"status": "ok", "app": "ScriptCut AI"}

@app.get("/api/projects", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(ProjectDB).all()

@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
def get_project(project_id: str):
    return projects_db.get(project_id, {"error": "Project not found"})
