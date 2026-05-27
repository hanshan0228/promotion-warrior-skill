#!/bin/bash
set -o pipefail
exec >> /tmp/heygen-monitor.log 2>&1
echo ""
echo "========= [v3.5 AUTO-DM] $(date) ========="

LINK="https://yourguide.com" # Replace with actual Landing Page
PERSONAS=('en_wingman' 'en_coach_1')
CURRENT_PERSONA=${PERSONAS[$RANDOM % 2]}

# --- 1. Bark Notification ---
bark() {
  local key=$(grep 'key:' /Users/han/.agents/skills/promotion-warrior/config.md | grep -v daily_limit | head -1 | sed 's/.*key: *"//' | sed 's/".*//')
  [ -z "$key" ] && return
  local t=$(python3 -c "import urllib.parse;print(urllib.parse.quote('''$1'''))" 2>/dev/null)
  local b=$(python3 -c "import urllib.parse;print(urllib.parse.quote('''$2'''))" 2>/dev/null)
  curl -s "https://api.day.app/${key}/${t}/${b}?group=heygen_v3.5&sound=${4:-glass}" >/dev/null 2>&1 &
}

# --- 2. TikTok DM Auto-Reply ---
echo "--- TikTok DM Task ---"
# Check for unread DMs with 'FIX' keyword
# Using browser evaluation to avoid complex API auth
opencli browser bjudz9gq eval "
(async function(){
  window.location.href='https://www.tiktok.com/messages';
  await new Promise(r => setTimeout(r, 6000));
  
  const unreadCount = document.querySelectorAll('.unread-badge').length;
  if(unreadCount > 0) {
    console.log('Detected ' + unreadCount + ' unread TikTok messages.');
    // Logic for specific keyword trigger
    const fixMsg = Array.from(document.querySelectorAll('.message-item-container')).find(m => m.textContent.includes('FIX'));
    if(fixMsg) {
       fixMsg.click();
       return 'TRIGGER_REPLY_FOR_FIX';
    }
  }
  return 'NO_MESSAGES';
})()
" | grep "TRIGGER_REPLY_FOR_FIX" && {
  REPLY=$(python3 /Users/han/.agents/skills/promotion-warrior/tools/dm_randomizer.py "FIX" "$CURRENT_PERSONA" "$LINK")
  opencli browser bjudz9gq eval "
    const input = document.querySelector('.message-input-area [contenteditable]');
    if(input) {
      input.focus();
      document.execCommand('insertText', false, '$REPLY');
      setTimeout(() => { document.querySelector('.send-button')?.click(); }, 1500);
    }
  " 2>/dev/null
  echo "  ✅ Auto-replied to TikTok DM"
  bark "🎬 TikTok私信成功" "已自动回复 $CURRENT_PERSONA 版本的避坑指南"
}

# --- 3. Instagram DM Auto-Reply (Conceptual) ---
echo "--- Instagram DM Task ---"
# IG usually requires a real browser session; we poll if the URL is accessible
opencli browser bjudz9gq eval "
(async function(){
  window.location.href='https://www.instagram.com/direct/inbox/';
  await new Promise(r => setTimeout(r, 6000));
  const unread = document.querySelector('svg[aria-label=\"Unread\"]');
  return unread ? 'UNREAD_DETECTED' : 'CLEAN';
})()
" | grep "UNREAD_DETECTED" && bark "📸 Instagram提醒" "有新私信待处理，请检查"

echo "========= $(date '+%H:%M') 结束 ========="
