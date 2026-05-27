# 黑名单与举报防御 — blacklist.md

> 记录所有举报过我们、导致内容被删或账号受损的用户和内容类型。
> Agent 每次操作前必须检查此文件，主动规避已知风险。

---

## 用户黑名单

> 这些用户曾经举报过我们或导致账号受损，永久跳过。

```yaml
blocked_users:

  - id: "xhs:投诉达人小李"
    platform: "小红书"
    reason: "举报了3次，导致账号A收到平台警告"
    date_added: "2026-03-20"
    severity: "high"
    notes: "该用户专门举报推广内容"

  - id: "reddit:u/spam_hunter"
    platform: "Reddit"
    reason: "在 r/productivity 举报了我们的评论，帖子被删"
    date_added: "2026-04-01"
    severity: "medium"

  - id: "tw:@reportbot_x"
    platform: "X"
    reason: "疑似举报机器人账号"
    date_added: "2026-04-10"
    severity: "high"
```

---

## 内容黑名单

> 这些内容类型/话题曾导致我们内容被删或账号被警告。

```yaml
blocked_content_patterns:

  - pattern: "扫码领取"
    platforms: ["xiaohongshu", "weibo"]
    reason: "触发平台违禁词，内容被删"
    date_added: "2026-02-15"
    severity: "critical"

  - pattern: "私信我获取优惠"
    platforms: ["xiaohongshu"]
    reason: "被平台识别为引流内容，账号降权"
    date_added: "2026-03-01"
    severity: "high"

  - pattern: "直接在评论里放 affiliate 链接"
    platforms: ["all"]
    reason: "通用规则，必然触发风控"
    date_added: "系统内置"
    severity: "critical"

  - pattern: "我有内部优惠码"
    platforms: ["instagram", "tiktok"]
    reason: "被多个用户举报为垃圾营销"
    date_added: "2026-04-05"
    severity: "high"
```

---

## 高风险话题黑名单

> 这些话题下发内容极易被举报，即使内容本身没问题。

```yaml
high_risk_topics:

  - topic: "负面评价帖/投诉帖"
    rule: "永远不在这类帖子下发任何推广相关内容"
    detection: "帖子标题或内容含：踩雷/避雷/投诉/差评/骗人/维权"

  - topic: "价格投诉/售后纠纷"
    rule: "跳过，不参与"
    detection: "内容含：退款/售后/被骗/假货"

  - topic: "平台反广告运动"
    rule: "检测到相关话题热搜时，全平台降低推广强度 50%"
    detection: "trending_monitor 扫到：整治营销号/清理广告"
```

---

## 账号风险地图

> 记录哪些账号在哪些话题/版块下已经触发过风控

```yaml
account_risk_map:

  - account: "小红书账号A"
    risky_topics: ["减肥产品", "医疗相关"]
    risky_boards: ["健康养生"]
    reason: "曾在这些话题下被折叠2次"
    restriction: "该账号不在这些话题下发任何内容"

  - account: "u/reddit_a"
    risky_subreddits: ["r/frugal"]
    reason: "在该版块被mod删帖一次"
    restriction: "该账号不再进入此版块"
```

---

## 举报应急处理

当收到平台举报通知时：

```
Step 1：立即停止该账号的所有操作
Step 2：将举报者加入 blocked_users
Step 3：分析被举报的内容，提取 pattern 加入 blocked_content_patterns
Step 4：评估账号损伤程度，更新 account_health.md
Step 5：48 小时内不在该平台的相同话题下操作
Step 6：写入 error_log.md，通知用户（alert_system P1）
```

---

## 防举报预检

每条内容发出前自动检查：

```
1. 目标用户是否在 blocked_users 列表中？
2. 内容是否包含 blocked_content_patterns 中的模式？
3. 当前账号是否有 account_risk_map 中对应的限制？
4. 话题是否属于 high_risk_topics？
全部通过 → 可以发出
任一命中 → 取消本条操作，记录日志
```
