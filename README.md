# TakeMeter

**Karina Ponze | Units 5 and 6**

TakeMeter is my text classifier for posts from **r/cscareerquestions**. I built it to separate supported arguments, unsupported takes, venting, and requests for personal advice. This README covers how I defined the labels, collected the posts, trained the model, and checked what it actually learned.

For setup, commands, and troubleshooting, start with **[RUNNING.md](RUNNING.md)**. Run `python test.py`, then open `takemeter.ipynb` from this folder and select the project's `.venv` kernel. Run section 1 to check the device before training. The project runs locally without accounts or API keys.

## Contents

- [What This Does](#what-this-does)
- [Label Taxonomy](#label-taxonomy)
- [The Dataset](#the-dataset)
- [The Training Run](#the-training-run)
- [How I Used AI](#how-i-used-ai)
- [Baseline vs. Trained](#baseline-vs-trained)
- [Run Log — Before](#run-log--before)
- [Verdicts and Diagnoses](#verdicts-and-diagnoses)
- [Agreement Report](#agreement-report)
- [The Improvement](#the-improvement)
- [What's Still Broken](#whats-still-broken)
- [Stretch Declarations](#stretch-declarations-written-before-building-them)

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

I chose **r/cscareerquestions** because people there discuss CS jobs, layoffs, AI, and the job market. Some posts explain a point with specific details, some are mostly frustration, and others ask for help with a personal decision. I wanted to see whether a classifier could learn the differences I noticed while reading.

**Distinctions I committed to** (each came from posts I read in a 40-post
sample, and each is something I can point at in the text):

1. **Claim or question.** Does the post assert something about the industry
   (e.g. "Good developers have improved development speed for at least x5"), or
   only ask something (e.g. "would you start applying?")?
2. **Specifics or vague.** Does the post cite numbers or concrete details (e.g.
   "12 people", "10-12 hours a day, six days a week"), or none at all?
3. **Reasoning or venting.** Does the post give a because/therefore, or mainly
   express a feeling (e.g. "What the fuck has happened to this profession?")?

I excluded most moderator megathreads, such as resume advice and salary sharing. Two were labeled and kept by mistake.

---

## Label Taxonomy
<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->


### `analysis`

**Definition:** Makes a claim and supports it with a concrete detail or
reasoning, such as a number, a timeframe, or a because/therefore.

**Example 1:**

> Over the last year or so i am and most of my friends and colleagues are
> working 10-12 hours a day, six days a week as companies have shifted to being
> "AI-first" or "AI-native," it is absolutely contrary to the claim that AI
> would make developers' lives easier and cut down on work time

**Example 2:**

> I work in company of 12 people and last 6 months we're been developing 100%
> with AI. [...] Good developers have improved development speed for at least x5.
> Bad developers are still bad developers. They introduce a lot of bugs with AI

### `hot_take`

**Definition:** A view about the industry, the market, or AI as a whole, or a
question put to the community for its views on such a general topic, offered
with no concrete detail or reasoning behind it. The answer matters to
everyone in the field, not only to the author.

**Example 1:**

> People cannot communicate anymore.

(from "Communication Breakdown", which asserts this as a sweeping trend and
illustrates it with a generic Person A / Person B pattern, not a specific case)

**Example 2:**

> CS has gone from arguably the single best to one of the worst career path in
> very short time and nobody has reallly came to terms with it yet. Has there
> ever being another collapse in a field as bad and rapidly as ours?

(from "Has any career in history collapsed as fast as CS?")

### `vent`

**Definition:** The point of the post is a feeling (frustration, nostalgia,
dread), with little or no argument behind it.

**Example 1:**

> What the fuck has happened to this profession?

(from "Company going full agentic", which describes a process then asks how to
feel about it)

**Example 2:**

> i miss those old days. [...] everyone just wants speed and results and the old
> way of doing things almost feels outdated even if it still feels so good deep
> down.

### `question`

**Definition:** Mainly asks for advice, information, or help with the author's
own situation (an offer, an interview, a career move), and makes no claim of
its own.

**Example 1:**

> Title - with all the layoff news, if your company did a large wave of layoffs
> in light of "restructuring", would you begin applying elsewhere? Why or why
> not?

**Example 2:**

> Say you apply for a role with Company A, didn't pass their background
> screening for whatever reason (criminal record, drugs, etc). Have you seen
> anyone reapply and then get hired?

### The hardest boundary

**Hardest pair:** `analysis` and `hot_take`, with `vent` close behind.

**My rule:** If a post uses a concrete detail to support a conclusion, I call it `analysis`, even if it sounds heated or ends with a question. If the feeling is the point and the details are only background, I call it `vent`. If it makes a confident claim without a supporting number, detail, or reason, I call it `hot_take`.

For example, “Why am I working more if AI was supposed to make coding easier?” cites working hours to question the promise of AI productivity. Under this rule, it fits `analysis`. My original cold label was `hot_take`, which I kept in the dataset. I explain that inconsistency in the hard cases below.

### A second boundary: `question` and `hot_take`

**The decision rule I used every time:**
Ask who the answer is for. If the author needs it to decide something in their
own life or work (an offer, an interview, a career move), it's `question`,
even if the post states unsupported claims along the way as assumptions. If
it's a view, or a request for views, on the industry, the market, or AI as a
whole, and the answer wouldn't change anything the author has to decide, it's
`hot_take`. If a post does both, the author's own decision wins.

Examples of the boundary: "Embedded systems, cybersecurity, networking, Edge
AI/ML, academia or pivot out of engineering" says AI will "wipe the entry level
of the field", but the post exists to ask for career advice, so it's
`question`. "Company conducting paper exams on campus for SWE roles. Thoughts?"
asks what the community thinks of a general hiring trend, so it's `hot_take`.

### A third boundary: `vent` and `hot_take`

**The decision rule I used every time:**
If a reader could reasonably reply "that's not true" (e.g. "Leetcode is a
scam"), it's a claim, so `hot_take`. If it only reports how the author feels
("I hate...", "I'm so done"), it's `vent`. If a post has both, the part the
post builds to wins, usually the ending.

Humor and sarcasm don't change the label. I label what the post does, not how
it sounds.

Examples of the boundary: "I hate that every standup is about AI now. Every.
Single. One. I can't take it anymore." is `vent`, because nobody can reply
"false" to "I hate it". "Management is clueless. Always has been. I'm so
done with this place." contains a claim, but it builds to "I'm so done", so it's
also `vent`.

---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Source:** Public posts from r/cscareerquestions. I collected posts through the hot, new, top (month), top (year), and controversial RSS feeds on 14-15 October 2026 to get some variety. I removed moderator megathreads and posts that were only a news link without the author's own text, apart from the two megathreads noted above.

**Labeling process:** I labeled the first 20 posts cold, without help or tools, and marked them `cold` in the note column. An AI assistant pre-labeled the other 205 using my definitions and decision rules, with high, medium, or low confidence recorded in the notes.

I started with the low-confidence rows, then read every pre-labeled post and recorded my own decision. I changed 42 of the 205 AI labels, about 1 in 5. The note column records which labels I confirmed and which I changed.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `question` | 77 | 34% |
| `analysis` | 56 | 25% |
| `hot_take` | 50 | 22% |
| `vent` | 42 | 19% |
| **Total** | 225 | 100% |

(Final counts after my review. No label is above the 70% cap.)

**Three hard cases**
<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->


**1.**
> *The post:* "Why am I working more if AI was supposed to make coding easier?"
>
> *Could have been:* `analysis`, `hot_take` or `vent`.
>
> *I chose, because:* `hot_take` when I labelled it cold, although I called it
> `analysis` in an earlier practice round. It gives hours (10-12 a day, six days
> a week), but they are claims about friends and colleagues that nobody can
> check, and it ends by asking whether it's like this for everyone. I keep my
> original cold label and record the inconsistency here.

**2.**
> *The post:* "Will the market get better with new PERM rules?"
>
> *Could have been:* `hot_take` or `question`.
>
> *I chose, because:* `hot_take`. It states a view ("until there is a
> tax/penalty for offshoring, it won't get better") and asks the community for
> its views on a general market question, not for help with the author's own
> decision.

**3.**
> *The post:* "Company conducting paper exams on campus for SWE roles.
> Thoughts?"
>
> *Could have been:* `hot_take` or `question`.
>
> *I chose, because:* `hot_take`. It asks what the community thinks of a
> hiring trend. The closing line ("whether or not they would take this
> opportunity") is personal, so it sits right on the question boundary.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, 128 tokens per
post, seed 42. Trained on CPU (torch 2.14.1+cpu), as recorded in
`results.json`. <!-- epochs, learning rate, batch size, seed -->

`results.json`. 

**Changes from the defaults:** None for the first run. I kept the notebook settings so I had a starting point to compare against.

**Split sizes:** train 157 / val 34 / test 34 (70/15/15 of 225 posts).
Test split per label: `analysis` 8, `hot_take` 8, `vent` 6, `question` 12.
`vent` has only 6 test examples, below the notebook's threshold of about 8, so
its metrics will move a lot between seeds. <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->

its metrics will move a lot between seeds. 

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

### Moment 1: Finding a missing label

- *What I asked for:* eight posts written to sit on the boundaries of my three
  labels, with the intended labels hidden, to stress-test my definitions.
- *What came back:* I matched 7 of 8. The miss was a confident claim with no
  support, which fit none of `analysis`, `vent` or `question`.
- *What I changed:* I added a fourth label, `hot_take`, and wrote a decision
  rule for `analysis` versus `hot_take`.

### Moment 2: Tightening the boundaries

- *What I asked for:* a second stress test of eight boundary posts, this time
  covering all four labels.
- *What came back:* I matched 6 of 8 cleanly. The split was a sarcastic complaint
  about every standup being about AI, which I first read as `hot_take` because
  of the humour.
- *What I changed:* I added a rule that humour and sarcasm don't change the
  label, and a `vent` versus `hot_take` tie-breaker ("could a reader reply that's
  not true?"). Later I redefined `hot_take` as a view on, or a discussion of,
  the industry as a whole, and rewrote the `question` boundary around whose
  decision the post is about.

**Pre-labelling disclosure:** An AI assistant pre-labelled 205 of my 225
posts, using my definitions and decision rules, and gave each a confidence. I
labelled the other 20 cold. I then read every pre-labelled row, wrote my own
label for each, and changed 42 of them. The labels in `labels.csv` are my
final decisions. The AI also helped draft the wording of this README and the
reasons on criteria 2 to 5, which I asked for. The criteria numbers are mine.

**Unit 6:** An AI coding assistant helped with the testing work. It ran
`baseline.py`, `agreement.py` and the three-seed training from the command line,
wrote `run_three_seeds.py` (including the class-weighting change), and drafted
the README tables, the diagnosis, the confusion-matrix write-ups and "What's
Still Broken" from the numbers in the result files. I read them and kept the
verdicts and numbers, which come from `results_three_seeds_before.json`,
`results_three_seeds_after.json`, `results_three_seeds_after2.json` and
`baseline_results.json`. It suggested class weighting and then training for more
epochs, and I agreed to both. The 30 staff labels, my nine adjudication calls and
their piles are my own. The assistant made two mistakes that I corrected: it first
said my label definitions were missing from the README (they were there), and it
wrote a commit hash into the README that it had not checked. I also opened the
TF's `staff_labels.csv` before my own labels were saved, which is noted in the
Agreement Report.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

**README editing:** I used ChatGPT to clean up the wording, organization, and formatting of this README. It preserved the reported numbers, verdicts, original stretch declarations, and my adjudication decisions. It also flagged a mismatch between the disagreement entries and the summary: the entries had all nine marked pile (a). I corrected entries 4, 7 and 8 to pile (c), which are the piles I originally gave for them. This editing pass did not rerun the experiments or verify the repository history.

---

## Baseline vs. Trained
<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->


| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.235 | 0.382 | +0.147 |
| Macro F1 | 0.100 | 0.189 | +0.089 |
| F1 — `analysis` | 0.400 | 0.222 | -0.178 |
| F1 — `hot_take` | 0.000 | 0.000 | +0.000 |
| F1 — `vent` | 0.000 | 0.000 | +0.000 |
| F1 — `question` | 0.000 | 0.533 | +0.533 |

Baseline: `facebook/bart-large-mnli`, zero-shot, using my definitions from
`label_definitions.txt` (`baseline_results.json`). Trained: seed 42, from
`results.json`. Both were scored on the same 34 posts in `test_split.csv`.

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->


My trained model will beat the zero-shot baseline most on `hot_take` and `vent`,
because those labels depend on my own tie-breaker rules ("could a reader reply
that's not true?", "the part the post builds to wins") that the baseline never
saw, while the two will be closest on `question`, which can be spotted from the
definition alone.

(Committed in `bd424d7`, before the baseline or comparison was run. It was
wrong: neither model scored above 0 on `hot_take` or `vent`, and `question` was
the label with the biggest gap, +0.533.)

<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

**What the gap means:**

My original trained model beat the baseline with definitions: 0.382 vs. 0.235 accuracy. But that baseline predicted `analysis` for 32 of 34 posts, so it was mostly repeating one label.

I also tested the baseline using only the label names (`baseline_results_bare.json`). It reached 0.529 accuracy and 0.433 macro F1, both higher than my original trained model. So the first training run did not improve on the stronger baseline. Its predictions were mostly `question`, as the confusion matrix below shows.

| Measure | Baseline with definitions | Baseline, bare names | Trained |
|---|---|---|---|
| Overall accuracy | 0.235 | 0.529 | 0.382 |
| Macro F1 | 0.100 | 0.433 | 0.189 |
| F1 — `analysis` | 0.400 | 0.400 | 0.222 |
| F1 — `hot_take` | 0.000 | 0.000 | 0.000 |
| F1 — `vent` | 0.000 | 0.667 | 0.000 |
| F1 — `question` | 0.000 | 0.667 | 0.533 |

---

## Run Log — Before
<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->


Device: CPU (PyTorch 2.14.1+cpu), recorded in `results_three_seeds_before.json`.
Seeds 42, 7 and 2024; 3 epochs, learning rate 2e-5, batch size 16, `distilbert-base-uncased`.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.70 on every seed | 0.382 | 0.382 | 0.353 | MISSED |
| 2. F1 of `analysis`, `vent`, `question` | each ≥ 0.60 on every seed | 0.222 / 0.000 / 0.533 | 0.222 / 0.000 / 0.533 | 0.000 / 0.000 / 0.522 | MISSED |
| 3. F1 of `hot_take` | ≥ 0.30 on every seed | 0.000 | 0.000 | 0.000 | MISSED |
| 4. Largest label share of labeled posts | ≤ 60% | 34% (`question`) | 34% | 34% | MET |
| 5. Relabel 20 posts a week later, matches | ≥ 80% | 65% (13/20) | 65% (13/20) | 65% (13/20) | MISSED |

Criterion 4 is a property of `labels.csv`, so it is the same on every seed.
Criterion 5 asks for a relabel of 20 of my own posts a week later. I relabeled
20 random posts from `labels.csv` without looking at my first labels
(`relabel_20.csv`) and matched 13 of 20, 65%. This is a property of my labels, so
it is the same on every seed. The staff set (70%, 30 posts, a different
taxonomy) points the same way.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42 (34 test posts):

| true \ predicted | analysis | hot_take | vent | question |
|---|---|---|---|---|
| **analysis** | 1 | 0 | 0 | 7 |
| **hot_take** | 0 | 0 | 0 | 8 |
| **vent** | 0 | 0 | 0 | 6 |
| **question** | 0 | 0 | 0 | 12 |

<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

**The biggest confusion:**

The model called 8 real `hot_take` posts `question`, while 0 real `question` posts went the other way. It also called 7 `analysis` posts and 6 `vent` posts `question`. On this seed, it predicted `question` for 33 of 34 posts. Its 0.382 accuracy came from getting 12 `question` posts and 1 `analysis` post right, rather than learning all four labels.

---

## Verdicts and Diagnoses
<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->


| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.70 on every seed | MISSED | 0.382, 0.382 and 0.353 are all below 0.70; no seed reached it. |
| 2 | F1 of `analysis`, `vent`, `question` | each ≥ 0.60 on every seed | MISSED | `vent` is 0.000 on all three seeds, `analysis` is 0.222 / 0.222 / 0.000, and `question` is 0.533 / 0.533 / 0.522. All three labels miss on every seed. |
| 3 | F1 of `hot_take` | ≥ 0.30 on every seed | MISSED | 0.000 on all three seeds. |
| 4 | No label above 60% | ≤ 60% | MET | The largest label, `question`, holds 34% of the 225 posts. |
| 5 | Relabel 20 posts, ≥ 80% match | ≥ 80% | MISSED | I relabeled 20 random posts from `labels.csv` blind (`relabel_20.csv`) and matched my original label on 13 of 20, 65%. The 7 mismatches are listed under What's Still Broken. |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->
**Criteria 1, 2 and 3: accuracy and per-label F1.** The clearest problem was that the model mostly guessed `question`. On seed 42, it chose that label for 33 of 34 test posts, and the other three labels had zero or one correct prediction each. Training loss moved from about 1.39 to 1.29 over three epochs, still close to 1.386 (ln 4), the loss from assigning equal probability to all four labels. That suggests the model had learned very little.

The accuracy spread was only 0.029, and seeds 42 and 7 had identical scores. That small spread was not reassuring: the model was repeating nearly the same answer.

My agreement report also points to a labeling problem. Six of my 9 disagreements with staff are pile (a), all on the `analysis` boundary: I under-called `analysis` on three posts and over-called it on three. The examples show that I sometimes followed tone instead of the written rule. That may explain some trouble with `analysis`, but it does not explain the collapse to `question`: the staff set uses a different taxonomy and has no `question` posts.

---

## Agreement Report
<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->


**Agreement rate:** 21 / 30 = 70%

Disclosure: I opened the TF's `staff_labels.csv` before my own labels were
saved. I labelled from the staff definitions in `data/staff_taxonomy.md`, but
the rate may be higher, and the adjudications easier, than if I had not seen
it.

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

### Disagreements

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

The piles mean: **(a)** a rule covered the case but I applied it loosely; **(b)** the definitions did not cover the case; **(c)** the rule was ambiguous and my reading was defensible.

**1.**
> *The post:* "I tracked sleep against session quality for eleven weeks. Under seven hours the next day's intervals were 6-8 seconds per mile slower, every time bar one. Small sample, one runner, but it's consistent enough that I've stopped scheduling hard days after late shifts."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* analysis. person kept track and analyzed
>
> *Which pile:* (a)

**2.**
> *The post:* "Carbon plates aren't the whole story. My times dropped 2% in the shoes and another 2% the following year in the same pair, when the only thing that changed was going from 35 to 50 miles a week."
>
> *Staff said / I said:* `analysis` / `reaction`
>
> *My call, and why:* analysis. person kept track and analyzed
>
> *Which pile:* (a)

**3.**
> *The post:* "Went back through the club results going back to 2012. Every single year the number of people who enter the spring marathon and don't start it sits between 18 and 23 percent. It's not a bad-luck year, it's the base rate."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* analysis. statistical point for baseline
>
> *Which pile:* (a)

**4.**
> *The post:* "Anyone who races more than once a month isn't training, they're just collecting medals."
>
> *Staff said / I said:* `hot_take` / `reaction`
>
> *My call, and why:* reaction. the way it is said “They’re just…”
>
> *Which pile:* (c)

**5.**
> *The post:* "Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story and the sport has a problem."
>
> *Staff said / I said:* `hot_take` / `analysis`
>
> *My call, and why:* hot_take. sense of sarcasm
>
> *Which pile:* (a)

**6.**
> *The post:* "Track sessions are wasted on anyone running slower than 8 minute miles. You'd get more out of just running more."
>
> *Staff said / I said:* `hot_take` / `analysis`
>
> *My call, and why:* hot_take. seemed more of an opinion than a stat
>
> *Which pile:* (a)

**7.**
> *The post:* "Every injury thread on this forum is the same injury and the same three replies."
>
> *Staff said / I said:* `hot_take` / `reaction`
>
> *My call, and why:* reaction. Person seemed annoyed there was no other info on the forum
>
> *Which pile:* (c)

**8.**
> *The post:* "Blew up at 20 with the pace band still in my hand like it was going to help. Rough one."
>
> *Staff said / I said:* `reaction` / `hot_take`
>
> *My call, and why:* hot_take. He thought the pace band was going to push him up
>
> *Which pile:* (c)

**9.**
> *The post:* "Wind was so bad on the out section I was leaning at about 20 degrees. Coming back felt like cheating."
>
> *Staff said / I said:* `reaction` / `analysis`
>
> *My call, and why:* reaction. “felt”
>
> *Which pile:* (a)

**What I noticed in my disagreements:**

Six of the nine disagreements are pile (a), all on the `analysis` boundary. I under-called `analysis` on three posts (sleep tracking, carbon plates, and club results since 2012) and over-called it on three (times down 3%, track sessions, and wind on the out section). The other three are pile (c), all on the `hot_take` and `reaction` boundary (races more than once a month, injury threads, and blew up at 20).

The reasons I wrote show a clearer pattern: I sometimes went by how a post sounded. For the 3% post, I wrote “sense of sarcasm.” For the wind post, I wrote “felt.” Elsewhere, I wrote “the way it is said” and “person seemed annoyed.” The staff rules instead ask whether a checkable fact supports the argument and whether the post centers on a claim or the writer's reaction.

My own taxonomy says humor and sarcasm do not change the label, so my sarcasm explanation shows the same consistency problem. I need to apply the written boundary more carefully instead of relying on the feeling of a post.

---

## The Improvement

**What I changed:** One thing: the training loss is now weighted by the inverse
of each label's frequency in the training split (class weighting), so mistakes
on rare labels cost more. Nothing else changed: same labels, split, seeds
(42, 7, 2024), 3 epochs, learning rate 2e-5, batch size 16 and
`distilbert-base-uncased`. The change is in `run_three_seeds.py`
(`use_class_weights`; commit `b6b1bde` made the change before the run, and the run
itself wrote `results_three_seeds_after.json`, committed in `91d8830`).

**Which diagnosis pointed at it:** Criteria 1, 2 and 3 missed because the model
guessed `question` for nearly every post (33 of 34 on seed 42) and scored 0 on
`hot_take` and `vent`. `question` is my biggest label (34%), so a model that
never leaves chance level learns to guess it. Weighting the loss is meant to
stop that single-label collapse.

### Run Log — After

Same device (CPU) and settings as the Before log.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.70 on every seed | 0.353 | 0.588 | 0.265 | MISSED |
| 2. F1 of `analysis`, `vent`, `question` | each ≥ 0.60 on every seed | 0.182 / 0.348 / 0.455 | 0.615 / 0.000 / 0.667 | 0.333 / 0.111 / 0.400 | MISSED |
| 3. F1 of `hot_take` | ≥ 0.30 on every seed | 0.333 | 0.632 | 0.000 | MISSED |
| 4. Largest label share of labeled posts | ≤ 60% | 34% (`question`) | 34% | 34% | MET |
| 5. Relabel 20 posts a week later, matches | ≥ 80% | 65% (13/20) | 65% (13/20) | 65% (13/20) | MISSED |

Before and after, side by side (mean of the three seeds in brackets):

| Measure | Before: 42 / 7 / 2024 | After: 42 / 7 / 2024 |
|---|---|---|
| Overall accuracy | 0.382 / 0.382 / 0.353 (0.372) | 0.353 / 0.588 / 0.265 (0.402) |
| Macro F1 | 0.189 / 0.189 / 0.130 (0.169) | 0.329 / 0.478 / 0.211 (0.339) |
| F1 — `analysis` | 0.222 / 0.222 / 0.000 (0.148) | 0.182 / 0.615 / 0.333 (0.377) |
| F1 — `hot_take` | 0.000 / 0.000 / 0.000 (0.000) | 0.333 / 0.632 / 0.000 (0.322) |
| F1 — `vent` | 0.000 / 0.000 / 0.000 (0.000) | 0.348 / 0.000 / 0.111 (0.153) |
| F1 — `question` | 0.533 / 0.533 / 0.522 (0.529) | 0.455 / 0.667 / 0.400 (0.507) |
| Accuracy spread across seeds | 0.029 | 0.324 |

Confusion matrix after (seed 42):

| true \ predicted | analysis | hot_take | vent | question |
|---|---|---|---|---|
| **analysis** | 1 | 1 | 4 | 2 |
| **hot_take** | 0 | 2 | 3 | 3 |
| **vent** | 2 | 0 | 4 | 0 |
| **question** | 0 | 1 | 6 | 5 |

**Did it help?** Partly, but it did not change any verdict. Criteria 1, 2 and 3 stayed MISSED, criterion 4 stayed MET, and criterion 5 stayed MISSED (65% self-agreement, which a model change cannot fix).

Class weighting helped the model move away from predicting one label. Before the change, `hot_take` and `vent` had F1 0.000 on every seed. Afterward, `hot_take` scored 0.333 and 0.632 on two seeds, and mean macro F1 rose from 0.169 to 0.339. Seed 7 also passed the individual F1 target for `analysis` (0.615) and `question` (0.667), though criterion 2 requires every listed label to pass on every seed.

The accuracy results were mixed. Mean accuracy went from 0.372 to 0.402, but it fell on seed 42 (0.382 to 0.353) and seed 2024 (0.353 to 0.265). The spread grew from 0.029 to 0.324. The small Before spread mainly reflected repeated `question` predictions; it was not evidence of a useful, stable classifier. With only 34 test posts, one post changes accuracy by about 3 points. I can say class weighting reduced the collapse, but these runs do not establish a reliable accuracy improvement.

### Confidence check (stretch)

The notebook records how sure the model was about each guess, split into the
most and least confident thirds of the test posts (11 posts per third).
Accuracy on the most confident third vs. the least confident third:

| Run | Seed 42 | Seed 7 | Seed 2024 |
|---|---|---|---|
| Before: most / least confident | 0.636 / 0.182 | 0.727 / 0.182 | 0.636 / 0.182 |
| After: most / least confident | 0.455 / 0.455 | 0.636 / 0.273 | 0.455 / 0.182 |

Confident predictions were right more often than unsure ones on five of six
runs; the exception is After seed 42, where the two thirds tied at 0.455. The
signal is weak, though: with 11 posts per third, one post is 9 points, and the
average confidence when right and when wrong is nearly the same (After seed 42:
0.274 vs. 0.275; Before seed 42: 0.347 vs. 0.338). The model is rarely sure
about anything (a four-way guess is 0.25).

### Per-label error write-up (stretch)

The worst label after the change is `vent` (F1 0.348, 0.000 and 0.111; mean
0.153). It is confused with `question` in both directions, and the direction
changes with the seed:

- Seed 42: 6 real `question` posts were called `vent`, and 0 real `vent` posts
  were called `question`. `analysis` (4) and `hot_take` (3) were also called
  `vent`, so on this seed `vent` is where uncertain posts landed.
- Seed 7: 4 of 6 real `vent` posts were called `question`, and 2 `hot_take`.
- Seed 2024: 4 of 6 real `vent` posts were called `question`, and 5 real
  `question` posts were called `vent`.

What the examples have in common: I did not save the model's prediction for each
post, so I cannot list the individual misclassified posts. The evidence I do
have is in my own labels. In my review queue, 6 posts I labelled `question` carry
the note "(also venting)", and my labels for `vent` posts include ones that ask
something at the end ("asks at the end but the point is feeling"). My README rule
is that `question` asks for help with the author's own situation and `vent` is a
post whose point is a feeling, but many career posts do both. If I labelled that
boundary by judgment call, a model trained on 157 posts has little to separate
them with.

### Second improvement: more epochs (stretch)

**What I changed:** One more thing on top of class weighting: training for 10
epochs instead of 3 (`python run_three_seeds.py after2`; commit `c6f3e25` has the
results, and the change was committed before the run). Class weighting, the
split, seeds, learning rate, batch size and model are the same as the
class-weighted run above, so this run differs from it by epochs only. I picked 10
once, before looking at any results, and did not try other values.

**Which diagnosis pointed at it:** The training loss in the class-weighted run
was still about 1.32 after 3 epochs, close to the 1.386 of guessing the four
labels equally, so the model had barely trained. A two-stage classifier (my
declared candidate) would not address that, and it would not fix the small,
unstable test set either, so I did not build it.

Run Log (class weights + 10 epochs), same device (CPU):

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.70 on every seed | 0.500 | 0.676 | 0.529 | MISSED |
| 2. F1 of `analysis`, `vent`, `question` | each ≥ 0.60 on every seed | 0.429 / 0.364 / 0.667 | 0.667 / 0.462 / 0.727 | 0.429 / 0.500 / 0.621 | MISSED |
| 3. F1 of `hot_take` | ≥ 0.30 on every seed | 0.308 | 0.778 | 0.462 | MET |
| 4. Largest label share of labeled posts | ≤ 60% | 34% (`question`) | 34% | 34% | MET |
| 5. Relabel 20 posts a week later, matches | ≥ 80% | 65% (13/20) | 65% (13/20) | 65% (13/20) | MISSED |

All three runs side by side (mean of three seeds in brackets):

| Measure | Before | + class weights | + 10 epochs |
|---|---|---|---|
| Overall accuracy | 0.382 / 0.382 / 0.353 (0.372) | 0.353 / 0.588 / 0.265 (0.402) | 0.500 / 0.676 / 0.529 (0.568) |
| Macro F1 | 0.189 / 0.189 / 0.130 (0.169) | 0.329 / 0.478 / 0.211 (0.339) | 0.442 / 0.658 / 0.503 (0.534) |
| F1 — `analysis` | 0.222 / 0.222 / 0.000 (0.148) | 0.182 / 0.615 / 0.333 (0.377) | 0.429 / 0.667 / 0.429 (0.508) |
| F1 — `hot_take` | 0.000 / 0.000 / 0.000 (0.000) | 0.333 / 0.632 / 0.000 (0.322) | 0.308 / 0.778 / 0.462 (0.516) |
| F1 — `vent` | 0.000 / 0.000 / 0.000 (0.000) | 0.348 / 0.000 / 0.111 (0.153) | 0.364 / 0.462 / 0.500 (0.442) |
| F1 — `question` | 0.533 / 0.533 / 0.522 (0.529) | 0.455 / 0.667 / 0.400 (0.507) | 0.667 / 0.727 / 0.621 (0.672) |
| Accuracy spread across seeds | 0.029 | 0.324 | 0.176 |

Confusion matrix, seed 42 (34 test posts):

| true \ predicted | analysis | hot_take | vent | question |
|---|---|---|---|---|
| **analysis** | 3 | 2 | 1 | 2 |
| **hot_take** | 1 | 2 | 1 | 4 |
| **vent** | 2 | 0 | 2 | 2 |
| **question** | 0 | 1 | 1 | 10 |

**Did it help?** Yes, compared with the class-weighted run,
which is the only thing it differs from. Mean accuracy went from 0.402 to 0.568,
mean macro F1 from 0.339 to 0.534, and the worst seed's accuracy from 0.265 to
0.500. Every label now has an F1 above 0 on every seed. Criterion 3 flipped from
MISSED to MET: `hot_take` is 0.308, 0.778 and 0.462, all at or above 0.30.
Training loss kept falling (seed 2024: about 1.39 to 0.78 over 10 epochs), which
fits a model that was undertrained at 3 epochs.

**What still missed:** Criteria 1 and 2 are still MISSED. Accuracy reached 0.676 on
seed 7, just under 0.70, and was 0.500 and 0.529 on the other seeds. In
criterion 2, `question` clears 0.60 on all three seeds (0.667, 0.727, 0.621), but
`vent` is below 0.60 on all three (0.364, 0.462, 0.500) and `analysis` is below
on two.

**How much I trust it:** The test split is 34 posts, so one post moves accuracy by
about 3 points, and seed 42's `hot_take` clears the 0.30 target by 0.008 on 8
posts, so that MET is fragile. The accuracy spread across seeds is still 0.176,
above the 10-point warning, so the dataset is still too small for a stable
measure. I read the results once and did not choose the number of epochs using
the test split, but the result is one set of three seeds, not a sweep.

Confidence check for this run, accuracy on the most vs. least confident third
(11 posts each): seed 42 0.364 / 0.545, seed 7 0.909 / 0.364, seed 2024
0.636 / 0.455. Confident predictions were right more often on two of three seeds;
on seed 42 the unsure third did better, so confidence is still not a reliable
signal here.

---

## What's Still Broken
<!-- For each criterion still missed: what you'd do, and why you stopped. -->


I stopped here because the unit asks for one measured improvement (I made two, the
second as a stretch item), and every remaining miss points at the data more than
at the training settings.

- **Criterion 1 (accuracy ≥ 0.70 on every seed): still MISSED.** Best result is
  0.676 on seed 7, and 0.500 and 0.529 on the other two. What I'd do: label more
  posts, especially `vent` (42 of 225), and use a bigger test split or repeat the
  split more times, because with 34 test posts one post is about 3 points and the
  spread across seeds is still 0.176.
- **Criterion 2 (F1 ≥ 0.60 for `analysis`, `vent`, `question`): still MISSED.**
  `question` passes on all three seeds; `vent` fails on all three (0.364, 0.462,
  0.500) and `analysis` fails on two (0.429, 0.429). What I'd do: add about 30
  more `vent` posts, and go back to the `analysis` boundary and apply my rule
  once, because 6 of my 9 staff disagreements were pile (a) on that boundary, so
  my own `analysis` labels are probably inconsistent. I'd also write a firmer rule
  for `vent` vs. `question`, since my review notes mark 6 `question` posts as
  "also venting".
- **Criterion 3 (`hot_take` F1 ≥ 0.30): MET after the changes, but fragile.**
  Seed 42 clears it by 0.008 on 8 posts. It meets the stated target in these runs, but I would want a larger test split before trusting that result.
- **Criterion 5 (relabel 20 posts, ≥ 80% match): MISSED, 13/20 = 65%.** I relabeled
  20 random posts blind. The 7 mismatches: #2 analysis→hot_take, #4 vent→question,
  #6 hot_take→analysis, #9 analysis→question, #11 question→analysis,
  #13 question→analysis, #20 hot_take→vent (first label → relabel). Six of the 7
  involve `analysis` or `question`, and #4 and #20 sit on the vent boundary. If I
  disagree with my own labels 35% of the time, that noise limits what the model can learn.

**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->


I meant my labels to capture what a post is doing (arguing from a fact, asserting
a claim, expressing a feeling, asking for help), decided by tie-breaker rules like
"the part the post builds to wins". On seed 42 the model gets `question` right
most often (10 of 12) and mixes up the rest, calling 4 of 8 `hot_take` posts and
2 of 6 `vent` posts `question`. My guess is that it separates posts that ask
something from posts that don't, and has not learned my other boundaries from
157 training posts, but I have not tested that.
<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->


---

## Stretch Declarations (written before building them)

I am attempting all three stretch items:

1. **Confidence check.** I will report whether the model's confident predictions
   are right more often than its unsure ones, using the `confidence` numbers
   already in `results_three_seeds_before.json`, with the counts behind it.
2. **Per-label error write-up.** For whichever label the confusion matrix shows
   is worst, I will say what it gets confused with and what those examples have
   in common.
3. **A second measured improvement.** After my first improvement, I will make a
   second change that my diagnosis points at, run it on the same three seeds in
   the same table format, and say whether it helped. My candidate is a
   two-stage classifier (`analysis` vs. everything else, then the remaining
   labels), but I will only build it if the diagnosis supports it. If it
   doesn't, I will say so and pick the change the diagnosis does point at.

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
