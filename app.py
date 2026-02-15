# APP: Updatime Monitiror App & App Activation Controller
# Author: Joeneil Taguan
# Linkedin: https://www.linkedin.com/in/jstaguan/

import panel as pn
import httpx
import asyncio
import pandas as pd
from datetime import datetime
import io

pn.extension(design='material')

history_data = []

# --- UI Components ---
title = pn.pane.Markdown("# 🚀 System Controller", styles={'margin-bottom': '20px'})

api_url_input = pn.widgets.TextInput(name="Windows API Address", value="http://host.docker.internal:8565")
bat_input = pn.widgets.TextInput(name="Path to run.bat", value="D:\\myApps\\app\\run.bat")
endpoint_input = pn.widgets.TextInput(name="Target Endpoint URL", value="http://127.0.0.1:8587")
delay_input = pn.widgets.IntInput(name="Startup Delay (Seconds)", value=10, start=0)

progress_bar = pn.widgets.Progress(name='Progress', value=0, bar_color='info', width=560, visible=False)
timer_pane = pn.pane.Markdown("", styles={'font-size': '14pt', 'color': '#2c3e50'})
result_pane = pn.pane.Alert("System Ready.", alert_type="info")
status_indicator = pn.indicators.LoadingSpinner(value=False, size=30, visible=False)

check_status_btn = pn.widgets.Button(name="🔍 Check Endpoint Status", button_type="default")
run_process_btn = pn.widgets.Button(name="⚡ Run .bat & Monitor", button_type="primary")
clear_btn = pn.widgets.Button(name="🗑️ Clear Log", button_type="light", width=100)

history_table = pn.widgets.DataFrame(pd.DataFrame(columns=['Timestamp', 'File', 'Endpoint', 'Status']), width=600, height=250)

def add_to_history(file, endpoint, status):
    history_data.append({'Timestamp': datetime.now().strftime("%H:%M:%S"), 'File': file.split('\\')[-1], 'Endpoint': endpoint, 'Status': status})
    history_table.value = pd.DataFrame(history_data)

clear_btn.on_click(lambda event: [history_data.clear(), setattr(history_table, 'value', pd.DataFrame(columns=['Timestamp', 'File', 'Endpoint', 'Status']))])

# --- Logic ---
async def check_endpoint_status(event=None):
    status_indicator.visible = True
    try:
        async with httpx.AsyncClient() as client:
            # Ask the Windows API to do the pinging
            res = await client.post(f"{api_url_input.value}/check-endpoint", json={"endpoint": endpoint_input.value})
            data = res.json()
            if data.get("is_alive"):
                result_pane.object = f"✅ **Live:** Windows API successfully reached {endpoint_input.value}."
                result_pane.alert_type = "success"
            else:
                result_pane.object = f"⚠️ **Status:** Windows API says it is offline. {data.get('error', '')}"
                result_pane.alert_type = "warning"
    except Exception as e:
        result_pane.object = f"❌ **Cannot reach Windows API:** {e}"
        result_pane.alert_type = "danger"
    finally:
        status_indicator.visible = False

async def run_bat_process(event=None):
    run_process_btn.disabled = True
    progress_bar.visible = True
    progress_bar.value = 0
    
    api_base = api_url_input.value
    file_path = bat_input.value
    target_url = endpoint_input.value
    
    # 1. SEND JSON TO RUN THE BAT
    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"{api_base}/start-process", json={"bat_path": file_path})
    except Exception as e:
        result_pane.object = f"❌ **Windows API Unreachable:** Ensure api.py is running on {api_base}. Error: {e}"
        result_pane.alert_type = "danger"
        run_process_btn.disabled = False
        return

    result_pane.object = "🚀 **Instruction Sent.** Waiting for initial startup delay..."
    result_pane.alert_type = "warning"
    
    # 2. UI COUNTDOWN
    for remaining in range(delay_input.value, 0, -1):
        timer_pane.object = f"⏳ **Checking in:** {remaining}s"
        await asyncio.sleep(1)
    
    # 3. ASK WINDOWS TO POLL ENDPOINT
    final_status = "Failed"
    for i in range(1, 6):
        progress_bar.value = i * 20
        timer_pane.object = f"🔄 **Attempt {i}/5...** Asking Windows API to check status."
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{api_base}/check-endpoint", json={"endpoint": target_url}, timeout=5.0)
                if res.json().get("is_alive"):
                    # Success formatting with clickable link!
                    result_pane.object = f"✨ **SUCCESS:** App is active! <br> 👉 **[Click here to open {target_url}]({target_url})**"
                    result_pane.alert_type = "success"
                    final_status = "Success"
                    break
        except Exception:
            pass
            
        if i < 5: await asyncio.sleep(10)

    if final_status == "Failed":
        result_pane.object = "⚠️ **Timeout:** Windows API could not reach the target app after 5 retries."
        result_pane.alert_type = "danger"
    
    add_to_history(file_path, target_url, final_status)
    timer_pane.object = ""
    progress_bar.visible = False
    run_process_btn.disabled = False

check_status_btn.on_click(check_endpoint_status)
run_process_btn.on_click(run_bat_process)

# --- Layout ---
layout = pn.Column(
    title,
    pn.Card(
        api_url_input, bat_input, endpoint_input, delay_input,
        pn.Row(check_status_btn, run_process_btn, status_indicator),
        title="Configuration", collapsible=False
    ),
    timer_pane, progress_bar, result_pane,
    pn.Row(pn.pane.Markdown("### 🕒 Execution History"), pn.Spacer(), clear_btn),
    history_table, width=600, align='center'
)

layout.servable()