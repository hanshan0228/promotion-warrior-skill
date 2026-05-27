#!/bin/bash
# ================================================================
# Reddit Visibility Checker (Shadow-ban Detection)
# ================================================================
LOGFILE="/tmp/reddit-visibility.log"
TARGET_URL="$1"
COMMENT_ID="$2"

[ -z "$TARGET_URL" ] || [ -z "$COMMENT_ID" ] && exit 1

echo "[$(date)] Checking visibility for $COMMENT_ID on $TARGET_URL" >> "$LOGFILE"

# 用无 Cookie 的 curl 模拟游客访问，检查源码中是否包含该评论 ID
# 很多时候 removed 的评论在作者视角可见，但在游客视角被隐藏
IS_VISIBLE=$(curl -s -L "$TARGET_URL" | grep "$COMMENT_ID")

if [ -z "$IS_VISIBLE" ]; then
    echo "❌ INVISIBLE (Shadow-banned or Auto-removed)" >> "$LOGFILE"
    # 触发 Bark 告警
    BARK_KEY=$(grep 'key:' /Users/han/.agents/skills/promotion-warrior/config.md | grep -v daily_limit | head -1 | sed 's/.*key: *"//' | sed 's/".*//')
    [ -n "$BARK_KEY" ] && curl -s "https://api.day.app/${BARK_KEY}/Reddit告警/账号权重不足评论被拦截?group=reddit_alert&sound=alarm" >/dev/null
    exit 1
else
    echo "✅ VISIBLE" >> "$LOGFILE"
    exit 0
fi
