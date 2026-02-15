# APP: Updatime Monitiror App & App Activation Controller
# Author: Joeneil Taguan
# Linkedin: https://www.linkedin.com/in/jstaguan/

import subprocess
import httpx
import os
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

class RunConfig(BaseModel):
    bat_path: str

class CheckConfig(BaseModel):
    endpoint: str

def execute_bat(bat_path: str):
    print(f"Target Path: {bat_path}")
    bat_dir = os.path.dirname(bat_path)
    bat_file = os.path.basename(bat_path)
    try:
        # Launching the visible Windows terminal
        cmd = f'start "{bat_file}" /d "{bat_dir}" cmd /k "{bat_file}"'
        subprocess.Popen(cmd, shell=True)
        print(f"✅ Executed: {bat_file}")
    except Exception as e:
        print(f"❌ Execution failed: {e}")

@app.post("/start-process")
async def start_process(config: RunConfig, background_tasks: BackgroundTasks):
    # Triggers the bat file in the background immediately
    background_tasks.add_task(execute_bat, config.bat_path)
    return {"status": "success", "message": f"Triggered {config.bat_path}"}

@app.post("/check-endpoint")
async def check_endpoint(config: CheckConfig):
    # The Windows machine does the pinging locally!
    try:
        with httpx.Client() as client:
            response = client.get(config.endpoint, timeout=5.0)
            if response.status_code == 200:
                return {"is_alive": True, "status_code": 200}
            return {"is_alive": False, "status_code": response.status_code}
    except Exception as e:
        return {"is_alive": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8565)