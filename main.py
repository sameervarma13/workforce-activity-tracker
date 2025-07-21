from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
import os
from fastapi.responses import FileResponse


app = FastAPI()

# In-memory data stores
from datetime import datetime

# Dummy Data
employees = {
    "emp-1": {"id": "emp-1", "identifier": "E001", "name": "Sameer", "active": True},
    "emp-2": {"id": "emp-2", "identifier": "E002", "name": "Bob", "active": False}
}

projects = {
    "proj-1": {"id": "proj-1", "name": "Dashboard Redesign", "employeeId": "emp-1"},
    "proj-2": {"id": "proj-2", "name": "API Integration", "employeeId": "emp-1"}
}

tasks = {
    "task-1": {"id": "task-1", "projectId": "proj-1", "name": "UI Revamp", "employeeId": "emp-1"},
    "task-2": {"id": "task-2", "projectId": "proj-2", "name": "POST Endpoint Refactor", "employeeId": "emp-1"}
}


time_logs = {
    "log-1": {
        "id": "log-1",
        "employeeId": "emp-2",
        "projectId": "proj-1",
        "taskId": "task-1",
        "action": "start",
        "timestamp": datetime.utcnow().isoformat()
    },
    "log-2": {
        "id": "log-2",
        "employeeId": "emp-2",
        "projectId": "proj-1",
        "taskId": "task-1",
        "action": "stop",
        "timestamp": datetime.utcnow().isoformat()
    }
}

screenshots = {}  # Leave empty or add if needed


# Models
class EmployeeCreate(BaseModel):
    identifier: str
    name: str

class ProjectCreate(BaseModel):
    name: str

class TaskCreate(BaseModel):
    projectId: str
    name: str

class TimeLogCreate(BaseModel):
    employeeId: str
    projectId: str
    taskId: str
    action: str  # "start" or "stop"

class ProjectCreate(BaseModel):
    name: str
    employeeId: str  # Add this field

class TaskCreate(BaseModel):
    projectId: str
    name: str
    employeeId: str  # Add this field


# =====================
# POST Endpoints
# =====================

@app.post("/employee")
def create_employee(emp: EmployeeCreate):
    eid = str(uuid.uuid4())
    employees[eid] = {
        "id": eid,
        "identifier": emp.identifier,
        "name": emp.name,
        "active": True
    }
    return employees[eid]

@app.patch("/employee/{employee_id}")
def deactivate_employee(employee_id: str):
    if employee_id in employees:
        employees[employee_id]["active"] = False
        return employees[employee_id]
    return {"error": "Employee not found"}

@app.post("/project")
def create_project(proj: ProjectCreate):
    pid = str(uuid.uuid4())
    projects[pid] = {
        "id": pid,
        "name": proj.name,
        "employeeId": proj.employeeId  # Store it
    }
    return projects[pid]

@app.post("/task")
def create_task(task: TaskCreate):
    tid = str(uuid.uuid4())
    tasks[tid] = {
        "id": tid,
        "projectId": task.projectId,
        "name": task.name,
        "employeeId": task.employeeId  # Store it
    }
    return tasks[tid]

@app.post("/time")
def clock_time(t: TimeLogCreate):
    eid = str(uuid.uuid4())
    time_logs[eid] = {
        "id": eid,
        "employeeId": t.employeeId,
        "projectId": t.projectId,
        "taskId": t.taskId,
        "action": t.action,
        "timestamp": datetime.utcnow().isoformat()
    }
    return time_logs[eid]


UPLOAD_DIR = "screenshots"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/screenshot")
async def upload_screenshot(
    employeeId: str = Form(...),
    timestamp: int = Form(...),
    permissionsGranted: bool = Form(...),
    ip: Optional[str] = Form(None),
    mac: Optional[str] = Form(None),
    os_info: Optional[str] = Form(None, alias="os"),  # Changed parameter name to avoid conflict
    screenshot: UploadFile = File(...)
):
    sid = str(uuid.uuid4())
    filename = f"{sid}.png"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(await screenshot.read())

    screenshots[sid] = {
        "id": sid,
        "employeeId": employeeId,
        "timestamp": timestamp // 1000,
        "permissionsGranted": permissionsGranted,
        "ip": ip,
        "mac": mac,
        "os": os_info,  # Use the renamed parameter
        "filename": filename
    }
    return screenshots[sid]

# =====================
# GET Endpoints
# =====================

@app.get("/employee")
def list_employees():
    return list(employees.values())

@app.get("/project")
def list_projects():
    return list(projects.values())

@app.get("/task")
def list_tasks():
    return list(tasks.values())

@app.get("/time")
def list_time_logs():
    return list(time_logs.values())

@app.get("/screenshot")
def list_screenshots():
    return list(screenshots.values())

@app.get("/screenshot/{screenshot_id}/image")
def get_screenshot_image(screenshot_id: str):
    if screenshot_id in screenshots:
        filename = screenshots[screenshot_id]["filename"]
        filepath = os.path.join(UPLOAD_DIR, filename)
        return FileResponse(filepath, media_type="image/png")
    return {"error": "Screenshot not found"}