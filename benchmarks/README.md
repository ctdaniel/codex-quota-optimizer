# CQO Benchmark Framework

The benchmark exists to answer one question honestly:

> Does Codex Quota Optimizer reduce avoidable agent work **while the task still passes the same acceptance criteria**?

It is not a token-savings calculator and it does not scrape private OpenAI usage data.

## What we measure

Record only behavior you can directly observe from the session or tool output:

- acceptance criteria passed / failed,
- files inspected,
- files changed,
- searches,
- focused checks,
- broad test-suite checks,
- subagents spawned,
- model escalations,
- repeated file reads,
- wall-clock time when available,
- model role / reasoning level used,
- notes about unusual conditions.

Do **not** estimate hidden tokens, remaining quota, or percentage savings.

If a client directly exposes token counts, keep them in the raw notes/source evidence rather than converting them into unsupported savings claims.

## Two benchmark modes

### 1. Controlled behavior benchmark

Use the same starting model and reasoning setting for both variants.

Purpose: isolate CQO's effects on:

- context discipline,
- change-surface discipline,
- verification scope,
- subagent use,
- repeated exploration.

### 2. Full-policy benchmark

Let each variant use its normal policy. CQO may route to a cheaper model/reasoning role when appropriate.

Purpose: evaluate the complete CQO workflow, including routing.

Always record the actual model role/reasoning used so the comparison stays transparent.

## Fair-run protocol

For every public comparison:

1. Start both variants from the **same repository commit**.
2. Use the **same task prompt and acceptance criteria**.
3. Use equivalent permissions/tool access.
4. Record a shared `pair_id` for the baseline and CQO run.
5. Do not reuse the modified working tree from the first run.
6. Prefer alternating run order across repeated pairs.
7. For public claims, use multiple pairs when practical; one pair is a case study, not a universal benchmark.
8. If either side fails acceptance, do not claim efficiency superiority from that pair.
9. Preserve raw notes or session evidence when publishing a case study.

## Result format

Store one JSON object per line:

```json
{"case_id":"checkout-bug","pair_id":"p1","variant":"baseline","benchmark_mode":"controlled","repo_commit":"abc123","acceptance_passed":true,"model_role":"balanced","reasoning":"medium","files_inspected":9,"files_changed":2,"searches":5,"focused_checks":1,"broad_checks":1,"subagents":0,"model_escalations":0,"repeated_reads":2,"wall_seconds":180,"notes":"Example shape only; replace with observed data."}
```

Then record the CQO run with the same `case_id` and `pair_id`.

### Required fields

- `case_id`
- `pair_id`
- `variant`: `baseline` or `cqo`
- `benchmark_mode`: `controlled` or `full-policy`
- `acceptance_passed`

### Optional numeric metrics

- `files_inspected`
- `files_changed`
- `searches`
- `focused_checks`
- `broad_checks`
- `subagents`
- `model_escalations`
- `repeated_reads`
- `wall_seconds`

Unknown values should be omitted rather than guessed.

## Generate a report

```bash
python benchmarks/report.py path/to/results.jsonl
```

Markdown output:

```bash
python benchmarks/report.py path/to/results.jsonl --format markdown
```

JSON output for further analysis:

```bash
python benchmarks/report.py path/to/results.jsonl --format json
```

The report only computes efficiency deltas for matched pairs where **both runs passed acceptance**.

Negative deltas mean CQO used less of that observable resource.

## Recommended first real-world cases

Build the first public case set from real repositories and real tasks:

1. **XS — documentation / mechanical patch**
2. **S — localized bug fix**
3. **M — small cross-file feature**
4. **L — debugging or migration task**

Do not manufacture results. The repository intentionally ships the framework before publishing benchmark numbers.

## Case study template

Use [case-study-template.md](./case-study-template.md) when publishing a measured example.
