from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="ScriptCut AI API")

class CutRange(BaseModel):
    start_time: float
    end_time: float

class Project(BaseModel):
    id: str
    title: str
    transcript: str
    cuts: List[CutRange] = []

# In-memory store for initial iteration
projects_db = {
    "proj-1": Project(
        id="proj-1",
        title="Sample Podcast Episode",
        transcript="Hello and welcome to our podcast. [CUT THIS PART] Today we talk about AI video editing.",
        cuts=[CutRange(start_time=12.5, end_time=18.0)]
    )
}

@app.get("/")
def read_root():
    return {"status": "ok", "app": "ScriptCut AI"}

@app.get("/api/projects")
def list_projects():
    return list(projects_db.values())

@app.get("/api/projects/{project_id}")
def get_project(project_id: str):
    return projects_db.get(project_id, {"error": "Project not found"})
