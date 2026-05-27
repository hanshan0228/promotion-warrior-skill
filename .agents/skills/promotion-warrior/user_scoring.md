# 用户分层评分 — user_scoring.md

> 不是所有目标用户都值得同等投入。
> 本文件对每个接触过的用户打分，高分用户投入好模型+更多时间，低分用户快速止损。

---

## 用户价值评分维度

每个用户从以下维度综合评分（满分 100）：

```yaml
scoring_dimensions:

  intent_score:           # 购买意图强度（最重要）
    weight: 40
    signals:
      asked_price: +20          # 主动问价格
      asked_where_to_buy: +20   # 问哪里买
      asked_for_link: +25       # 主动要链接
      expressed_pain: +15       # 表达了明确痛点
      said_considering: +10     # 说"在考虑"
      just_casual_question: +5  # 只是随便问问

  engagement_score:       # 互动深度
    weight: 25
    signals:
      replied_dm: +20           # 回复了私信
      replied_comment: +10      # 回复了评论
      liked_our_content: +5     # 点赞了我们内容
      followed_account: +15     # 关注了我们账号
      shared_our_content: +20   # 转发/收藏了我们内容

  profile_score:          # 用户画像匹配度
    weight: 20
    signals:
      matches_target_persona: +20   # 完全匹配目标用户画像
      partial_match: +10            # 部分匹配
      has_purchase_history: +15     # 简介/内容显示有购买行为
      high_follower_koc: -5         # KOC（可能只是蹭内容不买）

  response_quality:       # 回复质量
    weight: 15
    signals:
      detailed_reply: +15       # 回复内容详细认真
      short_but_engaged: +8     # 简短但明显感兴趣
      one_word_reply: +2        # 只回了一个字
      asking_more: +15          # 主动追问更多
```

---

## 用户分层

| 分层 | 分数区间 | 标签 | 资源分配策略 |
|------|----------|------|------------|
| S 级 | 80-100 | 🔥 高意向 | 最好模型（L6）+ 优先跟进 + 人工审核私信 |
| A 级 | 60-79 | ⭐ 有意向 | 好模型（L5）+ 正常跟进流程 |
| B 级 | 40-59 | 👀 观察中 | 中等模型（L3）+ 保持接触，不主动推进 |
| C 级 | 20-39 | 💤 低意向 | 小模型（L2）+ 最多2轮跟进，不转化就放弃 |
| D 级 | 0-19 | ❌ 无意向 | 停止跟进，移入冷池 |

---

## 用户评分记录

> 格式：平台:用户名 → 评分 + 分层 + 评分依据

```yaml
scored_users:

  - id: "xhs:晨晨_life"
    score: 85
    tier: "S"
    niche: "niche_01"
    score_breakdown:
      intent: 38      # 问了价格+要了链接
      engagement: 20  # 回复了私信，详细
      profile: 15     # 匹配目标画像
      response: 12    # 回复质量高
    last_updated: "2026-04-26"
    assigned_model: "claude-sonnet"
    notes: "强烈兴趣，等待最终决策"

  - id: "ig:@sarah.k"
    score: 62
    tier: "A"
    niche: "niche_01"
    score_breakdown:
      intent: 25
      engagement: 18
      profile: 12
      response: 7
    last_updated: "2026-04-26"
    assigned_model: "gpt-4o"
    notes: "感兴趣但犹豫，需要多一轮信任建立"

  - id: "weibo:科技控007"
    score: 35
    tier: "C"
    niche: "niche_01"
    score_breakdown:
      intent: 10
      engagement: 12
      profile: 8
      response: 5
    last_updated: "2026-04-25"
    assigned_model: "gemini-flash"
    notes: "只是随便问，最多再跟进1次"
```

---

## 评分更新规则

每次与用户互动后自动更新评分：

```
用户回复私信 → engagement_score 更新
用户问价格/要链接 → intent_score 大幅提升 → 立即升层
用户72h不回复 → score -10，考虑降层
用户明确拒绝 → 直接降为D级，移入冷池
```

---

## 冷池管理

D 级用户进入冷池，30 天后可以重新评估：

```yaml
cold_pool:
  - id: "xhs:用户A"
    entered: "2026-03-15"
    reason: "明确表示不感兴趣"
    reactivate_date: "2026-04-15"
    reactivate_check: "是否有新的购买信号"
```

---

## 高价值用户特别处理

S 级用户触发以下额外操作：

```
1. 通知用户（alert_system.md P2）："高价值用户 [ID] 升入 S 级"
2. 分配 claude-sonnet 处理所有后续回复
3. 回复前人工审核（如 review_mode=true）
4. 在 conversation_tracker.md 中标记为 VIP
5. 允许更短的回复间隔（最短 1 小时，而不是 2 小时）
```
