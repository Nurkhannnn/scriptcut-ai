from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.config import get_settings
from app.database import engine
from app.routers import projects

app = FastAPI(title="ScriptCut AI")
app.include_router(projects.router)


@app.get("/api/health", tags=["meta"])
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}


# Serve the built React app from the same process
static_dir = Path(get_settings().static_dir).resolve()
if (static_dir / "index.html").exists():
    if (static_dir / "assets").exists():
        app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def spa(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(404)
        candidate = (static_dir / full_path).resolve()
        if candidate.is_file() and static_dir in candidate.parents:
            return FileResponse(candidate)
        return FileResponse(static_dir / "index.html")
