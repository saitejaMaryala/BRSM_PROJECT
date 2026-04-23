# H1-H5 Test-Selection Context (Data Characteristics + Non-Parametric Results)

This file is intended as structured context for an LLM to decide which statistical test is most appropriate for each hypothesis.

## Dataset Fingerprint
- Source: participant-level files in data/individuals_cleaned
- Total participants: 166
- Between-subject groups:
  - NB (Natural cut): 87
  - AB (Abrupt cut): 79
- Per participant recognition trials: 40 (fixed)
  - BB frames: 20 (fixed)
  - EM frames: 20 (fixed)
- Confidence values available for all participants (no missing participant-level BB/EM means)

## Variable Characteristics Relevant for Test Choice
- condition/group: binary categorical (NB vs AB), between-subject
- target type: binary categorical (BB vs EM), within-subject (repeated within participant)
- resp.corr-derived accuracy:
  - trial-level binary (0/1)
  - participant-level summaries are percentages bounded in [0, 100]
  - bounded and often non-normal
- resp.rt-derived response time:
  - continuous positive, right-skew-prone
  - evaluated on correct trials in H1
- conf_radio.response-derived confidence:
  - Likert-style ordinal response (treated as numeric mean at participant level)
  - bounded, potentially non-normal
- Independence structure:
  - NB vs AB comparisons are independent samples
  - BB vs EM inside a participant are paired/repeated measures

## Hypothesis-Level Context for Test Selection

### H1
- Scientific question:
  - H1a: Is overall recognition accuracy higher in NB than AB?
  - H1b: Is response time faster in NB than AB?
- Data used:
  - Participant mean accuracy (%) by group
  - Participant median RT (correct trials) by group
- Design:
  - Independent groups (NB vs AB)
- Normality (Shapiro-Wilk):
  - Accuracy:
    - AB: W=0.9567, p=0.0091 (non-normal)
    - NB: W=0.9419, p=0.0007 (non-normal)
  - Median RT:
    - AB: W=0.8817, p<0.0001 (non-normal)
    - NB: W=0.9512, p=0.0025 (non-normal)
- Non-parametric test run:
  - Mann-Whitney U (two-sided)
- Results:
  - H1a accuracy: U=4254.50, p=0.0078, rank-biserial r=-0.2380
  - H1b median RT: U=3814.00, p=0.2228, rank-biserial r=-0.1099

### H2
- Scientific question:
  - Is BB-frame recognition accuracy higher in NB than AB?
- Data used:
  - Participant mean BB accuracy (%) by group
- Design:
  - Independent groups (NB vs AB)
- Normality (Shapiro-Wilk):
  - AB: W=0.9475, p=0.0027 (non-normal)
  - NB: W=0.9218, p=0.0001 (non-normal)
- Non-parametric test run:
  - Mann-Whitney U (two-sided)
- Results:
  - U=4192.50, p=0.0133, rank-biserial r=-0.2200

### H3
- Scientific question:
  - Is EM-frame recognition accuracy different between NB and AB?
- Data used:
  - Participant mean EM accuracy (%) by group
- Design:
  - Independent groups (NB vs AB)
- Normality (Shapiro-Wilk):
  - AB: W=0.9226, p=0.0001 (non-normal)
  - NB: W=0.9183, p<0.0001 (non-normal)
- Non-parametric test run:
  - Mann-Whitney U (two-sided)
- Results:
  - U=4087.50, p=0.0322, rank-biserial r=-0.1894

### H4
- Scientific question:
  - Interaction question on accuracy: Is the NB-vs-AB group difference larger for BB than for EM?
- Data used:
  - Within-participant difference score: DeltaAcc = BB_accuracy - EM_accuracy
  - Then compared DeltaAcc between NB and AB
- Design:
  - Mixed structure reduced to independent-group comparison on a paired-derived score
- Normality on DeltaAcc (Shapiro-Wilk):
  - NB: W=0.9663, p=0.02282 (non-normal)
  - AB: W=0.9677, p=0.04255 (non-normal)
- Non-parametric test run:
  - Mann-Whitney U on DeltaAcc (two-sided)
- Results:
  - U=3476.5, p=0.8971, rank-biserial r=-0.0116

### H5
- Scientific question:
  - Interaction question on confidence: Is the NB-vs-AB group difference larger for BB than for EM confidence?
- Data used:
  - Within-participant difference score: DeltaConf = BB_conf - EM_conf
  - Then compared DeltaConf between NB and AB
  - Also simple group comparisons for BB_conf and EM_conf separately
- Design:
  - Mixed structure reduced to independent-group comparison on a paired-derived score
- Normality on DeltaConf (Shapiro-Wilk):
  - NB: W=0.9800, p=0.1974 (approximately normal)
  - AB: W=0.9765, p=0.1529 (approximately normal)
- Non-parametric tests run:
  - Mann-Whitney U on DeltaConf (two-sided)
  - Mann-Whitney U for BB_conf (NB vs AB)
  - Mann-Whitney U for EM_conf (NB vs AB)
- Results:
  - Interaction (DeltaConf): U=4151.0, p=0.02085, r=-0.2079
  - BB_conf simple effect: U=4166.5, p=0.01826, r=-0.2124
  - EM_conf simple effect: U=3852.0, p=0.1793, r=-0.1209

## Compact Machine-Readable Summary

```yaml
sample:
  participants_total: 166
  groups: {NB: 87, AB: 79}
  trials_per_participant: 40
  bb_trials_per_participant: 20
  em_trials_per_participant: 20

h1:
  design: independent_groups
  outcomes: [accuracy_percent, median_rt_correct]
  normality: non_normal_for_both_groups_and_outcomes
  test_run: mann_whitney_u_two_sided
  results:
    accuracy: {U: 4254.50, p: 0.0078, r_rank_biserial: -0.2380}
    median_rt: {U: 3814.00, p: 0.2228, r_rank_biserial: -0.1099}

h2:
  design: independent_groups
  outcome: bb_accuracy_percent
  normality: non_normal_in_both_groups
  test_run: mann_whitney_u_two_sided
  result: {U: 4192.50, p: 0.0133, r_rank_biserial: -0.2200}

h3:
  design: independent_groups
  outcome: em_accuracy_percent
  normality: non_normal_in_both_groups
  test_run: mann_whitney_u_two_sided
  result: {U: 4087.50, p: 0.0322, r_rank_biserial: -0.1894}

h4:
  design: mixed_reduced_to_between_on_difference_score
  outcome: delta_acc_bb_minus_em
  normality: non_normal_in_both_groups
  test_run: mann_whitney_u_two_sided_on_delta
  result: {U: 3476.5, p: 0.8971, r_rank_biserial: -0.0116}

h5:
  design: mixed_reduced_to_between_on_difference_score
  outcome: delta_conf_bb_minus_em
  normality: approximately_normal_in_both_groups
  tests_run:
    interaction_delta: mann_whitney_u_two_sided
    bb_simple_effect: mann_whitney_u_two_sided
    em_simple_effect: mann_whitney_u_two_sided
  results:
    interaction_delta: {U: 4151.0, p: 0.02085, r_rank_biserial: -0.2079}
    bb_simple_effect: {U: 4166.5, p: 0.01826, r_rank_biserial: -0.2124}
    em_simple_effect: {U: 3852.0, p: 0.1793, r_rank_biserial: -0.1209}
```
