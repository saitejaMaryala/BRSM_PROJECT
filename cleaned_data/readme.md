# Cleaned Data Files

This folder contains the preprocessed outputs of the BRSM Movie Memory Experiment. The raw CSV logs of each participant have been aggregated into these files for easier metric calculation and statistical analysis.

There are two main files generated:

## 1. `cleaned_summary.csv`
This file acts as a **Participant-Level Summary**. Each row represents exactly **one participant**, aggregating all of their trials into single, overall scores.

### Columns:
* **`participant`**: The participant's unique Sub ID (e.g., `14.0`, `Sub41`).
* **`group`**: The experimental condition they were placed in. 
  * `NB` = Natural Cut (watched unaltered videos).
  * `AB` = Abrupt Cut (watched videos interrupted 1-5 seconds before a natural boundary).
* **`encoding_time_min`**: The total time (in minutes) they spent actively watching the videos before the recognition test.
* **`vigilance_pass`**: `True` or `False`. Indicates if the participant was paying attention based on the `THRESHOLD_MINUTES` configuration (if they took less than 27.05 minutes).
* **`accuracy`**: Their overall hit rate across all trials (e.g., `0.95` = 95%).
* **`mean_rt`**: Their average response time (in seconds) to make their choice during the recognition test.
* **`BB_accuracy`**: Their accuracy specifically on trials concerning "Before Boundary" (BB) frames (frames shown right before an event changed).
* **`EM_accuracy`**: Their accuracy specifically on "Event Middle" (EM) frames (frames taken from the middle of a continuous event).
* **`mean_confidence`**: Their average self-reported confidence score (on a scale of 1 to 5) across all answers.
* **`Age`, `Gender`, `Handedness`, `Vision`**: Demographic details matched and imported from `Demographic data.xlsx`.

---

## 2. `cleaned_trials.csv`
This file contains the **Trial-Level Data**. It is much larger because it contains **one row for every single image/question** that every participant answered. 

This file is necessary for running advanced statistical tests (e.g., ANOVAs or Reaction Time analysis) or for generating per-trial variance plots (like Box Plots), as you need to feed raw data into standard statistical models rather than using participant averages.

### Columns:
* **`participant`**: The participant's unique Sub ID.
* **`group`**: Their assigned condition (`NB` or `AB`).
* **`vigilance_pass`**: Whether they passed the vigilance check.
* **`target_type`**: The type of image shown for that specific question:
  * `BB` (Before Boundary image).
  * `EM` (Event Middle image). 
* **`correct`**: `1.0` if they selected the correct image; `0.0` if they fell for the Lure/Foil and made the wrong choice.
* **`rt`**: Their exact response time (in seconds) for that single question.
* **`confidence`**: The confidence rating (1 to 5) they gave for that specific answer.

---
*Note: In future steps (e.g., memory metric generation), extra calculated columns like Recognition Memory Index (REC) and Lure Discrimination Index (LDI) will be added to the output of this dataset.*
