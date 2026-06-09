# 多 Niche 并行管理 — niche_manager.md

> 支持同时运营多个 affiliate 项目，数据完全隔离，账号组独立分配。
> Agent 每次启动时先读取本文件，确认当前激活的 niche 和账号组。

---

## Niche 列表

```yaml
niches:
- id: dating_affiliate
  name: MatchFix Dating Engine
  status: inactive
  priority: 1
  account_group: group_dating
  config_file: niches/dating/config.md
  budget_daily_usd: 0.0
  start_date: '2026-05-23'
  notes: 当前主力项目 — 全平台情感截流与约会 Affiliate
- id: ai_tool_cashback_sniper
  name: AI Tool Cashback Sniper
  status: inactive
  priority: 2
  account_group: group_saas
  config_file: niches/ai_tool_cashback_sniper/config.md
  notes: 拦截正在考虑订阅 ChatGPT, Canva, Notion 等 AI 工具的高净值用户，引导至返现平台。
  start_date: '2026-06-08'
- id: luxury_travel_sniper
  name: Luxury Travel Sniper
  status: active
  priority: 2
  account_group: group_default
  config_file: niches/luxury_travel_sniper/config.md
  notes: 拦截正在预订高端酒店、机酒比价的高净值用户，引导至返现平台并提供机酒叠加攻略。
  start_date: '2026-06-08'
- id: fintech___rewards_sniper
  name: Fintech & Rewards Sniper
  status: inactive
  priority: 2
  account_group: group_default
  config_file: niches/fintech___rewards_sniper/config.md
  notes: 拦截正在挑选高收益信用卡、理财工具或讨论开卡奖励的用户，引导至高端金融返现与推荐链接。
  start_date: '2026-06-08'
- id: high_end_tech_sniper
  name: High-End Tech Sniper
  status: active
  priority: 2
  account_group: group_default
  config_file: niches/high_end_tech_sniper/config.md
  notes: 拦截正在购买 MacBook, 摄影器材或高端家电的用户，引导至高额返现通道并分享价格追踪攻略。
  start_date: '2026-06-08'
```

---

## 账号组分配规则

```yaml
account_groups:
  group_dating:
    platforms: ["reddit", "twitter_x", "tiktok", "instagram", "youtube"]
    accounts:
      reddit: ["u/hanshan0228"]
      twitter_x: ["@hanshan0228"]
      tiktok: ["hanshan0228"]
      instagram: ["hanshan0228"]
      youtube: ["hanshan0228"]
```

**账号组隔离原则：**
- 同一账号不能同时属于两个 niche 的账号组
- 账号组之间不做协同操作（避免跨 niche 暴露）
- 各 niche 的 promotion_log、performance、cost_tracker 数据完全分开存储

---

## 数据隔离结构

每个 niche 有独立的数据目录：

```
promotion-warrior/
├── niches/
│   └── dating/
│       ├── config.md
│       ├── intel.md
│       └── promotion_log.md
└── shared/
    ├── accounts.md
    ├── proxy_manager.md
    ├── session_manager.md
    ├── blacklist.md
    └── cross_platform_users.md
```

---

## 每日预算分配

```yaml
total_daily_budget: 0.00
# 纯有机推广，无 API 调用成本
```

---

## 执行调度规则

```
同一时间只运行一个 niche 的操作

调度顺序：
  1. 先处理回复监控（reply_monitor）
  2. 再按 priority 顺序执行主动操作
```

---

## Niche 效果追踪

| Niche | 本周花费 | 本周线索 | 本周转化 | CPA | ROI |
|-------|---------|----------|---------|-----|-----|
| Dating Affiliate | $0 | 0 | 0 | — | — |
