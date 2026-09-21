# CQO Benchmark Framework｜基准测试框架

这套 Benchmark 只回答一个问题：

> 在任务仍然通过**同一套验收标准**的前提下，Codex Quota Optimizer 是否减少了可以避免的 Agent 工作？

它不是 Token 节省计算器，也不会抓取 OpenAI 私有 Usage 数据。

## 记录什么

只记录能够从 Session / Tool 输出中直接观察到的行为：

- 验收标准通过 / 失败
- 读取文件数
- 修改文件数
- 搜索次数
- 定向检查次数
- 全量 / 广范围测试次数
- 启动 Subagent 数
- 模型升级次数
- 重复读取次数
- 可获取时的 Wall-clock time
- 实际使用的模型角色 / reasoning
- 特殊情况备注

未知数据直接省略，不猜测隐藏 Token、剩余额度或“节省百分比”。

## 两种 Benchmark 模式

### 1. Controlled behavior benchmark

Baseline 与 CQO 使用相同的起始模型和 reasoning。

主要隔离测试 CQO 在以下方面的作用：

- 上下文克制
- 修改面控制
- 验证范围
- Subagent 使用
- 重复探索

### 2. Full-policy benchmark

Baseline 按正常方式运行；CQO 可以按自己的策略选择更经济的模型角色或 reasoning。

主要测试完整 CQO 工作流，包括模型路由。

必须记录实际模型角色 / reasoning，确保比较透明。

## 公平测试协议

每个对外发布的比较都应该：

1. 从**同一个仓库 Commit**开始。
2. 使用**同一个任务 Prompt 和验收标准**。
3. 使用等价的权限和工具。
4. Baseline / CQO 使用同一个 `pair_id`。
5. 两次运行都从干净工作区开始。
6. 多次测试时尽量交替运行顺序。
7. 单个 Pair 只能称为 Case Study；需要更强结论时使用多个 Pair。
8. 任意一侧验收失败，该 Pair 都不能用于宣称效率优势。
9. 对外发布时尽量保留原始 Session Note / Command Log 等证据。

## 结果格式

每行一个 JSON 对象：

```json
{"case_id":"checkout-bug","pair_id":"p1","variant":"baseline","benchmark_mode":"controlled","repo_commit":"abc123","acceptance_passed":true,"model_role":"balanced","reasoning":"medium","files_inspected":9,"files_changed":2,"searches":5,"focused_checks":1,"broad_checks":1,"subagents":0,"model_escalations":0,"repeated_reads":2,"wall_seconds":180,"notes":"这里只展示字段结构，请替换为真实观察数据。"}
```

CQO Run 使用相同的 `case_id` 与 `pair_id`。

### 必填字段

- `case_id`
- `pair_id`
- `variant`：`baseline` 或 `cqo`
- `benchmark_mode`：`controlled` 或 `full-policy`
- `acceptance_passed`

## 生成报告

```bash
python benchmarks/report.py path/to/results.jsonl
```

Markdown：

```bash
python benchmarks/report.py path/to/results.jsonl --format markdown
```

JSON：

```bash
python benchmarks/report.py path/to/results.jsonl --format json
```

只有 Baseline 与 CQO **都通过验收**的匹配 Pair，才会进入效率 Delta。

负数代表 CQO 在该可观察指标上使用得更少。

## 第一批真实 Case 建议

首批公开 Case 建议覆盖：

1. **XS — 文档 / 机械修改**
2. **S — 局部 Bug 修复**
3. **M — 小型跨文件功能**
4. **L — Debug 或 Migration**

仓库会先发布 Benchmark Framework，再逐步加入真实测量结果，避免为了传播先制造漂亮数字。

发布真实 Case 时，可使用 [case-study-template.md](./case-study-template.md)。
