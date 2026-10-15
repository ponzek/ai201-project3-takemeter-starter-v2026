# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

<!-- Your criterion. It must name a number. -->

Overall accuracy is at least 0.70 on the held-out set, on each of the
three seeds.



**Why this target:**

I hoped for about 0.80, but I'm setting the floor at 0.70 to leave room for
doubt. `vent` is an emotional label and tone is hard to read from text alone,
so it will blur into the other labels. A random guesser on four labels gets
about 25%, so 0.70 is well above chance, and it has to hold on all three
seeds, not just the best one.



---

## 2.

<!-- Your criterion. -->

Each of `analysis`, `vent` and `question` has an F1 of at least 0.60 on the
held-out set, on each of the three seeds.



**Why this target:**

Chance on four labels is about 25%, so 0.60 is more than double that. It's
lower than my 0.70 overall target because the labels aren't equally easy:
`vent` is emotional and blurs into the others, so I expect it to be my
weakest of the three.



---

## 3.

<!-- Your criterion. -->

`hot_take` has an F1 of at least 0.30 on the held-out set, on each of the
three seeds.



**Why this target:**

`hot_take` is my thinnest label. It was rare in my 40-post reading sample, so
only a handful of examples will land in the test split, and its score will
jump a lot between seeds. That's why this target is much looser than the one
for the other labels. I know 0.30 is close to chance (about 25%), so it only
says the model learned something.

*Note added 15 Oct 2026, after the first run (original text above unchanged):
`hot_take` ended up at 50 of 225 posts (22%), about the same as `analysis`,
so it is no longer my thinnest label. `vent` is (42 posts, 6 in the test
split). The 0.30 target is unchanged.*



---

## 4.

<!-- Your criterion. -->

No label holds more than 60% of my 200 labeled posts.

*Note added 15 Oct 2026 (original text above unchanged): the final dataset
has 225 posts, and the largest label, `question`, holds 34%.*



**Why this target:**

The brief's hard cap is 70%, but a model that always guesses a label holding
70% of the data already scores 0.70, which is my overall accuracy target. At
60%, always guessing the biggest label scores 0.60, below my target, so
hitting 0.70 means the model learned more than the most common label.



---

## 5.

<!-- Your criterion. -->

When I relabel 20 of my posts a week later without looking at my first
labels, at least 80% match.



**Why this target:**

In my own stress tests I matched my intended labels on about 6 to 7 of 8
posts (75-88%), mostly missing on boundary cases. The model can't be
expected to be more consistent than I am, so 80% is about where I landed.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
