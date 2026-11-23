---
name: research-humanizer
description: |
  Draft or edit a systems research paper for ACM Transactions on Internet Technology (TOIT)
  so a systems reviewer without serverless background understands it on the first read.
  Removes AI and research-writing tells, then rebuilds paragraphs around a claim and its evidence.
  Tailored to the VOSS paper: its vocabulary, its forbidden terms and its measured claims.
  Use for the abstract, introduction, background, design, method, results, discussion,
  related work, conclusion, figure captions and response letters.
license: MIT
metadata:
  version: "0.1.0"
  target: "ACM TOIT, VOSS"
---

# Research Humanizer (systems papers, VOSS/TOIT)

This is a helper for the VOSS paper, not a general-purpose writing product. Its reader is a systems
reviewer who knows operating systems, distributed systems, networking and measurement, but not
serverless computing. The reviewer reads the paper cold. Every term must be clear from the page.

The skill has two passes:

- **Pass 1** removes habits that make research prose sound generated, inflated or evasive.
- **Pass 2** rebuilds the paper around claims, evidence and the reader's missing context.

Keep every fact. Do not add a number, citation, comparison or claim that is not in the source or the
generated macros. A rewrite that changes the meaning is an error, even if it reads better.

## 1. The reader

The reviewer:

- knows what a virtual machine, a TPM, a network round trip, a trace and a scheduler are;
- does **not** know what serverless is, what a cold start is, why a function needs a key, or why
  anyone would run a function on a machine they do not own;
- will stop when a sentence assumes knowledge that is not on the page;
- will check whether every claim has a figure, table, citation or design fact;
- will check whether measured and simulated values are separated;
- will check whether the baseline is the right one and whether it was given its standard mechanisms;
- will check whether the primary metric counts lost, late and wrong answers as misses.

Write for that person. Do not write for the authors, for a reviewer who already knows the answer, or
for a reader who will read the paper twice.

## 2. How to work

1. **List the facts.** For every paragraph, write the one claim it makes and the evidence for it:
   `F` figure, `T` table, `C` citation, `D` design fact, `M` measured number. A sentence with no
   mark is cut or joined to one that has a mark.
2. **Outline before prose.** One line per paragraph: the claim and its evidence. Do not write a
   paragraph that is not in the outline.
3. **Draft** with the vocabulary of §5. Define a term at first use.
4. **Cold-reader pass.** Read as the reviewer of §1. Mark every undefined term, every "how?", every
   sentence that answers a question nobody asked, and every claim without evidence. Fix and repeat
   once.
5. **Jargon pass.** Highlight every term that is not in §5. If it is used once, describe it in plain
   words. If it is used repeatedly, define it once and use it consistently. Do not rotate synonyms.
6. **Number pass.** Every number has a unit, what it measures, the machine or trace it came from,
   and a section pointer. Numbers come from generated macros, not from memory.
7. **Pass 1 and Pass 2** below. Then run `scripts/check.py` and fix what is real.
8. **Fact-check** against the macros, `docs/PARAMETERS.md`, the code and the results. If the data
   disagree with the outline, change the outline and say so.

## 3. Pass 1: research-writing tells

A tell counts when a careful writer would rarely make it on purpose. Several tells together are the
safeguard. The number is for the edit report.

### A. Staging instead of stating

| § | Tell | Fix |
|---|---|---|
| 1 | **Not X but Y.** "not just a cache, but a new abstraction"; "This is not X. It is Y." | State the point. Keep a contrast only if the reader really believes X. |
| 2 | **One-line closer or fragment.** "That is the real challenge." "No tuning. No surprises." | Cut it or merge it into the claim. |
| 3 | **Grand significance.** "pivotal", "opens the door", "has the potential to transform", "marks a shift" | Replace with the measured claim. |
| 4 | **Staged run-up.** "To this end", "Motivated by this", "In this section, we will..." | Start with the claim. A single roadmap sentence is enough. |
| 5 | **Arguing with no one.** "One might think", "It is tempting to", "Contrary to popular belief" | Cut unless the paper cites the person who said it. |
| 6 | **Rhetorical question.** "Why does this matter?" | Answer it in a statement. |
| 7 | **Forced triad.** "fast, reliable and scalable" | Keep three only if the meaning has three parts. |
| 8 | **Process narrative.** "We first tried X, then Y, and finally..." | Keep only a change that affects how the results are read; put it in the method or limitations. |

### B. Inflation and borrowed authority

| § | Tell | Fix |
|---|---|---|
| 9 | **Stock AI words.** delve, leverage, robust, seamless, crucial, pivotal, showcase, underscore, testament, landscape, realm, harness, utilize, facilitate, elucidate, intricate, meticulous, comprehensive, extensive, novel, state-of-the-art, cutting-edge, paradigm, synergy, holistic, empower, unlock, revolutionize, game-changer, unprecedented | Use the plain word. If the word carries a measurement ("robust to 20% dropping owners"), keep the measurement and drop the adjective. |
| 10 | **Vague importance.** "plays a key role", "is essential for", "is critical to" | Say what happens without it. |
| 11 | **Shallow `-ing` rider.** "..., highlighting the importance of...", "..., enabling...", "..., further demonstrating..." | Cut the rider unless it states a separate fact. |
| 12 | **Sales language.** "powerful", "strong", "best-in-class", "we are the first" | Say what was built and what was measured. |
| 13 | **Borrowed authority.** "experts agree", "industry reports", "it is widely known" | Name the source or cut it. |
| 14 | **Avoiding `is`/`are`/`has`.** "serves as", "acts as", "represents", "boasts", "features" | Use `is`, `are`, `has`. |
| 15 | **Nominalisation.** "make a decision", "perform an evaluation", "the utilisation of" | `decide`, `evaluate`, `using`. |
| 16 | **Hidden actor or passive.** "The token is validated before the request is forwarded." | Name the actor: "The gateway validates the token, then forwards the request." |
| 17 | **Stacked hedges.** "may potentially", "could arguably", "it is possible that" | Keep one qualifier. Keep the source's certainty. |
| 18 | **Self-assessment.** "Our evaluation is comprehensive", "This is a strong result" | Delete. The numbers are the assessment. |
| 19 | **Belief or expectation.** "We believe", "we expect", "we anticipate" | Delete, or label it as a hypothesis in the discussion. |
| 20 | **Chatbot residue.** "Great question", "I hope this helps", "Let me know" | Remove the wrapper. |

### C. Word-level defaults

| Write | Not |
|---|---|
| use | utilize, leverage, employ |
| show | demonstrate, exhibit, showcase |
| start, stop | commence, terminate |
| before | prior to |
| because | due to the fact that |
| to | in order to |
| then | subsequently |
| many | a large number of |
| about, approximately | only when the source is genuinely approximate; otherwise the exact value |
| can | is able to |
| we | the present author(s), this work (when `we` is the actor) |
| because | as (when it means because) |

Do not ban a technical word because it is long. Ban a word that hides the actor, the action or the
evidence.

## 4. Pass 2: systems-paper structure

| S | Rule |
|---|---|
| S1 | **One claim per paragraph.** The first sentence states the claim, not the topic. The rest is evidence. |
| S2 | **Every claim has evidence.** A figure, table, citation or design fact. If it has none, cut it or mark it as a design reason. |
| S3 | **Define at first use.** One clause, by what the thing is and does. Not by what it resembles, not by a vague size. |
| S4 | **Jargon budget.** A term used once is described in plain words. A term used repeatedly is defined once and used consistently. No synonym rotation. No coined label for a one-use mechanism. |
| S5 | **Explain the missing context.** A systems reader needs: what serverless is, what a cold start is, what keep-alive is, why a function has a key, what attestation proves, what a deadline is, who the tenant, owner and provider are. |
| S6 | **Mechanism accuracy.** Name the actor, the event and the order. No anthropomorphism ("the scheduler believes", "the worker suspects"). Name the owner class for every security claim. |
| S7 | **Numbers have provenance.** Value, unit, what it measures, machine or trace, section pointer. Two significant digits with an interval where the data support one. No "about" before a generated macro. |
| S8 | **Separate design, method and results.** Design never mentions the simulator. Method says what is real and what is modelled. Results open with the finding, then the evidence, then the figure. |
| S9 | **No process history** in the abstract, introduction or results. A change that affects the interpretation goes in the method or limitations. |
| S10 | **No overclaim.** "can" is not "does"; "in our runs" is not "in general"; one trace is not all workloads. State the limit plainly in the discussion. |
| S11 | **Active voice, simple tenses, short sentences.** One idea per sentence. No semicolons. No em dashes. |
| S12 | **Paragraphs are 3-6 sentences.** Do not chop reasoning into bullets. Tables are for parameters and results, not for arguments. |
| S13 | **Related work compares mechanisms**, not one-line dismissals. Cite the source of each baseline and list every deviation. |
| S14 | **Abstract:** problem, premise, what was built, headline measured result, basis. At most 170 words. No constants, no internal comparisons, no calibration detail, no process. |
| S15 | **Introduction:** context, setting, the two problems, premise, what it takes before a worker can run a function, what was built, contributions, headline numbers. No project history. |
| S16 | **Headings name what the section holds.** Sentence case. No "Towards", no "On the", no decorative labels. |
| S17 | **Captions are self-contained.** Every label and abbreviation in a figure is defined in the caption. A caption never says "see the text" for a term the reader needs. |
| S18 | **Use the VOSS vocabulary of §5 everywhere**, including figure labels, table headers and the explainer. |

## 5. VOSS vocabulary

Use these terms exactly. The left column is the paper's word; the right column is what not to write.

| Use | Not |
|---|---|
| function | task, job, work |
| invocation | request (except a client HTTP request), call |
| synchronous / asynchronous invocation | sync, async (in prose) |
| tenant | customer (after the first definition) |
| provider | the platform, the cloud |
| owner | donor, volunteer (for the person), host |
| volunteer machine | node, PC, box, donated machine |
| worker | node, host, machine (when the VOSS worker is meant) |
| session | donation session |
| sandbox | environment, container (unless meant), VM for the worker |
| warm sandbox | hot, pre-warmed instance |
| snapshot | checkpoint |
| cold start | start-up delay (when the whole preparation is meant) |
| keep-alive | pre-warm, warm pool |
| deadline | SLO, timeout. A timeout is the scheduler's per-attempt timer. |
| remote attestation, quote, verifier | standard meanings, defined once |
| function key | tenant key (unless the root key is meant), secret |
| key holder | trusted worker, provisioned worker |
| holder budget | exposure, exposure budget, trust score |
| provisioning | planner, planning, plan, slow loop |
| request placement | fast loop, routing (routing is the router's forwarding) |
| concurrency limit | slots |
| backup attempt | hedge, duplicate, second copy |
| owner who drops work / who forges results | Byzantine (unless citing), gray failure (cite once) |
| sampled audit | spot check, voting |
| ISP | provider (reserved for the platform) |
| deadlines met | success, success rate, goodput |

Never write in the VOSS paper: `planner`, `slow loop`, `fast loop`, `single-loop`, `two-timescale`
(except inside a citation), `slot`, `exposure`, `trust score`, `start-up level`, `filler`,
`early keys`, `perishable`, `referee`, `the front`, `judg*`, `returned work`, `second copy`,
`hedg*`, `cluster` (except a computer cluster in a citation), `broker`, `blockchain`, `E\d\d`,
`H\d+`, `R\d\d` as experiment names, `round`, `rerun`, `placeholder`, `frozen`, `the world` for the
simulated environment, or vendor names for our own models.

## 6. Cold-reader questions

Before finishing a section, answer these as the reviewer:

1. What is serverless, and why would anyone run it on a machine they do not own?
2. What is a cold start, and why does it matter for a deadline?
3. Why does a worker need a function key? Why can the provider not hold it?
4. What does attestation prove, and what does it not prove?
5. What does the scheduler decide, when, and with what information?
6. What is measured, what is simulated, and on which machines and traces?
7. What is the baseline, why is it the right comparison, and did it get its standard mechanisms?
8. What is the primary metric, and how are lost, late and forged answers counted?
9. What would make the result wrong, and what are the limits?
10. Is every number traceable to a table, figure or macro?

If a question has no answer on the page, the paper is not finished.

## 7. Rewrite examples

| Before | After |
|---|---|
| "The slow planner provisions workers ahead of demand." | "Every 30 seconds, the scheduler chooses which workers hold each function's key and which keep a warm sandbox." |
| "VOSS sends a second copy of an invocation." | "If the first attempt does not answer before its timer, VOSS also runs the invocation on a worker in another city or ISP. The first correct result is used." |
| "The tenant limits exposure." | "The tenant sets the largest number of workers that may hold a function's key at one time." |
| "The two feed on each other." | Delete, and join the two neighbouring facts. |
| "We propose a novel framework for serverless on volunteers." | "We describe VOSS, a scheduler that runs serverless functions on machines lent by their owners." |
| "Extensive experiments show that VOSS is robust." | "On the held-out trace, VOSS meets 91% of deadlines at K=8; when 20% of owners drop results, it meets 84%." |
| "Our approach is state-of-the-art." | "At K=8, VOSS meets more deadlines than the histogram baseline (91% against 76%, 10 seeds, paired)." |
| "This is challenging because owners can leave." | "An owner can switch the machine off at any time, and every warm sandbox and key on it is lost." |
| "The scheduler is efficient." | "A placement decision takes 0.4 ms at 500 workers, below 1% of the median synchronous deadline." |
| "We believe this generalises." | Delete, or "The result holds for the traced load and the calibrated fleet; Section 7 states the limits." |

## 8. Checker

`scripts/check.py` is a heuristic linter, not an AI detector. It flags the forbidden VOSS terms,
common research-writing tells, long sentences, semicolons, em dashes and a few number habits. It
does not understand context. Fix what is real; ignore a warning when the word is a citation, a
quoted title or a term the paper defines.

```bash
python scripts/check.py manuscript/sections/intro.tex
python scripts/check.py manuscript/sections/*.tex
```

## 9. Fidelity rules

- **Keep every fact, number, name, date and citation.** If a fact does not fit the style, change the
  sentence, not the fact.
- **Keep certainty at its strength.** "may" stays "may" or becomes "can"; it never becomes "does".
- **Add nothing.** No new number, example, citation, comparison or reason.
- **Do not make a word vaguer.** If the source does not define "verify", do not expand it.
- **Flag contradictions.** Keep both statements and say so in a note.
- **Never touch** code, commands, paths, URLs, identifiers, quotes, product names, numbers, units or
  versions.

## 10. Finish checklist

- [ ] Every paragraph's first sentence states its claim.
- [ ] Every claim has a figure, table, citation or design fact.
- [ ] Every term is defined at first use or in the glossary.
- [ ] No coined label, no one-use jargon, no synonym rotation.
- [ ] Every number has a unit, provenance and a section pointer.
- [ ] Measured and simulated values are separate.
- [ ] The primary metric counts lost, late and wrong answers as misses.
- [ ] The baseline is the right one and its deviations are listed.
- [ ] No process history in the abstract, introduction or results.
- [ ] No AI tell from §3 survives; `scripts/check.py` is clean or every warning is justified.
- [ ] A systems reviewer without serverless background can answer the ten questions in §6.
- [ ] The abstract is at most 170 words and contains no constant, internal comparison or process claim.
