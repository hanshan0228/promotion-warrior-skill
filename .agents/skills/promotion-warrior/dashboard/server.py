import os
import sys
import yaml
import json
import asyncio
import subprocess
import re
import urllib.request
import urllib.parse
from datetime import datetime
from typing import Optional, List, Dict
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Promotion Warrior Dashboard")

# Paths
BASE_DIR = "/Users/han/.cc-switch/skills/promotion-warrior"
LOG_FILE = "/tmp/dating-monitor.log"
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
PLIST_LABEL = "com.han.promotion-dashboard"
PLIST_PATH = os.path.expanduser(f"~/Library/LaunchAgents/{PLIST_LABEL}.plist")
PYTHON_PATH = os.path.join(DASHBOARD_DIR, "venv/bin/python3")

# Setup templates
templates = Jinja2Templates(directory=os.path.join(DASHBOARD_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(DASHBOARD_DIR, "static")), name="static")

# Helpers
def get_last_log_time():
    if not os.path.exists(LOG_FILE): return None
    return datetime.fromtimestamp(os.path.getmtime(LOG_FILE)).isoformat()

def is_script_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "enhanced-check.sh"]).decode()
        return len(output.strip()) > 0
    except: return False

def check_launchd():
    try:
        output = subprocess.check_output(["launchctl", "list"]).decode()
        return PLIST_LABEL in output
    except: return False

def get_launchd_interval():
    if not os.path.exists(PLIST_PATH): return None
    try:
        with open(PLIST_PATH, 'r') as f:
            content = f.read()
            match = re.search(r'<key>StartInterval</key>\s*<integer>(\d+)</integer>', content)
            if match: return int(match.group(1))
    except: pass
    return None

def parse_markdown_yaml(file_path: str, marker: str) -> Optional[Dict]:
    if not os.path.exists(file_path): return None
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            if marker in content:
                parts = content.split(marker)
                if len(parts) > 1:
                    match = re.search(r"```(?:yaml)?\n(.*?)\n```", parts[1], re.DOTALL)
                    if match: return yaml.safe_load(match.group(1))
    except Exception as e: print(f"Error parsing {file_path}: {e}")
    return None

def write_markdown_yaml(file_path: str, marker: str, data: Dict) -> bool:
    if not os.path.exists(file_path): return False
    try:
        with open(file_path, 'r') as f: content = f.read()
        if marker in content:
            parts = content.split(marker)
            if len(parts) > 1:
                yaml_block_pattern = r"(```(?:yaml)?\n)(.*?)\n(```)"
                def replace_yaml(match):
                    yaml_str = yaml.dump(data, allow_unicode=True, sort_keys=False)
                    return f"{match.group(1)}{yaml_str}{match.group(3)}"
                new_part = re.sub(yaml_block_pattern, replace_yaml, parts[1], count=1, flags=re.DOTALL)
                new_content = parts[0] + marker + new_part
                with open(file_path, 'w') as f: f.write(new_content)
                return True
    except Exception as e: print(f"Error writing {file_path}: {e}")
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
    if not os.path.exists(file_path): return []
    try:
        with open(file_path, 'r') as f: content = f.read()
        if section_header not in content: return []
        table_part = content.split(section_header)[1].split("##")[0].strip()
        lines = [l.strip() for l in table_part.split('\n') if '|' in l and '---' not in l]
        if not lines: return []
        headers = [h.strip() for h in lines[0].split('|')[1:-1]]
        data = []
        for line in lines[1:]:
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if len(cells) == len(headers): data.append(dict(zip(headers, cells)))
        return data
    except Exception as e: print(f"Error parsing table {section_header} in {file_path}: {e}")
    return []

# Models
class ProjectStatusUpdate(BaseModel): id: str; status: str
class ProjectCreate(BaseModel):
    name: str; notes: str; budget_daily_usd: float = 0.00; account_group: str = "group_default"
    affiliate_link: str = ""; subreddits: str = ""; frustration_keywords: str = ""; intent_keywords: str = ""; reply_templates: str = ""
class AccountUpdate(BaseModel):
    platform: str; name: str; status: str; persona: str; proxy: str = "direct"; daily_limit: int = 15; notes: str = ""
class StartRequest(BaseModel): interval_seconds: int = 1800
class SuggestRequest(BaseModel): product_name: str; product_description: str
class ReplyRequest(BaseModel): platform: str = "reddit"; account_profile: str; thing_id: str; text: str

# Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request): return templates.TemplateResponse(request=request, name="dashboard.html")
@app.get("/logs", response_class=HTMLResponse)
async def logs_page(request: Request): return templates.TemplateResponse(request=request, name="logs.html")
@app.get("/notifications", response_class=HTMLResponse)
async def notifications_page(request: Request): return templates.TemplateResponse(request=request, name="notifications.html")
@app.get("/config", response_class=HTMLResponse)
async def config_page(request: Request): return templates.TemplateResponse(request=request, name="config.html")
@app.get("/schedule", response_class=HTMLResponse)
async def schedule_page(request: Request): return templates.TemplateResponse(request=request, name="schedule.html")
@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request): return templates.TemplateResponse(request=request, name="projects.html")
@app.get("/accounts", response_class=HTMLResponse)
async def accounts_page(request: Request): return templates.TemplateResponse(request=request, name="accounts.html")
@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request): return templates.TemplateResponse(request=request, name="analytics.html")
@app.get("/insights", response_class=HTMLResponse)
async def insights_page(request: Request): return templates.TemplateResponse(request=request, name="insights.html")
@app.get("/feed", response_class=HTMLResponse)
async def feed_page(request: Request): return templates.TemplateResponse(request=request, name="feed.html")
@app.get("/inbox", response_class=HTMLResponse)
async def inbox_page(request: Request): return templates.TemplateResponse(request=request, name="inbox.html")

# API
@app.get("/api/status")
async def get_status():
    niche_info = parse_markdown_yaml(os.path.join(BASE_DIR, "niche_manager.md"), "## Niche 列表")
    active_niche = next((n for n in niche_info['niches'] if n.get('status') == 'active'), None) if niche_info else None
    bark_configured = False
    config_path = os.path.join(BASE_DIR, "config.md")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            if re.search(r'key:\s*".+"', f.read()): bark_configured = True
    reply_path = os.path.join(BASE_DIR, "reply_monitor.md")
    return {
        "run_state": "running" if is_script_running() else "idle", "last_log_at": get_last_log_time(),
        "active_niche": active_niche, "bark_configured": bark_configured, "launchd_active": check_launchd(),
        "launchd_interval": get_launchd_interval(), "queues": {"p0": count_in_markdown_table(reply_path, "### P0"), "p1": count_in_markdown_table(reply_path, "### P1")}
    }

@app.get("/api/feed")
async def get_lead_feed():
    niche_info = parse_markdown_yaml(os.path.join(BASE_DIR, "niche_manager.md"), "## Niche 列表")
    active_niche = next((n for n in niche_info.get('niches', []) if n.get('status') == 'active'), None) if niche_info else None
    if not active_niche: return {"leads": []}
    config_path = os.path.join(BASE_DIR, active_niche.get("config_file", ""))
    config_data = {}
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            content = f.read()
            match = re.search(r'```(?:yaml)?\n(.*?)\n```', content, re.DOTALL)
            yaml_str = match.group(1) if match else content
            try: config_data = yaml.safe_load(yaml_str) or {}
            except: pass
    leads = []
    # --- Reddit ---
    subreddits = config_data.get('target_audience', {}).get('subreddits', ['Tinder'])
    target_sub = subreddits[0] if subreddits else "Tinder"
    try:
        output = subprocess.check_output(f"opencli reddit subreddit {target_sub} --limit 3 -f json", shell=True, text=True, stderr=subprocess.DEVNULL)
        match = re.search(r'\[.*\]', output, re.DOTALL)
        if match:
            for p in json.loads(match.group(0)):
                text = p.get('selftext', p.get('title', ''))
                score_out = subprocess.check_output(f"echo {json.dumps({'comment': text})} | {PYTHON_PATH} {BASE_DIR}/lead_scorer_v2.py {config_path}", shell=True, text=True, stderr=subprocess.DEVNULL)
                score_res = json.loads(score_out)
                draft = subprocess.check_output(f"{PYTHON_PATH} {BASE_DIR}/tools/dm_randomizer.py {target_sub} en_wingman https://link {config_path}", shell=True, text=True, stderr=subprocess.DEVNULL).strip()
                leads.append({"platform": "reddit", "id": p.get('id'), "author": p.get('author'), "title": p.get('title'), "text": text, "url": p.get('url'), "score": score_res.get('score', 0), "grade": score_res.get('grade', 'C'), "factors": score_res.get('factors', []), "draft": draft})
    except: pass
    # --- Twitter/X ---
    queries = list(config_data.get('scoring_rules', {}).get('frustration_keywords', {"dating apps suck": 30}).keys())
    x_query = queries[0] if queries else "dating apps suck"
    try:
        x_out = subprocess.check_output(f"opencli twitter search '{x_query}' --limit 3 -f json", shell=True, text=True, stderr=subprocess.DEVNULL)
        x_match = re.search(r'\[.*\]', x_out, re.DOTALL)
        if x_match:
            for t in json.loads(x_match.group(0)):
                text = t.get('text', '')
                score_out = subprocess.check_output(f"echo {json.dumps({'comment': text})} | {PYTHON_PATH} {BASE_DIR}/lead_scorer_v2.py {config_path}", shell=True, text=True, stderr=subprocess.DEVNULL)
                score_res = json.loads(score_out)
                draft = subprocess.check_output(f"{PYTHON_PATH} {BASE_DIR}/tools/dm_randomizer.py X_SNIPE en_wingman https://link {config_path}", shell=True, text=True, stderr=subprocess.DEVNULL).strip()
                leads.append({"platform": "twitter", "id": t.get('id'), "author": t.get('author', 'unknown'), "title": "New Tweet", "text": text, "url": f"https://twitter.com/x/status/{t.get('id')}", "score": score_res.get('score', 0), "grade": score_res.get('grade', 'C'), "factors": score_res.get('factors', []), "draft": draft})
    except: pass
    leads.sort(key=lambda x: x['score'], reverse=True)
    return {"leads": leads}

@app.get("/api/inbox")
async def get_inbox(platform: str = "reddit", profile: str = "bjudz9gq"):
    if platform == "reddit":
        js = "(async function(){ try { const r = await fetch('https://www.reddit.com/message/inbox/.json?limit=15', {credentials:'include'}); const d = await r.json(); return JSON.stringify(d?.data?.children || []); } catch(e) { return JSON.stringify({error: e.toString()}); } })()"
    else: # twitter
        js = "(async function(){ return JSON.stringify([]); })()" # Mock for now
    try:
        output = subprocess.check_output(f"opencli browser {profile} eval \"{js}\"", shell=True, text=True)
        match = re.search(r'\[.*\]|\{.*\}', output, re.DOTALL)
        if match:
            try: return {"messages": json.loads(json.loads(match.group(0)))}
            except: return {"messages": json.loads(match.group(0))}
        return {"messages": []}
    except: return {"messages": [], "error": "Fetch failed"}

@app.post("/api/inbox/reply")
async def send_reply(req: ReplyRequest):
    safe_text = req.text.replace("'", "\\'").replace("\n", "\\n")
    if req.platform == "reddit":
        js = f"(async function(){{ try {{ const body = 'thing_id={req.thing_id}&text=' + encodeURIComponent('{safe_text}') + '&api_type=json'; const r = await fetch('https://www.reddit.com/api/comment', {{ method: 'POST', credentials: 'include', headers: {{'Content-Type': 'application/x-www-form-urlencoded'}}, body: body }}); return await r.text(); }} catch(e) {{ return e.toString(); }} }})()"
    else: # twitter
        js = "() => 'Not implemented'"
    try:
        output = subprocess.check_output(f"opencli browser {req.account_profile} eval \"{js}\"", shell=True, text=True)
        return {"status": "success", "raw": output}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/magic/suggest")
async def magic_suggest(req: SuggestRequest):
    config_path = os.path.join(BASE_DIR, "config.md")
    api_key = None
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            match = re.search(r"sk-[a-zA-Z0-9]+", f.read())
            if match: api_key = match.group(0)
    if not api_key: raise HTTPException(status_code=400, detail="API Key not found")
    prompt = f"Expert Reddit growth advice for ProductName: {req.product_name}, Description: {req.product_description}. Return JSON: {{\"keywords\":[], \"subreddits\":[]}}"
    url = "https://api.deepseek.com/chat/completions"
    data = json.dumps({"model": "deepseek-chat", "messages": [{"role": "system", "content": prompt}], "response_format": {"type": "json_object"}}).encode('utf-8')
    req_obj = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"})
    try:
        with urllib.request.urlopen(req_obj) as response:
            return json.loads(json.loads(response.read().decode('utf-8'))['choices'][0]['message']['content'])
    except: raise HTTPException(status_code=500, detail="API Error")

@app.get("/api/projects")
async def get_projects(): return {"projects": parse_markdown_yaml(os.path.join(BASE_DIR, "niche_manager.md"), "## Niche 列表").get('niches', [])}

@app.post("/api/projects")
async def create_project(project: ProjectCreate):
    niche_manager_path = os.path.join(BASE_DIR, "niche_manager.md")
    niche_info = parse_markdown_yaml(niche_manager_path, "## Niche 列表")
    project_id = re.sub(r'[^a-z0-9]', '_', project.name.lower())
    project_dir = os.path.join(BASE_DIR, "niches", project_id)
    os.makedirs(project_dir, exist_ok=True)
    config_path = os.path.join(project_dir, "config.md")
    config_obj = {"niche": project.name, "conversion": { "affiliate_link": project.affiliate_link or "" }, "target_audience": { "subreddits": [s.strip() for s in project.subreddits.split(',')] if project.subreddits else [] }, "scoring_rules": { "frustration_keywords": {k.strip(): 30 for k in project.frustration_keywords.split(',')} if project.frustration_keywords else {}, "intent_keywords": [k.strip() for k in project.intent_keywords.split(',')] if project.intent_keywords else [] }, "responses": { "FIX": { "en_wingman": [r.strip() for r in project.reply_templates.split('\n') if r.strip()] if project.reply_templates else ["I was in the exact same spot..."] } } }
    with open(config_path, 'w') as f:
        f.write(f"# Config: {project.name}\n\n```yaml\n")
        yaml.dump(config_obj, f, allow_unicode=True, sort_keys=False)
        f.write("```\n")
    new_niche = {"id": project_id, "name": project.name, "status": "inactive", "priority": 2, "account_group": project.account_group, "config_file": f"niches/{project_id}/config.md", "notes": project.notes, "start_date": datetime.now().strftime("%Y-%m-%d")}
    niche_info['niches'].append(new_niche)
    write_markdown_yaml(niche_manager_path, "## Niche 列表", niche_info)
    return {"message": "Created"}

@app.post("/api/projects/toggle")
async def toggle_project(update: ProjectStatusUpdate):
    niche_manager_path = os.path.join(BASE_DIR, "niche_manager.md")
    niche_info = parse_markdown_yaml(niche_manager_path, "## Niche 列表")
    for n in niche_info['niches']:
        if n['id'] == update.id: n['status'] = update.status
    write_markdown_yaml(niche_manager_path, "## Niche 列表", niche_info)
    return {"message": "Updated"}

@app.get("/api/projects/{project_id}/config")
async def get_project_config(project_id: str):
    with open(os.path.join(BASE_DIR, "niches", project_id, "config.md"), 'r') as f:
        m = re.search(r"```(?:yaml)?\n(.*?)\n```", f.read(), re.DOTALL)
        return {"config": yaml.safe_load(m.group(1)) if m else {}}

@app.post("/api/projects/{project_id}/config")
async def update_project_config(project_id: str, request: Request):
    data = await request.json()
    path = os.path.join(BASE_DIR, "niches", project_id, "config.md")
    with open(path, 'r') as f: content = f.read()
    m = re.search(r"(```(?:yaml)?\n)(.*?)\n(```)", content, re.DOTALL)
    new_c = content[:m.start()] + m.group(1) + yaml.dump(data, allow_unicode=True) + m.group(3) + content[m.end():]
    with open(path, 'w') as f: f.write(new_c)
    return {"message": "Updated"}

@app.get("/api/projects/{project_id}/insights")
async def get_project_insights(project_id: str):
    p = os.path.join(BASE_DIR, "niches", project_id, "insights.md")
    return {"content": open(p).read() if os.path.exists(p) else "No insights."}

@app.get("/api/accounts")
async def get_accounts():
    platforms = {}
    with open(os.path.join(BASE_DIR, "accounts.md")) as f:
        sections = re.split(r'##\s+', f.read())
        for sec in sections:
            lines = sec.strip().split('\n')
            if not lines: continue
            pk = lines[0].split(' ')[0].lower()
            platforms[pk] = []
            for l in lines:
                if l.startswith('|') and '---' not in l and '账号名' not in l:
                    p = [i.strip() for i in l.split('|')[1:-1]]
                    if len(p) >= 3: platforms[pk].append({'name': p[0], 'status': p[1], 'persona': p[2], 'comment_info': p[3] if len(p)>3 else "0/0", 'dm_info': p[4] if len(p)>4 else "0/0", 'proxy': p[5] if len(p)>5 else "direct", 'daily_limit': p[6] if len(p)>6 else "15", 'notes': p[-1] if len(p)>7 else ""})
    return {"platforms": platforms}

@app.post("/api/accounts")
async def update_account(update: AccountUpdate):
    path = os.path.join(BASE_DIR, "accounts.md")
    with open(path) as f: lines = f.readlines()
    new_l = []; in_p = False
    for l in lines:
        if l.startswith('## '): in_p = update.platform.lower() in l.lower()
        if in_p and l.startswith('|') and f"| {update.name} |" in l:
            p = [i.strip() for i in l.split('|')]
            p[2] = update.status; p[3] = update.persona; p[6] = update.proxy; p[7] = str(update.daily_limit); p[8] = update.notes
            new_l.append('| ' + ' | '.join(p[1:-1]) + ' |\n')
        else: new_l.append(l)
    with open(path, 'w') as f: f.writelines(new_l)
    return {"message": "Updated"}

@app.get("/api/analytics")
async def get_analytics():
    p = os.path.join(BASE_DIR, "performance.md")
    return {"funnel": parse_markdown_table(p, "**漏斗数据：**"), "platforms": parse_markdown_table(p, "## 平台效果对比"), "personas": parse_markdown_table(p, "## 人设效果对比")}

@app.get("/api/notifications/summary")
async def get_notifications_summary():
    p = os.path.join(BASE_DIR, "alert_system.md")
    return {"channels": parse_markdown_yaml(p, "## 通知渠道配置").get("channels", {}), "p0_rules": parse_markdown_yaml(p, "### P0").get("p0_alerts", []), "p1_rules": parse_markdown_yaml(p, "### P1").get("p1_alerts", [])}

@app.get("/api/logs")
async def get_logs(limit: int = 100):
    lines = open(LOG_FILE).readlines() if os.path.exists(LOG_FILE) else ["No log."]
    return {"logs": lines[-limit:]}

@app.post("/api/control/run-now")
async def run_now():
    if is_script_running(): return JSONResponse(status_code=409, content={"message": "Already running"})
    subprocess.Popen(["/bin/bash", os.path.join(BASE_DIR, "enhanced-check.sh")], start_new_session=True, cwd=BASE_DIR)
    return {"message": "Started"}

@app.post("/api/control/start")
async def start_scheduler(req: Optional[StartRequest] = None):
    i = req.interval_seconds if req else 1800
    with open(PLIST_PATH, 'w') as f: f.write(f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><dict><key>Label</key><string>{PLIST_LABEL}</string><key>ProgramArguments</key><array><string>/bin/bash</string><string>{os.path.join(BASE_DIR, "enhanced-check.sh")}</string></array><key>StartInterval</key><integer>{i}</integer><key>StandardOutPath</key><string>{LOG_FILE}</string><key>StandardErrorPath</key><string>{LOG_FILE}</string><key>WorkingDirectory</key><string>{BASE_DIR}</string><key>KeepAlive</key><true/><key>RunAtLoad</key><true/></dict></plist>')
    subprocess.run(["launchctl", "unload", PLIST_PATH], stderr=subprocess.DEVNULL)
    subprocess.run(["launchctl", "load", PLIST_PATH])
    return {"message": "Started"}

@app.post("/api/control/stop")
async def stop_scheduler():
    subprocess.run(["launchctl", "unload", PLIST_PATH])
    if os.path.exists(PLIST_PATH): os.remove(PLIST_PATH)
    subprocess.run(["pkill", "-f", "enhanced-check.sh"])
    subprocess.run(["pkill", "-f", "opencli"])
    return {"message": "Stopped"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8787)
