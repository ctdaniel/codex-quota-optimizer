# Changelog

All notable changes to this project will be documented here.

## [0.2.2] - 2026-09-21

### Added
- Paired Baseline-vs-CQO benchmark framework with controlled and full-policy modes.
- Honest benchmark result schema and case-study template.
- Local benchmark report generator with text, Markdown, and JSON output.
- Acceptance-gated comparisons: efficiency deltas are only calculated when both runs pass the same acceptance criteria.
- Benchmark tests and CI smoke coverage.
- English and Simplified Chinese benchmark methodology.

### Changed
- CQO CLI/package version aligned to 0.2.2.
- Roadmap now separates the benchmark framework from future published real-world measurements.

## [0.2.1] - 2026-09-21

### Added
- `cqo doctor` for zero-network local installation diagnostics.
- Doctor checks Python compatibility, Skill presence, journal writability, Git availability, CLI PATH visibility, and active-session state.

### Changed
- `cqo audit` output now separates observed local facts from CQO policy guarantees for clearer, more honest reporting.
- README now reflects successful HOL Codex Plugin Catalog listing.

## [0.2.0] - 2026-09-20

### Added
- Zero-friction runtime policy: no extra model call, no network dependency, no blocking budget gate, and no automatic subagents from CQO itself.
- Optional local `cqo` CLI with `start`, `status`, `audit`, and `history`.
- Local heuristic Task Classifier with English and Chinese risk/complexity signals.
- Soft Session Budgets for discovery, implementation paths, reasoning, verification, and subagent use.
- Local-only task journal under `~/.cqo` (or `CQO_HOME`) with no telemetry or private account scraping.
- Task-level Usage Audit that reports local change surface and CQO policy guardrails without inventing token-savings percentages.
- Python unit tests and CLI smoke-test CI.

### Changed
- Execution budgets are explicitly advisory and may expand automatically when correctness requires more context or verification.
- The optional CLI is an inspection layer, not a runtime dependency.
- Direct `install.sh` installs a convenient `cqo` command under `~/.local/bin`.

## [0.1.0] - 2026-09-18

### Added
- Dual Skill / Plugin distribution with a portable `plugin.json` and Codex compatibility manifest.
- HOL Plugin Scanner CI and marketplace-ready icon/package structure.
- Initial `codex-quota-optimizer` Skill.
- Task-size routing from XS to XL.
- Model and reasoning escalation policy.
- Context-budget and minimal-change rules.
- Layered verification policy.
- Economy, Balanced, and Emergency modes.
- Compact repository snapshot helper.
- Change-scope / verification helper.
- English and Simplified Chinese documentation.
- Skill UI metadata and visual assets.
