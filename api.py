# APP: Updatime Monitiror App & App Activation Controller
# Author: Joeneil Taguan
# Linkedin: https://www.linkedin.com/in/jstaguan/

import subprocess
import time
import httpx
import os
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

class RunConfig(BaseModel):
    bat_path: str
    endpoint: str
    delay_seconds: int

def run_and_monitor(config: RunConfig):
    # Extract directory and filename
    bat_dir = os.path.dirname(config.bat_path)
    bat_file = os.path.basename(config.bat_path)

    try:
        # Construct the command to open a NEW window
        # start "Title" /d "Directory" cmd /k "filename"
        launch_cmd = f'start "{bat_file}" /d "{bat_dir}" cmd /k "{bat_file}"'
        
        subprocess.Popen(launch_cmd, shell=True)
        print(f"✅ New terminal opened for: {bat_file}")
    except Exception as e:
        print(f"❌ Failed to launch .bat: {e}")
        return

    # Wait for the app to warm up
    print(f"🕒 Waiting {config.delay_seconds}s before checking {config.endpoint}...")
    time.sleep(config.delay_seconds)

    # Retry Loop
    max_retries = 5
    retry_interval = 10

    with httpx.Client() as client:
        for attempt in range(1, max_retries + 1):
            try:
                response = client.get(config.endpoint, timeout=5.0)
                if response.status_code == 200:
                    print(f"✨ SUCCESS: {bat_file} is active at {config.endpoint}")
                    return
            except httpx.RequestError:
                print(f"🔄 Attempt {attempt}/5: {bat_file} not ready yet...")
            
            if attempt < max_retries:
                time.sleep(retry_interval)

    print(f"⚠️ ALERT: {bat_file} failed to respond after {max_retries} retries.")

@app.post("/start-process")
async def start_process(config: RunConfig, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_and_monitor, config)
    return {"message": "Instruction sent. Check new terminal window for logs."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8565)