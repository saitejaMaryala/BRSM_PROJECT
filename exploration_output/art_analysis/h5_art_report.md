# H5: Aligned Rank Transform (ART) ANOVA on Confidence

To test the interaction between Group (NB vs AB) and Target Type (BB vs EM) on confidence on an ordinal Likert scale, the Aligned Rank Transform (ART) non-parametric ANOVA was utilized.

## Methodology
1. **Alignment**: Responses (mean confidence) were aligned by extracting out the main effects of Group and Target Type to isolate the interaction variance component.
2. **Ranking**: These interaction-aligned responses were then ranked across all participants.
3. **Testing**: We computed the within-subject difference between ranked BB and EM responses ($Rank_{BB} - Rank_{EM}$) and tested this difference across groups with an independent samples t-test to evaluate the interaction effect.

## Results
- **t-statistic**: 1.8701
- **p-value**: 0.0632

**Conclusion**: The Group x Target Type interaction was not significant under the ART approach.

## Plots
![Aligned Rank Interaction Profile](h5_art_interaction_profile.png)

![Rank Differences Distribution](h5_art_rank_differences.png)
