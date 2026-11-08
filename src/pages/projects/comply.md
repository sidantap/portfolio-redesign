---
layout: ../../layouts/Project.astro
title: comply., a system of record for DOT drug and alcohol testing
kind: Product engineering
org: Personal project
date: '2026-11'
period: 2026 – now
summary: Employers that run DOT random testing often keep the pool in spreadsheets and send it to an outside administrator they can't see into. comply. keeps the whole program in one record, from the HR system to the inspector.
impact: Live for FAA (14 CFR Part 120); the other DOT agencies are next
img: img/comply.jpg
tags: [system of record, state machines, reproducible randomness, fisher-yates sampling, seeded prng, identity resolution, hr system integration, audit trail, regulatory compliance, 14 cfr part 120, 49 cfr part 40, unit testing, react, typescript, vitest, three.js]
links:
  - { t: complydot.org, href: 'https://www.complydot.org' }
  - { t: Play the brand intro, href: 'https://sidantap.github.io/portfolio/comply.html' }
---

<figure><img src="../../img/comply.jpg" alt="The comply. homepage" /><figcaption>Fig. 1 · complydot.org</figcaption></figure>

## The problem

Every DOT-regulated employer, airlines, trucking, rail, transit, pipelines, must randomly test its safety-sensitive employees for drugs and alcohol. In practice the pool often lives in a spreadsheet, the selection happens inside an outside administrator's black box, and results come back as files someone re-keys. When an inspector asks "show me who was eligible on March 3 and why this person was picked", the answer takes days.

comply. is built around one record that answers that question instantly.

## One record, many moves

Employees sync from the HR system (Workday, ADP, UKG, Paycor, BambooHR). Identity resolution links aliases and rehires to the same person, coverage rules decide who is in a tested job, and every pool change waits in an approval queue with its HR reason attached.

Once someone is selected, their test is a **case**, and a case can only move in ways the regulations allow:

<figure><img src="../../fig/comply-states.svg" alt="State machine from To schedule to Site booked, Notified, Collected, With MRO and Result in, with side paths to DER review, Excused and Cancelled" /><figcaption>Fig. 2 · The case state machine, transcribed from the product's transition table</figcaption></figure>

- A notified test **can't be rescheduled**: the employee goes straight to testing (14 CFR 120.109(b)(8)).
- Alcohol tests skip the MRO; only drug results go through one.
- **Refusals are the DER's call**, recorded through their own review step.
- Excusing or cancelling a case requires a written reason, and only a recorded result counts toward the annual rate.

Encoding this as a state machine rather than free-form statuses is what makes the record trustworthy: an impossible history can't be written.

## A draw anyone can check

<figure><img src="../../fig/comply-draw.svg" alt="Eight names sorted by ID, then three steps of a partial Fisher–Yates shuffle that swap a random later name into the next position" /><figcaption>Fig. 3 · How a selection is made, step by step (illustrative pool)</figcaption></figure>

Each draw runs a **partial Fisher–Yates shuffle** over the pool sorted by employee ID, using a **seeded xoshiro128\*\*** random number generator. Fisher–Yates gives every person an equal chance, which the rule requires (14 CFR 120.109(b)(5)). Because the seed is stored with the draw, anyone can re-run it and get exactly the same names. That turns "trust us, it was random" into something an inspector can verify. Draws are also idempotent: a double click can't create a second one.

## Alerts before an inspector finds it

Person-level checks flag the problems the FAA has actually fined employers for: people in tested jobs missing from the pool, overdue follow-up tests, new hires working before a history check, a pool falling behind its annual pace. All six 2026 FAA enforcement cases map to an alert the demo raises. The rate math follows FAA AC 120-126A, and the audit packet and draft MIS numbers are always ready.

## Built so far

- React 19 and TypeScript, with the rules as pure, tested domain code: **28 unit tests** on selection, rates and compliance logic.
- A demo with a fictional airline and made-up people.
- A brand intro: the word "comply" crashes into its period, and a firefly lights the dot and lands in front of the name. Its flight is simulated, not keyframed: steering with arrival braking, wander, pitch from velocity and wings that fold on landing.

The program manager makes every decision. The software keeps the record.
