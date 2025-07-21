# local_agent.py

import time
import uuid
import requests
import platform
import os
import threading
from datetime import datetime
from PIL import ImageGrab

API_URL = "http://localhost:8000"
EMPLOYEE_ID = "emp-1"  # Set this externally when calling `start`

running = False
thread = None

def take_screenshots():
    global running
    while running:
        try:
            screenshot = ImageGrab.grab()
            filename = f"{uuid.uuid4()}.png"
            screenshot.save(filename, "PNG")

            with open(filename, "rb") as img_file:
                response = requests.post(
                    f"{API_URL}/screenshot",
                    data={
                        "employeeId": EMPLOYEE_ID,
                        "timestamp": int(time.time()),
                        "permissionsGranted": True,
                        "ip": "",  # Optional: populate dynamically
                        "mac": "",  # Optional: populate dynamically
                        "os": platform.system()
                    },
                    files={"screenshot": img_file}
                )

            os.remove(filename)
            print("[✓] Screenshot uploaded at", datetime.now().strftime("%I:%M:%S %p"))

        except Exception as e:
            print("[!] Error:", e)

        time.sleep(10)

def start():
    global running, thread
    if not running and EMPLOYEE_ID:
        running = True
        thread = threading.Thread(target=take_screenshots)
        thread.start()
        print("[✓] Screenshot agent started")

def stop():
    global running
    if running:
        running = False
        print("[✓] Screenshot agent stopped")
