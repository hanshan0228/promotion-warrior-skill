# 风险分散策略 — risk_diversification.md

> 所有账号跑同一套策略是系统性风险。
> 本文件定义账号矩阵的多样化配置，确保单一风险不导致全局崩溃。

---

## 风险分散的四个维度

```
维度 1：人设多样化    → 不同账号扮演不同身份
维度 2：切入角度多样化 → 不同账号用不同话题切入同一 niche
维度 3：平台分散      → 不过度依赖单一平台
维度 4：转化路径多样化 → 不同账号指向不同承接端
```

---

## 账号矩阵设计

### 人设矩阵（不同身份，覆盖不同用户群）

```yaml
account_matrix:

  # 身份 A：普通用户型（最多，60% 账号）
  type_a_regular_user:
    description: "普通人分享使用经历，亲切真实"
    platforms: ["xiaohongshu", "weibo", "instagram", "tiktok"]
    approach: "共情 + 分享经验"
    target_users: "刚开始了解这个 niche 的新手"
    persona_files: ["zh_persona_1", "en_persona_1"]
    risk_level: "low"   # 最自然，风险最低

  # 身份 B：深度研究型（20% 账号）
  type_b_researcher:
    description: "对领域有深度研究，给专业建议"
    platforms: ["weibo", "reddit", "twitter_x", "facebook"]
    approach: "专家分析 + 对比测评"
    target_users: "认真在做决策的中级用户"
    persona_files: ["zh_persona_2", "en_persona_2"]
    risk_level: "medium"

  # 身份 C：踩坑者型（10% 账号）
  type_c_been_there:
    description: "踩过坑、走过弯路，分享避坑经验"
    platforms: ["xiaohongshu", "douyin", "tiktok"]
    approach: "避坑 + 对比 + 推荐"
    target_users: "谨慎型用户，怕被坑"
    persona_files: ["zh_persona_1", "en_persona_1"]
    risk_level: "low"

  # 身份 D：社群达人型（10% 账号）
  type_d_community:
    description: "活跃于相关社群，擅长互动和建立连接"
    platforms: ["facebook", "reddit", "weibo"]
    approach: "社群互动 + 口碑传播"
    target_users: "喜欢社群归属感的用户"
    persona_files: ["en_persona_2", "zh_persona_2"]
    risk_level: "medium"
```

---

## 切入角度分散

同一个 niche，不同账号用不同切入角度，避免所有账号都在说同一件事：

```yaml
angle_distribution:
  angle_a: "省钱/性价比角度"         # 30% 账号
  angle_b: "效果/结果角度"           # 25% 账号
  angle_c: "简单/省时角度"           # 20% 账号
  angle_d: "对比/选择角度"           # 15% 账号
  angle_e: "新手入门/避坑角度"       # 10% 账号
```

每个账号在 accounts.md 中标注 `angle` 字段，生成内容时必须围绕该角度切入。

---

## 平台依赖度控制

```yaml
platform_dependency_limits:
  # 单一平台的账号数量不超过总数的 X%
  max_accounts_per_platform: 0.30   # 30%

  # 单一平台的操作量不超过总量的 X%
  max_volume_per_platform: 0.35     # 35%

  # 如果某平台当日出现异常（多账号同时限流），触发平台风险警报
  platform_risk_threshold: 0.5     # 50% 以上账号同时出问题 = 平台风险
```

---

## 转化路径分散

```yaml
conversion_path_distribution:
  # 不同比例的账号指向不同承接端
  wechat_private: 0.40     # 40% 账号引导加微信
  telegram: 0.25           # 25% 账号引导进 Telegram
  direct_link: 0.25        # 25% 账号直接发 affiliate 链接
  no_conversion: 0.10      # 10% 纯养号账号，不做转化（保护整体账号矩阵）
```

---

## 风险隔离规则

```
账号分组隔离：
  将所有账号分为 A/B/C 三组，每组包含各类型账号
  正常情况下三组同时运行
  某平台出现风险时，先暂停 A 组，观察 24 小时
  风险扩大 → 暂停 B 组，只保留 C 组最保守的操作
  风险解除后 → 先恢复 A 组，观察 48 小时无异常后恢复 B 组

niche 分散（可选，长期策略）：
  主力 niche：60% 资源
  次要 niche 1：25% 资源（相关但不完全相同）
  次要 niche 2：15% 资源（探索新方向）
  任意单一 niche 出问题，损失不超过 60%
```

---

## 账号矩阵现状（手动维护）

| 账号ID | 平台 | 类型 | 切入角度 | 转化路径 | 隔离组 | 当前状态 |
|--------|------|------|----------|----------|--------|----------|
| 填入 | 小红书 | type_a | angle_a | wechat | A组 | active |
| 填入 | Instagram | type_b | angle_d | telegram | B组 | active |

---

## 风险事件记录

| 日期 | 风险类型 | 影响范围 | 触发阈值 | 处理措施 | 恢复时间 |
|------|----------|----------|----------|----------|----------|
| — | — | — | — | — | — |
