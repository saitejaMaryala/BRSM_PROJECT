"""
Hypothesis 7: Metacognitive Calibration is Poorer in the Abrupt Cut Group
=========================================================================

Metacognitive calibration refers to how well confidence tracks actual accuracy.
A well-calibrated participant gives high confidence when correct and low
confidence when incorrect.

If abrupt cuts create degraded or "fuzzy" memory traces near event boundaries,
participants in the Abrupt Cut group may have poorer metacognitive insight —
their confidence ratings may not discriminate as well between correct and
incorrect responses (i.e., weaker confidence-accuracy correlation).

Measured by: gamma correlation (Goodman-Kruskal) between confidence and
accuracy per participant, then comparing gamma across groups.

Test: Welch's t-test comparing mean gamma correlation (NB vs AB).
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

plots_dir = '../exploration_output/h7_analysis'
os.makedirs(plots_dir, exist_ok=True)


def goodman_kruskal_gamma(x, y):
    """
    Compute Goodman-Kruskal gamma — an ordinal association measure.
    Appropriate for confidence (ordinal) × accuracy (binary).
    """
    concordant = 0
    discordant = 0
    n = len(x)
    for i in range(n):
        for j in range(i+1, n):
            dx = x.iloc[i] - x.iloc[j]
            dy = y.iloc[i] - y.iloc[j]
            product = dx * dy
            if product > 0:
                concordant += 1
            elif product < 0:
                discordant += 1
    denom = concordant + discordant
    if denom == 0:
        return np.nan
    return (concordant - discordant) / denom


def main():
    trials = pd.read_csv('../cleaned_data/cleaned_trials.csv')

    print("=" * 60)
    print("H7: METACOGNITIVE CALIBRATION (CONFIDENCE-ACCURACY LINK)")
    print("=" * 60)

    # --- Compute gamma per participant ---
    print("\nComputing per-participant Goodman-Kruskal gamma... (this may take a moment)")

    gammas = []
    for (pid, grp), group_df in trials.groupby(['participant', 'group']):
        g = goodman_kruskal_gamma(group_df['confidence'], group_df['correct'])
        gammas.append({'participant': pid, 'group': grp, 'gamma': g})

    gamma_df = pd.DataFrame(gammas)

    nb_gamma = gamma_df[gamma_df['group'] == 'NB']['gamma'].dropna()
    ab_gamma = gamma_df[gamma_df['group'] == 'AB']['gamma'].dropna()

    print(f"\n--- Descriptive Statistics ---")
    print(f"NB gamma: M={nb_gamma.mean():.4f}, SD={nb_gamma.std():.4f}, n={len(nb_gamma)}")
    print(f"AB gamma: M={ab_gamma.mean():.4f}, SD={ab_gamma.std():.4f}, n={len(ab_gamma)}")

    # --- Test ---
    t_stat, p_val = stats.ttest_ind(nb_gamma, ab_gamma, equal_var=False)
    n1, n2 = len(nb_gamma), len(ab_gamma)
    pooled_std = np.sqrt(((n1-1)*nb_gamma.std()**2 + (n2-1)*ab_gamma.std()**2) / (n1+n2-2))
    cohens_d = (nb_gamma.mean() - ab_gamma.mean()) / pooled_std if pooled_std > 0 else 0

    print(f"\n--- Group Comparison ---")
    print(f"t({n1+n2-2}) = {t_stat:.4f}, p = {p_val:.4g}")
    print(f"Cohen's d = {cohens_d:.4f}")

    if p_val < 0.05:
        print(">> SIGNIFICANT: Abrupt group has poorer metacognitive calibration!")
    else:
        print(">> No significant difference in metacognitive calibration.")

    # --- Also: simple confidence gap (correct - incorrect) per participant ---
    conf_gap = trials.groupby(['participant', 'group', 'correct'])['confidence'].mean().reset_index()
    conf_gap_pivot = conf_gap.pivot_table(index=['participant', 'group'], columns='correct', values='confidence').reset_index()
    conf_gap_pivot.columns = ['participant', 'group', 'conf_incorrect', 'conf_correct']
    conf_gap_pivot['conf_gap'] = conf_gap_pivot['conf_correct'] - conf_gap_pivot['conf_incorrect']

    nb_gap = conf_gap_pivot[conf_gap_pivot['group'] == 'NB']['conf_gap'].dropna()
    ab_gap = conf_gap_pivot[conf_gap_pivot['group'] == 'AB']['conf_gap'].dropna()

    t_gap, p_gap = stats.ttest_ind(nb_gap, ab_gap, equal_var=False)
    print(f"\n--- Confidence Gap (correct - incorrect) ---")
    print(f"NB conf gap: M={nb_gap.mean():.4f}")
    print(f"AB conf gap: M={ab_gap.mean():.4f}")
    print(f"t = {t_gap:.4f}, p = {p_gap:.4g}")

    # --- Visualization ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Panel A: Gamma distribution by group
    ax1 = axes[0]
    sns.boxplot(data=gamma_df, x='group', y='gamma', palette=['#c44e52', '#4c72b0'],
                ax=ax1, width=0.5)
    sns.stripplot(data=gamma_df, x='group', y='gamma', color='black', alpha=0.3,
                  ax=ax1, size=4, jitter=True)
    ax1.set_title('Metacognitive Calibration (Gamma)\nby Condition', fontsize=13, pad=10)
    ax1.set_ylabel('Goodman-Kruskal Gamma', fontsize=12)
    ax1.set_xlabel('Condition', fontsize=12)
    ax1.set_xticklabels(['Abrupt Cut', 'Natural Cut'])
    ax1.axhline(0, color='gray', linestyle='--', alpha=0.5)

    # Panel B: Confidence by correctness per group
    ax2 = axes[1]
    plot_df = trials.copy()
    plot_df['Outcome'] = plot_df['correct'].map({1.0: 'Correct', 0.0: 'Incorrect'})
    sns.barplot(data=plot_df, x='Outcome', y='confidence', hue='group',
                palette=['#4c72b0', '#c44e52'], ax=ax2, errorbar='ci', capsize=0.1)
    ax2.set_title('Confidence by Accuracy & Condition', fontsize=13, pad=10)
    ax2.set_ylabel('Mean Confidence Rating', fontsize=12)
    ax2.set_xlabel('')
    ax2.legend(title='Condition')
    ax2.set_ylim(2.5, 4.8)

    fig.suptitle('H7: Does Abrupt Segmentation Impair Metacognitive Insight?', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'h7_metacognition.png'), dpi=300, bbox_inches='tight')
    print(f"\nSaved: h7_metacognition.png")


    # --- Auto-generated Extra Plots ---
    try:
        df_p = pd.read_csv('../cleaned_data/cleaned_trials.csv')
        df_s = pd.read_csv('../cleaned_data/cleaned_summary.csv')
        
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=df_s, x='group', y='BB_accuracy', palette='Set2')
        sns.swarmplot(data=df_s, x='group', y='BB_accuracy', color='k', alpha=0.5)
        plt.title('H7: Violin + Swarm of BB Accuracy')
        plt.savefig(os.path.join(plots_dir, 'h7_extra_plots_bb_accuracy.png'), dpi=300)
        plt.close()
        
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_s, x='group', y='EM_accuracy', palette='Set2')
        sns.swarmplot(data=df_s, x='group', y='EM_accuracy', color='k', alpha=0.5)
        plt.title('H7: Box + Swarm of EM Accuracy')
        plt.savefig(os.path.join(plots_dir, 'h7_extra_plots_em_accuracy.png'), dpi=300)
        plt.close()
        
        if 'rt' in df_p.columns:
            plt.figure(figsize=(10, 6))
            sns.violinplot(data=df_p, x='group', y='rt', hue='target_type', split=True, palette='muted')
            plt.title('H7: RT distributions by Group and Target Type')
            plt.ylim(0, 15)
            plt.savefig(os.path.join(plots_dir, 'h7_extra_plots_rt.png'), dpi=300)
            plt.close()
            
    except Exception as e:
        print(f"Extra plots failed: {e}")
    # ---------------------------------

if __name__ == '__main__':
    main()
