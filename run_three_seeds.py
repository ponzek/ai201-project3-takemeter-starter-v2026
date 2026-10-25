"""Run takemeter.ipynb sections 6 and 7 from the command line.

Uses the notebook's own cells so the numbers are exactly what the notebook
would produce. The single-split training and evaluation tails of cells 12, 14
and 16 are cut off, because cell 16 overwrites results.json and
test_split.csv, which are the committed unit 5 evidence.

Usage:
    python run_three_seeds.py            # RUN_LABEL = "before"
    python run_three_seeds.py after      # RUN_LABEL = "after" (class weights)
    python run_three_seeds.py after2     # class weights + 10 epochs
"""
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

run_label = sys.argv[1] if len(sys.argv) > 1 else "before"

with open("takemeter.ipynb", encoding="utf-8") as f:
    cells = json.load(f)["cells"]


def source(i):
    return "".join(cells[i]["source"])


# Cut each of these cells just before the line that runs one training pass.
CUTS = {
    12: "train_df, val_df, test_df = split_dataset(df, SEED)",
    14: "trainer, tokenizer = train_model(",
    16: "results = evaluate(trainer, tokenizer, test_df, LABELS, seed=SEED)",
}

ns = {"__name__": "__main__"}


def use_class_weights(ns):
    """The ONE change for the 'after' run: weight the loss by 1 / label frequency.

    The notebook's train_model builds a Trainer from the global name `Trainer`.
    Swapping that name for a subclass changes only the loss; the labels, split,
    seeds, epochs, learning rate, batch size and model are all untouched.
    """
    import torch

    base_trainer = ns["Trainer"]

    class WeightedTrainer(base_trainer):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            y = torch.tensor(self.train_dataset["labels"])
            counts = torch.bincount(y, minlength=self.model.config.num_labels).float()
            self.class_weights = len(y) / (len(counts) * counts.clamp(min=1))

        def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
            labels = inputs.pop("labels")
            outputs = model(**inputs)
            loss = torch.nn.functional.cross_entropy(
                outputs.logits, labels,
                weight=self.class_weights.to(outputs.logits.device),
            )
            return (loss, outputs) if return_outputs else loss

    ns["Trainer"] = WeightedTrainer


for i in (2, 4, 6, 8, 10, 12, 14, 16, 19, 21, 23):
    code = source(i)
    if i in CUTS:
        code = code.split(CUTS[i])[0]
    if i == 19:
        code = code.replace('RUN_LABEL = "before"', f'RUN_LABEL = "{run_label}"')
        if run_label in ("after", "after2"):
            use_class_weights(ns)
    exec(compile(code, f"notebook_cell_{i}", "exec"), ns)
    if i == 6 and run_label == "after2":
        # Second change: train longer. Everything else matches the 'after' run.
        ns["EPOCHS"] = 10
        print("after2: EPOCHS set to 10")
