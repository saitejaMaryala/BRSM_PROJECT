"""
Hypothesis 5: Confidence is Selectively Reduced for BB Frames in the Abrupt Cut Group
=====================================================================================

If abrupt cuts disrupt the encoding of pre-boundary information, participants
in the Abrupt Cut group should not only be less accurate on BB frames, but
also report LOWER subjective confidence specifically for those frames.

For Event-Middle frames, confidence should remain comparable across groups
since mid-event encoding is unaffected by the boundary manipulation.

This tests whether the disruption affects not just memory performance but also
the subjective *quality* of the memory trace (metamemory).

Test: 2×2 Mixed ANOVA on confidence (Group × Target Type),
      plus targeted t-tests on BB and EM confidence separately.
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

plots_dir = '../exploration_output/h5_analysis'
os.makedirs(plots_dir, exist_ok=True)

def main():
    trials = pd.read_csv('../cleaned_data/cleaned_trials.csv')

    print("=" * 60)
    print("H5: CONFIDENCE SELECTIVELY REDUCED FOR BB IN ABRUPT GROUP")
    print("=" * 60)

    # Compute per-participant mean confidence for BB and EM
    conf_by_participant = trials.groupby(['participant', 'group', 'target_type'])['confidence'].mean().reset_index()
    conf_pivot = conf_by_participant.pivot_table(index=['participant', 'group'],
                                                  columns='target_type',
                                                  values='confidence').reset_index()

    nb = conf_pivot[conf_pivot['group'] == 'NB']
    ab = conf_pivot[conf_pivot['group'] == 'AB']

    print("\n--- Descriptive Statistics (Mean Confidence) ---")
    print(f"NB - BB frames: M={nb['BB'].mean():.4f}, SD={nb['BB'].std():.4f}")
    print(f"NB - EM frames: M={nb['EM'].mean():.4f}, SD={nb['EM'].std():.4f}")
    print(f"AB - BB frames: M={ab['BB'].mean():.4f}, SD={ab['BB'].std():.4f}")
    print(f"AB - EM frames: M={ab['EM'].mean():.4f}, SD={ab['EM'].std():.4f}")

    # Test 1: Group difference in BB confidence
    t_bb, p_bb = stats.ttest_ind(nb['BB'].dropna(), ab['BB'].dropna(), equal_var=False)
    print(f"\n--- BB Frame Confidence: NB vs AB ---")
    print(f"t = {t_bb:.4f}, p = {p_bb:.4g}")
    if p_bb < 0.05:
        print(">> SIGNIFICANT: Abrupt group shows lower confidence for BB frames.")
    else:
        print(">> No significant difference in BB frame confidence.")

    # Test 2: Group difference in EM confidence
    t_em, p_em = stats.ttest_ind(nb['EM'].dropna(), ab['EM'].dropna(), equal_var=False)
    print(f"\n--- EM Frame Confidence: NB vs AB ---")
    print(f"t = {t_em:.4f}, p = {p_em:.4g}")
    if p_em < 0.05:
        print(">> SIGNIFICANT: Groups differ even for EM frames.")
    else:
        print(">> No significant difference in EM frame confidence (as predicted).")

    # Test 3: Interaction — compare (BB - EM) confidence difference across groups
    nb['BB_minus_EM_conf'] = nb['BB'] - nb['EM']
    ab['BB_minus_EM_conf'] = ab['BB'] - ab['EM']

    t_int, p_int = stats.ttest_ind(nb['BB_minus_EM_conf'].dropna(), ab['BB_minus_EM_conf'].dropna(), equal_var=False)
    print(f"\n--- Interaction Test (BB-EM confidence difference) ---")
    print(f"NB (BB-EM conf diff): M={nb['BB_minus_EM_conf'].mean():.4f}")
    print(f"AB (BB-EM conf diff): M={ab['BB_minus_EM_conf'].mean():.4f}")
    print(f"t = {t_int:.4f}, p = {p_int:.4g}")

    if p_int < 0.05:
        print(">> SIGNIFICANT INTERACTION: Confidence impairment is selective to BB frames in AB group!")
    else:
        print(">> No significant interaction on confidence.")

    # --- Visualization ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Panel A: Grouped bar plot
    ax = axes[0]
    x = np.arange(2)
    width = 0.3
    ax.bar(x - width/2, [nb['BB'].mean(), nb['EM'].mean()], width,
           yerr=[nb['BB'].sem(), nb['EM'].sem()],
           label='Natural Cut', color='#4c72b0', alpha=0.8, capsize=5, edgecolor='black')
    ax.bar(x + width/2, [ab['BB'].mean(), ab['EM'].mean()], width,
           yerr=[ab['BB'].sem(), ab['EM'].sem()],
           label='Abrupt Cut', color='#c44e52', alpha=0.8, capsize=5, edgecolor='black')
    ax.set_ylabel('Mean Confidence Rating', fontsize=12)
    ax.set_title('Confidence by Group × Target Type', fontsize=13, pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(['Before-Boundary', 'Event-Middle'], fontsize=11)
    ax.legend(title='Condition')
    ax.set_ylim(3.5, 4.8)

    # Panel B: Violin plot of confidence distributions
    ax2 = axes[1]
    trials_copy = trials.copy()
    trials_copy['target_type'] = trials_copy['target_type'].map({'BB': 'Before-Boundary', 'EM': 'Event-Middle'})
    sns.violinplot(data=trials_copy, x='target_type', y='confidence', hue='group',
                   split=True, palette=['#4c72b0', '#c44e52'], ax=ax2, inner='quartile')
    ax2.set_title('Confidence Distribution by Condition', fontsize=13, pad=10)
    ax2.set_xlabel('')
    ax2.set_ylabel('Confidence Rating', fontsize=12)
    ax2.legend(title='Condition')

    fig.suptitle('H5: Confidence Selectively Impaired for Boundary Frames?', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'h5_confidence_bb.png'), dpi=300, bbox_inches='tight')
    print(f"\nSaved: h5_confidence_bb.png")


    # --- Auto-generated Extra Plots ---
    try:
        df_p = pd.read_csv('../cleaned_data/cleaned_trials.csv')
        df_s = pd.read_csv('../cleaned_data/cleaned_summary.csv')
        
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=df_s, x='group', y='BB_accuracy', palette='Set2')
        sns.swarmplot(data=df_s, x='group', y='BB_accuracy', color='k', alpha=0.5)
        plt.title('H5: Violin + Swarm of BB Accuracy')
        plt.savefig(os.path.join(plots_dir, 'h5_extra_plots_bb_accuracy.png'), dpi=300)
        plt.close()
        
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_s, x='group', y='EM_accuracy', palette='Set2')
        sns.swarmplot(data=df_s, x='group', y='EM_accuracy', color='k', alpha=0.5)
        plt.title('H5: Box + Swarm of EM Accuracy')
        plt.savefig(os.path.join(plots_dir, 'h5_extra_plots_em_accuracy.png'), dpi=300)
        plt.close()
        
        if 'rt' in df_p.columns:
            plt.figure(figsize=(10, 6))
            sns.violinplot(data=df_p, x='group', y='rt', hue='target_type', split=True, palette='muted')
            plt.title('H5: RT distributions by Group and Target Type')
            plt.ylim(0, 15)
            plt.savefig(os.path.join(plots_dir, 'h5_extra_plots_rt.png'), dpi=300)
            plt.close()
            
    except Exception as e:
        print(f"Extra plots failed: {e}")
    # ---------------------------------

if __name__ == '__main__':
    main()
