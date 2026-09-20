<p align="center">
  <img src="./assets/hero.svg" alt="Codex Quota Optimizer" width="100%" />
</p>

<p align="center">
  <a href="./README.zh-CN.md"><strong>简体中文</strong></a> · <strong>English</strong>
</p>

<p align="center">
  <a href="./LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-111827.svg"></a>
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111827.svg">
  <img alt="Codex Plugin" src="https://img.shields.io/badge/Codex-Plugin-111827.svg">
  <img alt="Plus & Pro" src="https://img.shields.io/badge/ChatGPT-Plus%20%2F%20Pro-111827.svg">
  <img alt="No telemetry" src="https://img.shields.io/badge/telemetry-none-0F766E.svg">
</p>

# Spend less Codex allowance. Keep the engineering quality.

**Codex Quota Optimizer** is an open-source Codex Skill + Plugin that reduces avoidable Plus / Pro usage while keeping the task correct. The same canonical Skill powers both direct Skill installs and Plugin distribution.

Codex does not only spend allowance on writing code. It can also spend it on **re-reading a repository, using a stronger model than necessary, over-reasoning, running broad tests too early, spawning unnecessary subagents, and doing work outside the requested scope**.

This Skill gives Codex a simple policy:

> **Use the cheapest reliable execution path first. Escalate only when the evidence says it is necessary.**

It does **not** bypass limits, scrape private quota data, or weaken verification to fake savings.

---

## See the difference in 30 seconds

| Typical waste | With Codex Quota Optimizer |
|---|---|
| Use a powerful model for every task | Classify task complexity and route to the lowest adequate model |
| Read large parts of the repo “just in case” | Search first, read only the change surface and direct dependencies |
| Use high reasoning by default | Start low; increase reasoning only when ambiguity requires it |
| Run the full test suite after small edits | Verify in layers: touched file → focused test → package → full suite |
| Spawn subagents because they are available | Use them only when parallel decomposition genuinely helps |
| Refactor nearby code while fixing one issue | Make the smallest coherent patch that satisfies acceptance criteria |
| Let a stronger model rediscover everything | Compress known facts before escalating |

<p align="center">
  <img src="./assets/optimization-loop.svg" alt="Codex Quota Optimizer workflow" width="96%" />
</p>

---

## Install

### Option A — One-line Skill install · recommended

Install the Skill with the cross-agent Skills CLI:

```bash
npx skills add ctdaniel/codex-quota-optimizer --skill codex-quota-optimizer
```

This is the fastest path for Codex users and also makes the Skill discoverable through the wider Skills ecosystem.

### Option B — Direct global install

Use the repository installer across all of your Codex projects:

```bash
git clone https://github.com/ctdaniel/codex-quota-optimizer.git
cd codex-quota-optimizer
./install.sh
```

It installs to:

```text
~/.agents/skills/codex-quota-optimizer
```

Codex should detect the Skill automatically. Restart Codex if it does not appear immediately.

### Option C — Repository-local

Copy the canonical Skill source:

```text
skills/codex-quota-optimizer/
```

into your project's:

```text
.agents/skills/codex-quota-optimizer/
```

Commit it with the repository if you want the whole team to use the same usage policy.

> Codex officially supports user-level Skills in `~/.agents/skills` and repository Skills in `.agents/skills`. See the [OpenAI Skills documentation](https://developers.openai.com/docs/build-skills).

---

## Use it

### 1. Explicit invocation

In Codex CLI / IDE, type `$` and select the Skill, or invoke it directly:

```text
$codex-quota-optimizer
Fix this checkout bug. Keep the implementation reliable, but minimize unnecessary Codex usage.
```

### 2. Natural language

Implicit invocation is enabled, so requests like these can trigger it automatically:

```text
Please save my Codex quota while implementing this feature.
```

```text
My Plus allowance is getting low. Finish this with the smallest reliable usage footprint.
```

```text
Use the cheapest adequate model and focused tests first. Escalate only if needed.
```

### 3. Emergency mode

When you tell Codex that your allowance is nearly exhausted, the Skill becomes more aggressive about saving usage:

- no optional refactors,
- no broad repository exploration,
- no unnecessary subagents,
- one implementation path,
- cheapest adequate model,
- focused verification first.

Correctness and explicit acceptance criteria still take priority.

---

## What the Skill optimizes

<table>
<tr>
<td width="50%" valign="top">

### 🧠 Model & reasoning routing

Classifies work from **XS → XL**, then starts with the least expensive model / reasoning level that should reliably handle it.

It escalates only when the task becomes genuinely ambiguous, cross-cutting, risky, or hard to debug.

</td>
<td width="50%" valign="top">

### 🔎 Context control

Uses targeted search, current diffs, project instructions and compact repository maps before opening large amounts of code.

The goal is to avoid paying repeatedly for repository rediscovery.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### ✂️ Minimal change surface

Keeps edits focused on the acceptance criteria and avoids unrelated cleanup, dependency upgrades and “while I'm here” refactors.

</td>
<td width="50%" valign="top">

### ✅ Layered verification

Runs the smallest relevant checks first and expands verification only when the scope or risk justifies it.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🧩 Subagent discipline

Parallel agents can multiply work and context. The Skill uses them only when a large task can truly benefit from independent parallel workstreams.

</td>
<td width="50%" valign="top">

### 🧾 Checkpoint compression

For long tasks, Codex keeps a compact handoff state — goal, decisions, touched files, tests, next action — instead of repeatedly reconstructing the same context.

</td>
</tr>
</table>

---

## Model routing philosophy

Current OpenAI guidance positions the model family roughly like this:

| Task shape | Preferred role | Current example | Starting reasoning |
|---|---|---|---|
| Mechanical / repetitive | Fastest, most economical | GPT-5.6 Luna | Low |
| Everyday coding | Balanced | GPT-5.6 Terra | Low / Medium |
| Complex, open-ended work | Deep reasoning | GPT-5.6 Sol | Medium |
| Hardest multi-step / multi-tool work | Strongest available | GPT-6 Astra | As needed |

The exact model lineup and plan availability can change, so the Skill **routes by capability role first, model name second**. It does not hard-code a fixed Plus or Pro message count.

OpenAI also notes that higher reasoning levels consume more time/tokens, and recommends increasing reasoning when the task actually needs deeper analysis. See [Codex model guidance](https://developers.openai.com/docs/models).

---

## Verification ladder

```text
Level 1     touched-file checks
    ↓
Level 2     closest focused behavior test
    ↓
Level 3     package / module typecheck, lint or tests
    ↓
Level 4     full suite / release gate
```

A local change should not automatically pay the cost of Level 4.

---

## Two small helper tools

The Skill works without these scripts, but they can reduce repository discovery overhead.

### Compact repository snapshot

```bash
python skills/codex-quota-optimizer/scripts/repo_snapshot.py --compact
```

Produces a compact project map while ignoring common generated/vendor directories such as `node_modules`, `dist`, `.next`, `coverage`, and `.venv`.

### Change-scope analyzer

```bash
python skills/codex-quota-optimizer/scripts/change_scope.py
```

Summarizes the current Git change surface and suggests a sensible verification level.

Both scripts are local-only and dependency-light.

---

## Modes

| Mode | Designed for | Behavior |
|---|---|---|
| **Economy** | Plus, long coding sessions, lower remaining allowance | strict scope, economical model first, focused checks |
| **Balanced** | Pro or normal daily development | balanced model first, deeper model when justified |
| **Emergency** | allowance nearly exhausted | one path, no optional work, minimum reliable exploration and verification |

These are **behavioral budgets**, not fake quota counters.

---

## What it deliberately does not do

- ❌ bypass or evade OpenAI usage limits
- ❌ claim to know your exact remaining allowance when Codex does not expose it
- ❌ scrape private account / usage pages
- ❌ collect credentials
- ❌ send telemetry
- ❌ reduce correctness just to make a usage number look smaller

Plus and Pro usage rules can change. OpenAI currently notes that supported agentic features can share an allowance, so current account usage / reset state should be checked in the product's usage UI when it matters. See the [OpenAI Help Center](https://help.openai.com/en/articles/12642688-using-credits-for-flexible-usage-in-chatgpt-freegopluspro).

---

## Project structure

```text
codex-quota-optimizer/
├── plugin.json                    # portable Agent Plugin manifest
├── .codex-plugin/
│   └── plugin.json                # Codex compatibility manifest
├── skills/
│   └── codex-quota-optimizer/     # single canonical Skill source
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/
│       └── scripts/
├── assets/                        # Plugin icon + README visuals
├── examples/
├── install.sh                     # installs Skill to ~/.agents/skills
└── README.zh-CN.md
```

---

## Roadmap

- [ ] Local **Usage Journal** for task-level observations — no private account scraping
- [ ] **Task Classifier** output: task size, recommended model role, reasoning, verification scope
- [ ] **Session Budget** for discovery / coding / verification work
- [ ] End-of-task **Usage Audit** showing avoidable work that was skipped
- [ ] Framework-aware focused-test discovery
- [x] Plugin packaging for dual Skill / Plugin distribution
- [ ] HOL Codex Plugin Catalog listing
- [x] One-line Skills CLI installation
- [ ] Benchmark suite comparing default and optimized workflows

Ideas and PRs are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Why open source?

The optimization policy should be inspectable.

You should be able to see exactly what the Skill tells Codex to do, change the policy for your own workflow, and contribute better heuristics as Codex evolves.

No black-box quota tricks — just better engineering discipline for agentic coding.

---

## License

MIT © 2026

If this Skill saves you meaningful Codex usage, a ⭐ helps more people find it.