# Contributing

Thanks for helping make Codex Quota Optimizer more useful.

The project has one core job: **reduce avoidable Codex usage without reducing correctness**.

## Contribution principles

- Prefer durable behavioral rules over hard-coded plan limits.
- Route by model role/capability first; treat current model names as changeable examples.
- Add scripts only when deterministic tooling clearly reduces model context or tool work.
- Keep helper scripts dependency-free when practical.
- Never add credential collection, private usage-page scraping, quota bypassing, or telemetry by default.
- Avoid optimizations that save usage by skipping verification that the task genuinely needs.

## Before opening a PR

1. Run both helper scripts in a Git repository.
2. Keep `SKILL.md` focused enough to be useful after Codex selects it.
3. Verify current OpenAI documentation before changing model-routing or quota-related claims.
4. Keep English and Chinese README user-facing behavior aligned when the product flow changes.

## Useful contribution areas

- framework-aware focused-test discovery,
- better repository snapshot heuristics,
- task classification rules,
- usage-audit ideas that do not require private account scraping,
- benchmarks for common coding task shapes,
- documentation and installation improvements.
