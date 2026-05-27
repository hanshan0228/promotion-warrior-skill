# 平台政策监控 — policy_monitor.md

> 各平台规则在持续变化，人工感知太慢。
> 本文件定期检查平台规则变化，自动更新到系统配置。

---

## 监控来源

```yaml
monitor_sources:
  xiaohongshu:
    - url: "https://www.xiaohongshu.com/protocol/community-rules"
    - url: "https://creator.xiaohongshu.com/creator/home"   # 创作者中心公告
    - signal: "关注小红书官方账号的公告帖"
    check_frequency: "每周二"

  weibo:
    - url: "https://weibo.com/admin"    # 微博官方公告
    - signal: "微博管理员公告"
    check_frequency: "每周二"

  instagram:
    - url: "https://help.instagram.com/477434105621119"  # Community Guidelines
    - url: "https://www.instagram.com/blog/"
    check_frequency: "每两周"

  twitter_x:
    - url: "https://help.twitter.com/en/rules-and-policies"
    - url: "https://blog.twitter.com/"
    check_frequency: "每两周"

  reddit:
    - url: "https://www.redditinc.com/policies/content-policy"
    - signal: "监控各目标 subreddit 的 mod 公告"
    check_frequency: "每周，subreddit规则每天检查"

  tiktok:
    - url: "https://www.tiktok.com/community-guidelines"
    check_frequency: "每两周"

  facebook:
    - url: "https://www.facebook.com/communitystandards/"
    check_frequency: "每月"

  douyin:
    - url: "https://creator.douyin.com/creator-micro/home"
    check_frequency: "每周二"
```

---

## 关键变化检测项

每次检查时，重点关注以下内容是否有变化：

```
1. 私信/DM 发送限制（频率/数量上限）
2. 评论内容规则（哪些词/内容类型被禁）
3. 外链政策（能否在评论/简介里放链接）
4. 账号封禁标准（什么行为会导致封号）
5. 营销内容规范（推广内容的标注要求）
6. 新功能上线（可能带来新的操作机会）
```

---

## 政策变化记录

| 日期 | 平台 | 变化类型 | 具体内容 | 影响评估 | 已更新到 |
|------|------|----------|----------|----------|----------|
| 2026-04-15 | 小红书 | 私信限制 | 新账号（注册<30天）每日私信上限从20条降为5条 | 高，影响新号养号策略 | accounts.md, warmup_plan.md |
| 2026-04-01 | Reddit | subreddit规则 | r/productivity 新增规则：不允许任何形式的产品推荐 | 高，该版块停止操作 | blacklist.md, config.md |
| 2026-03-20 | Instagram | 算法变化 | Reels 互动权重提升，普通帖子权重下降 | 中，调整内容策略 | content_calendar.md |
| 2026-03-10 | X | 私信政策 | 非互关用户的私信进入请求箱，接受率下降 | 高，先 follow 再私信更重要 | SKILL.md |

---

## 自动更新触发

发现政策变化后，自动触发对应文件更新：

```yaml
auto_update_map:

  "私信频率限制变化":
    update_files: ["accounts.md", "SKILL.md"]
    update_content: "对应平台的每账号私信上限"

  "新增违禁词":
    update_files: ["config.md"]
    update_content: "forbidden_words 列表"

  "subreddit规则变化":
    update_files: ["blacklist.md", "config.md"]
    update_content: "禁用该 subreddit 或调整操作策略"

  "平台整体收紧":
    update_files: ["account_health.md", "content_calendar.md"]
    update_content: "该平台操作强度降低 30%，持续观察"

  "新功能/新机会":
    update_files: ["SKILL.md", "content_calendar.md"]
    update_content: "加入新的操作方式说明"
```

---

## 平台风险评级（实时更新）

| 平台 | 当前风险等级 | 主要风险点 | 建议操作强度 | 上次评估 |
|------|------------|-----------|------------|----------|
| 小红书 | 🟡 中 | 新账号私信限制收紧 | 正常，新号谨慎 | 2026-04-15 |
| 微博 | 🟢 低 | 暂无重大变化 | 正常 | 2026-04-10 |
| 抖音 | 🟢 低 | 暂无重大变化 | 正常 | 2026-04-10 |
| Instagram | 🟡 中 | 非互关私信接受率下降 | 正常，先互关再私信 | 2026-04-01 |
| X | 🟡 中 | 私信进请求箱 | 正常，先互关 | 2026-03-10 |
| Facebook | 🟢 低 | 暂无重大变化 | 正常 | 2026-04-01 |
| Reddit | 🔴 高 | 多个目标版块收紧规则 | 降低 50%，谨慎 | 2026-04-01 |
| TikTok | 🟡 中 | 算法变化频繁 | 正常，多发评论少私信 | 2026-04-05 |

---

## 政策监控周报（每周二自动生成）

```
📋 平台政策监控周报 [日期]

本周变化：
  [有变化则列出，无变化则显示"本周各平台无重大政策变化"]

风险等级变化：
  [有变化则标注，例如：Reddit 从 🟡中 升为 🔴高]

自动执行的更新：
  [列出本周因政策变化自动更新的配置]

需要人工处理：
  [列出需要用户确认的变化]
```
