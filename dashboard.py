import requests
import streamlit as st
from datetime import datetime
import pytz

API_URL = "http://localhost:8000"
pacific = pytz.timezone("America/Los_Angeles")

def format_timestamp(ts):
    return datetime.fromtimestamp(ts, pacific).strftime("%I:%M:%S %p")

def get_data():
    employees = requests.get(f"{API_URL}/employee").json()
    time_logs = requests.get(f"{API_URL}/time").json()
    screenshots = requests.get(f"{API_URL}/screenshot").json()
    projects = requests.get(f"{API_URL}/project").json()
    tasks = requests.get(f"{API_URL}/task").json()
    return employees, time_logs, screenshots, projects, tasks

def submit_project(name, employee_id):
    requests.post(f"{API_URL}/project", json={"name": name, "employeeId": employee_id})

def submit_task(project_id, task_name, employee_id):
    requests.post(f"{API_URL}/task", json={"projectId": project_id, "name": task_name, "employeeId": employee_id})

def submit_employee(identifier, name):
    requests.post(f"{API_URL}/employee", json={"identifier": identifier, "name": name})

st.title("Workforce Monitoring Dashboard")

# Create employee section
st.subheader("Create New Employee")
new_identifier = st.text_input("Employee Identifier (e.g., E003)")
new_name = st.text_input("Employee Name")
if st.button("Add Employee"):
    if new_identifier.strip() and new_name.strip():
        submit_employee(new_identifier.strip(), new_name.strip())
        st.success(f"Employee '{new_name}' added!")
        st.rerun()
    else:
        st.warning("Both fields are required.")

# Load data
employees, time_logs, screenshots, projects, tasks = get_data()

employee_dict = {e["id"]: e for e in employees}
project_dict = {p["id"]: p["name"] for p in projects}
task_dict = {t["id"]: t for t in tasks}

selected_employee = st.selectbox(
    "Select Employee", options=employees, format_func=lambda x: f'{x["name"]} ({ "Inactive" if not x["active"] else "Active" })'
)

if selected_employee:
    eid = selected_employee["id"]
    is_active = selected_employee["active"]

    st.subheader("Projects and Tasks")
    relevant_projects = [p for p in projects if p.get("employeeId") == eid]
    relevant_project_ids = {p["id"] for p in relevant_projects}
    relevant_tasks = [t for t in tasks if t["projectId"] in relevant_project_ids and t.get("employeeId") == eid]

    if relevant_tasks:
        for t in relevant_tasks:
            proj_name = project_dict.get(t["projectId"], "Unknown")
            st.write(f"{proj_name} → {t['name']}")
    else:
        st.write("No tasks available.")

    if not is_active:
        st.warning("This employee is inactive. You cannot add new projects or tasks.")
    else:
        st.subheader("Add Project")
        new_project_name = st.text_input("New Project Name")
        if st.button("Create Project"):
            if new_project_name.strip():
                submit_project(new_project_name, eid)
                st.success("Project created!")
                st.rerun()
            else:
                st.warning("Project name cannot be empty.")

        st.subheader("Add Task")
        filtered_projects = [p for p in projects if p.get("employeeId") == eid]
        if filtered_projects:
            selected_proj = st.selectbox("Assign to Project", filtered_projects, format_func=lambda x: x["name"])
            new_task_name = st.text_input("New Task Name")
            if st.button("Create Task"):
                if new_task_name.strip():
                    submit_task(selected_proj["id"], new_task_name, eid)
                    st.success("Task created!")
                    st.rerun()
                else:
                    st.warning("Task name cannot be empty.")
        else:
            st.warning("No projects available for this employee. Add a project first.")

    st.subheader("Time Logs")
    logs = [l for l in time_logs if l["employeeId"] == eid]
    logs.sort(key=lambda x: x["timestamp"], reverse=True)
    for l in logs:
        ts = datetime.fromisoformat(l["timestamp"]).astimezone(pacific).strftime("%I:%M:%S %p")
        st.write(f'{selected_employee["name"]} {l["action"].capitalize()} at {ts}')

    st.subheader("Screenshots")
    user_screenshots = [s for s in screenshots if s["employeeId"] == eid]
    user_screenshots.sort(key=lambda x: x["timestamp"], reverse=True)
    for s in user_screenshots[:5]:
        try:
            ts = format_timestamp(s["timestamp"])
            img_url = f"{API_URL}/screenshot/{s['id']}/image"
            st.image(img_url, caption=f"{ts}", width=300)
        except Exception as e:
            st.write(f"Error displaying image: {e}")
