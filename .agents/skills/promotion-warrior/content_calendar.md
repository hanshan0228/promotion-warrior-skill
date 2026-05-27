# 内容日历与排期 — content_calendar.md

> 真实运营有节奏，不是随机跑。
> 本文件定义每周/每月的操作节奏，Agent 根据日历决定本次操作强度。

---

## 运营节奏原则

```
强弱交替：密集投放后必须有休息期，避免账号行为过于规律
节假日前置：重要节点前 3-7 天开始加大投放，节点当天反而降低
冷启动保护：新账号前两周强制轻量运营，不参与密集投放期
平台错峰：不同平台在同一天使用不同强度，分散风险
```

---

## 每周节奏模板

```yaml
weekly_rhythm:
  monday:
    intensity: "medium"      # 周一：中等强度，周末积累的需求开始释放
    focus_platforms: ["xiaohongshu", "weibo", "instagram"]
    tier_distribution: {tier1: 5, tier2: 3, tier3: 2}

  tuesday:
    intensity: "high"        # 周二：全周最高峰
    focus_platforms: ["all"]
    tier_distribution: {tier1: 6, tier2: 4, tier3: 3}

  wednesday:
    intensity: "high"
    focus_platforms: ["all"]
    tier_distribution: {tier1: 6, tier2: 4, tier3: 3}

  thursday:
    intensity: "medium"      # 周四：稍降，养号
    focus_platforms: ["douyin", "tiktok", "twitter_x"]
    tier_distribution: {tier1: 5, tier2: 3, tier3: 2}

  friday:
    intensity: "high"        # 周五：周末前冲量
    focus_platforms: ["all"]
    tier_distribution: {tier1: 7, tier2: 4, tier3: 3}

  saturday:
    intensity: "low"         # 周六：轻量运营，以 Tier 1 养号为主
    focus_platforms: ["xiaohongshu", "instagram", "tiktok"]
    tier_distribution: {tier1: 8, tier2: 2, tier3: 1}

  saturday:
    intensity: "rest"        # 周日：账号休息，只处理回复，不主动出击
    focus_platforms: []
    tier_distribution: {tier1: 0, tier2: 0, tier3: 0}
    only_do: ["reply_monitor", "conversation_tracker"]
```

---

## 每月节奏

```yaml
monthly_rhythm:
  week_1: "ramp_up"      # 第一周：爬坡，逐步提升强度
  week_2: "peak"         # 第二周：全力冲刺
  week_3: "maintain"     # 第三周：维持，观察数据
  week_4: "cooldown"     # 第四周：降温，账号休养，准备下月
```

---

## 节假日日历（中国）

```yaml
cn_holidays:
  - name: "春节"
    date_range: ["2027-01-28", "2027-02-04"]
    pre_boost_days: 7       # 节前 7 天加大投放
    during_intensity: "low" # 节中降低（用户都在过年）
    post_boost_days: 3      # 节后 3 天反弹期

  - name: "双11"
    date_range: ["2026-11-11", "2026-11-11"]
    pre_boost_days: 14
    during_intensity: "maximum"
    post_boost_days: 2

  - name: "618"
    date_range: ["2026-06-18", "2026-06-18"]
    pre_boost_days: 10
    during_intensity: "maximum"
    post_boost_days: 2

  - name: "双12"
    date_range: ["2026-12-12", "2026-12-12"]
    pre_boost_days: 7
    during_intensity: "high"
    post_boost_days: 1

  - name: "情人节"
    date_range: ["2027-02-14", "2027-02-14"]
    pre_boost_days: 5
    during_intensity: "high"
    post_boost_days: 0
```

---

## 节假日日历（全球英文平台）

```yaml
global_holidays:
  - name: "Black Friday"
    date_range: ["2026-11-27", "2026-11-27"]
    pre_boost_days: 14
    during_intensity: "maximum"
    post_boost_days: 3      # Cyber Monday 延续

  - name: "Cyber Monday"
    date_range: ["2026-11-30", "2026-11-30"]
    during_intensity: "maximum"

  - name: "Christmas"
    date_range: ["2026-12-25", "2026-12-25"]
    pre_boost_days: 14
    during_intensity: "medium"  # 圣诞当天用户不在线
    post_boost_days: 3

  - name: "New Year"
    date_range: ["2027-01-01", "2027-01-01"]
    pre_boost_days: 5
    during_intensity: "low"
    post_boost_days: 5      # 新年计划热潮

  - name: "Valentine's Day"
    date_range: ["2027-02-14", "2027-02-14"]
    pre_boost_days: 7
    during_intensity: "high"
    post_boost_days: 0
```

---

## 强度定义

```yaml
intensity_levels:
  maximum:
    tier_multiplier: 2.0    # 默认操作量的 2 倍
    interval_reduction: 0.7 # 操作间隔缩短到 70%
    platforms: "all"

  high:
    tier_multiplier: 1.5
    interval_reduction: 0.85
    platforms: "all"

  medium:
    tier_multiplier: 1.0    # 默认值
    interval_reduction: 1.0
    platforms: "focus_platforms"

  low:
    tier_multiplier: 0.5
    interval_reduction: 1.3
    platforms: "focus_platforms"

  rest:
    tier_multiplier: 0.0
    interval_reduction: 0
    platforms: []
    only_do: ["reply_monitor", "conversation_tracker", "trending_monitor"]
```

---

## 特殊排期（手动添加）

> 针对特定事件手动设置的一次性排期

| 日期 | 事件 | 强度 | 重点平台 | 重点内容方向 | 状态 |
|------|------|------|----------|-------------|------|
| 填入 | 填入事件名 | high | 小红书 | 填入内容方向 | 待执行 |

---

## 日历执行规则

Agent 每次启动时：
1. 读取今天是星期几 → 匹配 weekly_rhythm 强度
2. 检查今天是否在节假日范围内 → 节假日优先级高于周节奏
3. 检查特殊排期表是否有今日条目 → 特殊排期最高优先级
4. 将最终强度传入执行参数，覆盖 config.md 中的默认值
5. rest 模式下只执行 only_do 中列出的被动任务
