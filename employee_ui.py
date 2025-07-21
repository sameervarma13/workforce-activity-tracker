import streamlit as st
import requests
import datetime
import pytz
import local_agent  

API_URL = "http://localhost:8000"
EMPLOYEE_ID = "emp-1"

# Format UTC to Pacific
def format_time(utc_str):
    utc_dt = datetime.datetime.fromisoformat(utc_str)
    pacific = pytz.timezone("US/Pacific")
    return utc_dt.astimezone(pacific).strftime("%I:%M:%S %p")

st.set_page_config(page_title="Sameer's Employee Portal", layout="centered")
st.title("Sameer's Employee Dashboard")

# ==========================
# Time Logs & Clock Status
# ==========================
time_logs = requests.get(f"{API_URL}/time").json()
emp_logs = [log for log in time_logs if log["employeeId"] == EMPLOYEE_ID]
emp_logs.sort(key=lambda x: x["timestamp"], reverse=True)

is_clocked_in = emp_logs and emp_logs[0]["action"] == "start"

st.markdown("### Status")
if is_clocked_in:
    st.success(f"Clocked In at {format_time(emp_logs[0]['timestamp'])}")
else:
    st.warning("Not Clocked In")

# ==========================
# Display project/task
# ==========================
projects = requests.get(f"{API_URL}/project").json()
tasks = requests.get(f"{API_URL}/task").json()

employee_projects = [p for p in projects if p.get("employeeId") == EMPLOYEE_ID]
employee_tasks = [t for t in tasks if t.get("employeeId") == EMPLOYEE_ID]

st.markdown("### Current Project & Task")

if employee_projects:
    latest_project = employee_projects[-1]
    st.write(f"Project: {latest_project['name']}")
else:
    latest_project = None
    st.write("Project: N/A")

if employee_tasks:
    latest_task = employee_tasks[-1]
    st.write(f"Task: {latest_task['name']}")
else:
    latest_task = None
    st.write("Task: N/A")

# ==========================
# Clock in/out buttons
# ==========================
st.markdown("### Clock Actions")

if not latest_project or not latest_task:
    st.warning("No available project and task. Ask your manager to assign one.")
else:
    if not is_clocked_in:
        if st.button("Clock In"):
            requests.post(f"{API_URL}/time", json={
                "employeeId": EMPLOYEE_ID,
                "projectId": latest_project["id"],
                "taskId": latest_task["id"],
                "action": "start"
            })
            local_agent.EMPLOYEE_ID = EMPLOYEE_ID
            local_agent.start()
            st.rerun()
    else:
        if st.button("Clock Out"):
            requests.post(f"{API_URL}/time", json={
                "employeeId": EMPLOYEE_ID,
                "projectId": latest_project["id"],
                "taskId": latest_task["id"],
                "action": "stop"
            })
            local_agent.stop()
            st.rerun()

# ==========================
# Time Log History
# ==========================
st.markdown("### Time Log History")
if emp_logs:
    for log in emp_logs:
        action = "Clocked In" if log["action"] == "start" else "Clocked Out"
        st.write(f"{action} at {format_time(log['timestamp'])}")
else:
    st.info("No time logs available.")
