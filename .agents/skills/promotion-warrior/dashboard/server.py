import os
import sys
import yaml
import json
import asyncio
import subprocess
import re
from datetime import datetime
from typing import Optional, List, Dict
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Promotion Warrior Dashboard")

# Paths
BASE_DIR = "/Users/han/.agents/skills/promotion-warrior"
LOG_FILE = "/tmp/dating-monitor.log"
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
PLIST_LABEL = "com.han.promotion-warrior"
PLIST_PATH = os.path.expanduser(f"~/Library/LaunchAgents/{PLIST_LABEL}.plist")

# Setup templates
templates = Jinja2Templates(directory=os.path.join(DASHBOARD_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(DASHBOARD_DIR, "static")), name="static")

# Helpers
def get_last_log_time():
    if not os.path.exists(LOG_FILE):
        return None
    return datetime.fromtimestamp(os.path.getmtime(LOG_FILE)).isoformat()

def is_script_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "enhanced-check.sh"]).decode()
        return len(output.strip()) > 0
    except:
        return False

def check_launchd():
    try:
        output = subprocess.check_output(["launchctl", "list"]).decode()
        return PLIST_LABEL in output
    except:
        return False

def get_launchd_interval():
    if not os.path.exists(PLIST_PATH):
        return None
    try:
        with open(PLIST_PATH, 'r') as f:
            content = f.read()
            match = re.search(r'<key>StartInterval</key>\s*<integer>(\d+)</integer>', content)
            if match:
                return int(match.group(1))
    except:
        pass
    return None

def parse_markdown_yaml(file_path: str, marker: str) -> Optional[Dict]:
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            if marker in content:
                parts = content.split(marker)
                if len(parts) > 1:
                    match = re.search(r"```(?:yaml)?\n(.*?)\n```", parts[1], re.DOTALL)
                    if match:
                        return yaml.safe_load(match.group(1))
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    return None

def write_markdown_yaml(file_path: str, marker: str, data: Dict) -> bool:
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        if marker in content:
            parts = content.split(marker)
            if len(parts) > 1:
                yaml_block_pattern = r"(```(?:yaml)?\n)(.*?)\n(```)"
                def replace_yaml(match):
                    yaml_str = yaml.dump(data, allow_unicode=True, sort_keys=False)
                    return f"{match.group(1)}{yaml_str}{match.group(3)}"
                new_part = re.sub(yaml_block_pattern, replace_yaml, parts[1], count=1, flags=re.DOTALL)
                new_content = parts[0] + marker + new_part
                with open(file_path, 'w') as f:
                    f.write(new_content)
                return True
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
    return False

def count_in_markdown_table(file_path: str, section: str) -> int:
    if not os.path.exists(file_path): return 0
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            if section in content:
                table_part = content.split(section)[1].split("###")[0].strip()
                lines = [l for l in table_part.split("\n") if "|" in l and "---" not in l and "时间" not in l and "示例" not in l and "—" not in l]
                return len(lines)
    except: pass
    return 0

def parse_markdown_table(file_path: str, section_header: str) -> List[Dict]:
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        if section_header not in content:
            return []
        table_part = content.split(section_header)[1].split("##")[0].strip()
        lines = [l.strip() for l in table_part.split('\n') if '|' in l and '---' not in l]
        if not lines:
            return []
        headers = [h.strip() for h in lines[0].split('|')[1:-1]]
        data = []
        for line in lines[1:]:
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if len(cells) == len(headers):
                data.append(dict(zip(headers, cells)))
        return data
    except Exception as e:
        print(f"Error parsing table {section_header} in {file_path}: {e}")
    return []

# Models
class ProjectStatusUpdate(BaseModel):
    id: str
    status: str

class ProjectCreate(BaseModel):
    name: str
    notes: str
    budget_daily_usd: float = 0.00
    account_group: str = "group_default"
    affiliate_link: str = ""
    subreddits: str = ""
    frustration_keywords: str = ""
    intent_keywords: str = ""
    reply_templates: str = ""

class AccountUpdate(BaseModel):
    platform: str
    name: str
    status: str
    persona: str
    proxy: str = "direct"
    daily_limit: int = 15
    notes: str = ""

class StartRequest(BaseModel):
    interval_seconds: int = 1800

# Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")

@app.get("/logs", response_class=HTMLResponse)
async def logs_page(request: Request):
    return templates.TemplateResponse(request=request, name="logs.html")

@app.get("/notifications", response_class=HTMLResponse)
async def notifications_page(request: Request):
    return templates.TemplateResponse(request=request, name="notifications.html")

@app.get("/config", response_class=HTMLResponse)
async def config_page(request: Request):
    return templates.TemplateResponse(request=request, name="config.html")

@app.get("/schedule", response_class=HTMLResponse)
async def schedule_page(request: Request):
    return templates.TemplateResponse(request=request, name="schedule.html")

@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request):
    return templates.TemplateResponse(request=request, name="projects.html")

@app.get("/accounts", response_class=HTMLResponse)
async def accounts_page(request: Request):
    return templates.TemplateResponse(request=request, name="accounts.html")

@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request):
    return templates.TemplateResponse(request=request, name="analytics.html")

# API
@app.get("/api/status")
async def get_status():
    niche_manager_path = os.path.join(BASE_DIR, "niche_manager.md")
    niche_info = parse_markdown_yaml(niche_manager_path, "## Niche 列表")
    active_niche = None
    if niche_info and 'niches' in niche_info:
        active_niche = next((n for n in niche_info['niches'] if n.get('status') == 'active'), None)
    bark_configured = False
    config_path = os.path.join(BASE_DIR, "config.md")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            if re.search(r'key:\s*".+"', f.read()):
                bark_configured = True
    reply_path = os.path.join(BASE_DIR, "reply_monitor.md")
    q_p0 = count_in_markdown_table(reply_path, "### P0")
    q_p1 = count_in_markdown_table(reply_path, "### P1")
    return {
        "run_state": "running" if is_script_running() else "idle",
        "last_log_at": get_last_log_time(),
        "active_niche": active_niche,
        "bark_configured": bark_configured,
        "launchd_active": check_launchd(),
        "launchd_interval": get_launchd_interval(),
        "queues": {"p0": q_p0, "p1": q_p1}
    }

@app.get("/api/projects")
async def get_projects():
    niche_manager_path = os.path.join(BASE_DIR, "niche_manager.md")
    niche_info = parse_markdown_yaml(niche_manager_path, "## Niche 列表")
    return {"projects": niche_info.get('niches', []) if niche_info else []}

@app.post("/api/projects")
async def create_project(project: ProjectCreate):
    niche_manager_path = os.path.join(BASE_DIR, "niche_manager.md")
    niche_info = parse_markdown_yaml(niche_manager_path, "## Niche 列表")
    if not niche_info or 'niches' not in niche_info: niche_info = {'niches': []}
    project_id = re.sub(r'[^a-z0-9]', '_', project.name.lower())
    if any(n.get('id') == project_id for n in niche_info['niches']):
        project_id = f"{project_id}_{int(datetime.now().timestamp())}"
    project_dir = os.path.join(BASE_DIR, "niches", project_id)
    os.makedirs(project_dir, exist_ok=True)
    config_path = os.path.join(project_dir, "config.md")
    config_obj = {
        "niche": project.name, "timezone": "America/New_York",
        "conversion": { "affiliate_link": project.affiliate_link or "https://example.com" },
        "target_audience": { "subreddits": [s.strip() for s in project.subreddits.split(',')] if project.subreddits else ["entrepreneur", "SaaS"] },
        "scoring_rules": {
            "frustration_keywords": {k.strip(): 30 for k in project.frustration_keywords.split(',')} if project.frustration_keywords else {"zero traffic": 30, "no sales": 30},
            "intent_keywords": [k.strip() for k in project.intent_keywords.split(',')] if project.intent_keywords else ["how", "help", "recommend"]
        },
        "responses": {
            "FIX": { "en_wingman": [r.strip() for r in project.reply_templates.split('\n') if r.strip()] if project.reply_templates else ["Hey, check out my bio for a tool that solves this!"] }
        }
    }
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            f.write(f"# Config: {project.name}\n\n```yaml\n")
            yaml.dump(config_obj, f, allow_unicode=True, sort_keys=False)
            f.write("```\n")
    new_niche = {
        "id": project_id, "name": project.name, "status": "inactive", "priority": 2,
        "account_group": project.account_group, "config_file": f"niches/{project_id}/config.md",
        "budget_daily_usd": project.budget_daily_usd, "start_date": datetime.now().strftime("%Y-%m-%d"),
        "notes": project.notes
    }
    niche_info['niches'].append(new_niche)
    success = write_markdown_yaml(niche_manager_path, "## Niche 列表", niche_info)
    if not success: raise HTTPException(status_code=500, detail="Failed to save project configuration")
    return {"message": "Project created successfully", "project": new_niche}

@app.post("/api/projects/toggle")
async def toggle_project(update: ProjectStatusUpdate):
    niche_manager_path = os.path.join(BASE_DIR, "niche_manager.md")
    niche_info = parse_markdown_yaml(niche_manager_path, "## Niche 列表")
    if not niche_info or 'niches' not in niche_info: raise HTTPException(status_code=404, detail="Projects configuration not found")
    updated = False
    for n in niche_info['niches']:
        if n.get('id') == update.id:
            n['status'] = update.status
            updated = True
            break
    if not updated: raise HTTPException(status_code=404, detail="Project not found")
    success = write_markdown_yaml(niche_manager_path, "## Niche 列表", niche_info)
    if not success: raise HTTPException(status_code=500, detail="Failed to save project configuration")
    return {"message": f"Project {update.id} status updated to {update.status}", "projects": niche_info['niches']}

@app.get("/api/projects/{project_id}/config")
async def get_project_config(project_id: str):
    config_path = os.path.join(BASE_DIR, "niches", project_id, "config.md")
    if not os.path.exists(config_path): return {"config": {}}
    with open(config_path, 'r') as f: content = f.read()
    match = re.search(r"```(?:yaml)?\n(.*?)\n```", content, re.DOTALL)
    yaml_str = match.group(1) if match else content
    try:
        data = yaml.safe_load(yaml_str)
        return {"config": data if isinstance(data, dict) else {}}
    except: return {"config": {}}

@app.post("/api/projects/{project_id}/config")
async def update_project_config(project_id: str, request: Request):
    data = await request.json()
    config_path = os.path.join(BASE_DIR, "niches", project_id, "config.md")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f: content = f.read()
        match = re.search(r"(```(?:yaml)?\n)(.*?)\n(```)", content, re.DOTALL)
        if match:
            yaml_str = yaml.dump(data, allow_unicode=True, sort_keys=False)
            new_content = content[:match.start()] + match.group(1) + yaml_str + match.group(3) + content[match.end():]
        else: new_content = yaml.dump(data, allow_unicode=True, sort_keys=False)
    else:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        new_content = yaml.dump(data, allow_unicode=True, sort_keys=False)
    with open(config_path, 'w') as f: f.write(new_content)
    return {"message": "Config updated"}

@app.get("/api/accounts")
async def get_accounts():
    accounts_path = os.path.join(BASE_DIR, "accounts.md")
    platforms = {}
    if os.path.exists(accounts_path):
        with open(accounts_path, 'r') as f: content = f.read()
        sections = re.split(r'##\s+', content)
        for sec in sections:
            lines = sec.strip().split('\n')
            if not lines: continue
            platform_name = lines[0].strip()
            platform_key = platform_name.split(' ')[0].lower()
            platforms[platform_key] = []
            for line in lines:
                if line.startswith('|') and '---' not in line and '账号名' not in line:
                    parts = [p.strip() for p in line.split('|')[1:-1]]
                    if len(parts) >= 3:
                        platforms[platform_key].append({
                            'name': parts[0], 'status': parts[1], 'persona': parts[2],
                            'comment_info': parts[3] if len(parts) > 3 else "0/0",
                            'dm_info': parts[4] if len(parts) > 4 else "0/0",
                            'proxy': parts[5] if len(parts) > 5 else "direct",
                            'daily_limit': parts[6] if len(parts) > 6 else "15",
                            'notes': parts[-1] if len(parts) > 7 else ""
                        })
    return {"platforms": platforms}

@app.post("/api/accounts")
async def update_account(update: AccountUpdate):
    accounts_path = os.path.join(BASE_DIR, "accounts.md")
    if not os.path.exists(accounts_path): raise HTTPException(status_code=404, detail="accounts.md not found")
    with open(accounts_path, 'r') as f: lines = f.readlines()
    new_lines = []
    in_target_platform = False
    updated = False
    for line in lines:
        if line.startswith('## '): in_target_platform = update.platform.lower() in line.lower()
        if in_target_platform and line.startswith('|') and f"| {update.name} |" in line:
            parts = [p.strip() for p in line.split('|')]
            # Column mapping: | (0) Name (1) Status (2) Persona (3) CommentCount (4) DMCount (5) Proxy (6) Limit (7) Notes (8) |
            if len(parts) >= 9:
                parts[2] = update.status
                parts[3] = update.persona
                parts[6] = update.proxy
                parts[7] = str(update.daily_limit)
                parts[8] = update.notes
                new_lines.append('| ' + ' | '.join(parts[1:-1]) + ' |\n')
                updated = True
            else:
                parts[2] = update.status
                new_lines.append('| ' + ' | '.join(parts[1:-1]) + ' |\n')
                updated = True
        else: new_lines.append(line)
    if not updated: # Maybe need to add as new? handled in a separate endpoint usually
        pass
    with open(accounts_path, 'w') as f: f.writelines(new_lines)
    return {"message": "Account updated successfully"}

@app.post("/api/accounts/add")
async def add_account(update: AccountUpdate):
    accounts_path = os.path.join(BASE_DIR, "accounts.md")
    if not os.path.exists(accounts_path): raise HTTPException(status_code=404, detail="accounts.md not found")
    with open(accounts_path, 'r') as f: content = f.read()
    new_row = f"| {update.name} | {update.status} | {update.persona} | 0/15 | 0/5 | {update.proxy} | {update.daily_limit} | {update.notes} |\n"
    # Find the platform section and append to its table
    pattern = rf"(## {update.platform}.*?\n\|.*?\n\|.*?\n)"
    if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
        new_content = re.sub(pattern, rf"\1{new_row}", content, count=1, flags=re.IGNORECASE | re.DOTALL)
        with open(accounts_path, 'w') as f: f.write(new_content)
        return {"message": "Account added"}
    raise HTTPException(status_code=400, detail="Platform table not found in accounts.md")

@app.get("/api/config/summary")
async def get_config_summary():
    niche_manager_path = os.path.join(BASE_DIR, "niche_manager.md")
    niche_info = parse_markdown_yaml(niche_manager_path, "## Niche 列表")
    accounts_path = os.path.join(BASE_DIR, "accounts.md")
    accounts = []
    if os.path.exists(accounts_path):
        with open(accounts_path, 'r') as f:
            for line in f:
                if "|" in line and "---" not in line and "active" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) > 3: accounts.append({"name": parts[1], "status": parts[2], "persona": parts[3]})
    return { "niche_info": niche_info, "accounts": accounts, "base_dir": BASE_DIR }

@app.get("/api/notifications/summary")
async def get_notifications_summary():
    alert_path = os.path.join(BASE_DIR, "alert_system.md")
    channels = parse_markdown_yaml(alert_path, "## 通知渠道配置")
    p0_rules = parse_markdown_yaml(alert_path, "### P0")
    p1_rules = parse_markdown_yaml(alert_path, "### P1")
    if channels and "channels" in channels:
        for c in channels["channels"]:
            for k in channels["channels"][c]:
                if "key" in k or "token" in k or "password" in k:
                    val = str(channels["channels"][c][k])
                    channels["channels"][c][k] = val[:4] + "****" if len(val) > 4 else "****"
    return { "channels": channels.get("channels", {}) if channels else {}, "p0_rules": p0_rules.get("p0_alerts", []) if p0_rules else [], "p1_rules": p1_rules.get("p1_alerts", []) if p1_rules else [] }

@app.get("/api/logs")
async def get_logs(limit: int = 100):
    if not os.path.exists(LOG_FILE): return {"logs": ["Log file not found at " + LOG_FILE]}
    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
            return {"logs": lines[-limit:]}
    except: return {"logs": ["Error reading logs"]}

@app.get("/api/analytics")
async def get_analytics():
    perf_path = os.path.join(BASE_DIR, "performance.md")
    return { "funnel": parse_markdown_table(perf_path, "**漏斗数据：**"), "platforms": parse_markdown_table(perf_path, "## 平台效果对比"), "personas": parse_markdown_table(perf_path, "## 人设效果对比"), "daily": parse_markdown_table(perf_path, "## 每日明细") }

@app.post("/api/control/run-now")
async def run_now():
    if is_script_running(): return JSONResponse(status_code=409, content={"message": "Script is already running"})
    script_path = os.path.join(BASE_DIR, "enhanced-check.sh")
    subprocess.Popen(["/bin/bash", script_path], start_new_session=True, cwd=BASE_DIR)
    return {"message": "Started script execution"}

@app.post("/api/control/test-notify")
async def test_notify():
    script_path = os.path.join(BASE_DIR, "enhanced-check.sh")
    cmd = f"source {script_path}; bark '🧪 Dashboard Test' 'System is operational' 2>/dev/null"
    subprocess.Popen(["/bin/bash", "-c", cmd], start_new_session=True)
    return {"message": "Notification command sent"}

@app.post("/api/control/start")
async def start_scheduler(req: Optional[StartRequest] = None):
    interval = req.interval_seconds if req else 1800
    script_path = os.path.join(BASE_DIR, "enhanced-check.sh")
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict><key>Label</key><string>{PLIST_LABEL}</string><key>ProgramArguments</key><array><string>/bin/bash</string><string>{script_path}</string></array><key>StartInterval</key><integer>{interval}</integer><key>StandardOutPath</key><string>{LOG_FILE}</string><key>StandardErrorPath</key><string>{LOG_FILE}</string><key>WorkingDirectory</key><string>{BASE_DIR}</string></dict></plist>"""
    try:
        os.makedirs(os.path.dirname(PLIST_PATH), exist_ok=True)
        with open(PLIST_PATH, 'w') as f: f.write(plist_content)
        subprocess.run(["launchctl", "unload", PLIST_PATH], stderr=subprocess.DEVNULL)
        subprocess.run(["launchctl", "load", PLIST_PATH], check=True)
        return {"message": f"Scheduler started (every {interval//60}m)", "interval": interval}
    except: raise HTTPException(status_code=500, detail="Failed to start launchd")

@app.post("/api/control/stop")
async def stop_scheduler():
    try:
        subprocess.run(["launchctl", "unload", PLIST_PATH], check=True)
        if os.path.exists(PLIST_PATH): os.remove(PLIST_PATH)
        return {"message": "Scheduler stopped and removed"}
    except: raise HTTPException(status_code=500, detail="Failed to stop launchd")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8787)
