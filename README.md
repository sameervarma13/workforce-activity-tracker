# Workforce Manager: Contract Worker Monitoring Dashboard

Workforce Manager is a local-first workforce management application designed to monitor and manage contract workers. It features real-time screenshot capture, a backend API for managing employee sessions, and a user-friendly dashboard to review worker activity.

## Features

- Periodic screenshot capture for contract worker activity
- Organized local storage of screenshot data
- Streamlit-based dashboard to review worker sessions
- FastAPI backend for managing employees and session data
- UI to create and manage contract worker profiles

## Repository Structure

```
.
├── main.py                # FastAPI backend server
├── dashboard.py           # Streamlit dashboard to visualize worker activity
├── employee_ui.py         # UI module for creating and managing employee profiles
├── local_agent.py         # Screenshot capture agent (run locally on worker device)
├── screenshots/           # Local folder for storing captured screenshots
```

## Getting Started

1. **Install dependencies**
   ```
   pip install fastapi streamlit uvicorn opencv-python
   ```

2. **Run the backend server**
   ```
   uvicorn main:app --reload
   ```

3. **Launch the dashboard**
   ```
   streamlit run dashboard.py
   ```

4. **Start the screenshot agent**
   ```
   python local_agent.py
   ```

## Usage Notes

- Screenshots are saved to the `screenshots/` folder.
- Designed for local environments and trusted networks.
- Extendable to include login tracking, permission flags, and remote upload for enterprise use.

