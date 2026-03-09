# Hypothesis 1 Analysis: Recognition Accuracy and Response Times

**Hypothesis:** *Participants who viewed Naturally cut videos are expected to show higher recognition accuracy and faster response times (RTs) compared to those who viewed Abruptly cut videos.*

---

## 1. Normality Assessment
Before conducting comparative statistical tests, the Participant-Level mean data was assessed for normality using the **Shapiro-Wilk test** (`scipy.stats.shapiro`).

### Why use the Shapiro-Wilk test?
The Shapiro-Wilk test evaluates the Null Hypothesis ($H_0$) that data is drawn from a normally distributed population. It is considered the most powerful and reliable test for normality, especially suited for medium sample sizes ($N \approx 80-90$). 
- **Decision Rule:** If $p < 0.05$, we reject the null hypothesis and conclude the data is *not* normally distributed.

### Results of Normality Check:
As is common in cognitive memory and bounded-performance data, **all metrics significantly violated the assumption of normality**.

*   **Participant Mean Accuracy (%)**
    *   **Abrupt Cut (AB):** Statistic = 0.9567, $p$ = 0.0091 (**NOT Normal**)
    *   **Natural Cut (NB):** Statistic = 0.9419, $p$ = 0.0007 (**NOT Normal**)
*   **Participant Median Response Time (Correct Trials)**
    *   **Abrupt Cut (AB):** Statistic = 0.8817, $p$ < 0.0000 (**NOT Normal**)
    *   **Natural Cut (NB):** Statistic = 0.9512, $p$ = 0.0025 (**NOT Normal**)
*   **Participant Mean Response Time (Correct Trials)**
    *   **Abrupt Cut (AB):** Statistic = 0.8995, $p$ < 0.0000 (**NOT Normal**)
    *   **Natural Cut (NB):** Statistic = 0.9268, $p$ = 0.0001 (**NOT Normal**)

*(Visual Q-Q scatter plots confirming this non-parametric distribution are available in the accompanying output folder).*

---

## 2. Statistical Comparison (Mann-Whitney U Test)
Because the data violated normality assumptions, a standard Independent Samples T-Test could not be used. Instead, the **Mann-Whitney U Test**—a robust non-parametric alternative—was utilized to compare the two independent groups.

### H1a: Recognition Accuracy
*   **Natural Cut (NB):** $N = 87$, Median $= 87.50\%$
*   **Abrupt Cut (AB):** $N = 79$, Median $= 85.00\%$
*   **Test Statistic:** $U = 4254.50$
*   **Significance:** $p = 0.0078$ **(Significant)**
*   **Effect Size (Rank-Biserial $r$):** $-0.2380$
*   **Conclusion:** The Natural Cut group performed significantly better than the Abrupt Cut group. The effect size indicates a *Small-to-Medium* effect, reflecting a modest but mathematically reliable improvement in memory encoding when natural boundaries are preserved.

### H1b: Response Time (RT)
*   **Natural Cut (NB):** $N = 87$, Median $= 4.49$ seconds
*   **Abrupt Cut (AB):** $N = 79$, Median $= 4.33$ seconds
*   **Test Statistic:** $U = 3814.00$
*   **Significance:** $p = 0.2228$ **(Not Significant)**
*   **Effect Size (Rank-Biserial $r$):** $-0.1099$
*   **Conclusion:** There was no statistically significant difference in median response times between the two conditions. The boundary disruption did not reliably speed up or slow down how quickly participants recognized correct frames.

---

## 3. Explanatory Notes on Methodology

### The Mann-Whitney U Test
Because the Shapiro-Wilk test proved our data is not normally distributed, we cannot use a standard Independent Samples T-Test (which compares the *means* of normal curves). Instead, we used the **Mann-Whitney U Test**, a non-parametric alternative.
- **How it works:** It combines all participants from both groups (166 total) and ranks them from 1st place to 166th place. It then checks if the participants belonging to the Natural Cut (NB) group systematically sit higher in the rankings than the Abrupt Cut (AB) group.
- **Interpretation:** The test yielded a p-value of `0.0078` for accuracy, meaning there is less than a 1% probability this difference occurred by random chance. The Natural Cut boundary disruption genuinely impaired memory encoding.

### Effect Size (Rank-Biserial Correlation)
Even if a test is "statistically significant" (p < 0.05), we still need to know if the real-world difference is large or meaningful. For the Mann-Whitney U test, we calculate the **Rank-Biserial Correlation ($r$)** to measure this.
- **Scale:** It ranges from -1 to 1.
- **Interpretation:** The accuracy effect size of `0.2380` is generally considered a **Small-to-Medium effect**. This means that while the Natural Cut group performed reliably better, the actual boost to memory isn't massive—it's a modest, reliable improvement. For response time, the effect size (`0.1099`) is negligible.

### Why a "Two-Sided" Test?
Although the initial hypothesis predicted a specific direction (NB > AB), a strict **Two-Sided** test was utilized:
1.  **Academic Rigor:** Reviewers in the psychological sciences strongly prefer two-sided tests as the default to protect against false positives (p-hacking), as one-sided tests effectively halve the required $p$-value threshold.
2.  **Detecting the Unexpected:** A one-sided test mathematically blinds the analysis to the possibility that the opposite result might occur. A two-sided test ensures any massive deviation is properly caught. 
*Note: Even using this stricter Two-Sided standard, the accuracy difference remained highly significant ($p = 0.0078$).*