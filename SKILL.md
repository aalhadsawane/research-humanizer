---
name: research-humanizer
description: |
  Draft or edit the VOSS systems paper for ACM Transactions on Internet Technology so a systems
  reviewer without serverless background understands it on the first read. Removes research-writing
  tells and rebuilds paragraphs around a claim and its evidence. Tailored to VOSS: its vocabulary,
  forbidden terms and measured claims. Use for the abstract, introduction, background, design,
  method, results, discussion, related work, conclusion and captions.
license: MIT
metadata:
  version: "0.2.0"
  target: "ACM TOIT, VOSS"
---

# Research Humanizer (VOSS/TOIT)

A checklist for the VOSS paper, not a general writing product. The reader is a systems reviewer who
knows operating systems, networking and measurement but not serverless computing. Every term must be
clear from the page.

Keep every fact. Do not add a number, citation, comparison or claim that is not in the source or the
generated macros. A rewrite that changes the meaning is an error, even if it reads better.

## 1. Reader

- Knows VMs, TPMs, round trips, traces, schedulers.
- Does not know what serverless is, what a cold start is, why a function needs a key, or why anyone
  would run one on a machine they do not own.
- Stops when a sentence assumes knowledge that is not on the page.
- Checks every claim for a figure, table, citation or design fact.
- Checks that measured and simulated values are separate, and that lost, late and wrong answers
  count as misses.

## 2. Process

1. **Claim and evidence.** For each paragraph, write its one claim and the evidence: `F` figure,
   `T` table, `C` citation, `D` design fact, `M` measured number. A sentence with no mark is cut or
   joined to one that has a mark.
2. **Outline before prose.** One line per paragraph: claim and evidence.
3. **Draft** with the vocabulary of §6. Define a term at first use.
4. **Cold-reader pass.** Answer the ten questions in §7. If a question has no answer on the page,
   add one plain clause, not a paragraph.
5. **Style and numbers.** Apply §3-§5. Every number has a unit, what it measures, the machine or
   trace, and a section pointer. Run `scripts/check.py`.
6. **Fact-check** against the macros, `docs/PARAMETERS.md`, the code and the results.

## 3. Pass 1: research-writing tells

| Tell | Fix |
|---|---|
| **Not X but Y.** "not just a cache, but an abstraction" | State the point. Keep a contrast only if the reader believes X. |
| **One-line closer or fragment.** "That is the real challenge." | Cut it or merge it into the claim. |
| **Grand significance.** "pivotal", "opens the door", "marks a shift" | Replace with the measured claim. |
| **Staged run-up.** "To this end", "Motivated by this" | Start with the claim. |
| **Absent objection.** "One might think", "It is tempting to" | Cut unless citing the person who said it. |
| **Rhetorical question.** "Why does this matter?" | Answer it in a statement. |
| **Forced triad.** "fast, reliable and scalable" | Keep three only if the meaning has three parts. |
| **Stock AI words.** delve, leverage, robust, seamless, crucial, showcase, underscore, testament, landscape, realm, harness, utilize, facilitate, comprehensive, extensive, novel, state-of-the-art, paradigm, holistic, empower, unlock | Use the plain word. Keep a measurement, drop the adjective. |
| **Vague importance.** "plays a key role", "is critical to" | Say what happens without it. |
| **Shallow `-ing` rider.** "..., highlighting...", "..., enabling..." | Cut unless it states a separate fact. |
| **Sales language.** "powerful", "best-in-class", "we are the first" | Say what was built and measured. |
| **Borrowed authority.** "experts agree", "industry reports" | Name the source or cut it. |
| **Avoiding is/are/has.** "serves as", "acts as", "represents" | Use is, are, has. |
| **Nominalisation.** "make a decision", "perform an evaluation" | decide, evaluate. |
| **Hidden actor.** "The token is validated before..." | Name the actor: "The gateway validates the token, then forwards..." |
| **Stacked hedges.** "may potentially", "could arguably" | Keep one qualifier; keep the source's certainty. |
| **Self-assessment.** "Our evaluation is comprehensive." | Delete. The numbers are the assessment. |
| **Belief.** "We believe", "we expect" | Delete, or label a hypothesis in the discussion. |
| **Process narrative.** "We first tried X, then Y." | Keep only a change that affects how the results are read. |

Word defaults: use, not utilize/leverage; show, not demonstrate/exhibit; start/stop, not
commence/terminate; before, not prior to; because, not due to the fact that; to, not in order to;
then, not subsequently; many, not a large number of; can, not is able to.

## 4. Pass 2: systems-paper structure

| S | Rule |
|---|---|
| S1 | **One claim per paragraph.** The first sentence states the claim, not the topic. |
| S2 | **Every claim has evidence:** figure, table, citation or design fact. |
| S3 | **Define at first use.** One clause, by what the thing is and does. |
| S4 | **Jargon budget.** A one-use term is described in plain words. A repeated term is defined once and used consistently. No synonym rotation, no coined label. |
| S5 | **Explain the missing context:** serverless, cold start, keep-alive, function key, attestation, deadline, tenant, owner, provider. |
| S6 | **Mechanism accuracy.** Name the actor, event and order. No anthropomorphism. Name the owner class for security claims. |
| S7 | **Numbers have provenance.** Value, unit, what it measures, machine or trace, section pointer. Two significant digits with an interval where supported. |
| S8 | **Separate design, method, results.** Design never mentions the simulator. Method says what is real and modelled. Results open with the finding, then evidence, then figure. |
| S9 | **No process history** in the abstract, introduction or results. A change that affects interpretation goes in method or limitations. |
| S10 | **No overclaim.** "can" is not "does"; "in our runs" is not "in general". State limits plainly in the discussion. |
| S11 | **Active voice, simple tenses, short sentences.** One idea per sentence. No semicolons. No em dashes. |
| S12 | **Paragraphs 3-6 sentences.** No bullets for reasoning. Tables for parameters and results. |
| S13 | **Related work compares mechanisms**, not one-line dismissals. Cite every baseline's source and list deviations. |
| S14 | **Abstract:** problem, premise, what was built, headline measured result, basis. At most 170 words. No constants, internal comparisons, calibration detail or process. |
| S15 | **Introduction:** context, setting, two problems, premise, what it takes before a worker can run a function, what was built, contributions, headline numbers. No project history. |
| S16 | **Headings name what the section holds.** Sentence case. No "Towards", "On the", or decorative labels. |
| S17 | **Captions are self-contained.** Define every label and abbreviation. |

## 5. Do not announce the style

Follow the rules silently. Do not write a sentence that tells the reader the text is being clear,
simple, direct or jargon-free. The text should show it.

Never write phrases such as: "in plain terms", "plainly", "simply put", "to put it simply", "the
simple version", "the short version", "in short", "in brief", "explained simply", "as simple as it
gets", "without jargon", "in other words", "to be clear", "the point is", "let me explain", "for
clarity", "what this means is", "this means that", "at its core", "in essence", "basically".

Also avoid announcing paper structure when the heading already does it: "This section explains...",
"In this paper, we...", "We state...", "We describe..." are usually removable. State the fact.

## 6. VOSS vocabulary

| Use | Not |
|---|---|
| function | task, job, work |
| invocation | request (except a client HTTP request), call |
| synchronous / asynchronous invocation | sync, async in prose |
| tenant | customer after the first definition |
| provider | the platform, the cloud |
| owner | donor, volunteer (person), host |
| volunteer machine | node, PC, box, donated machine |
| worker | node, host, machine when the VOSS worker is meant |
| session | donation session |
| sandbox | environment, container unless meant |
| warm sandbox | hot, pre-warmed instance |
| snapshot | checkpoint |
| cold start | start-up delay when the whole preparation is meant |
| keep-alive | pre-warm, warm pool |
| deadline | SLO, timeout (a timeout is the per-attempt timer) |
| function key | tenant key unless the root key is meant, secret |
| key holder | trusted worker, provisioned worker |
| holder budget | exposure, trust score |
| provisioning | planner, planning, plan, slow loop |
| request placement | fast loop, routing (routing is the router's forwarding) |
| concurrency limit | slots |
| backup attempt | hedge, duplicate, second copy |
| owner who drops work / who forges results | Byzantine unless citing, gray failure after one citation |
| sampled audit | spot check, voting |
| ISP | provider (reserved for the platform) |
| deadlines met | success, success rate, goodput |

Never write: planner, slow loop, fast loop, single-loop, two-timescale (except in a citation),
slot, exposure, trust score, start-up level, filler, early keys, perishable, referee, the front,
judg*, returned work, second copy, hedg*, cluster (except a computer cluster in a citation), broker,
blockchain, E\d\d, H\d+, R\d\d as experiment names, round, rerun, placeholder, frozen, the world for
the simulated environment, or vendor names for our own models.

## 7. Cold-reader questions

1. What is serverless, and why run it on a machine you do not own?
2. What is a cold start, and why does it matter for a deadline?
3. Why does a worker need a function key? Why can the provider not hold it?
4. What does attestation prove, and what does it not prove?
5. What does the scheduler decide, when, and with what information?
6. What is measured, what is simulated, on which machines and traces?
7. What is the baseline, why is it right, and did it get its standard mechanisms?
8. What is the primary metric, and how are lost, late and forged answers counted?
9. What would make the result wrong, and what are the limits?
10. Is every number traceable to a table, figure or macro?

## 8. Rewrite examples

| Before | After |
|---|---|
| "The slow planner provisions workers ahead of demand." | "Every 30 seconds, the scheduler chooses which workers hold each function's key and which keep a warm sandbox." |
| "VOSS sends a second copy of an invocation." | "If the first attempt does not answer before its timer, VOSS also runs the invocation on a worker in another city or ISP. The first correct result is used." |
| "Extensive experiments show that VOSS is robust." | "On the held-out trace, VOSS meets 91% of deadlines at K=8; when 20% of owners drop results, it meets 84%." |

## 9. Fidelity and finish

- Keep every fact, number, name, date and citation. Keep certainty at its strength.
- Add nothing. Do not make a word vaguer. Flag contradictions.
- Never touch code, commands, paths, URLs, identifiers, quotes, product names, numbers or units.

- [ ] Every paragraph opens with its claim.
- [ ] Every claim has a figure, table, citation or design fact.
- [ ] Every term is defined at first use or in the glossary.
- [ ] No coined label, no one-use jargon, no synonym rotation.
- [ ] Every number has a unit, provenance and section pointer.
- [ ] Measured and simulated values are separate.
- [ ] Lost, late and wrong answers count as misses.
- [ ] No process history in abstract, introduction or results.
- [ ] No style announcement from §5.
- [ ] `scripts/check.py` is clean or every warning is justified.
- [ ] A systems reviewer without serverless background can answer §7.
- [ ] Abstract at most 170 words, no constant, internal comparison or process claim.

The author's 30 heuristics and the approved opening sequence are in
`references/voss-heuristics.md` when present. Use them as a second checklist; the VOSS writing
specification wins if they disagree.
