# 私域承接端 — backend_bridge.md

> 私信只是入口，承接端决定最终转化率。
> 本文件定义私信之后的完整承接流程，确保前端流量不流失。

---

## 承接端类型配置

```yaml
backend_type: "填入你的承接方式"
# 可选：wechat_private / wechat_group / telegram / independent_site / link_in_bio
```

---

## 承接方式详细配置

### 方式 A：微信私域

```yaml
wechat:
  # 加微信的话术（私信中不能直接说"加我微信"，要用暗语或引导）
  invite_method: "indirect"    # indirect=间接引导 / qrcode=二维码 / keyword=关键词触发

  # 间接引导话术（在私信中用）
  indirect_phrases_zh:
    - "方便的话可以加个联系方式，我把资料发你"
    - "这个说起来比较复杂，私下聊比较方便"
    - "有个详细的对比我整理过，发你看看？"

  # 通过后的欢迎语（用户加上后第一条消息）
  welcome_message_zh: |
    你好！看到你在[平台]问的问题，刚好我研究过这块
    给你发个我整理的对比资料，看看对你有没有帮助～
    有问题随时问我

  # 朋友圈配合（加上后朋友圈要有配合内容，不能是空号）
  moments_strategy: "每天 1-2 条，70% 生活内容，30% niche 相关分享"

  # 微信群承接（有群的情况下）
  group:
    enabled: false
    invite_after_days: 3      # 加好友 X 天后邀请入群
    group_name: "填入群名"
```

### 方式 B：Telegram 频道/群组

```yaml
telegram:
  channel_link: "https://t.me/your_channel"
  group_link: "https://t.me/your_group"

  # 私信中的引导话术（英文平台）
  invite_phrases_en:
    - "I put together a resource doc, easier to share on Telegram — want me to send it over?"
    - "I have a comparison guide I can share, what's the best way to reach you?"

  # 加入后的欢迎消息
  welcome_message_en: |
    Hey! Saw your question about [topic] — dropped you a message here
    I put together some notes on this, sharing below
    Feel free to ask anything 👇

  # 频道内容节奏
  channel_posting: "每天 1-2 条 niche 相关有用内容，不超过 30% 推广"
```

### 方式 C：独立站 / Affiliate 落地页

```yaml
independent_site:
  landing_page_url: "https://your-site.com"

  # 链接传递方式（不能在评论里直接发）
  link_delivery_method: "dm_only"    # 只在私信里发

  # 私信中的话术
  link_phrases_zh:
    - "我把链接发你，你自己看看，不一定适合你"
    - "这个我是在这里找到的，你参考一下"
  link_phrases_en:
    - "here's the link, take a look — not sure if it's exactly what you need"
    - "found this a while back, might be relevant for you"

  # UTM 参数追踪（区分不同平台来源）
  utm_tracking:
    xiaohongshu: "?utm_source=xhs&utm_medium=dm"
    weibo: "?utm_source=weibo&utm_medium=dm"
    instagram: "?utm_source=ig&utm_medium=dm"
    twitter_x: "?utm_source=twitter&utm_medium=dm"
    reddit: "?utm_source=reddit&utm_medium=dm"
    tiktok: "?utm_source=tiktok&utm_medium=dm"
    facebook: "?utm_source=fb&utm_medium=dm"
    douyin: "?utm_source=douyin&utm_medium=dm"
```

---

## 承接漏斗追踪

```
前端（社媒）→ 私信转化 → 承接端 → 最终转化

每个阶段追踪：
  私信发出数（conversation_tracker.md）
  ↓
  私信回复数（Stage 1+）
  ↓
  承接端到达数（加微信/进群/点击链接）
  ↓
  最终购买/注册数（cost_tracker.md → Affiliate 收益记录）
```

---

## 承接端质量检查

Agent 每周检查以下指标，低于阈值时通知用户：

```yaml
quality_checks:
  # 私信回复 → 承接端转化率（太低说明承接话术有问题）
  dm_to_backend_rate_min: 0.30    # 低于 30% 预警

  # 承接端 → 最终转化率
  backend_to_conversion_rate_min: 0.05   # 低于 5% 预警

  # 微信加好友通过率（太低说明账号或话术有问题）
  wechat_accept_rate_min: 0.60    # 低于 60% 预警
```

---

## 承接端内容日历配合

私域内容要与社媒节奏配合，节假日前社媒加大投放的同时，私域要同步做好承接准备：

```
节假日前 3 天：
  - 微信朋友圈/Telegram 频道预热节日相关内容
  - 群内提前发福利预告，提升活跃度

节假日当天：
  - 准备好快速回复话术，社媒流量进来时能及时承接
  - 不要让用户等超过 2 小时没有回应

节假日后：
  - 跟进未转化的线索，发送节后内容
```
