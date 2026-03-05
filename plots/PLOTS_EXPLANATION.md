# BRSM Project - Data Visualization Guide

**Date:** March 5, 2026  
**Sample:** 164 participants (78 Abrupt Cut, 86 Natural Cut)  
**Task:** Recognition memory for video frames

---

## Overview

This document explains the 5 key visualizations generated from the BRSM experiment investigating how abrupt disruptions in video continuity affect memory encoding. All plots use clean, minimal aesthetics with statistical significance testing.

---

## Plot 1: Accuracy by Condition

**File:** `1_accuracy_by_condition.png`

### What it Shows

Bar plot comparing overall recognition accuracy between the two experimental conditions:

- **Abrupt Cut (Red):** Videos interrupted 1-5 seconds before natural event boundaries
- **Natural Cut (Blue):** Videos played with natural, uninterrupted continuity

### Key Findings

- **Abrupt Cut:** 83.75% accuracy
- **Natural Cut:** 86.98% accuracy
- **Statistical Result:** t(162) = 2.66, **p = 0.009** ⭐ **SIGNIFICANT**
- **Interpretation:** Participants showed significantly **better memory** for naturally cut videos compared to abruptly interrupted ones, supporting the hypothesis that disrupting event boundaries impairs memory encoding.

### Why This Matters

This is the **primary finding** of the experiment. The significant difference suggests that artificial interruptions before natural event boundaries disrupt the encoding process, consistent with Event Segmentation Theory.

---

## Plot 2: Accuracy by Frame Type

**File:** `2_accuracy_by_frame_type.png`

### What it Shows

Bar plot comparing recognition accuracy for two types of target frames:

- **Before Boundary (Orange):** Frames presented 1-5 seconds before an event boundary
- **Event Middle (Green):** Frames from the middle of events (between boundaries)

### Key Findings

- **Before Boundary:** 83.99% accuracy
- **Event Middle:** 86.89% accuracy
- **Statistical Result:** t(326) = 2.77, **p = 0.006** ⭐ **SIGNIFICANT**
- **Interpretation:** Frames from event middles are remembered **better** than frames near boundaries, suggesting boundary proximity affects memory encoding.

### Why This Matters

This finding aligns with the **boundary advantage** literature, showing that frames at different temporal positions within events have different memorability. Event-middle frames may be less susceptible to disruption effects.

---

## Plot 3: Condition × Frame Type Interaction

**File:** `3_interaction_condition_frame.png`

### What it Shows

Grouped bar plot showing how the effect of video condition (Abrupt vs Natural) differs across frame types (Before Boundary vs Event Middle). This 2×2 design reveals whether the two factors interact.

### Key Findings

**Abrupt Cut Condition:**

- Before Boundary: 82.18%
- Event Middle: 85.32%
- Gap: 3.14%

**Natural Cut Condition:**

- Before Boundary: 85.64%
- Event Middle: 88.31%
- Gap: 2.67%

### Interpretation

The pattern suggests that:

1. **Both frame types** are affected by the abrupt cut manipulation
2. The **natural condition shows better performance** across both frame types
3. There may be a slightly larger disruption effect for before-boundary frames in the abrupt condition, though this would require formal interaction testing to confirm

### Why This Matters

This visualization helps identify whether certain types of frames are more vulnerable to disruption, providing insights into the mechanisms of boundary-related memory effects.

---

## Plot 4: Response Time by Condition

**File:** `4_rt_by_condition.png`

### What it Shows

Bar plot comparing how long participants took to make recognition decisions (in seconds) across conditions, analyzing only **correct trials**.

### Key Findings

- **Abrupt Cut:** 5.22 seconds
- **Natural Cut:** 5.42 seconds
- **Statistical Result:** t(162) = 1.22, **p = 0.223** (NOT SIGNIFICANT)
- **Interpretation:** Response times did not differ significantly between conditions, suggesting no speed-accuracy tradeoff. Both groups took similar amounts of time to make decisions.

### Why This Matters

The lack of RT difference indicates that the accuracy effect is **not due to different decision strategies** or speed-accuracy tradeoffs. Participants in both conditions were equally deliberate in their responses, strengthening the interpretation that the accuracy difference reflects genuine memory encoding differences.

---

## Plot 5: Confidence Ratings by Condition

**File:** `5_confidence_by_condition.png`

### What it Shows

Bar plot comparing participants' subjective confidence ratings (1-5 scale) across conditions.

### Key Findings

- **Abrupt Cut:** 4.08 confidence
- **Natural Cut:** 4.20 confidence
- **Statistical Result:** t(162) = 1.82, **p = 0.070** (MARGINALLY SIGNIFICANT)
- **Interpretation:** There is a trend toward higher confidence in the natural cut condition, though it doesn't quite reach conventional statistical significance (p < 0.05).

### Why This Matters

The trend suggests participants in the natural condition may have had **stronger memory traces**, leading to slightly more confident responses. This provides converging evidence with the accuracy findings and suggests that the encoding advantage for natural videos extends beyond just performance to subjective memory strength.

---

## Statistical Summary

### Main Effects

1. **Condition Effect on Accuracy:** ✅ Significant (p = 0.009)
   - Natural Cut > Abrupt Cut by 3.23 percentage points
2. **Frame Type Effect on Accuracy:** ✅ Significant (p = 0.006)
   - Event Middle > Before Boundary by 2.90 percentage points

3. **Condition Effect on RT:** ❌ Not Significant (p = 0.223)
   - No difference in response speed

4. **Condition Effect on Confidence:** ⚠️ Marginal (p = 0.070)
   - Trend toward higher confidence in Natural Cut

### Implications

The results support the hypothesis that **abrupt disruptions at event boundaries impair memory encoding**. Key insights:

1. **Boundary Disruption Matters:** Interrupting videos before natural event boundaries significantly reduces recognition memory
2. **Frame Position Matters:** Frames from event middles are better remembered than boundary-proximal frames
3. **Not a Speed Issue:** The effect is not explained by different response strategies or speed-accuracy tradeoffs
4. **Genuine Memory Effect:** The pattern suggests a real encoding disruption rather than a strategic or motivational difference

### Recommendations for Analysis

1. Consider running a 2×2 ANOVA to formally test the Condition × Frame Type interaction
2. Examine individual differences: Are some participants more susceptible to disruption?
3. Explore whether confidence ratings predict accuracy differently across conditions
4. Consider trial-level analyses to examine temporal dynamics

---

## Color Legend

- 🔴 **Red:** Abrupt Cut condition
- 🔵 **Blue:** Natural Cut condition
- 🟠 **Orange:** Before Boundary frames
- 🟢 **Green:** Event Middle frames

## Significance Markers

- \*\*\* p < 0.001
- \*\* p < 0.01
- - p < 0.05

---

**For questions or additional analyses, contact:** gargi.shukla@research.iiit.ac.in
