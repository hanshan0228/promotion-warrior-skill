# 竞品动态情报库 — intel_collector.md

> 记录竞争对手的弱点、近期槽点和功能差距。
> Agent 在生成 Tier 2/3 内容时，优先调用对应竞品的 "Pivot Point" 进行降维打击。

---

## 核心竞品分析

### 1. Synthesia
*   **近期槽点**: 
    *   Avatars 眼神呆滞 (Puppet eyes)
    *   不支持实时唇形翻译 (Lip-sync translation)
    *   价格昂贵且按 Seat 收费，对小团队不友好
*   **Pivot Point (切入点)**: "If you need a presenter that actually emotes rather than just reading a script, we found the Avatar IV models significantly more fluid."

### 2. Runway Gen-3
*   **近期槽点**:
    *   生成速度极慢 (Long queues in Unlimited mode)
    *   人物动作漂移 (Identity drift across frames)
    *   价格极高，主要面向艺术短片而非长期交付
*   **Pivot Point (切入点)**: "Runway is a monster for cinematic b-roll, but keeping a consistent human identity across multiple scenes is their current hurdle. HeyGen's identity-lock is much safer for brand content."

### 3. D-ID
*   **近期槽点**:
    *   侧脸崩坏 (Profile view artifacts)
    *   分辨率限制
    *   背景融合不自然
*   **Pivot Point (切入点)**: "D-ID is a great entry-level tool, but for professional-grade resolution and natural background blending, the jump to a session-based engine is worth it."

### 4. Kling AI / Luma Dream Machine
*   **近期槽点**:
    *   难以控制人物唇形 (Hard to control lip-sync)
    *   语言支持有限
*   **Pivot Point (切入点)**: "Luma/Kling are legendary for movement, but if you need them to *say* something specific for 60 seconds, you'll burn through credits. Hybrid workflow is the answer."

---

## 情报更新规则
1. 每当监控脚本抓取到 5 条以上的相同竞品吐槽，自动更新 "近期槽点"。
2. 每周分析一次各大官推的 Release Note，更新优势对比。
