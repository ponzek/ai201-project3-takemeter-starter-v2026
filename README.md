# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

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

TakeMeter sorts posts from **r/cscareerquestions** (public, no login needed), a
community where people discuss CS jobs, layoffs, AI and the job market. Posts
there range from reasoned arguments backed by real numbers to venting with no
point to bare questions. The classifier is meant to tell those kinds of post
apart.

**Distinctions I committed to** (each came from posts I read in a 40-post
sample, and each is something I can point at in the text):

1. **Claim or question.** Does the post assert something about the industry
   (e.g. "Good developers have improved development speed for at least x5"), or
   only ask something (e.g. "would you start applying?")?
2. **Specifics or vague.** Does the post cite numbers or concrete details (e.g.
   "12 people", "10-12 hours a day, six days a week"), or none at all?
3. **Reasoning or venting.** Does the post give a because/therefore, or mainly
   express a feeling (e.g. "What the fuck has happened to this profession?")?

Most mod megathreads (resume advice, salary sharing) are excluded from the
data. Two were labelled and kept by mistake.




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

**Which two labels:** `analysis` and `hot_take` (with `vent` as a close
second)

**The decision rule I used every time:**
If the post gives a concrete detail and uses it to support a conclusion, it's
`analysis`, even if the tone is heated or it ends with a question. If the
feeling is the point and the details are only backdrop, it's `vent`. If a post
states a confident claim but offers no number, detail, or because, it's
`hot_take`, even when the tone is calm. A claim with no support is not
`analysis`.

Example of the boundary: "Why am I working more if AI was supposed to make
coding easier?" has burnout and venting in it, but it cites hours and uses them
to argue that the AI productivity boost is really overtime, so it's `analysis`.

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

**Where the posts came from:** r/cscareerquestions, public posts only. I pulled
the public RSS feeds for hot, new, top (month), top (year) and controversial on
14-15 October 2026, so the sample isn't all one kind of post. I removed
moderator megathreads (resume advice, salary sharing, rant and interview
threads) and posts that were only a news link with no text of their own.

**How I labelled them:** I labelled the first 20 posts cold, with no help and
no tools (note column: `cold`). An AI assistant pre-labelled the other 205 using
my definitions and decision rules, and gave each a confidence of high, medium or
low (note column: `pre-labelled by AI, confidence ...`). I reviewed the
low-confidence rows first.

I read every pre-labelled row and wrote a label for each one, whether I agreed
or not. I changed 42 of the 205 AI labels (about 1 in 5). Rows are marked in the
note column as confirmed or changed.

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

**Anything I changed from the defaults, and why:** Nothing. I used the
notebook defaults for the first run.

**Split sizes:** train 157 / val 34 / test 34 (70/15/15 of 225 posts).
Test split per label: `analysis` 8, `hot_take` 8, `vent` 6, `question` 12.
`vent` has only 6 test examples, below the notebook's threshold of about 8, so
its metrics will move a lot between seeds. <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* eight posts written to sit on the boundaries of my three
  labels, with the intended labels hidden, to stress-test my definitions.
- *What came back:* I matched 7 of 8. The miss was a confident claim with no
  support, which fit none of `analysis`, `vent` or `question`.
- *What I changed:* I added a fourth label, `hot_take`, and wrote a decision
  rule for `analysis` versus `hot_take`.

**Moment 2**

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

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

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

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->
The trained model beats the baseline that used my definitions (0.382 vs. 0.235
accuracy). That baseline predicted `analysis` for 32 of 34 posts, so it was
mostly guessing one label. When I removed the definitions and gave it only the
bare label names (`baseline_results_bare.json`), it scored 0.529 accuracy and
0.433 macro F1, which is higher than my trained model. So against a fair
baseline my fine-tuning has not yet added anything: the trained model mostly
predicts `question` (see the confusion matrix below).

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
| 5. Relabel 20 posts a week later, matches | ≥ 80% | not measured | not measured | not measured | NOT TESTED |

Criterion 4 is a property of `labels.csv`, so it is the same on every seed.
Criterion 5 asks for a relabel of 20 of my own posts a week later; I have not
done that relabel. The only agreement evidence I have is the staff set (70%, 30
posts, a different taxonomy), which is a proxy and not a test of this criterion.

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

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->
8 real `hot_take` posts were called `question`, and 0 real `question` posts went
the other way. The same is true of `analysis` (7 called `question`) and `vent`
(6 called `question`). The model did not learn a boundary between `question` and
the other three labels: it called 33 of 34 posts `question`, and its 0.382
accuracy is the 13 it got right by that guess (12 `question` and 1 `analysis`).



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
| 5 | Relabel 20 posts, ≥ 80% match | ≥ 80% | NOT TESTED | I have not done the relabel. The staff agreement of 70% is a proxy on a different taxonomy, so I am not calling it MET or MISSED. |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->
**Criteria 1, 2 and 3 (accuracy and per-label F1).** Cause: the model did not
learn to separate the labels at all and mostly guessed `question`. Evidence:
(1) on seed 42 it predicted `question` for 33 of 34 test posts, and the other
three labels each have zero or one correct; (2) training loss barely moved,
from about 1.39 to 1.29 over three epochs, and 1.386 (ln 4) is the loss of
guessing the four labels equally, so it never left chance level; (3) accuracy
is stable across seeds (spread 0.029) and seeds 42 and 7 give identical
numbers, so this is not one unlucky split. The model-versus-labels question is
decided by the agreement report below: [fill in after adjudication: how many of
the 9 disagreements are pile (a), and what that says about whether my own labels
were applied consistently].



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

**Disagreements**

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
> *Which pile:* (a)

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
> *Which pile:* (a)

**8.**
> *The post:* "Blew up at 20 with the pace band still in my hand like it was going to help. Rough one."
>
> *Staff said / I said:* `reaction` / `hot_take`
>
> *My call, and why:* hot_take. He thought the pace band was going to push him up
>
> *Which pile:* (a)

**9.**
> *The post:* "Wind was so bad on the out section I was leaning at about 20 degrees. Coming back felt like cheating."
>
> *Staff said / I said:* `reaction` / `analysis`
>
> *My call, and why:* reaction. “felt”
>
> *Which pile:* (a)

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



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
