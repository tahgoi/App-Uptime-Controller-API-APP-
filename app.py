# APP: Updatime Monitiror App & App Activation Controller
# Author: Joeneil Taguan
# Linkedin: https://www.linkedin.com/in/jstaguan/

import panel as pn
import httpx
import asyncio
import pandas as pd
from datetime import datetime
import io
import webbrowser  # <-- Added import here

pn.extension(design='material')

# --- State Management ---
history_data = []

# --- UI Components ---
title = pn.pane.Markdown("# 🚀 System Controller", styles={'margin-bottom': '20px'})

bat_input = pn.widgets.TextInput(name="Path to run.bat", value="C:\\myapps\\app\\run.bat")
endpoint_input = pn.widgets.TextInput(name="Endpoint URL", value="http://localhost:8565")
delay_input = pn.widgets.IntInput(name="Startup Delay (Seconds)", value=10, start=0)

progress_bar = pn.widgets.Progress(name='Progress', value=0, bar_color='info', width=560, visible=False)
timer_pane = pn.pane.Markdown("", styles={'font-size': '14pt', 'color': '#2c3e50'})
result_pane = pn.pane.Alert("System Ready.", alert_type="info")
status_indicator = pn.indicators.LoadingSpinner(value=False, size=30, visible=False)

check_status_btn = pn.widgets.Button(name="🔍 Check Endpoint Status", button_type="default")
run_process_btn = pn.widgets.Button(name="⚡ Run .bat & Monitor", button_type="primary")
clear_btn = pn.widgets.Button(name="🗑️ Clear Log", button_type="light", width=100)

def get_csv_data():
    if not history_data:
        return io.BytesIO(b"No data")
    df = pd.DataFrame(history_data)
    return io.BytesIO(df.to_csv(index=False).encode())

export_btn = pn.widgets.FileDownload(
    callback=get_csv_data, filename="execution_log.csv", label="📥 Export CSV", button_type="success", width=150
)

history_table = pn.widgets.DataFrame(
    pd.DataFrame(columns=['Timestamp', 'File', 'Endpoint', 'Status']),
    name='Execution History', width=600, height=250, autosize_mode='fit_columns'
)

def add_to_history(file, endpoint, status):
    new_entry = {
        'Timestamp': datetime.now().strftime("%H:%M:%S"),
        'File': file.split('\\')[-1],
        'Endpoint': endpoint,
        'Status': status
    }
    history_data.append(new_entry)
    history_table.value = pd.DataFrame(history_data)

def clear_history(event):
    history_data.clear()
    history_table.value = pd.DataFrame(columns=['Timestamp', 'File', 'Endpoint', 'Status'])

clear_btn.on_click(clear_history)

async def check_endpoint_status(event=None):
    status_indicator.visible = True
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint_input.value, timeout=5.0)
            if response.status_code == 200:
                result_pane.object = "✅ **Live:** Endpoint is responding."
                result_pane.alert_type = "success"
            else:
                result_pane.object = f"⚠️ **Status:** Code {response.status_code}"
                result_pane.alert_type = "warning"
    except Exception:
        result_pane.object = "❌ **Offline:** Cannot reach endpoint."
        result_pane.alert_type = "danger"
    finally:
        status_indicator.visible = False

async def run_bat_process(event=None):
    run_process_btn.disabled = True
    progress_bar.visible = True
    progress_bar.value = 0
    file_path = bat_input.value
    target_url = endpoint_input.value
    
    try:
        async with httpx.AsyncClient() as client:
            await client.post("http://127.0.0.1:8565/start-process", 
                              json={"bat_path": file_path, "endpoint": target_url, "delay_seconds": delay_input.value})
    except Exception as e:
        result_pane.object = f"❌ **API Error:** {e}"
        result_pane.alert_type = "danger"
        add_to_history(file_path, target_url, "API Connection Failed")
        run_process_btn.disabled = False
        return

    result_pane.object = "🚀 **Process Triggered.** Waiting for startup..."
    result_pane.alert_type = "warning"
    
    for remaining in range(delay_input.value, 0, -1):
        timer_pane.object = f"⏳ **Checking in:** {remaining}s"
        await asyncio.sleep(1)
    
    final_status = "Failed"
    for i in range(1, 6):
        progress_bar.value = i * 20
        timer_pane.object = f"🔄 **Attempt {i}/5...**"
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(target_url, timeout=3.0)
                if res.status_code == 200:
                    result_pane.object = "✨ **SUCCESS:** App is active! Opening browser..."
                    result_pane.alert_type = "success"
                    final_status = "Success"
                    
                    # <-- The minimal change to open the browser
                    webbrowser.open(target_url) 
                    
                    break
        except:
            pass
        if i < 5: await asyncio.sleep(10)

    if final_status == "Failed":
        result_pane.object = "⚠️ **Timeout:** App failed to respond."
        result_pane.alert_type = "danger"
    
    add_to_history(file_path, target_url, final_status)
    timer_pane.object = ""
    progress_bar.visible = False
    run_process_btn.disabled = False

check_status_btn.on_click(check_endpoint_status)
run_process_btn.on_click(run_bat_process)

layout = pn.Column(
    title,
    pn.Card(
        bat_input, endpoint_input, delay_input,
        pn.Row(check_status_btn, run_process_btn, status_indicator),
        title="Configuration", collapsible=False
    ),
    timer_pane, progress_bar, result_pane,
    pn.Row(pn.pane.Markdown("### 🕒 Execution History"), pn.Spacer(), export_btn, clear_btn),
    history_table, width=600, align='center'
)

layout.servable()