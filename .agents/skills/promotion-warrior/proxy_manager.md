# 代理 IP 管理 — proxy_manager.md

> 每个账号必须绑定独立 IP，同一 IP 不能同时登录多个账号。
> Agent 每次操作前检查当前账号的代理状态，失效则切换备用。

---

## 核心原则

```
一账号一 IP：每个社媒账号绑定一个固定代理 IP
IP 归属地匹配：代理 IP 的地区要与账号注册地区一致
  - 中文账号（小红书/微博/抖音）→ 中国大陆 IP
  - 英文账号（Instagram/X/Reddit）→ 账号注册国家的 IP
  - TikTok → 目标受众所在国家的 IP
不共享：任何两个账号不使用同一个 IP
```

---

## 代理类型推荐

| 类型 | 稳定性 | 价格 | 适合场景 |
|------|--------|------|----------|
| 住宅代理（Residential） | ★★★★★ | 高 | 主力账号，长期稳定运营 |
| 移动代理（Mobile 4G/5G） | ★★★★☆ | 高 | 高风险平台（小红书/TikTok） |
| 数据中心代理（Datacenter） | ★★★☆☆ | 低 | 养号期，风险较低的操作 |
| 静态住宅（ISP） | ★★★★☆ | 中 | 平衡型，适合大多数场景 |

**强烈建议：** 小红书和 TikTok 用住宅代理或移动代理，这两个平台风控最严。

---

## 代理池配置

```yaml
# 中文平台代理池
cn_proxies:
  - id: "cn_proxy_01"
    type: "residential"
    provider: "填入代理商"
    endpoint: "host:port"
    username: "user"
    password: "pass"
    location: "Shanghai"
    bound_account: "小红书账号A"    # 绑定的账号
    status: "active"
    last_check: "2026-04-26 10:00"
    response_time_ms: 0

  - id: "cn_proxy_02"
    type: "residential"
    provider: "填入代理商"
    endpoint: "host:port"
    username: "user"
    password: "pass"
    location: "Beijing"
    bound_account: "微博账号A"
    status: "active"
    last_check: "—"
    response_time_ms: 0

# 英文平台代理池
en_proxies:
  - id: "en_proxy_01"
    type: "residential"
    provider: "填入代理商"
    endpoint: "host:port"
    username: "user"
    password: "pass"
    location: "US-California"
    bound_account: "@instagram_account_a"
    status: "active"
    last_check: "—"
    response_time_ms: 0

  - id: "en_proxy_02"
    type: "datacenter"
    provider: "填入代理商"
    endpoint: "host:port"
    username: "user"
    password: "pass"
    location: "US-NewYork"
    bound_account: "@twitter_account_a"
    status: "active"
    last_check: "—"
    response_time_ms: 0

# 备用代理池（主代理失效时临时使用）
backup_proxies:
  - id: "backup_01"
    type: "datacenter"
    endpoint: "host:port"
    username: "user"
    password: "pass"
    location: "US"
    bound_account: null             # 备用，不固定绑定
    status: "standby"
```

---

## 代理健康检查规则

每次启动时，对本次要用到的代理执行健康检查：

```
检查项目：
  1. 连通性：能否访问目标平台（不一定登录，只检查能否访问）
  2. 响应时间：> 3000ms 标记为"慢速"，> 8000ms 标记为"不可用"
  3. IP 纯净度：检查 IP 是否在黑名单（使用 ipqualityscore 或同类服务）

结果处理：
  - 正常 → 继续使用
  - 慢速 → 记录警告，仍可使用但优先切换
  - 不可用 → 标记 status: "failed"，切换到备用代理
  - IP 被拉黑 → 标记 status: "blacklisted"，通知用户更换
```

---

## 代理切换规则

```
主代理失效 → 切换到 backup 池中同地区的备用代理
备用也失效 → 该账号本次跳过，记录到 error_log.md
切换后 → 在 accounts.md 中记录"本次使用备用代理"
恢复后 → 手动将 status 改回 active
```

---

## 代理使用记录（Agent 自动维护）

| 时间 | 代理ID | 账号 | 平台 | 响应时间 | 状态 | 备注 |
|------|--------|------|------|----------|------|------|
| — | — | — | — | — | — | — |

---

## 代理商推荐参考

| 代理商 | 类型 | 支持地区 | 特点 |
|--------|------|----------|------|
| Oxylabs | 住宅/移动 | 全球 | 稳定，适合长期 |
| Bright Data | 住宅/移动/数据中心 | 全球 | 功能最全，价格高 |
| Smartproxy | 住宅/数据中心 | 全球 | 性价比高 |
| 922proxy | 住宅 | 中国/全球 | 中文账号首选 |
| Kookeey | 住宅/移动 | 中国 | 国内平台专用 |

> 注意：选代理商时确认支持 HTTP/HTTPS/SOCKS5，并支持账号密码认证方式。
