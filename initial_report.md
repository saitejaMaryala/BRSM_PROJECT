# Memory Encoding Across Event Boundaries: An Initial Analysis Report

## Executive Summary

This report presents an investigation into how disruptions in video continuity affect our ability to remember what we've seen. We test whether artificially interrupting videos at critical moments (event boundaries) impairs memory compared to watching videos with their natural flow. This research has implications for understanding how our brains organize and store memories in everyday life.

---

## 1. Introduction

### 1.1 Why This Matters

Imagine watching a movie where commercial breaks suddenly appear in the middle of important scenes versus during natural scene transitions. Which version would you remember better? This question is central to understanding how our brains build and store memories of continuous experiences.

Every day, our brains process streams of continuous information—watching videos, having conversations, or performing tasks. To make sense of this flow, our minds naturally break experiences into meaningful chunks called "events." The points where one event ends and another begins are called **event boundaries**. These boundaries play a crucial role in how we encode memories.

### 1.2 Research Context

This study builds on **Event Segmentation Theory (EST)**, a framework explaining how humans divide continuous experiences into discrete, meaningful events. According to this theory, our working memory maintains "event models" that help us predict what will happen next. When our predictions fail—such as when something unexpected occurs—we experience an update, creating an event boundary.

---

## 2. Literature Review and Theoretical Background

### 2.1 Event Segmentation Theory (Zacks et al., 2007)

Event Segmentation Theory proposes that people parse continuous flows of events into smaller, discrete units to make sense of them. The main principles include:

- **Event Models**: Our working memory maintains models that guide perceptual processing and remain stable across time
- **Prediction Errors**: When activity becomes less predictable, prediction errors increase, triggering updates to event models
- **Boundary Perception**: Event boundaries are perceived when transient changes in perceptual systems occur

**Key factors affecting event segmentation:**

- **Bottom-up processing**: Sensory cues that change with environmental or movement changes
- **Top-down processing**: Prior event schemas, goals, and plans

**Memory implications**: Abrupt disruptions from external cues may disrupt memory encoding because the event model fails to update properly. Boltz (1992) demonstrated that inserting advertisement breaks at natural event boundaries improved later recall, while breaks at non-boundaries impaired memory.

### 2.2 Event Horizon Model (Radvansky & Zacks, 2017)

The Event Horizon Model extends EST and describes how event representations are structured in memory. A critical principle is the **Boundary Advantage**:

- **Event boundaries serve as anchors in long-term memory (LTM)**
- Boundaries facilitate encoding because processing at boundaries is crucial for updating event models
- Benefits include improved encoding, recall during segmentation, and retention of boundary points in memory

**Evidence for boundary advantage:**

- Participants with less agreement on event boundaries performed poorer on memory tests
- Deleting time segments between events improves recall compared to deleting boundary segments (Schwan & Garsoffky, 2004)

### 2.3 Film Editing and Perceptual Manipulation (Cutting, Brunick, & Candan, 2012)

This study analyzed Hollywood films from 1940-2010 to understand what triggers event boundaries. Key findings:

- **Physical metrics** that trigger prediction errors include: shot dynamics, motion, luminance and color, space-time, and location
- Event boundaries were perceived primarily based on **bottom-up perceptual cues** rather than character goals or story
- Film editing introduces **abrupt cuts** between shots, forcing viewers' cognitive systems to update event models

This supports the hypothesis that perceptual manipulation generates prediction errors and creates event boundaries.

### 2.4 Boundary Objects in Memory (Swallow, Zacks & Abrams, 2009)

Three experiments examined how objects presented at event boundaries are encoded differently:

**Key findings:**

- Items present at the time of boundary perception were **better encoded**
- **Boundary objects** were recognized better than non-boundary objects
- The boundary advantage is even stronger **across** event boundaries

**Film editing implications**: When a film cuts to a new shot (e.g., actors carrying laundry down stairs—a change in activity and location), this creates a perceptual shift. Abrupt cuts trigger prediction failure, affecting memory encoding and leaving durable memory traces.

---

## 3. Experimental Design

### 3.1 Overview

This experiment comprised **two phases** involving **two independent participant groups**:

1. **Encoding Phase**: Participants watched short video clips
2. **Recognition Phase**: Participants identified previously seen frames

### 3.2 Stimuli Preparation

**Video Selection:**

- **40 short videos** selected from YouTube Shorts
- An independent group of annotators segmented videos by indicating **coarse-grained event boundaries** via key presses
- Event boundaries derived from temporal agreement across annotators

**Two Experimental Conditions:**

1. **Natural Cut (NB) Condition**: Videos ended at their original, uninterrupted timelines
2. **Abrupt Cut (AB) Condition**: Videos were subtly interrupted **1–5 seconds before a consensus event boundary** and resumed at a point corresponding to the onset of a new event context

**Duration Control**: Natural Cut video lengths were adjusted so their average duration matched that of Abrupt Cut videos.

### 3.3 Participants

- **Total participants**: 170 (171 data files available)
- **Abrupt Cut group**: 80 participants
- **Natural Cut group**: 90 participants
- **Note**: First 13 participants' data not available due to data error

### 3.4 Encoding Phase

- Participants viewed videos attentively
- **Vigilance check**: 5 videos were repeated; participants pressed spacebar to skip repeated clips
- Between-subjects design: Each participant saw either all Abrupt or all Natural videos

### 3.5 Recognition Phase

**Task structure:**

- On each trial, two frames from the same video were presented: one **target** (previously seen) and one **lure** (unseen)
- Participants selected which frame they had seen
- **Confidence rating**: 5-point scale (1 = not at all confident, 5 = very confident)

**Difficulty manipulation:**

- Similarity between targets and lures varied across three levels: easy, moderate, and difficult

**Frame types:**

- **Before Boundary (BB)**: Frames occurring 1-5 seconds before an event boundary
- **Event Middle (EM)**: Frames occurring between two boundaries (middle of an event)

---

## 4. Data Description

### 4.1 Data Files

Our dataset consists of:

1. **`abruptmovies.csv`** (46 rows): Video information for Abrupt Cut condition
   - Columns: `path`, `duration`, `is_repeat`
   - 40 unique videos + 5 repeated for vigilance

2. **`naturalmovies.csv`** (46 rows): Video information for Natural Cut condition
   - Columns: `path`, `duration`, `is_repeat`
   - 40 unique videos + 5 repeated for vigilance

3. **`target_and_lures.csv`** (41 rows): Frame pair information
   - Columns: `movie_id`, `target_img`, `lure_img`
   - Frame naming convention indicates type: `BB_T` (Before Boundary Target), `EM_T` (Event Middle Target), `L` (Lure)

4. **Individual participant files** (171 files): Trial-by-trial data for each participant
   - Naming convention: `sub[ID]_[AB/NB]_recognitionstage_[timestamp].csv`
   - 80 files for AB condition, 90 files for NB condition

### 4.2 Key Variables

**Performance Measures:**

- **`resp.corr`**: Whether identification was correct (1 = correct, 0 = incorrect)
- **`resp.rt`**: Response time in seconds during recognition
- **`conf_radio.response`**: Confidence rating (1-5 scale)

**Experimental Variables:**

- **Condition**: Abrupt Cut (AB) vs. Natural Cut (NB) [between-subjects]
- **Frame Type**: Before Boundary (BB) vs. Event Middle (EM) [within-subjects]
- **Difficulty**: Similarity level between target and lure (easy/moderate/difficult)

**Demographic Variables:**

- Age, gender, handedness, vision
- Caffeine consumption (last 2 hours)
- Alcohol/smoking (last 12 hours)

**Timing Variables:**

- Encoding phase duration (total time viewing videos)
- Recognition phase timing
- Response times for each trial

### 4.3 Data Quality Metrics

**Vigilance Criterion:**

- Time between `instruction_2.stopped` and `Videos.stopped` represents encoding duration
- Repeated videos account for 5.6 minutes
- Participants exceeding **27.05 minutes** during encoding were considered inattentive
- This accounts for 25 seconds per repeated video before being skipped

---

## 5. Research Hypotheses

### 5.1 Primary Hypotheses (From Experiment Design)

#### Hypothesis 1: Overall Recognition Performance

**H1a**: Participants who viewed **Natural Cut videos** will show **higher recognition accuracy** compared to those who viewed Abrupt Cut videos.

**Rationale**: Natural videos preserve event continuity, allowing proper event model updates. Abrupt cuts disrupt this process, impairing encoding.

**H1b**: Participants in the Natural Cut group will have **faster response times (RTs)** compared to the Abrupt Cut group.

**Rationale**: Better-encoded memories are retrieved more easily, resulting in faster responses.

#### Hypothesis 2: Boundary-Related Memory Effects

**H2**: Recognition accuracy for **Before Boundary (BB) frames** will be **higher in the Natural Cut group** than in the Abrupt Cut group.

**Rationale**: In Natural Cut videos, pre-boundary frames benefit from the natural boundary advantage. In Abrupt Cut videos, this advantage is disrupted by the artificial interruption.

#### Hypothesis 3: Event-Middle Frame Performance

**H3**: Recognition performance for **Event Middle (EM) frames** will **not differ significantly** between Natural Cut and Abrupt Cut groups.

**Rationale**: EM frames are less sensitive to boundary manipulations since they occur within stable event representations.

### 5.2 Additional Novel Hypotheses

#### Hypothesis 4: Interaction Between Condition and Frame Type

**H4**: There will be a **significant interaction** between Condition (AB vs. NB) and Frame Type (BB vs. EM), such that:

- The difference in accuracy between BB and EM frames will be larger in the NB condition
- In the AB condition, BB and EM performance will be more similar

**Rationale**: Disrupting the natural boundary should eliminate or reduce the boundary advantage, flattening the difference between frame types.

#### Hypothesis 5: Confidence-Accuracy Relationship

**H5a**: The correlation between confidence ratings and accuracy will be **stronger in the Natural Cut group** compared to the Abrupt Cut group.

**Rationale**: Better encoding leads to more reliable metacognitive monitoring.

**H5b**: For **correct responses**, confidence ratings will be **higher in the Natural Cut group**. For **incorrect responses**, confidence ratings will not differ between groups.

**Rationale**: Strong memories generate higher confidence; weak memories show similar low confidence regardless of cause.

#### Hypothesis 6: Response Time Patterns

**H6**: For **BB frames only**, response times will be **faster in the Natural Cut group**. For **EM frames**, response times will be similar across groups.

**Rationale**: The boundary advantage in natural videos facilitates faster retrieval specifically for boundary-related content.

#### Hypothesis 7: Difficulty Moderation

**H7**: The effect of Condition (AB vs. NB) on accuracy will be **moderated by difficulty level**, with larger condition differences for **difficult trials**.

**Rationale**: When discrimination is easy, ceiling effects may mask encoding differences. Difficult discriminations are more sensitive to encoding quality.

#### Hypothesis 8: Individual Differences

**H8**: Participants with higher overall vigilance (fewer skipped repeated videos, shorter encoding times) will show:

- Higher overall accuracy
- Smaller differences between AB and NB conditions (if they can overcome the disruption)

**Rationale**: Attention and engagement may buffer against encoding disruptions.

#### Hypothesis 9: Memory Indices

**H9a**: **Recognition Memory Index (REC)** will be higher in the Natural Cut group.

_REC = P("old" | Target) - P("old" | Foil)_

**H9b**: **Lure Discrimination Index (LDI)** will be higher in the Natural Cut group.

_LDI = P("similar" | Lure) - P("similar" | Foil)_

**Rationale**: Better encoding should improve both general recognition and fine-grained discrimination.

#### Hypothesis 10: Error Patterns

**H10**: In the Abrupt Cut group, **errors will be more common for BB frames** occurring immediately before the disruption compared to BB frames in the Natural Cut group.

**Rationale**: The abrupt cut specifically disrupts encoding at the pre-boundary moment.

---

## 6. Planned Analyses

### 6.1 Data Preprocessing

**Steps:**

1. **Quality Control**
   - Apply vigilance criterion (encoding time > 27.05 minutes = exclude)
   - Check for incomplete data or technical issues
   - Identify outliers (RTs > 3 SD from mean)
2. **Data Cleaning**
   - Remove practice trials if any
   - Handle missing values
   - Code frame types (BB vs. EM) from image filenames
3. **Variable Calculation**
   - Compute Recognition Memory Index (REC)
   - Compute Lure Discrimination Index (LDI)
   - Calculate mean accuracy, RT by condition and frame type
   - Create difficulty categorization if not explicit

4. **Data Aggregation**
   - Participant-level summaries
   - Trial-level data for mixed-effects models

### 6.2 Descriptive Statistics

**Planned tables and figures:**

1. **Participant Demographics** (by condition)
   - Age distribution
   - Gender breakdown
   - Handedness
   - Caffeine/alcohol consumption patterns

2. **Task Performance Overview**
   - Mean accuracy by condition
   - Mean RT by condition
   - Confidence ratings distribution
   - Vigilance check performance

3. **Stimulus Characteristics**
   - Video duration distribution (AB vs. NB)
   - Number of BB vs. EM frames
   - Frame type distribution across videos

### 6.3 Primary Statistical Analyses

#### Analysis 1: Overall Recognition Accuracy (H1a)

**Method**: Independent samples t-test (or Mann-Whitney U if non-normal)

- **IV**: Condition (AB vs. NB)
- **DV**: Overall recognition accuracy (proportion correct)
- **Expected outcome**: NB > AB

**Alternative**: Mixed-effects logistic regression with random intercepts for participants and videos

#### Analysis 2: Overall Response Time (H1b)

**Method**: Independent samples t-test on median RTs

- **IV**: Condition (AB vs. NB)
- **DV**: Median response time (seconds)
- **Expected outcome**: NB < AB

**Note**: Analyze correct trials only to avoid confounding accuracy with RT

#### Analysis 3: Condition × Frame Type Interaction (H2, H3, H4)

**Method**: 2×2 Mixed ANOVA

- **Between-subjects IV**: Condition (AB vs. NB)
- **Within-subjects IV**: Frame Type (BB vs. EM)
- **DV**: Recognition accuracy

**Planned comparisons:**

- NB_BB vs. AB_BB (test H2)
- NB_EM vs. AB_EM (test H3)
- Interaction contrast (test H4)

**Advanced alternative**: Mixed-effects logistic regression

```
accuracy ~ Condition * FrameType + (1 + FrameType | Participant) + (1 | Video)
```

#### Analysis 4: Confidence-Accuracy Relationship (H5)

**Method**:

- Calculate point-biserial correlations between confidence (1-5) and accuracy (0/1) for each participant
- Compare correlation magnitudes across conditions using Fisher's Z transformation
- Analyze confidence ratings separately for correct vs. incorrect trials (2×2 ANOVA)

#### Analysis 5: Frame-Type Specific RT Analysis (H6)

**Method**: 2×2 Mixed ANOVA on response times (correct trials only)

- **Between**: Condition (AB vs. NB)
- **Within**: Frame Type (BB vs. EM)
- **Expected**: Significant interaction with NB showing RT advantage for BB frames specifically

#### Analysis 6: Difficulty as Moderator (H7)

**Method**: 2×3 Mixed ANOVA

- **Between**: Condition (AB vs. NB)
- **Within**: Difficulty (Easy / Moderate / Difficult)
- **DV**: Accuracy
- **Expected**: Condition × Difficulty interaction

**Follow-up**: Simple effects of Condition at each Difficulty level

#### Analysis 7: Vigilance and Individual Differences (H8)

**Method**:

- Compute vigilance index (number of repeated videos skipped, encoding duration)
- Regression analysis: Accuracy ~ Condition \* Vigilance
- Test whether vigilance moderates condition effects

#### Analysis 8: Memory Indices (H9)

**Method**: Independent samples t-tests

- Compare REC values between AB and NB groups
- Compare LDI values between AB and NB groups
- **Note**: Requires identification of foils in the data

#### Analysis 9: Error Pattern Analysis (H10)

**Method**:

- Within AB group: Compare error rates for BB vs. EM frames
- Between groups: Compare BB error rates specifically
- Chi-square or logistic regression for categorical outcomes

### 6.4 Exploratory Analyses

1. **Video-level variability**: Some videos may be more memorable than others
   - Variance components analysis
   - Identify specific videos driving effects

2. **Temporal dynamics**: Does performance change over the recognition test?
   - Trial number as a covariate or moderator
   - Fatigue or learning effects

3. **Confidence calibration curves**
   - Plot accuracy as a function of confidence rating
   - Compare calibration between groups

4. **Response time distributions**
   - Examine RT distribution shapes (ex-Gaussian analysis)
   - Identify fast guesses vs. slow deliberations

5. **Demographics effects**
   - Age, gender, caffeine consumption as covariates
   - Exploratory subgroup analyses

### 6.5 Multiple Comparisons Correction

Given the multiple hypotheses and planned comparisons, we will control for Type I error using:

#### Primary Hypotheses (H1-H3)

**Method**: **Bonferroni-Holm correction** for the family of 3 primary tests

- More conservative but protects against false discoveries
- Maintains familywise error rate at α = .05

#### Secondary/Novel Hypotheses (H4-H10)

**Method**: **False Discovery Rate (FDR) control** using Benjamini-Hochberg procedure

- Controls expected proportion of false discoveries
- Less conservative than Bonferroni, appropriate for exploratory analyses
- Set FDR at q = .05

#### Within-Hypothesis Comparisons

**Method**: Planned contrasts with **no correction** when:

- Comparisons are orthogonal
- Directly test a priori hypotheses
- Example: Simple effects within a significant interaction

**Method**: Tukey's HSD when:

- Conducting post-hoc pairwise comparisons
- Multiple levels of a factor require comparison
- Example: Comparing all difficulty levels pairwise

#### Mixed-Effects Models

**Method**: No correction for fixed effects

- Each parameter tests a distinct hypothesis
- Conservative enough due to model complexity
- Use Type III tests for interaction terms

#### Reporting Strategy

We will report:

1. **Uncorrected p-values** for all tests
2. **Corrected p-values** or adjusted α thresholds
3. **Effect sizes** (Cohen's d, η², odds ratios) with 95% confidence intervals
4. Clear distinction between confirmatory and exploratory analyses

**Rationale**: This approach balances:

- Protection against false positives (Bonferroni for primary tests)
- Statistical power (FDR for secondary tests)
- Transparency (reporting both corrected and uncorrected values)

---

## 7. Descriptive Statistics Results

### 7.1 Participant Characteristics

**[TO DO: Insert Table 1 - Demographic Summary by Condition]**

| Variable                  | Natural Cut (N=90) | Abrupt Cut (N=80) | Test Statistic | p-value |
| ------------------------- | ------------------ | ----------------- | -------------- | ------- |
| Age (years), M (SD)       | [TBD]              | [TBD]             | t = [TBD]      | [TBD]   |
| Gender (% female)         | [TBD]%             | [TBD]%            | χ² = [TBD]     | [TBD]   |
| Handedness (% right)      | [TBD]%             | [TBD]%            | χ² = [TBD]     | [TBD]   |
| Caffeine in 2h (% yes)    | [TBD]%             | [TBD]%            | χ² = [TBD]     | [TBD]   |
| Alcohol/smoke 12h (% yes) | [TBD]%             | [TBD]%            | χ² = [TBD]     | [TBD]   |

**Interpretation note**: We will verify that groups are balanced on demographic variables. Any significant differences will be controlled for in subsequent analyses.

---

**[TO DO: Insert Figure 1 - Age Distribution by Condition]**

- Histogram or density plot comparing age distributions
- Visual check for balance between conditions

---

### 7.2 Vigilance and Data Quality

**[TO DO: Insert Table 2 - Vigilance Metrics]**

| Metric                                   | Natural Cut | Abrupt Cut | Total  |
| ---------------------------------------- | ----------- | ---------- | ------ |
| Mean encoding time (min), M (SD)         | [TBD]       | [TBD]      | [TBD]  |
| N exceeding 27.05 min threshold          | [TBD]       | [TBD]      | [TBD]  |
| % retained after exclusion               | [TBD]%      | [TBD]%     | [TBD]% |
| Mean repeated videos skipped, M (SD)     | [TBD]       | [TBD]      | [TBD]  |
| Recognition phase duration (min), M (SD) | [TBD]       | [TBD]      | [TBD]  |

**Interpretation note**: Participants with encoding times > 27.05 minutes will be excluded from primary analyses but may be examined separately as a low-vigilance subgroup.

---

### 7.3 Stimulus Characteristics

**[TO DO: Insert Table 3 - Video Duration Summary]**

| Condition            | N videos | Mean duration (s) | SD    | Min   | Max   |
| -------------------- | -------- | ----------------- | ----- | ----- | ----- |
| Natural Cut (unique) | 40       | [TBD]             | [TBD] | [TBD] | [TBD] |
| Abrupt Cut (unique)  | 40       | [TBD]             | [TBD] | [TBD] | [TBD] |
| Repeated videos      | 5        | [TBD]             | [TBD] | [TBD] | [TBD] |

**Note**: Durations should be similar between conditions by design. Statistical test will confirm no systematic difference.

---

**[TO DO: Insert Figure 2 - Video Duration Distributions]**

- Box plots or violin plots comparing duration distributions
- Verification of duration matching between conditions

---

**[TO DO: Insert Table 4 - Frame Type Distribution]**

| Frame Type           | N targets | Percentage |
| -------------------- | --------- | ---------- |
| Before Boundary (BB) | [TBD]     | [TBD]%     |
| Event Middle (EM)    | [TBD]     | [TBD]%     |
| Total                | 40        | 100%       |

**Note**: Extract frame types from `target_and_lures.csv` based on filename patterns (\_BB_T vs. \_EM_T).

---

### 7.4 Overall Task Performance

**[TO DO: Insert Table 5 - Recognition Performance Summary]**

| Measure                  | Natural Cut | Abrupt Cut | Difference | Effect Size (Cohen's d) |
| ------------------------ | ----------- | ---------- | ---------- | ----------------------- |
| Mean accuracy, M (SD)    | [TBD]       | [TBD]      | [TBD]      | [TBD]                   |
| Median RT (s), Mdn (IQR) | [TBD]       | [TBD]      | [TBD]      | [TBD]                   |
| Mean confidence, M (SD)  | [TBD]       | [TBD]      | [TBD]      | [TBD]                   |

---

**[TO DO: Insert Figure 3 - Recognition Accuracy by Condition]**

- Bar plot with error bars (95% CI or SE)
- Individual participant points overlaid to show distribution

---

**[TO DO: Insert Figure 4 - Response Time Distribution by Condition]**

- Density plots or violin plots
- Separate panels for correct vs. incorrect trials

---

**[TO DO: Insert Figure 5 - Confidence Rating Distribution]**

- Histogram or bar chart showing distribution of confidence ratings (1-5)
- Separate panels for Natural Cut vs. Abrupt Cut
- Further separated by correct vs. incorrect responses

---

### 7.5 Performance by Frame Type

**[TO DO: Insert Table 6 - Accuracy by Condition and Frame Type]**

| Frame Type           | Natural Cut M (SD) | Abrupt Cut M (SD) | Within-NB Diff | Within-AB Diff |
| -------------------- | ------------------ | ----------------- | -------------- | -------------- |
| Before Boundary (BB) | [TBD]              | [TBD]             | -              | -              |
| Event Middle (EM)    | [TBD]              | [TBD]             | -              | -              |
| BB - EM difference   | [TBD]              | [TBD]             | [TBD]          | [TBD]          |

**Interpretation note**: Look for the predicted interaction pattern where Natural Cut shows a BB advantage but Abrupt Cut does not.

---

**[TO DO: Insert Figure 6 - Interaction Plot: Condition × Frame Type]**

- Line plot showing accuracy for BB and EM frames
- Separate lines for Natural Cut vs. Abrupt Cut
- Error bars representing 95% CI

---

**[TO DO: Insert Table 7 - Response Time by Condition and Frame Type]**

| Frame Type           | Natural Cut Mdn (IQR) | Abrupt Cut Mdn (IQR) |
| -------------------- | --------------------- | -------------------- |
| Before Boundary (BB) | [TBD]                 | [TBD]                |
| Event Middle (EM)    | [TBD]                 | [TBD]                |

---

**[TO DO: Insert Figure 7 - Response Time by Condition and Frame Type]**

- Violin plots or box plots
- Correct trials only

---

### 7.6 Performance by Difficulty Level

**[TO DO: Insert Table 8 - Accuracy by Difficulty and Condition]**

| Difficulty | Natural Cut M (SD) | Abrupt Cut M (SD) | Condition Difference |
| ---------- | ------------------ | ----------------- | -------------------- |
| Easy       | [TBD]              | [TBD]             | [TBD]                |
| Moderate   | [TBD]              | [TBD]             | [TBD]                |
| Difficult  | [TBD]              | [TBD]             | [TBD]                |

**Note**: Difficulty levels may need to be inferred from the data or may be explicitly coded. Check data structure.

---

**[TO DO: Insert Figure 8 - Difficulty Moderation Effect]**

- Line plot showing accuracy across difficulty levels
- Separate lines for Natural Cut vs. Abrupt Cut
- Test whether lines converge or diverge

---

### 7.7 Confidence and Metacognition

**[TO DO: Insert Table 9 - Confidence by Accuracy and Condition]**

| Condition   | Correct M (SD) | Incorrect M (SD) | Difference |
| ----------- | -------------- | ---------------- | ---------- |
| Natural Cut | [TBD]          | [TBD]            | [TBD]      |
| Abrupt Cut  | [TBD]          | [TBD]            | [TBD]      |

---

**[TO DO: Insert Figure 9 - Confidence Calibration Curves]**

- Scatter plot: Confidence rating (x-axis) vs. Accuracy (y-axis)
- Separate panels or colors for Natural Cut vs. Abrupt Cut
- Perfect calibration line (diagonal) for reference

---

**[TO DO: Insert Table 10 - Confidence-Accuracy Correlation]**

| Condition       | Point-biserial r | 95% CI | p-value |
| --------------- | ---------------- | ------ | ------- |
| Natural Cut     | [TBD]            | [TBD]  | [TBD]   |
| Abrupt Cut      | [TBD]            | [TBD]  | [TBD]   |
| Fisher's Z test | -                | -      | [TBD]   |

---

### 7.8 Memory Indices

**[TO DO: Calculate and Report Memory Indices]**

**Recognition Memory Index (REC):**

- Formula: REC = P("old" | Target) - P("old" | Foil)
- Natural Cut: [TBD]
- Abrupt Cut: [TBD]
- t-test result: t([df]) = [TBD], p = [TBD], d = [TBD]

**Lure Discrimination Index (LDI):**

- Formula: LDI = P("similar" | Lure) - P("similar" | Foil)
- Natural Cut: [TBD]
- Abrupt Cut: [TBD]
- t-test result: t([df]) = [TBD], p = [TBD], d = [TBD]

**Note**: Identify foils in dataset (frames never shown during encoding) to calculate these indices.

---

## 8. Inferential Statistics Results

### 8.1 Primary Hypothesis Tests

#### H1a: Overall Recognition Accuracy

**[TO DO: Conduct independent samples t-test]**

- **Test**: Independent samples t-test (two-tailed)
- **IV**: Condition (Natural Cut vs. Abrupt Cut)
- **DV**: Overall recognition accuracy (proportion correct)

**Results**:

- Natural Cut: M = [TBD], SD = [TBD], N = [TBD]
- Abrupt Cut: M = [TBD], SD = [TBD], N = [TBD]
- t([df]) = [TBD], p = [TBD], d = [TBD], 95% CI [TBD, TBD]
- **Corrected α** (Bonferroni-Holm): [TBD]
- **Decision**: [Reject/Fail to reject] H0

**Interpretation**: [TO DO: Interpret whether Natural Cut group showed significantly higher accuracy than Abrupt Cut group, and discuss magnitude of effect]

---

#### H1b: Overall Response Time

**[TO DO: Conduct independent samples t-test on median RTs]**

- **Test**: Independent samples t-test on median response times (correct trials only)
- **IV**: Condition (Natural Cut vs. Abrupt Cut)
- **DV**: Median response time (seconds)

**Results**:

- Natural Cut: Mdn = [TBD], IQR = [TBD], N = [TBD]
- Abrupt Cut: Mdn = [TBD], IQR = [TBD], N = [TBD]
- t([df]) = [TBD], p = [TBD], d = [TBD], 95% CI [TBD, TBD]
- **Corrected α** (Bonferroni-Holm): [TBD]
- **Decision**: [Reject/Fail to reject] H0

**Interpretation**: [TO DO: Interpret whether Natural Cut group showed faster response times than Abrupt Cut group]

---

#### H2 & H3: Condition × Frame Type Interaction

**[TO DO: Conduct 2×2 Mixed ANOVA]**

- **Design**: 2 (Condition: NB vs. AB) × 2 (Frame Type: BB vs. EM) Mixed ANOVA
- **Between-subjects**: Condition
- **Within-subjects**: Frame Type
- **DV**: Recognition accuracy

**Main Effects**:

1. **Condition**: F([df1], [df2]) = [TBD], p = [TBD], η²p = [TBD]
2. **Frame Type**: F([df1], [df2]) = [TBD], p = [TBD], η²p = [TBD]

**Interaction Effect**:

- **Condition × Frame Type**: F([df1], [df2]) = [TBD], p = [TBD], η²p = [TBD]
- **Corrected α** (Bonferroni-Holm for primary family): [TBD]
- **Decision**: [Significant/Non-significant] interaction

**Planned Comparisons**:

1. **H2 Test**: BB frames, Natural Cut vs. Abrupt Cut
   - NB_BB: M = [TBD], SD = [TBD]
   - AB_BB: M = [TBD], SD = [TBD]
   - t([df]) = [TBD], p = [TBD], d = [TBD]
   - **Decision**: [TO DO]

2. **H3 Test**: EM frames, Natural Cut vs. Abrupt Cut
   - NB_EM: M = [TBD], SD = [TBD]
   - AB_EM: M = [TBD], SD = [TBD]
   - t([df]) = [TBD], p = [TBD], d = [TBD]
   - **Decision**: [TO DO]

3. **Within Natural Cut**: BB vs. EM
   - t([df]) = [TBD], p = [TBD], d = [TBD]

4. **Within Abrupt Cut**: BB vs. EM
   - t([df]) = [TBD], p = [TBD], d = [TBD]

**Interpretation**: [TO DO: Describe the pattern of results and whether they support the boundary advantage hypothesis]

---

**[TO DO: Insert Figure 10 - Interaction Plot with Statistical Annotations]**

- Include significance markers (\* p < .05, ** p < .01, \*** p < .001)
- Show pairwise comparison results

---

### 8.2 Secondary Hypothesis Tests

#### H4: Interaction Effect (Confirmatory Test)

**[TO DO: Test interaction contrast]**

This was tested in the mixed ANOVA above. The specific contrast of interest:

- (NB_BB - NB_EM) - (AB_BB - AB_EM)
- Contrast value = [TBD]
- SE = [TBD]
- t([df]) = [TBD], p = [TBD]
- **FDR-corrected p-value**: [TBD]

---

#### H5: Confidence-Accuracy Relationship

**[TO DO: Compare correlations between groups]**

**H5a**: Correlation strength comparison

- Natural Cut r = [TBD], Abrupt Cut r = [TBD]
- Fisher's Z transformation: Z = [TBD], p = [TBD]
- **FDR-corrected p-value**: [TBD]
- **Decision**: [TO DO]

**H5b**: Confidence ratings by accuracy and condition

**[TO DO: Conduct 2×2 Mixed ANOVA]**

- **Between**: Condition (NB vs. AB)
- **Within**: Accuracy (Correct vs. Incorrect)
- **DV**: Confidence rating

**Results**:

- Main effect of Condition: F([df1], [df2]) = [TBD], p = [TBD], η²p = [TBD]
- Main effect of Accuracy: F([df1], [df2]) = [TBD], p = [TBD], η²p = [TBD]
- Interaction: F([df1], [df2]) = [TBD], p = [TBD], η²p = [TBD]
- **FDR-corrected p-values**: [TBD]

**Simple effects for correct responses**:

- NB: M = [TBD], AB: M = [TBD]
- t([df]) = [TBD], p = [TBD], d = [TBD]

**Simple effects for incorrect responses**:

- NB: M = [TBD], AB: M = [TBD]
- t([df]) = [TBD], p = [TBD], d = [TBD]

---

#### H6: Frame-Type Specific RT Effects

**[TO DO: Conduct 2×2 Mixed ANOVA on RT]**

- **Between**: Condition (NB vs. AB)
- **Within**: Frame Type (BB vs. EM)
- **DV**: Response time (correct trials only)

**Results**:

- Main effect of Condition: F([df1], [df2]) = [TBD], p = [TBD], η²p = [TBD]
- Main effect of Frame Type: F([df1], [df2]) = [TBD], p = [TBD], η²p = [TBD]
- Interaction: F([df1], [df2]) = [TBD], p = [TBD], η²p = [TBD]
- **FDR-corrected p-values**: [TBD]

**Simple effects**:

- BB frames: NB vs. AB, t([df]) = [TBD], p = [TBD], d = [TBD]
- EM frames: NB vs. AB, t([df]) = [TBD], p = [TBD], d = [TBD]

---

#### H7: Difficulty as Moderator

**[TO DO: Conduct 2×3 Mixed ANOVA]**

- **Between**: Condition (NB vs. AB)
- **Within**: Difficulty (Easy / Moderate / Difficult)
- **DV**: Accuracy

**Results**:

- Main effect of Condition: F([df1], [df2]) = [TBD], p = [TBD], η²p = [TBD]
- Main effect of Difficulty: F([df1], [df2]) = [TBD], p = [TBD], η²p = [TBD]
- Interaction: F([df1], [df2]) = [TBD], p = [TBD], η²p = [TBD]
- **FDR-corrected p-values**: [TBD]

**Simple effects of Condition at each Difficulty level**:

1. Easy: t([df]) = [TBD], p = [TBD], d = [TBD]
2. Moderate: t([df]) = [TBD], p = [TBD], d = [TBD]
3. Difficult: t([df]) = [TBD], p = [TBD], d = [TBD]

---

#### H8: Vigilance as Moderator

**[TO DO: Conduct regression analysis]**

**Model**: Accuracy ~ Condition + Vigilance + Condition × Vigilance

**Results**:

- Condition (β = [TBD], SE = [TBD], t = [TBD], p = [TBD])
- Vigilance (β = [TBD], SE = [TBD], t = [TBD], p = [TBD])
- Condition × Vigilance (β = [TBD], SE = [TBD], t = [TBD], p = [TBD])
- R² = [TBD], Adjusted R² = [TBD]
- **FDR-corrected p-values**: [TBD]

**Interpretation**: [TO DO: Determine whether vigilance buffers the negative effect of abrupt cuts]

---

#### H9: Memory Indices

**[TO DO: Compare REC and LDI between conditions]**

**REC (Recognition Memory Index)**:

- Independent samples t-test
- t([df]) = [TBD], p = [TBD], d = [TBD], 95% CI [TBD, TBD]
- **FDR-corrected p-value**: [TBD]

**LDI (Lure Discrimination Index)**:

- Independent samples t-test
- t([df]) = [TBD], p = [TBD], d = [TBD], 95% CI [TBD, TBD]
- **FDR-corrected p-value**: [TBD]

---

#### H10: Error Patterns

**[TO DO: Analyze error rates for BB frames]**

**Within Abrupt Cut group**:

- BB error rate: [TBD]%
- EM error rate: [TBD]%
- McNemar's test or paired t-test: [TBD]

**Between groups (BB frames only)**:

- Natural Cut BB error rate: [TBD]%
- Abrupt Cut BB error rate: [TBD]%
- Chi-square or independent t-test: [TBD]
- **FDR-corrected p-value**: [TBD]

---

### 8.3 Summary of Hypothesis Testing Results

**[TO DO: Create summary table of all hypothesis tests]**

| Hypothesis            | Test       | Result | Corrected p | Effect Size | Support          |
| --------------------- | ---------- | ------ | ----------- | ----------- | ---------------- |
| H1a: NB > AB accuracy | t-test     | [TBD]  | [TBD]       | d = [TBD]   | [Yes/No/Partial] |
| H1b: NB < AB RT       | t-test     | [TBD]  | [TBD]       | d = [TBD]   | [Yes/No/Partial] |
| H2: NB_BB > AB_BB     | Contrast   | [TBD]  | [TBD]       | d = [TBD]   | [Yes/No/Partial] |
| H3: NB_EM ≈ AB_EM     | Contrast   | [TBD]  | [TBD]       | d = [TBD]   | [Yes/No/Partial] |
| H4: Interaction       | ANOVA      | [TBD]  | [TBD]       | η²p = [TBD] | [Yes/No/Partial] |
| H5a: r_NB > r_AB      | Fisher Z   | [TBD]  | [TBD]       | -           | [Yes/No/Partial] |
| H5b: Conf by Acc×Cond | ANOVA      | [TBD]  | [TBD]       | η²p = [TBD] | [Yes/No/Partial] |
| H6: RT interaction    | ANOVA      | [TBD]  | [TBD]       | η²p = [TBD] | [Yes/No/Partial] |
| H7: Difficulty mod    | ANOVA      | [TBD]  | [TBD]       | η²p = [TBD] | [Yes/No/Partial] |
| H8: Vigilance mod     | Regression | [TBD]  | [TBD]       | β = [TBD]   | [Yes/No/Partial] |
| H9a: REC              | t-test     | [TBD]  | [TBD]       | d = [TBD]   | [Yes/No/Partial] |
| H9b: LDI              | t-test     | [TBD]  | [TBD]       | d = [TBD]   | [Yes/No/Partial] |
| H10: BB errors        | Chi-square | [TBD]  | [TBD]       | OR = [TBD]  | [Yes/No/Partial] |

---

## 9. Exploratory Analyses Results

### 9.1 Video-Level Variability

**[TO DO: Examine which videos are most/least memorable]**

**Approach**:

- Calculate mean accuracy for each video across participants
- Identify videos with highest/lowest recognition rates
- Test whether video effects are consistent across conditions

**[TO DO: Insert Figure 11 - Video-Level Recognition Rates]**

- Forest plot or bar chart showing accuracy for each video
- Error bars representing 95% CI
- Videos ranked from most to least memorable

**Variance components analysis**:

- Participant variance: [TBD]%
- Video variance: [TBD]%
- Residual variance: [TBD]%

**Interpretation**: [TO DO: Discuss whether certain videos consistently show better/worse memory across conditions, or whether effects are condition-specific]

---

### 9.2 Temporal Dynamics

**[TO DO: Examine performance changes over the recognition test]**

**Approach**:

- Divide recognition test into blocks (e.g., first third, middle third, last third)
- Test for linear or quadratic trends

**[TO DO: Insert Figure 12 - Accuracy Over Time]**

- Line plot: Trial number (x-axis) vs. Accuracy (y-axis)
- Separate lines for Natural Cut vs. Abrupt Cut
- Loess smoothing to visualize trends

**Analysis**:

- Mixed ANOVA: Condition × Block
- Linear trend test
- Results: [TBD]

**Interpretation**: [TO DO: Determine whether participants show fatigue effects, learning effects, or stable performance]

---

### 9.3 Confidence Calibration

**[TO DO: Generate calibration curves]**

**[TO DO: Insert Figure 13 - Confidence Calibration Curves (Expanded)]**

- X-axis: Confidence rating (1-5)
- Y-axis: Proportion correct
- Separate panels for Natural Cut vs. Abrupt Cut
- Diagonal line representing perfect calibration
- Data points sized by number of trials

**Calibration statistics**:

- Brier score (Natural Cut): [TBD]
- Brier score (Abrupt Cut): [TBD]
- Over/underconfidence index: [TBD]

**Interpretation**: [TO DO: Discuss whether participants are well-calibrated and whether this differs by condition]

---

### 9.4 Response Time Distributional Analysis

**[TO DO: Examine RT distribution characteristics]**

**Approach**:

- Fit ex-Gaussian distributions to RT data (separately by condition)
- Compare distribution parameters (μ, σ, τ)

**[TO DO: Insert Figure 14 - RT Distribution Parameters]**

- Compare μ (Gaussian mean), σ (Gaussian SD), and τ (exponential component) between conditions

**Results**:

- Natural Cut: μ = [TBD], σ = [TBD], τ = [TBD]
- Abrupt Cut: μ = [TBD], σ = [TBD], τ = [TBD]
- Statistical comparisons: [TBD]

**Interpretation**: [TO DO: Discuss whether condition affects the typical response speed (μ), consistency (σ), or presence of slow outliers (τ)]

---

### 9.5 Demographic and State Variables

**[TO DO: Test demographic variables as covariates]**

**Age effects**:

- Correlation with accuracy: r = [TBD], p = [TBD]
- Interaction with Condition: [TBD]

**Gender effects**:

- Main effect: F([df]) = [TBD], p = [TBD]
- Interaction with Condition: [TBD]

**Caffeine effects**:

- Caffeine vs. No caffeine accuracy: [TBD]
- Interaction with Condition: [TBD]

**[TO DO: Insert Figure 15 - Exploratory Covariate Effects]**

- Panel plot showing key demographic effects

**Interpretation**: [TO DO: Identify any demographic or state variables that significantly predict memory performance or interact with experimental condition]

---

### 9.6 Additional Patterns and Observations

**[TO DO: Report any unexpected or noteworthy patterns observed in the data]**

Examples to check:

- Order effects (were certain videos always shown early/late?)
- Practice effects within the recognition test
- Specific video features associated with better memory
- Outlier participants or trials
- Non-linearities in relationships

---

## 10. Visualizations Summary

### Planned Figures

1. **Figure 1**: Age distribution by condition
2. **Figure 2**: Video duration distributions
3. **Figure 3**: Recognition accuracy by condition (bar plot)
4. **Figure 4**: Response time distributions
5. **Figure 5**: Confidence rating distributions
6. **Figure 6**: Condition × Frame Type interaction (line plot)
7. **Figure 7**: Response time by condition and frame type
8. **Figure 8**: Difficulty moderation effect
9. **Figure 9**: Confidence calibration curves
10. **Figure 10**: Interaction plot with statistical annotations
11. **Figure 11**: Video-level recognition rates
12. **Figure 12**: Accuracy over time (temporal dynamics)
13. **Figure 13**: Expanded calibration curves
14. **Figure 14**: RT distribution parameters
15. **Figure 15**: Exploratory covariate effects

**Note**: All figures will include:

- Clear axis labels with units
- Legends where applicable
- Error bars (95% CI or SE, specified in caption)
- Color-blind friendly palettes
- High-resolution exports for publication

---

## 11. Discussion and Interpretation

### 11.1 Summary of Key Findings

**[TO DO: Synthesize main results]**

This section will summarize:

1. Whether abrupt cuts impaired overall memory performance (H1)
2. Whether the boundary advantage was disrupted by abrupt cuts (H2)
3. Whether event-middle frames were unaffected (H3)
4. Which secondary hypotheses were supported
5. Notable exploratory findings

---

### 11.2 Theoretical Implications

**[TO DO: Connect findings to Event Segmentation Theory]**

Discuss how results:

- Support or challenge EST predictions
- Inform understanding of event boundaries in memory
- Relate to boundary advantage (or lack thereof)
- Connect to prediction error frameworks

---

### 11.3 Practical Implications

**[TO DO: Discuss real-world applications]**

Potential applications:

- Film editing and media production
- Educational video design
- Commercial placement in media
- User experience design for video platforms
- Advertising effectiveness

---

### 11.4 Limitations

**[TO DO: Identify study limitations]**

Consider:

1. **Sample characteristics**: Online sample, specific demographics
2. **Stimulus characteristics**: YouTube Shorts, limited video types
3. **Boundary identification**: Reliance on annotator agreement
4. **Timing of cuts**: 1-5 second window may vary in impact
5. **Recognition test format**: Forced-choice may not capture all memory aspects
6. **Lack of baseline**: No condition with no boundaries at all
7. **Generalizability**: Short social media videos may not generalize to other contexts

---

### 11.5 Future Directions

**[TO DO: Propose follow-up studies]**

Potential future research:

1. Vary timing of abrupt cuts (immediately before vs. slightly before boundary)
2. Test recall measures in addition to recognition
3. Include physiological measures (eye-tracking, pupillometry, EEG)
4. Manipulate boundary strength (weak vs. strong boundaries)
5. Test with longer-form content (movies, lectures)
6. Examine individual differences in event segmentation ability
7. Investigate neural correlates using fMRI or EEG
8. Test interventions to reduce disruption effects

---

## 12. Conclusions

**[TO DO: Provide concluding statements]**

Final concluding remarks will:

- Restate the research question and approach
- Summarize whether hypotheses were supported
- Emphasize the most important theoretical contribution
- Note practical relevance
- Provide a forward-looking statement about the implications for understanding memory and event perception

---

## 13. References

Boltz, M. (1992). Temporal accent structure and the remembering of filmed narratives. _Journal of Experimental Psychology: Human Perception and Performance_, _18_(1), 90–105.

Cutting, J. E., Brunick, K. L., & Candan, A. (2012). Perceiving event dynamics and parsing Hollywood films. _Journal of Experimental Psychology: Human Perception and Performance_, _38_(6), 1476–1490.

Radvansky, G. A., & Zacks, J. M. (2017). Event boundaries in memory and cognition. _Current Opinion in Behavioral Sciences_, _17_, 133–140. https://doi.org/10.1016/j.cobeha.2017.08.006

Schwan, S., & Garsoffky, B. (2004). The cognitive representation of filmic event summaries. _Applied Cognitive Psychology_, _18_(1), 37–55.

Swallow, K. M., Zacks, J. M., & Abrams, R. A. (2009). Event boundaries in perception affect memory encoding and updating. _Journal of Experimental Psychology: General_, _138_(2), 236–257. https://doi.org/10.1037/a0015631

Zacks, J. M., Speer, N. K., Swallow, K. M., Braver, T. S., & Reynolds, J. R. (2007). Event perception: A mind-brain perspective. _Psychological Bulletin_, _133_(2), 273–293. https://doi.org/10.1037/0033-2909.133.2.273

---

## 14. Appendices

### Appendix A: Data Processing Code

**[TO DO: Include or reference data processing scripts]**

Location: `/code/preprocess.py` and `/code/analysis.py`

---

### Appendix B: Statistical Analysis Code

**[TO DO: Include or reference analysis scripts]**

Location: `/code/analysis.py`

---

### Appendix C: Supplementary Tables

**[TO DO: Include additional detailed tables as needed]**

Examples:

- Full correlation matrix
- Video-level statistics
- Participant exclusion details
- Additional demographic breakdowns

---

### Appendix D: Supplementary Figures

**[TO DO: Include additional visualization]**

Examples:

- Residual plots for model diagnostics
- Individual participant performance profiles
- Additional exploratory visualizations
