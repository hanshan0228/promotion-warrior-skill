# 语义指纹与去重引擎 — dedup_engine.md

> 记录最近 200 条回复的语义特征，确保内容多样性，规避平台反垃圾系统。

---

## 内容指纹记录 (Recent 200)

| 语义 ID | 切入角度 | 核心关键词 | 情感基调 | 使用次数 | 状态 |
|---------|----------|------------|----------|----------|------|
| F-001 | 技术对比 | Lip-sync, Avatar IV | 专业/客观 | 12 | ⚠️ 冷却中 (相似度高) |
| F-002 | 成本优化 | ROI, Agency, Scalability | 商业/引导 | 5 | ✅ 活跃 |
| F-003 | 审美批判 | Cinematic, Textures, Lighting | 导演/感性 | 3 | ✅ 活跃 |
| F-004 | 翻译出海 | Multilingual, Global, Translation | 专家/实用 | 2 | ✅ 活跃 |
| F-005 | 情感共鸣 | Community, Stories, Joy | 温暖/共情 | 8 | ✅ 活跃 |

---

## 去重逻辑 (Engine Rules)

1. **强制轮换**: 连续 3 次使用相同“切入角度”后，必须强制切换到另一个人设和情感基调。
2. **关键词抑制**: 如果 "HeyGen" 在近 5 条回复中出现超过 3 次，下一条回复严禁使用品牌词，改为“技术方案描述”。
3. **句式混淆**: 每次生成内容必须随机从 3 种开篇方式中选取：
    - 提问式: "Have you noticed how...?"
    - 回应式: "I ran into the same issue with..."
    - 观察式: "The market seems to be moving towards..."
