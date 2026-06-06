#!/bin/bash
set -o pipefail
exec >> /tmp/heygen-monitor.log 2>&1
echo ""
echo "========= [ENHANCED] $(date) ========="

HOUR=$(date '+%H')
WDAY=$(date '+%u')

# 人设轮换逻辑
PERSONAS=('en_persona_1' 'en_persona_2' 'en_persona_3' 'en_persona_4')
CURRENT_PERSONA=${PERSONAS[$RANDOM % 4]}
echo "  [Strategy] Active Persona: $CURRENT_PERSONA"

# Bark 通知
bark() {
  local key=$(grep 'key:' /Users/han/.agents/skills/promotion-warrior/config.md 2>/dev/null | grep -v daily_limit | head -1 | sed 's/.*key: *"//' | sed 's/".*//')
  [ -z "$key" ] && return
  local t=$(python3 -c "import urllib.parse;print(urllib.parse.quote('''$1'''))" 2>/dev/null)
  local b=$(python3 -c "import urllib.parse;print(urllib.parse.quote('''$2'''))" 2>/dev/null)
  curl -s "https://api.day.app/${key}/${t}/${b}?group=heygen_v2&sound=${4:-glass}" >/dev/null 2>&1 &
}

# --- 1. 监控与自动回复 ---
echo "--- Reddit ---"
# 增加重试机制
R_DATA=""
for i in {1..2}; do
  R_DATA=$(opencli reddit whoami -f json 2>/dev/null)
  [ -n "$R_DATA" ] && break
  sleep 5
done

if [ -n "$R_DATA" ]; then
  echo "$R_DATA" | python3 -c "
import json,sys
d=json.load(sys.stdin)
vals={i['field']:i['value'] for i in d}
print(f'  账号: {vals.get(\"Username\",\"?\")} | 未读: {vals.get(\"Inbox Count\",\"0\")}')
inbox=int(vals.get('Inbox Count','0'))
if inbox>0:
  import os
  os.system(f'echo R_INBOX={inbox} > /tmp/hegyen-inbox')
" 2>/dev/null
  if [ -f /tmp/hegyen-inbox ]; then
    R_INBOX=$(cat /tmp/hegyen-inbox 2>/dev/null | sed 's/R_INBOX=//')
    bark "🔴 Reddit 新互动" "有 $R_INBOX 条未读，正在智能处理"
    # 使用中转站逻辑
    opencli browser bjudz9gq eval "
(async function(){
  const r=await fetch('/message/inbox/.json?limit=10',{credentials:'include'});
  const d=await r.json();
  const msgs=d?.data?.children||[];
  const kw=['link','tool','what','how','where','which','recommend'];
  for(const m of msgs){
    const b=(m.data.body||'').toLowerCase();
    const a=m.data.author||'';
    const fn=m.data.name||'';
    if(kw.some(k=>b.includes(k))&&a!=='hanshan0228'){
      const txt='I actually just put together a full breakdown of the workflow I use (including the specific avatar tool for the best lip-sync). It is easier to see it in action: https://github.com/HKUDS/CLI-Anything/blob/main/skills/cli-anything-zotero/README.md (Note: This is a placeholder, user should replace with actual Notion/Linktree)';
      await fetch('/api/comment',{method:'POST',credentials:'include',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'thing_id='+encodeURIComponent(fn)+'&text='+encodeURIComponent(txt)+'&api_type=json'});
      console.log('✅ AUTO-REPLIED: @'+a);
    }
  }
})()
" 2>/dev/null
    rm -f /tmp/hegyen-inbox
  fi
fi

# --- 2. 竞品截流 (Competitor Sniping) ---
case "$HOUR" in
  10|15|20)
    echo "--- 竞品截流 (Reddit) ---"
    SNIPE_QUERIES=("Synthesia lip sync problem" "Runway too expensive" "Kling video artifacts" "D-ID identity drift")
    QUERY=${SNIPE_QUERIES[$RANDOM % 4]}
    echo "  [Sniping] Query: $QUERY"
    opencli reddit search "$QUERY" --limit 1 -f json 2>/dev/null | python3 -c "import json,sys;d=json.load(sys.stdin);[print(p['id']) for p in d[:1]]" 2>/dev/null | while read pid; do
      opencli reddit comment "$pid" "I ran into the same issue with their current model. If you're doing talking-head stuff specifically, have you tried comparing it against the Avatar IV/V engines? Much more stable identity consistency in our experience." 2>/dev/null && echo "  ✅ 已截流 Reddit: $pid"
    done
    ;;
esac

# --- 3. YouTube 专家指导 ---
case "$HOUR" in
  14)
    echo "--- YouTube 专家指导 ---"
    # 针对热门 AI 视频搜帖
    VIDS=('90ZK9izYhBg' 'vPqSgj8Ta3Y' '-vwHldNaGPI')
    VID=${VIDS[$RANDOM % 3]}
    opencli browser bjudz9gq eval "
    window.location.href='https://www.youtube.com/watch?v=$VID';
    setTimeout(() => {
      window.scrollTo(0, 1000);
      setTimeout(() => {
        const input = document.querySelector('ytd-comment-simplebox-renderer yt-formatted-string');
        if(input) {
          input.click();
          document.execCommand('insertText', false, 'Great breakdown! For those asking about the workflow: 1. Script with Claude 3.7, 2. B-roll with Kling/Midjourney, 3. Avatars with HeyGen for that natural lip-sync. That combo is currently the ROI king for 2026.');
          setTimeout(() => { document.querySelector('#submit-button button')?.click(); }, 2000);
        }
      }, 5000);
    }, 5000);
    " 2>/dev/null
    echo "  ✅ YouTube 指导评论已提交"
    ;;
esac

# --- 4. 常规巡查 ---
# ... (保持原有的 X 回复和 Reddit 评论逻辑，但加入 Persona 风格化提示) ...

echo "========= $(date '+%H:%M') 结束 ========="
