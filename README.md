# research-humanizer

A writing skill for the VOSS paper, submitted to ACM Transactions on Internet Technology (TOIT).
It is a reading and editing checklist for systems papers whose reviewer knows systems but not
serverless computing.

It is deliberately narrow. It is not a general-purpose humanizer and it does not try to be
ASD-STE100. It keeps the technical content, the uncertainty and the evidence, and removes the habits
that make a paper sound generated, inflated or evasive.

## What it does

- **Pass 1** removes research-writing tells: not-X-but-Y, one-line closers, inflated significance,
  stock AI words, hidden actors, stacked hedges, process narrative and self-assessment.
- **Pass 2** rebuilds paragraphs around one claim and its evidence, defines terms for a reader who
  does not know serverless, and enforces the VOSS vocabulary.

The full instructions are in [`SKILL.md`](SKILL.md).

## Use it

In a Claude/agent session, ask the agent to read `SKILL.md` before editing the manuscript, or load
the directory as a skill. Then:

```bash
python scripts/check.py manuscript/sections/intro.tex
python scripts/check.py manuscript/sections/*.tex
```

The checker is a heuristic. It flags forbidden VOSS terms, common AI/research tells, long sentences,
semicolons, em dashes and a few number habits. A warning can be legitimate in a citation, a quoted
title or a term the paper defines. Read the line; fix what is real.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | The skill: reader, process, Pass 1 tells, Pass 2 rules, VOSS vocabulary, cold-reader questions, examples, fidelity rules, finish checklist. |
| `scripts/check.py` | Dependency-free heuristic checker for `.tex` and `.md`. |

## Scope

The target is the VOSS paper. The vocabulary and examples come from its writing specification
(`manuscript/WRITING_SPEC.md`) and the author's feedback log (`manuscript/HUMAN_FEEDBACK.md`).
Do not generalise the rules without checking them against that paper first.

## Provenance

Inspired by the structure of
[`Dodaios/ste80-humanizer`](https://github.com/Dodaios/ste80-humanizer): two passes, numbered tells,
fidelity rules, a checker. The content is different: this skill is for systems research, not for
simplified technical English, and its vocabulary is VOSS-specific.

## License

MIT. See [`LICENSE`](LICENSE).
