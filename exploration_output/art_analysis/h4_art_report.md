n# H4: Aligned Rank Transform (ART) ANOVA on Accuracy

To robustly test the interaction between Group (NB vs AB) and Target Type (BB vs EM) on non-normal, bounded accuracy data, we implemented the Aligned Rank Transform (ART) for non-parametric ANOVA.

## Methodology
1. **Alignment**: Data were aligned to isolate the interaction effect by removing the main effect of Group, the main effect of Target Type, and the grand mean.
2. **Ranking**: The aligned responses were ranked globally across all participants and conditions.
3. **Testing**: To test the interaction in this 2x2 mixed design, we computed the within-subject difference of the aligned ranks (BB - EM) and performed an independent samples t-test on these differences between the NB and AB groups. This procedure yields an exact equivalent to the F-test for interaction in a mixed ANOVA on ranks.

## Results
- **t-statistic**: 0.5926
- **p-value**: 0.5543

**Conclusion**: We failed to find a significant Group x Target Type interaction on accuracy using the ART approach. This aligns with the previous simple Mann-Whitney analysis on unranked difference scores.

## Plots
![Aligned Rank Interaction Profile](h4_art_interaction_profile.png)

![Rank Differences Distribution](h4_art_rank_differences.png)
