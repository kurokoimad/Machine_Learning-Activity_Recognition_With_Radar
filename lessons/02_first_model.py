"""Lesson 2: train a first model on the 88 hand-made features and evaluate it honestly.

What this script does:
  1. load the feature table (X = 88 numbers per recording, y = activity label)
  2. a "dumb" baseline: always predict the most frequent class
  3. a real model: standardise the features, then logistic regression
  4. evaluate it twice: once with a WRONG random split, once split by person
  5. save a confusion matrix of the honest evaluation

Run from the project root:  .venv/bin/python lessons/02_first_model.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, f1_score
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DATA = Path(__file__).resolve().parent.parent / "Radar-Startpaket"
META = ["datei", "kampagne", "person", "aktivitaet_nr", "aktivitaet", "wiederholung",
        "alter", "geschlecht", "umgebung", "dauer_s", "spektrogramm"]
NAMES = ["walk", "sit down", "stand up", "pick up", "drink", "fall"]

tab = pd.read_csv(DATA / "radar_merkmale.csv")
X = tab.drop(columns=META).to_numpy()   # (1754, 88): the inputs. dauer_s is excluded on purpose:
                                        # walking is the only 10/20 s activity, so it would give the answer away.
y = tab["aktivitaet_nr"].to_numpy()     # (1754,): the correct answers, 1..6
groups = tab["person"].to_numpy()       # who performed each recording
print(f"X {X.shape}, y {y.shape}, {len(np.unique(groups))} persons\n")

# A model = preprocessing + classifier, chained so both are fitted only on training data.
# StandardScaler: shift/scale every feature to mean 0, std 1 (features have very different units).
# LogisticRegression: learns one weight per feature and class; training = gradient-based
# minimisation of an error function (cross-entropy), exactly the idea from lecture 3.
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
baseline = DummyClassifier(strategy="most_frequent")

# Cross-validation: split the data into 5 parts, train on 4, test on the 5th, rotate.
# Every recording is predicted exactly once by a model that never saw it.
wrong_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)         # ignores persons
honest_cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=0)  # a person is only ever in one fold


def evaluate(name, estimator, cv):
    uses_groups = isinstance(cv, StratifiedGroupKFold)
    pred = cross_val_predict(estimator, X, y, cv=cv, groups=groups if uses_groups else None)
    acc = accuracy_score(y, pred)
    f1 = f1_score(y, pred, average="macro")  # mean F1 over classes: punishes ignoring the rare "fall" class
    print(f"{name:45s} accuracy {acc:6.1%}   macro-F1 {f1:6.1%}")
    return pred


evaluate("baseline (most frequent class), by person", baseline, honest_cv)
evaluate("logistic regression, RANDOM split (wrong)", model, wrong_cv)
pred = evaluate("logistic regression, split BY PERSON (honest)", model, honest_cv)

fig, ax = plt.subplots(figsize=(7, 6))
ConfusionMatrixDisplay.from_predictions(y, pred, display_labels=NAMES, normalize="true",
                                        values_format=".0%", cmap="Blues", ax=ax, colorbar=False)
ax.set_title("Logistic regression, 5-fold CV split by person\n(rows: true activity, normalised)")
out = Path(__file__).resolve().parent / "02_confusion_logreg.png"
fig.savefig(out, dpi=120, bbox_inches="tight")
print("\nsaved", out)
