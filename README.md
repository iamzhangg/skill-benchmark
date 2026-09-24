# Skill Benchmark / Agent Skill 行为评测

[![CI](https://github.com/iamzhangg/skill-benchmark/actions/workflows/ci.yml/badge.svg)](https://github.com/iamzhangg/skill-benchmark/actions/workflows/ci.yml)

An installable Agent Skill and zero-dependency runner for testing Agent Skills with realistic scenarios and transparent assertions.

相比“截一张成功截图”，它会检查输出文本、文件产物和 JSON 数据，并允许把安全或授权要求设置为 blocking assertion：一旦失败，平均分再高也不能发布。

## Assertions

- `contains` and `not_contains`
- `regex`
- `file_exists`
- `json_path`
- blocking failures plus configurable score thresholds

## Install

```bash
npx skills add iamzhangg/skill-benchmark
```

## Demo

```bash
python scripts/grade.py examples/cases.json examples/results.json --output report.md
python -m unittest discover -s tests -v
```

The runner grades saved transcripts and artifact manifests, so the example is reproducible without an API key. See [`references/case-format.md`](references/case-format.md) for the schema.

Part of [Agent Skill Lab](https://github.com/iamzhangg/agent-skill-lab). Released under the [MIT License](LICENSE).

## Portfolio path / 作品集路径

This runner is the verification layer for the portfolio's installable Skills. Pair it with [Agent UX Audit](https://github.com/iamzhangg/agent-ux-audit) for experience findings and [Agent Trust Lab](https://github.com/iamzhangg/agent-trust-lab) for visible autonomy-policy exploration. Passing scenarios demonstrate bounded behavior, not universal reliability.
