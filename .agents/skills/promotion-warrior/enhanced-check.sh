#!/bin/bash
set -o pipefail
exec >> /tmp/dating-monitor.log 2>&1
echo ""

PYTHON_CMD="/Users/han/.cc-switch/skills/promotion-warrior/dashboard/venv/bin/python3"

ACTIVE_NICHES=$($PYTHON_CMD -c "import yaml, re; f=open('/Users/han/.cc-switch/skills/promotion-warrior/niche_manager.md').read(); match=re.search(r'\`\`\`(?:yaml)?\n(.*?)\n\`\`\`', f.split('## Niche 列表')[1], re.DOTALL); d=yaml.safe_load(match.group(1)); print(' '.join([n['id'] for n in d.get('niches', []) if n.get('status') == 'active']))" 2>/dev/null)

if [ -z "$ACTIVE_NICHES" ]; then
  echo "========= [ENGINE] $(date) ========="
  echo "No active niches found. Exiting."
  exit 0
fi

for NICHE_ID in $ACTIVE_NICHES; do
  NICHE_NAME=$($PYTHON_CMD -c "import yaml, re; f=open('/Users/han/.cc-switch/skills/promotion-warrior/niche_manager.md').read(); match=re.search(r'\`\`\`(?:yaml)?\n(.*?)\n\`\`\`', f.split('## Niche 列表')[1], re.DOTALL); d=yaml.safe_load(match.group(1)); print(next((n['name'] for n in d.get('niches', []) if n['id'] == '$NICHE_ID'), 'Unknown Niche'))" 2>/dev/null)

  echo "========= [ENGINE: $NICHE_NAME] $(date) ========="

  HOUR=$(date '+%H')
  WDAY=$(date '+%u')

  # 人设轮换逻辑
  PERSONAS=('en_wingman' 'en_coach_1')
  CURRENT_PERSONA=${PERSONAS[$RANDOM % 2]}
  # 读取该 Niche 的特定配置
  CONFIG_FILE=$($PYTHON_CMD -c "import yaml, re; f=open('/Users/han/.cc-switch/skills/promotion-warrior/niche_manager.md').read(); match=re.search(r'\`\`\`(?:yaml)?\n(.*?)\n\`\`\`', f.split('## Niche 列表')[1], re.DOTALL); d=yaml.safe_load(match.group(1)); print(next((n['config_file'] for n in d.get('niches', []) if n['id'] == '$NICHE_ID'), ''))" 2>/dev/null)

  if [ -n "$CONFIG_FILE" ] && [ -f "/Users/han/.cc-switch/skills/promotion-warrior/$CONFIG_FILE" ]; then
    AFFILIATE_LINK=$($PYTHON_CMD -c "import yaml, re; f=open('/Users/han/.cc-switch/skills/promotion-warrior/$CONFIG_FILE').read(); match=re.search(r'\`\`\`(?:yaml)?\n(.*?)\n\`\`\`', f, re.DOTALL); d=yaml.safe_load(match.group(1)) if match else yaml.safe_load(f); print(d.get('conversion',{}).get('affiliate_link', 'https://yourguide.com'))" 2>/dev/null)
    # 如果没有 yaml 代码块包裹，尝试直接解析
    if [ "$AFFILIATE_LINK" == "None" ] || [ -z "$AFFILIATE_LINK" ]; then
        AFFILIATE_LINK=$($PYTHON_CMD -c "import yaml; f=open('/Users/han/.cc-switch/skills/promotion-warrior/$CONFIG_FILE').read(); d=yaml.safe_load(f); print(d.get('conversion',{}).get('affiliate_link', 'https://yourguide.com'))" 2>/dev/null)
    fi

    # Read subreddits from config
    SUBREDDITS_STR=$($PYTHON_CMD -c "import yaml, re; f=open('/Users/han/.cc-switch/skills/promotion-warrior/$CONFIG_FILE').read(); match=re.search(r'\`\`\`(?:yaml)?\n(.*?)\n\`\`\`', f, re.DOTALL); d=yaml.safe_load(match.group(1)) if match else yaml.safe_load(f); print(' '.join(d.get('target_audience',{}).get('subreddits', ['Tinder', 'Bumble', 'hingeapp'])))" 2>/dev/null)
    if [ -z "$SUBREDDITS_STR" ] || [ "$SUBREDDITS_STR" == "None" ]; then
      SUBREDDITS_STR=$($PYTHON_CMD -c "import yaml; f=open('/Users/han/.cc-switch/skills/promotion-warrior/$CONFIG_FILE').read(); d=yaml.safe_load(f); print(' '.join(d.get('target_audience',{}).get('subreddits', ['Tinder', 'Bumble', 'hingeapp'])))" 2>/dev/null)
    fi
  else
    AFFILIATE_LINK="https://yourguide.com"
    SUBREDDITS_STR="Tinder Bumble hingeapp dating_advice"
  fi

  read -a SUBREDDITS <<< "$SUBREDDITS_STR"
  if [ ${#SUBREDDITS[@]} -eq 0 ]; then
      SUBREDDITS=("Tinder" "Bumble" "hingeapp" "dating_advice")
  fi

  echo "  [Strategy] Active Persona: $CURRENT_PERSONA | Link: $AFFILIATE_LINK | Subreddits: ${SUBREDDITS[*]}"

  # Bark 通知
  bark() {
    local key=$(grep 'key:' /Users/han/.cc-switch/skills/promotion-warrior/config.md 2>/dev/null | grep -v daily_limit | head -1 | sed 's/.*key: *\"//' | sed 's/\".*//')
    [ -z "$key" ] && return
    local t=$($PYTHON_CMD -c "import urllib.parse;print(urllib.parse.quote('''$1'''))" 2>/dev/null)
    local b=$($PYTHON_CMD -c "import urllib.parse;print(urllib.parse.quote('''$2'''))" 2>/dev/null)
    curl -s "https://api.day.app/${key}/${t}/${b}?group=dating_engine_v4&sound=${4:-glass}" >/dev/null 2>&1 &
  }

  # --- 1. Reddit 监控与自动回复 ---
  echo "--- Reddit ---"

  # 自动选择一个还有额度的账号
  ACC_INFO=$($PYTHON_CMD /Users/han/.cc-switch/skills/promotion-warrior/tools/account_manager.py pick "Reddit" "comment" 2>/dev/null)
  if [ -z "$ACC_INFO" ]; then
    echo "  ⚠️ 无可用 Reddit 账号（额度已满或未启用）。跳过本轮。"
  else
    CURRENT_USER=$(echo "$ACC_INFO" | cut -d'|' -f1)
    CURRENT_STATUS=$(echo "$ACC_INFO" | cut -d'|' -f3)

    if [ "$CURRENT_STATUS" == "warming" ]; then
        echo "  [Warming] Account $CURRENT_USER is in WARMING mode. Running Tier 0 operations on r/AskReddit."
        # Grab a random hot post from AskReddit
        WARMING_POST=$(opencli reddit subreddit AskReddit --limit 1 -f json 2>/dev/null)
        WP_ID=$(echo "$WARMING_POST" | $PYTHON_CMD -c "import json,sys;d=json.load(sys.stdin);print(d[0]['id'] if len(d)>0 else '')" 2>/dev/null)
        if [ -n "$WP_ID" ] && ! grep -q "$WP_ID" /Users/han/.cc-switch/skills/promotion-warrior/sent_posts.log 2>/dev/null; then
            WARM_REPLY=$(echo "$WARMING_POST" | $PYTHON_CMD /Users/han/.cc-switch/skills/promotion-warrior/tools/warming_mode.py 2>/dev/null)
            if [ -n "$WARM_REPLY" ] && [ "$WARM_REPLY" != "None" ]; then
                if opencli reddit comment "$WP_ID" "$WARM_REPLY" 2>/dev/null; then
                    echo "  ✅ 养号评论成功 (r/AskReddit): $WP_ID"
                    echo "$WP_ID" >> /Users/han/.cc-switch/skills/promotion-warrior/sent_posts.log
                    $PYTHON_CMD /Users/han/.cc-switch/skills/promotion-warrior/tools/account_manager.py increment "Reddit" "$CURRENT_USER" "comment"
                fi
            fi
        fi
    else
        echo "  [Account] Using Reddit Account: $CURRENT_USER"
        R_DATA=""
        for i in {1..2}; do
          R_DATA=$(opencli reddit whoami -f json 2>/dev/null)
          [ -n "$R_DATA" ] && break
          sleep 5
        done

        if [ -n "$R_DATA" ]; then
          echo "$R_DATA" | $PYTHON_CMD -c "
import json,sys
d=json.load(sys.stdin)
vals={i['field']:i['value'] for i in d}
print(f'  账号: {vals.get(\"Username\",\"?\")} | 未读: {vals.get(\"Inbox Count\",\"0\")} ')
inbox=int(vals.get('Inbox Count','0'))
if inbox>0:
  import os
  os.system(f'echo R_INBOX={inbox} > /tmp/dating-inbox')
" 2>/dev/null
          if [ -f /tmp/dating-inbox ]; then
            R_INBOX=$(cat /tmp/dating-inbox 2>/dev/null | sed 's/R_INBOX=//')
            bark "🔴 Reddit 新互动" "有 $R_INBOX 条未读，正在智能处理"
            # 使用中转站逻辑
            opencli browser bjudz9gq eval "
        (async function(){
          const r=await fetch('/message/inbox/.json?limit=10',{credentials:'include'});
          const d=await r.json();
          const msgs=d?.data?.children||[];
          const kw=['zero matches','dating apps suck','shadowbanned','ghosted','tinder','bumble','hinge','matches','profile','review','advice'];
          for(const m of msgs){
            const b=(m.data.body||'').toLowerCase();
            const a=m.data.author||'';
            const fn=m.data.name||'';
            if(kw.some(k=>b.includes(k))&&a!=='hanshan0228'){
              const txt='I actually pinned a free diagnostic tool on my profile that breaks down exactly why the algorithm might be hiding you. Check my bio, it changed my match rate overnight.';
              await fetch('/api/comment',{method:'POST',credentials:'include',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'thing_id='+encodeURIComponent(fn)+'&text='+encodeURIComponent(txt)+'&api_type=json'});
              console.log('TRIGGER_REPLY_SUCCESS_@'+a);
            }
          }
        })()
        " 2>/dev/null | grep -q "TRIGGER_REPLY_SUCCESS" && {
            echo "  ✅ 成功回复私信，计入配额"
            $PYTHON_CMD /Users/han/.cc-switch/skills/promotion-warrior/tools/account_manager.py increment "Reddit" "$CURRENT_USER" "comment"
        }
            rm -f /tmp/dating-inbox
          fi
        fi
    fi
  fi

  # --- 2. 泛受众截流 (Reddit Bio Routing) ---
  echo "--- 泛受众截流 (Reddit) ---"

  for SUB in "${SUBREDDITS[@]}"; do
    ACC_INFO=$($PYTHON_CMD /Users/han/.cc-switch/skills/promotion-warrior/tools/account_manager.py pick "Reddit" "comment" 2>/dev/null)
    if [ -z "$ACC_INFO" ]; then break; fi
    CURRENT_USER=$(echo "$ACC_INFO" | cut -d'|' -f1)
    CURRENT_STATUS=$(echo "$ACC_INFO" | cut -d'|' -f3)
    if [ "$CURRENT_STATUS" == "warming" ]; then continue; fi

    echo "  [Sniping] Subreddit: r/$SUB | Account: $CURRENT_USER"

    opencli reddit subreddit "$SUB" --limit 50 -f json 2>/dev/null | $PYTHON_CMD -c "import json,sys;d=json.load(sys.stdin);[print(p['id']) for p in d]" 2>/dev/null | while read pid; do
      if [ -z "$pid" ]; then continue; fi
      if grep -q "$pid" /Users/han/.cc-switch/skills/promotion-warrior/sent_posts.log 2>/dev/null; then continue; fi

      POST_DATA=$(opencli reddit read "$pid" --limit 20 -f json 2>/dev/null)
      COMMENT_TEXT=$(echo "$POST_DATA" | $PYTHON_CMD -c "import json,sys;d=json.load(sys.stdin);print(d[0].get('text','') if isinstance(d, list) and len(d) > 0 else '')" 2>/dev/null)
      COMMENT_COUNT=$(echo "$POST_DATA" | $PYTHON_CMD -c "import json,sys;d=json.load(sys.stdin);print(len(d)-1 if isinstance(d, list) else 0)" 2>/dev/null)

      if [ "$COMMENT_COUNT" -gt 10 ]; then
          echo "$POST_DATA" | $PYTHON_CMD /Users/han/.cc-switch/skills/promotion-warrior/tools/insight_tracker.py "$pid" "$NICHE_ID" "$NICHE_NAME" "Promotion Campaign" "$CURRENT_PERSONA"
      fi

      SCORE_JSON=$(echo "{\"comment\": \"$COMMENT_TEXT\", \"user_info\": {}}" | $PYTHON_CMD /Users/han/.cc-switch/skills/promotion-warrior/lead_scorer_v2.py "/Users/han/.cc-switch/skills/promotion-warrior/$CONFIG_FILE" 2>/dev/null)
      GRADE=$(echo "$SCORE_JSON" | $PYTHON_CMD -c "import json,sys;print(json.load(sys.stdin).get('grade','C'))" 2>/dev/null)

      if [[ "$GRADE" == "S" || "$GRADE" == "A" ]]; then
        REPLY=$($PYTHON_CMD /Users/han/.cc-switch/skills/promotion-warrior/tools/dm_randomizer.py "$SUB" "$CURRENT_PERSONA" "$AFFILIATE_LINK" "/Users/han/.cc-switch/skills/promotion-warrior/$CONFIG_FILE")
        if opencli reddit comment "$pid" "$REPLY" 2>/dev/null; then
            echo "  ✅ 已截流 Reddit r/$SUB ($GRADE): $pid"
            echo "$pid" >> /Users/han/.cc-switch/skills/promotion-warrior/sent_posts.log
            $PYTHON_CMD /Users/han/.cc-switch/skills/promotion-warrior/tools/account_manager.py increment "Reddit" "$CURRENT_USER" "comment"
            sleep 15
        fi
      fi
    done
  done

  # --- 3. YouTube 情感导师 (暂时关闭) ---
  echo "--- YouTube 情感导师 (已禁用) ---"

  # --- 4. Twitter / X 关键词截流 (Search Matrix) ---
  echo "--- X (Twitter) 拦截 ---"
  USER_KEYWORDS=$($PYTHON_CMD -c "import yaml, re; f=open('/Users/han/.cc-switch/skills/promotion-warrior/$CONFIG_FILE').read(); match=re.search(r'\`\`\`(?:yaml)?\n(.*?)\n\`\`\`', f, re.DOTALL); d=yaml.safe_load(match.group(1)) if match else yaml.safe_load(f); print(' '.join(d.get('keywords', {}).get('en', ['dating app'])))" 2>/dev/null)
  if [ -z "$USER_KEYWORDS" ] || [ "$USER_KEYWORDS" == "None" ]; then
      USER_KEYWORDS=$($PYTHON_CMD -c "import yaml; f=open('/Users/han/.cc-switch/skills/promotion-warrior/$CONFIG_FILE').read(); d=yaml.safe_load(f); print(' '.join(d.get('keywords', ['dating app'])))" 2>/dev/null)
  fi
  PRIMARY_KW=$(echo "$USER_KEYWORDS" | awk '{print $1}')
  X_QUERIES=("$PRIMARY_KW 推荐" "$PRIMARY_KW 梯子" "求 $PRIMARY_KW" "$PRIMARY_KW 机场" "机场 推荐" "梯子 稳定" "$PRIMARY_KW 挂了" "zero matches" "dating apps suck")

  for X_QUERY in "${X_QUERIES[@]}"; do
    echo "  [Sniping X] Matrix Query: $X_QUERY"
    opencli twitter search "$X_QUERY" --limit 10 -f json 2>/dev/null | $PYTHON_CMD -c "import json,sys;d=json.load(sys.stdin);[print(p['id']) for p in d]" 2>/dev/null | while read tid; do
      if [ -z "$tid" ]; then continue; fi
      if grep -q "$tid" /Users/han/.cc-switch/skills/promotion-warrior/sent_posts.log 2>/dev/null; then continue; fi

      REPLY=$($PYTHON_CMD /Users/han/.cc-switch/skills/promotion-warrior/tools/dm_randomizer.py "X_SNIPE" "$CURRENT_PERSONA" "$AFFILIATE_LINK" "/Users/han/.cc-switch/skills/promotion-warrior/$CONFIG_FILE")
      if opencli twitter reply "$tid" "$REPLY" 2>/dev/null; then
          echo "  ✅ 已截流 X (Twitter): $tid"
          echo "$tid" >> /Users/han/.cc-switch/skills/promotion-warrior/sent_posts.log
      fi
      sleep 10
    done
  done

  echo "========= $(date '+%H:%M') 结束 $NICHE_NAME ========="
  echo ""
done
