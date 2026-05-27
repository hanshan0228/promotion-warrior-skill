# HEARTBEAT 配置说明

> 将以下内容复制到 ~/.openclaw/HEARTBEAT.md 对应位置。
> HEARTBEAT.md 是 OpenClaw 的定时任务引擎，格式为 cron 表达式 + prompt。

---

## 复制以下内容到 HEARTBEAT.md

```markdown
## promotion-warrior 主任务

- cron: 0 */30 9-23 * * *
- description: 每天 9:00-23:00 每 30 分钟执行一次社媒引流任务
- prompt: |
    使用 promotion-warrior skill 执行本轮引流任务。
    按照 SKILL.md 中的启动检查清单依次执行，包括：
    1. 先检查 reply_monitor.md，处理所有 P0/P1 待回复项
    2. 扫描 competitors.md 中的竞品账号新内容
    3. 执行本轮 Tier 1/2/3 操作
    4. 更新所有日志文件
    完成后简报告知本轮执行了哪些操作、有无异常。

## promotion-warrior 回复监控（高频）

- cron: 0 */15 9-23 * * *
- description: 每 15 分钟检查一次是否有新回复需要处理
- prompt: |
    只执行 promotion-warrior 的回复监控任务：
    扫描所有已启用平台的通知/消息，
    将新回复写入 reply_monitor.md 对应优先级队列。
    如有 P0 级别（对方主动私信），立即通知我。
    不执行其他引流操作。

## promotion-warrior 每日重置

- cron: 0 0 0 * * *
- description: 每天零点重置账号今日操作计数
- prompt: |
    执行 promotion-warrior 的每日重置任务：
    1. 将 accounts.md 中所有账号的"今日计数"重置为 0
    2. 检查 error_log.md 中冷却时间已过的账号，恢复为 active
    3. 检查 accounts.md 中 warming 状态账号的注册天数，
       如已满足条件自动升级为 active 并通知我
    4. 不执行任何引流操作

## promotion-warrior 周报

- cron: 0 9 0 * * 0
- description: 每周日早上 9 点生成周报
- prompt: |
    根据 performance.md 中本周的数据，生成 promotion-warrior 周报：
    1. 汇总本周各平台操作量和回复率
    2. 对比各人设效果
    3. 列出表现最好的 3 条评论句式
    4. 建议下周需要调整的策略
    5. 将周报写入 performance.md 的周报区块，并发送给我
```

---

## 时间说明

| 任务 | 频率 | 原因 |
|------|------|------|
| 主任务 | 每 30 分钟 | 覆盖各平台时间窗口，每天约执行 28 次 |
| 回复监控 | 每 15 分钟 | P0 回复需要及时，6h 内回复转化率高 |
| 每日重置 | 每天零点 | 重置配额，防止超限 |
| 周报 | 每周日 9 点 | 定期复盘优化策略 |

---

## 注意事项

- HEARTBEAT.md 中 cron 表达式格式：`秒 分 时 日 月 周`
- `0 */30 9-23 * * *` = 每天 9:00 到 23:00 之间每 30 分钟的整点和半点执行
- `0 */15 9-23 * * *` = 每天 9:00 到 23:00 之间每 15 分钟执行
- `0 0 0 * * *` = 每天凌晨 0:00 执行
- `0 9 0 * * 0` = 每周日 9:00 执行（周 = 0 代表周日）
- Mac mini 需保持开机且 OpenClaw 进程运行，HEARTBEAT 才能正常触发
