# 异常通知系统 — alert_system.md

> 账号被封、代理失效、预算超限等情况需要实时推送，不能只写日志等你去看。
> 本文件配置通知渠道和分级规则。

---

## 通知渠道配置

```yaml
channels:
  # 微信推送（通过企业微信机器人或 Server酱）
  wechat:
    enabled: true
    method: "server_chan"          # server_chan / wechat_work_bot
    server_chan_key: "填入你的 Server酱 SendKey"
    # Server酱：https://sct.ftqq.com/
    # 免费版每天 5 条，付费版无限制

  # Telegram Bot 推送
  telegram:
    enabled: false
    bot_token: "填入 Bot Token"
    chat_id: "填入你的 Chat ID"

  # 飞书 Webhook
  feishu:
    enabled: false
    webhook_url: "填入飞书机器人 Webhook URL"

  # 邮件（备用）
  email:
    enabled: false
    smtp_host: "smtp.gmail.com"
    smtp_port: 587
    from: "your@email.com"
    to: "your@email.com"
    password: "填入邮箱密码"
```

---

## 通知分级

### P0 — 紧急（立即推送，任何时间）

```yaml
p0_alerts:
  - event: "account_banned"
    message: "🚨 账号被封！{platform} 账号 {account} 已被封禁，请立即处理"
    action_required: "检查账号状态，考虑申诉或重开"

  - event: "all_proxies_failed"
    message: "🚨 代理全部失效！{platform} 所有代理不可用，操作已暂停"
    action_required: "检查代理商，更换或补充代理"

  - event: "budget_exceeded"
    message: "🚨 预算超限！今日已花费 ${amount}，已暂停所有操作"
    action_required: "检查 cost_tracker.md，调整预算或确认继续"

  - event: "all_sessions_expired"
    message: "🚨 {platform} 所有账号 Cookie 失效，操作已暂停"
    action_required: "重新登录所有账号"

  - event: "api_all_keys_failed"
    message: "🚨 {model} 所有 API key 失效，无法生成内容"
    action_required: "检查 API key 状态，补充有效 key"
```

### P1 — 重要（立即推送，但不叫醒）

```yaml
p1_alerts:
  - event: "account_cooldown"
    message: "⚠️ {platform} 账号 {account} 触发限流，冷却 {hours} 小时"

  - event: "session_expiring_soon"
    message: "⚠️ {platform} 账号 {account} Cookie 将在 {days} 天后过期，请及时更新"

  - event: "health_score_critical"
    message: "⚠️ {platform} 账号 {account} 健康分降至 {score}，已降低操作强度"

  - event: "proxy_degraded"
    message: "⚠️ 代理 {proxy_id} 响应异常（{ms}ms），已切换备用"

  - event: "daily_budget_warning"
    message: "⚠️ 今日已花费 ${amount}，接近预算上限 ${limit}"

  - event: "platform_risk_detected"
    message: "⚠️ {platform} 疑似收紧管控，{count} 个账号同时触发限流"
```

### P2 — 提示（汇总到每日/每周报告）

```yaml
p2_alerts:
  - event: "new_reply_p0"
    message: "💬 {platform} 用户 {user} 主动私信，等待回复"

  - event: "conversion_achieved"
    message: "🎉 {platform} 用户 {user} 完成转化！"

  - event: "ab_test_winner"
    message: "📊 A/B 测试 {test_id} 已产生胜者：{winner}，回复率 {rate}"

  - event: "auto_update_applied"
    message: "🔄 系统自动更新了 {file}：{change_summary}"

  - event: "competitor_viral_post"
    message: "📈 竞品 {account} 在 {platform} 出现爆文（{metric}），已加入情报队列"
```

---

## 每日汇总报告

每天 23:00 自动发送：

```
📊 Promotion Warrior 日报 [日期]

今日操作概览：
  评论发出：X 条（Tier1: X / Tier2: X）
  私信发出：X 条
  新增对话：X 个
  收到回复：X 条
  转化：X 个

账号状态：
  正常：X 个 | 冷却：X 个 | 需要处理：X 个

今日花费：$X.XX（预算剩余：$X.XX）

待处理事项：
  - [列出需要人工处理的事项]

明日计划：
  - [基于日历和当前状态的明日预期操作]
```

---

## 通知静默时段

```yaml
quiet_hours:
  enabled: true
  start: "23:30"
  end: "07:00"
  # 静默时段内只有 P0 级别才推送
  p0_always_send: true
```

---

## 通知历史（Agent 自动维护）

| 时间 | 级别 | 事件 | 内容摘要 | 是否已处理 |
|------|------|------|----------|------------|
| — | — | — | — | 待处理 |
