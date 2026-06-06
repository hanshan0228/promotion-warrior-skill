---
name: promotion-warrior
description: |
  社媒内容策略顾问与社区运营专家。帮助用户在小红书、微博、抖音、Instagram、X、
  Facebook、Reddit、TikTok 上制定内容策略、生成真实有价值的评论和私信内容、
  追踪互动效果、优化转化漏斗。
  基于 3-Tier 内容漏斗（曝光→互动→私信），支持多 niche 并行管理、A/B 内容测试、
  用户价值分层、竞品内容分析、热点感知、效果追踪与 ROI 分析。
  所有内容生成均以提供真实价值为前提，遵循各平台社区规范。
  当用户说"帮我写评论""生成私信内容""分析竞品""制定内容策略""追踪互动效果"等时触发。
version: "5.0.0 (Unified Growth Edition)"
tags: [social-media, dating, affiliate, growth-hacking, auto-dm, dashboard, proxy]
data_dir: "~/.openclaw/skills/promotion-warrior/data/"
---

# Promotion Warrior v5.0 (Unified Growth Hub)

全平台“情感收割”与“降维打击”引擎。从技术工具推广进化为高转化的全自动化多项目增长系统。

## 🌟 核心架构 (v5.0)

1. **可视化指挥中心 (Growth Dashboard)**: 
   * 基于 FastAPI + Tailwind 实现。
   * **Project Hub**: 一键新建/启停多个推广项目（如 Dating, SaaS, AI Tool）。
   * **Account Pool**: 集中管控全平台账号，支持多代理 (Proxy) 绑定与配额监控。
   * **Live Logs**: 实时流式输出巡查日志，支持错误/成功高亮。
   * **Analytics**: 自动解析转化漏斗，对比各平台与人设的 ROI。

2. **多项目引擎 (Multi-Niche Loop)**:
   * 引擎自动遍历所有 Active 项目。
   * 每个项目拥有独立的 `config.md`（包含专属链接、关键词、目标 Subreddits）。
   * 实现跨业务线同步引流，互不干扰。

3. **智能账号管理 (Smart Account Rotation)**:
   * **配额追踪**: 实时记录每个账号的今日评论/私信数，达到上限自动切号。
   * **多代理隔离**: 支持为每个账号绑定独立代理，彻底规避 IP 关联封禁。
   * **人设绑定**: 每个账号可独立指定话术风格。

4. **高并发引流策略 (Bio Routing)**:
   * **无限火力**: 移除了抓取限制，单次轮询深度分析每个板块 50+ 最新贴。
   * **安全导流**: 采用“高价值干货回复 + Bio/Pinned Post 引流”策略，极大提升账号安全性。

## 📂 核心目录结构

```
promotion-warrior/
├── dashboard/              ← Web 控制面板 (FastAPI App)
│   ├── server.py           ← 后端主入口
│   ├── templates/          ← HTML 模板 (Jinja2)
│   └── static/             ← 样式与脚本
├── niches/                 ← 多项目配置目录
│   └── dating/             ← 约会引擎主攻项目
├── tools/
│   ├── account_manager.py  ← 账号配额与轮换工具
│   ├── dm_randomizer.py    ← 智能话术生成器 (Bio-Routing 版)
│   └── lead_scorer_v2.py   ← NLP 评分引擎 (扩充词库版)
├── enhanced-check.sh       ← 核心执行引擎 (高并发多项目版)
├── niche_manager.md        ← 全局项目注册表
├── accounts.md             ← 全球账号池与状态记录 (含 Proxy/Limit)
└── alert_system.md         ← 自动化告警规则
```

## 🛠️ 操作说明

### 1. 启动控制面板
```bash
cd dashboard && ./venv/bin/python3 server.py
```
访问：[http://127.0.0.1:8787](http://127.0.0.1:8787)

### 2. 核心控制逻辑
*   **Run Now**: 立即拉起一轮全球截流巡查。
*   **Start Scheduler**: 注册 macOS `launchd` 服务，实现每 15/30/60 分钟自动巡航。
*   **Edit Config**: 直接在网页上修改每个项目的关键词与话术模板。

## 📸 平台策略

### 🔴 Reddit (核心火力点)
*   **动作**: 深度扫描 `r/Tinder`, `r/Bumble`, `r/hingeapp`, `r/dating_advice` 等板块。
*   **逻辑**: 检测到绝望信号（zero matches, am i ugly, profile review），自动发送引流干货。

### 🐦 Twitter & X (趋势拦截)
*   **动作**: 实时检索带有强烈意图（Recommend tool, Giving up）的推文。

---

**核心原则：内容必须提供真实价值，遵循各平台社区规范。**
