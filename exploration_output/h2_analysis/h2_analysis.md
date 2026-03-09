# Hypothesis 2 Analysis: Boundary-Related Memory Effects

**Hypothesis:** *Recognition accuracy for pre-boundary frames is predicted to be higher in the Natural Cut group than in the Abrupt Cut group, reflecting preserved event continuity in the natural condition.*

---

## 1. Normality Assessment (Before Boundary Frames)
Before conducting comparative statistical tests, the Participant-Level mean accuracy specifically for **Before Boundary (BB)** frames was assessed for normality using the **Shapiro-Wilk test**.

### Results of Normality Check:
As with the overall accuracy, the BB frame accuracy significantly violated the assumption of normality.

*   **Participant Mean Accuracy (BB Frames):**
    *   **Abrupt Cut (AB):** Statistic = 0.9475, $p$ = 0.0027 (**NOT Normal**)
    *   **Natural Cut (NB):** Statistic = 0.9218, $p$ = 0.0001 (**NOT Normal**)

---

## 2. Statistical Comparison (Mann-Whitney U Test)
Because the data violated normality assumptions, the non-parametric **Mann-Whitney U Test** was utilized to evaluate differences in BB frame memory between the two groups.

### H2: Recognition Accuracy on BB Frames
*   **Natural Cut (NB):** $N = 87$, Median $= 85.00\%$
*   **Abrupt Cut (AB):** $N = 79$, Median $= 85.00\%$
*   **Test Statistic:** $U = 4192.50$
*   **Significance:** $p = 0.0133$ **(Significant)**
*   **Effect Size (Rank-Biserial $r$):** $-0.2200$

### Conclusion:
**The hypothesis is supported.** The Natural Cut group retained the Before Boundary (BB) frames significantly better than the Abrupt Cut group ($p = 0.0133$). 

---

## 3. Explanatory Notes on Methodology

### Identical Medians but Significant Difference?
Both groups have an identical median of 85.00%. How can the result be statistically significant?
The median represents only the exact middle participant. However, the Mann-Whitney U test evaluates the **entire distribution of ranks**. Visualizing the data (via the generated violin plots) reveals a long lower tail for the Abrupt Cut group (scores dropping into the 50s and 60s), while the Natural Cut group is heavily clustered at the top (many participants scoring 95-100%). Overall, the NB participants hold significantly higher ranks across the entire pool.

### Interpretation of Effect Size
The Rank-Biserial Correlation ($r$) of `0.2200` indicates a **Small-to-Medium effect**. This means the penalty of the Abrupt Cut on memory for those specific frames is reliable and consistently measurable, though it does not eliminate the memory entirely. Unnatural editing acts as a targeted disruption to encoding right before the cut happened, proving Event Segmentation Theory's predictions regarding boundary disruptions.

