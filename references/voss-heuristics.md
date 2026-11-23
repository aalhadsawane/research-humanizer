# VOSS heuristics (condensed from `manuscript/HUMAN_FEEDBACK.md`)

Use this as a second checklist after `SKILL.md`. Each line is a pattern the author reported, not a
one-off fix. Check the whole paper for it.

| # | Check |
|---|---|
| 1 | The abstract and introduction serve a cold reader. No in-house label is used as if it were established vocabulary. Describe a component by what it does. |
| 2 | The abstract states the problem, the main architectural idea and the headline result against established baselines. No tuning, internal comparisons, ablations or cost. |
| 3 | No arbitrary parameter in the abstract. A parameter that was not swept is not a contribution. |
| 4 | Introduce the system's structure before a sentence depends on it. |
| 5 | Use the paper's later vocabulary. Read the body before describing a component in the front matter. |
| 6 | Claims match the results. Stress what was measured, not what the design effort emphasised. Length follows findings. |
| 7 | Wording is mechanism-accurate. If a capability cannot be explained, describe the certain event instead. |
| 8 | The abstract is not the introduction. No narrative connectives or "what remains". |
| 9 | Keep the context the reader needs; keep calibration detail out of the abstract. Calibration belongs in the method and limits. |
| 10 | Explain every domain term for a systems reader without serverless background: cold start, keep-alive, warm sandbox, snapshot, key, attestation, deadline. One clause at first use. |
| 11 | Contributions are what was built and found, not tools used, not project history. |
| 12 | Every number has its provenance at first use: what it measures, on which machine or trace, with a section pointer. |
| 13 | Contributions are self-explanatory. Say what the reader gains, not how the work was organised. |
| 14 | No vague connective or filler sentence. If it cannot be checked, delete it and join its neighbours. |
| 15 | Say literally what the system does, in the words an engineer would use. Check the body that it is what the code does. |
| 16 | A figure is as detailed as the claim it supports. Every label is defined in the caption. |
| 17 | Separate wording fixes from experiment and code work. Wording goes in the `.tex`; a needed measurement goes in the experiment plan and is marked. |
| 18 | Praise tells you the target. The approved introduction defines every term at first use, states the premise instead of listing it as a contribution, names components by what they do, and has no history. |
| 19 | No colloquial quotation or casual phrasing. Use the formal term and define it once. |
| 20 | A paragraph opener states the concrete claim the paragraph proves, not a vague topic. |
| 21 | Define a term by what it is and does, not by a vague size or by equating it with one implementation. |
| 22 | State a modelling assumption where its terms are defined; say which real systems differ. |
| 23 | A definition sentence is readable on its own. |
| 24 | The introduction uses no serverless-specific word a general systems reader lacks. "Capacity, counted as invocations a worker can run at the same time" beats "slots". |
| 25 | Define model quantities from the code, not from a doc or a guess. State an assumed share as assumed and unswept. |
| 26 | State each assumed parameter once, in a table. Do not name another platform's behaviour without a verified citation. |
| 27 | A choice that departs from common practice comes with its reason, checked against the paper's own mechanism. |
| 28 | Name the familiar datacenter pattern first, then where the volunteer setting differs, then the design. |
| 29 | Re-derive every formula from the code. Say for each input whether the scheduler is told it or estimates it. |
| 30 | Every sentence follows from the section's question. Say why an outside fact matters before citing it. Keep method caveats in Limitations. |

## The approved opening sequence

Keep this order in the introduction:

1. Serverless functions run on request and execute for well under a second.
2. Before a function runs, the platform prepares a sandbox, fetches code, loads the runtime and
   libraries, and runs initialisation. This is the cold start, and it often exceeds the execution.
3. Providers keep sandboxes alive and start them ahead of demand on machines they own.
4. Edge platforms run functions in many cities, also on provider-owned machines.
5. Ask whether machines the provider does not own can serve such invocations.

Then the setting, the two problems, the premise, what it takes before a worker can run a function,
what was built, and the measured headline numbers.

## The "three things" paragraph

Before a volunteer machine can run a tenant's function, three things must happen, and each takes
time: the machine boots the image and passes attestation; it obtains the function's key; it starts a
sandbox. All three are lost when the session ends. Each key holder is one more machine the key could
leak from, so the tenant limits their number. Use measured numbers with the machine and section.
