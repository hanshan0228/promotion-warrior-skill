# 成本与 ROI 追踪 — cost_tracker.md

> 追踪每天的实际花费和每个转化的获客成本，找出 ROI 最高的平台和策略。
> Agent 每次操作后更新 token 消耗，每周日生成成本报告。

---

## 成本构成

```
总成本 = API 调用费用 + 代理 IP 费用 + （可选）账号购买费用
ROI = 转化收益 / 总成本
CPL（每个线索成本）= 总成本 / 进入 conversation_tracker 的用户数
CPA（每个转化成本）= 总成本 / 实际转化数
```

---

## API 定价配置（填入你的实际单价）

```yaml
api_pricing:
  # 单位：美元/百万 token（input/output 分开）
  gemini_flash:
    input: 0.075      # $0.075 / 1M tokens
    output: 0.30
  gpt4o:
    input: 2.50
    output: 10.00
  gpt4o_mini:
    input: 0.15
    output: 0.60
  claude_sonnet:
    input: 3.00
    output: 15.00
  deepseek_v3:
    input: 0.27
    output: 1.10

proxy_pricing:
  # 单位：美元/GB 或 美元/IP/月
  cn_residential: 3.00    # 美元/GB
  en_residential: 2.50    # 美元/GB
  datacenter: 0.50        # 美元/IP/月
  estimated_gb_per_day: 0.5  # 估算每天代理流量
```

---

## 每日成本记录（Agent 自动更新）

| 日期 | Tier1 Token | Tier2 Token | Tier3 Token | 分析 Token | API费用($) | 代理费用($) | 总费用($) | 新增线索 | 转化数 | CPL($) | CPA($) |
|------|-------------|-------------|-------------|------------|------------|------------|----------|---------|--------|--------|--------|
| 示例 | 28,000 | 42,000 | 44,800 | 3,000 | 0.85 | 0.25 | 1.10 | 5 | 1 | 0.22 | 1.10 |

---

## 平台 ROI 对比

| 平台 | 本周费用($) | 本周线索数 | 本周转化数 | CPL($) | CPA($) | ROI评级 |
|------|-----------|-----------|-----------|--------|--------|---------|
| 小红书 | 0 | 0 | 0 | — | — | 待统计 |
| 微博 | 0 | 0 | 0 | — | — | 待统计 |
| 抖音 | 0 | 0 | 0 | — | — | 待统计 |
| Instagram | 0 | 0 | 0 | — | — | 待统计 |
| X | 0 | 0 | 0 | — | — | 待统计 |
| Facebook | 0 | 0 | 0 | — | — | 待统计 |
| Reddit | 0 | 0 | 0 | — | — | 待统计 |
| TikTok | 0 | 0 | 0 | — | — | 待统计 |

---

## 模型成本对比

| 模型 | 本周调用次数 | 本周 Token 消耗 | 本周费用($) | 平均每条成本($) |
|------|-------------|----------------|------------|----------------|
| gemini-flash | 0 | 0 | 0 | — |
| gpt-4o | 0 | 0 | 0 | — |
| claude-sonnet | 0 | 0 | 0 | — |
| deepseek-v3 | 0 | 0 | 0 | — |

---

## 预算控制

```yaml
budget_limits:
  daily_max_usd: 5.00       # 每日最大花费（超出则停止当天操作）
  weekly_max_usd: 30.00     # 每周最大花费
  monthly_max_usd: 100.00   # 每月最大花费

  # 预警阈值（达到后通知用户）
  daily_warning_usd: 4.00
  weekly_warning_usd: 25.00

  # 低 ROI 自动暂停规则
  # 连续 7 天 CPA > X 美元的平台，自动暂停并通知用户
  auto_pause_cpa_threshold: 20.00
```

---

## 周报成本摘要（每周日自动生成）

```
💰 Promotion Warrior 成本周报 [日期]

本周总支出：$X.XX
├── API 费用：$X.XX（占 XX%）
│   ├── gemini-flash：$X.XX（Tier 1 主力）
│   ├── gpt-4o：$X.XX（Tier 2 主力）
│   └── claude-sonnet：$X.XX（Tier 3 主力）
└── 代理费用：$X.XX（占 XX%）

转化数据：
├── 总线索数：X 人（进入对话跟进）
├── 实际转化数：X 人
├── 平均 CPL：$X.XX / 线索
└── 平均 CPA：$X.XX / 转化

平台 ROI 排名：
  🥇 [平台]：CPA $X.XX
  🥈 [平台]：CPA $X.XX
  🥉 [平台]：CPA $X.XX
  ⚠️  [平台]：CPA $X.XX（建议减少投入）

建议：
  - [自动生成的优化建议]
```

---

## Affiliate 收益记录

| 日期 | 平台 | 用户 | 转化类型 | 预估收益($) | 是否已到账 |
|------|------|------|----------|------------|------------|
| — | — | — | — | — | — |
