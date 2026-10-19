# Project journal — Radar activity recognition

Running log of decisions and results. Every number here comes from a script in `lessons/`
and is reproducible with the pinned `requirements.txt`. The 6-page paper is written from this file.

## Roadmap

| Step | Topic | Paper section | Status |
|---|---|---|---|
| 0 | Environment setup (venv, libraries) | — | done |
| 1 | Look at the spectrograms | Data | done |
| 2 | First model on the 88 features, honest evaluation | Method, Results | done |
| 3 | Compare classifiers (k-NN, SVM, random forest), tune hyperparameters with nested CV | Method, Results | next |
| 4 | Dimensionality reduction: PCA / t-SNE of the features (lectures 2–3) | Data analysis | |
| 5 | Feature importance and selection: which of the 88 features matter? | Results | |
| 6 | CNN directly on the spectrograms (PyTorch) | Method, Results | |
| 7 | Robustness: train on some environments, test on others | Discussion | |
| 8 | Write the paper (Introduction, Related work, Data, Method, Results, Discussion) | all | |

## Dataset (for the "Data" section)

Source: Fioranelli et al., *Radar signatures of human activities*, University of Glasgow, 2019,
DOI 10.5525/gla.researchdata.848, CC BY 4.0. FMCW radar, 5.8 GHz.

- 1754 recordings, 105 persons (aged 21–98), 7 campaigns, 4 environments
  (lab 876, retirement home 301, senior centre 289, common room 288)
- 6 classes: walk 312, sit down 312, stand up 311, pick up 311, drink 310, **fall 198**
- Recordings per person: median 18 (min 4, max 36)
- Inputs: (a) 88 hand-crafted features from the middle 5-s window; (b) micro-Doppler
  spectrograms, 128 Doppler bins × 149/305/618 time frames
- No missing values in the features; features are not normalised.

Pitfalls found while exploring:

- **Duration gives the label away.** Walking is the only class recorded for 10/20 s, so
  `dauer_s` (and the raw spectrogram width) must not be used as input. For the CNN, crop every
  spectrogram to the same 5 s.
- **Falls are missing in two campaigns.** NGHomes has 3 falls, West Cumbria has 0 (elderly
  participants). So "environment" and "fall" are correlated, and per-environment results must be
  read with this in mind.
- Some spectrograms contain horizontal lines at about ±3 m/s (e.g. the fall of P36). These are
  probably interference, not body motion.

## Evaluation protocol (for the "Method" section)

- 5-fold cross-validation with `StratifiedGroupKFold`, grouped by `person`: no person appears
  in both training and test data, and class proportions are kept per fold. `random_state=0`.
- Metrics: accuracy and **macro-F1** (the mean F1 over the 6 classes). Macro-F1 matters because
  falls are the rarest and most important class.
- Preprocessing (standardisation) sits inside the pipeline, so it is fitted on training folds only.

## Results log

### Step 2 — first model (`lessons/02_first_model.py`)

| Model | Split | Accuracy | Macro-F1 |
|---|---|---|---|
| Majority class (baseline) | by person | 17.7 % | 8.6 % |
| Standardise + logistic regression | random (leaky) | 88.3 % | 88.8 % |
| Standardise + logistic regression | **by person** | **87.8 %** | **88.2 %** |
| 1-NN (standardised) | random / by person | 86.8 % / 85.0 % | — |
| Random forest, 300 trees | random / by person | 89.7 % / 88.9 % | — |

Observations:

- A linear model already reaches about 88 % on unseen persons, five times the baseline.
- The random split inflates accuracy by only 0.5–1.8 points on these features. This suggests the
  features carry little person-specific information. The person split stays mandatory, because the
  gap can be much larger for a CNN on raw spectrograms (to be checked in step 6).
- Confusion matrix (`lessons/02_confusion_logreg.png`): walk, sit down, stand up and fall are each
  recognised about 95 % of the time. **Pick up ↔ drink** is the main error (23 % / 19 % swapped). Both
  are slow upper-body movements of a standing person with little torso motion. This is the
  question for steps 5 and 6: which features or models separate these two?
