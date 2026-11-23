#!/usr/bin/env python3
"""Heuristic style checker for the VOSS paper (research-humanizer, Pass 1).

This is not an AI detector and not a compliance check. It flags terms and habits that the VOSS
writing specification forbids or that usually hide the actor, the claim or the evidence. A warning
can be legitimate in a citation, a quoted title or a term the paper defines; read the line.

Usage:
    python scripts/check.py manuscript/sections/intro.tex
    python scripts/check.py manuscript/sections/*.tex
    python scripts/check.py --strict manuscript/sections/*.tex   # exit 1 on any warning
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Rule:
    code: str
    pattern: str
    suggestion: str
    severity: str = "warn"  # warn | error


RULES: tuple[Rule, ...] = (
    # VOSS vocabulary (WRITING_SPEC.md §4.2). These are errors by default.
    Rule("V01", r"\bplanner\b", "provisioning, or describe what it decides", "error"),
    Rule("V02", r"\bslow[ -]loop\b", "provisioning", "error"),
    Rule("V03", r"\bfast[ -]loop\b", "request placement", "error"),
    Rule("V04", r"\bsingle[ -]loop\b", "describe the baseline", "error"),
    Rule("V05", r"\btwo[ -]timescale\b", "only in a citation", "error"),
    Rule("V06", r"\bslots?\b", "concurrency limit, concurrent invocations", "error"),
    Rule("V07", r"\bexposure\b", "key holders, holder budget", "error"),
    Rule("V08", r"\btrust score\b", "holder budget, attestation", "error"),
    Rule("V09", r"\bstart-up level\b", "state of the function on the worker", "error"),
    Rule("V10", r"\bfiller\b", "describe the invocation class", "error"),
    Rule("V11", r"\bearly keys\b", "pre-released keys (baseline name only)", "error"),
    Rule("V12", r"\bperishable\b", "describe the event", "error"),
    Rule("V13", r"\breferee\b", "verifier", "error"),
    Rule("V14", r"\bthe front\b", "router, front end", "error"),
    Rule("V15", r"\bjudg(?:e|es|ed|ing|ment)\b", "marks as failed, estimates", "error"),
    Rule("V16", r"\breturned work\b", "result", "error"),
    Rule("V17", r"\bsecond copy\b", "backup attempt", "error"),
    Rule("V18", r"\bhedg(?:e|es|ed|ing)\b", "backup attempt", "error"),
    Rule("V19", r"\bcluster(?:s|ed|ing)?\b", "only a computer cluster in a citation", "error"),
    Rule("V20", r"\bbroker\b", "remove or cite the system", "error"),
    Rule("V21", r"\bblockchain\b", "remove", "error"),
    Rule("V22", r"\bE\d\d[a-z]*\b|\bH\d+\b|\bR\d\d\b", "describe the experiment, not its code", "error"),
    Rule("V23", r"\b(?:round|rerun|placeholder|frozen)\b", "describe the fact, not the process", "error"),
    Rule("V24", r"\bthe world\b", "the simulated environment, the model", "error"),

    # AI and research-writing tells (SKILL.md §3).
    Rule("A01", r"\bnot (?:just|only)\b[^.]{0,80}\bbut\b", "state the point directly"),
    Rule("A02", r"\b(?:delve|leverage|utilize|utilise|showcase|underscore|testament|landscape|realm|"
                r"harness|facilitate|elucidate|intricate|meticulous|holistic|synergy|paradigm|"
                r"empower|unlock|revolutioni[sz]e|game[ -]changer|cutting[ -]edge)\b",
         "use the plain word"),
    Rule("A03", r"\b(?:pivotal|crucial|seamless|comprehensive|extensive|novel|unprecedented)\b",
         "keep the fact, drop the adjective"),
    Rule("A04", r"\bstate[ -]of[ -]the[ -]art\b", "name the baseline and the measured comparison"),
    Rule("A05", r"\b(?:plays?|played) a (?:key|central|critical) role\b", "say what happens without it"),
    Rule("A06", r"\b(?:is|are|was|were) (?:essential|critical|crucial) (?:for|to)\b",
         "say what happens without it"),
    Rule("A07", r"\b(?:highlighting|ensuring|enabling|allowing|fostering|reflecting|demonstrating)\b",
         "cut the rider unless it states a separate fact"),
    Rule("A08", r"\b(?:powerful|best[ -]in[ -]class|world[ -]class|groundbreaking|stunning)\b",
         "say what was built and measured"),
    Rule("A09", r"\b(?:experts|industry|researchers) (?:agree|say|argue)\b", "name the source or cut it"),
    Rule("A10", r"\b(?:serves? as|acts? as|represents?|boasts?|features?)\b", "use is, are, has"),
    Rule("A11", r"\bmake (?:a|an) (?:decision|evaluation|comparison|choice)\b",
         "decide, evaluate, compare, choose"),
    Rule("A12", r"\b(?:may|might|could) (?:potentially|arguably|possibly)\b", "keep one qualifier"),
    Rule("A13", r"\b(?:we|this paper) (?:believe|expect|anticipate)\b", "cut, or label as a hypothesis"),
    Rule("A14", r"\b(?:it is|it's) worth noting\b|\bnotably\b|\bimportantly\b", "cut the signpost"),
    Rule("A15", r"\bin this paper,? we (?:propose|present|introduce)\b",
         "say what was built; a roadmap sentence is enough"),
    Rule("A16", r"\bextensive (?:experiments|evaluation|experiments? show)\b",
         "say what was measured and the result"),
    Rule("A17", r"\bto the best of our knowledge\b", "cut unless the claim was checked against the literature"),
    Rule("A18", r"\b(?:one|a reader) might (?:think|ask|wonder)\b|\bcontrary to (?:popular belief|common)\b",
         "cut the absent objection"),
    Rule("A19", r"\b(?:that is|that's) the (?:real|key) (?:challenge|win|point)\b", "cut the closer"),
    Rule("A20", r"\b(?:great|excellent) question\b|\bi hope this helps\b|\blet me know\b", "remove chatbot residue"),
    Rule("A21", r"\b(?:in plain (?:terms|english)|plainly|simply put|to put it simply|put simply|in simple terms|the simple version|the short version|in short|in brief|explained simply|as simple as it gets|without jargon|in other words|to be clear|the point is|let me explain|for clarity|what this means is|this means that|at its core|in essence|basically)\b",
         "state the fact; do not announce that the text is clear or simple"),
    Rule("A22", r"\bthis (?:section|paper) (?:explains|describes|shows|introduces)\b|\bin this (?:section|paper),? we\b",
         "start with the claim; the heading already says what the section is"),

    # Word-level defaults.
    Rule("W01", r"\bin order to\b", "to"),
    Rule("W02", r"\bdue to the fact that\b", "because"),
    Rule("W03", r"\bprior to\b", "before"),
    Rule("W04", r"\bsubsequently\b", "then"),
    Rule("W05", r"\b(?:commence|terminate)\b", "start, stop"),
    Rule("W06", r"\b(?:demonstrate|exhibit)s?\b", "show"),
    Rule("W07", r"\bis able to\b", "can"),
    Rule("W08", r"\ba large number of\b", "many"),
    Rule("W09", r"\b(?:very|quite|rather)\b", "cut the intensifier"),
    Rule("W10", r"\b(?:significant|significantly|substantial|substantially|dramatic|dramatically)\b",
         "give the number and the interval; keep 'significant' only for a statistical test"),
    Rule("W11", r"\b(?:robust|scalable|efficient|performant)\b", "say to what, up to what size, at what cost"),
    Rule("W12", r"\b(?:various|several) (?:ways|methods|approaches|systems)\b", "name them"),
    Rule("W13", r"\babout\s+\d", "use the exact generated number"),
    Rule("W14", r"\b(?:e\.g\.|i\.e\.)\b", "for example, that is"),
    Rule("W15", r"\betc\.", "name the remaining items or cut"),
    Rule("W16", r"\b(?:is|are) (?:performed|observed|shown|measured)\b", "name the actor"),

    # Mechanics.
    Rule("M01", r";", "split the sentence; no semicolons"),
    Rule("M02", r"—|–", "no em or en dashes; use a period, comma or parentheses"),
    Rule("M03", r"\s--\s", "no double hyphen dash"),
)


def strip_comments(text: str, suffix: str) -> list[str]:
    """Blank comments and code blocks while keeping line numbers."""
    lines = text.splitlines()
    if suffix == ".tex":
        return [re.sub(r"(?<!\\)%.*$", "", line) for line in lines]
    out: list[str] = []
    fenced = False
    for line in lines:
        if line.lstrip().startswith("```"):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else line)
    return out


def check(path: Path, max_sentence: int) -> list[tuple[int, str, str, str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = strip_comments(text, path.suffix)
    found: list[tuple[int, str, str, str]] = []
    for i, line in enumerate(lines, 1):
        for rule in RULES:
            for m in re.finditer(rule.pattern, line, flags=re.IGNORECASE):
                found.append((i, rule.code, m.group(0), rule.suggestion))
        # Sentence length: split on terminal punctuation, keep it simple.
        for sentence in re.split(r"(?<=[.!?])\s+", line.strip()):
            words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-]*", sentence)
            if len(words) > max_sentence:
                found.append((i, "S01", f"{len(words)}-word sentence", f"split it (max {max_sentence})"))
    return found


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="research-humanizer-check", description=__doc__)
    p.add_argument("files", type=Path, nargs="+")
    p.add_argument("--strict", action="store_true", help="exit 1 when anything is found")
    p.add_argument("--max-sentence", type=int, default=35)
    a = p.parse_args(argv)
    total = 0
    for path in a.files:
        if not path.exists():
            print(f"{path}: not found", file=sys.stderr)
            return 2
        rows = check(path, a.max_sentence)
        for line, code, match, suggestion in rows:
            print(f"{path}:{line}: [{code}] {match!r} -> {suggestion}")
        total += len(rows)
    print(f"\n{total} warning(s) in {len(a.files)} file(s). Read each line; citations and defined terms can be legitimate.")
    return 1 if a.strict and total else 0


if __name__ == "__main__":
    raise SystemExit(main())
