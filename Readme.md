# 🚀 Process Controller & Monitor V1.0.0 - tj
> Author: Joeneil Taguan  
> Linkedin: https://www.linkedin.com/in/jstaguan/

# 📝 Description
A dual-component system designed to execute Windows batch files and monitor endpoint health with built-in retry logic.
This project consists of a FastAPI backend (api.py) that handles the heavy lifting of process execution and network polling, and a HoloViz Panel frontend (app.py) providing a user-friendly dashboard to trigger tasks.

# Workflow:

User enters a .bat path and a health check URL in the Dashboard.

The Dashboard sends a request to the API.

The API executes the .bat, waits for a custom delay, then checks the endpoint 5 times (every 10 seconds) before reporting a final status.

# 📂 Folder Structure
Plaintext

project-root/
│
├── api.py              # FastAPI Backend (Port 8520)
├── app.py              # Panel HoloViz Dashboard (Port 8510)
├── run.bat             # Master Launcher Script
├── requirements.txt    # Python Dependencies
└── README.md           # Documentation

# ⚙️ How to Activate

## Prerequisites
Python 3.9 or higher installed.

Windows OS (required for .bat execution via the API).

## Installation
Clone or download this repository.

Open a terminal in the project folder and install dependencies:

Bash

> pip install -r requirements.txt

Launching the Services
Simply double-click the run.bat file in the root directory.

## Two new command prompt windows will open.

Your default web browser will automatically open the Dashboard at 
> http://localhost:8565.

## Manual Execution
If you prefer to run them manually:

> API: python api.py

> App: panel serve app.py --port 8510 --show

Note for api.py: Make sure you update the uvicorn.run line at the bottom of your api.py to use port=8520 so it matches the dashboard's configuration!

## Activate in Windows Upon Start Up using Task Scheduler (Advanced)

1. Open the Start Menu, type Task Scheduler, and hit Enter.

2. On the right-hand panel, click Create Basic Task...

3. Name: Give it a name like "System Controller Launcher" and click Next.

4. Trigger: Select When I log on and click Next.

5. Action: Select Start a program and click Next.

6. Program/script: Click Browse and select your run.bat file.

7. Start in (Optional but highly recommended): Type the path to the folder that contains your run.bat (e.g., C:\scripts\). If you skip this, Windows might try to run it in the wrong directory, causing errors.

8. Click Finish.

### (Optional Delay): If you want to delay it by a few seconds:

Find your new task in the middle list, right-click it, and choose Properties.

Go to the Triggers tab, select the trigger, and click Edit.

Check the box for Delay task for: and set it to 30 seconds or 1 minute.


## Autho Information



# ⚠️ Legal Disclaimer & Terms of Use
For Educational Purposes Only This application, including its source code and associated scripts, is provided strictly for educational and learning purposes. It was developed as a proof-of-concept to demonstrate process management and endpoint monitoring using Python, FastAPI, and Panel.

Assumption of Risk By downloading, configuring, or executing this software, you acknowledge and agree that you are solely responsible for how it is used. This application has the capability to execute system-level background processes and batch scripts (.bat). Misconfiguration, malicious scripts, or improper use of these features can lead to unintended system behavior, resource exhaustion, or data loss. Please review the code carefully and ensure you fully understand the contents of any .bat file before executing it through this interface.

"As Is" Condition The developer provides this software on an "AS IS" and "AS AVAILABLE" basis. There are no warranties of any kind, either express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, or non-infringement. The developer makes no guarantees regarding the stability, security, or reliability of the application.

Limitation of Liability Under no circumstances shall the developer or any contributors be held liable for any direct, indirect, incidental, special, exemplary, or consequential damages. This includes, but is not limited to, system downtime, loss of data, loss of profits, or unauthorized system access arising in any way out of the use, inability to use, or modification of this software, even if advised of the possibility of such damage.