"""
Hypothesis 4: Group × Target Type Interaction on Recognition Accuracy
=====================================================================

The effect of abrupt cuts on memory is SELECTIVE to boundary-adjacent frames.
Specifically, the difference in recognition accuracy between Natural Cut and
Abrupt Cut groups should be significantly LARGER for Before-Boundary (BB)
frames than for Event-Middle (EM) frames.

This is the critical theoretical test: if abrupt interruptions specifically
disrupt the updating of event models at boundaries, then only frames encoded
near those boundaries should suffer — not frames encoded mid-event.

Test: 2×2 Mixed ANOVA (Group: NB vs AB × Target Type: BB vs EM)
Key prediction: Significant interaction effect.
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

plots_dir = '../exploration_output/h4_analysis'
os.makedirs(plots_dir, exist_ok=True)

def main():
    df = pd.read_csv('../cleaned_data/cleaned_summary.csv')
    trials = pd.read_csv('../cleaned_data/cleaned_trials.csv')

    print("=" * 60)
    print("H4: GROUP × TARGET TYPE INTERACTION ON ACCURACY")
    print("=" * 60)

    # --- Approach 1: Two-way mixed ANOVA using summary stats ---
    # Group (between): NB vs AB
    # Target Type (within): BB vs EM
    # DV: accuracy

    nb = df[df['group'] == 'NB'][['participant', 'BB_accuracy', 'EM_accuracy']].copy()
    ab = df[df['group'] == 'AB'][['participant', 'BB_accuracy', 'EM_accuracy']].copy()

    # Compute the BB-EM difference for each participant (within-subject contrast)
    nb['BB_minus_EM'] = nb['BB_accuracy'] - nb['EM_accuracy']
    ab['BB_minus_EM'] = ab['BB_accuracy'] - ab['EM_accuracy']

    print("\n--- Descriptive Statistics ---")
    print(f"NB BB accuracy: M={nb['BB_accuracy'].mean():.4f}, SD={nb['BB_accuracy'].std():.4f}")
    print(f"NB EM accuracy: M={nb['EM_accuracy'].mean():.4f}, SD={nb['EM_accuracy'].std():.4f}")
    print(f"AB BB accuracy: M={ab['BB_accuracy'].mean():.4f}, SD={ab['BB_accuracy'].std():.4f}")
    print(f"AB EM accuracy: M={ab['EM_accuracy'].mean():.4f}, SD={ab['EM_accuracy'].std():.4f}")

    print(f"\nNB (BB - EM difference): M={nb['BB_minus_EM'].mean():.4f}, SD={nb['BB_minus_EM'].std():.4f}")
    print(f"AB (BB - EM difference): M={ab['BB_minus_EM'].mean():.4f}, SD={ab['BB_minus_EM'].std():.4f}")

    # --- Test the interaction ---
    # The interaction in a 2×2 design can be tested by comparing
    # the within-subject difference (BB - EM) between the two groups
    t_stat, p_val = stats.ttest_ind(nb['BB_minus_EM'].dropna(), ab['BB_minus_EM'].dropna(), equal_var=False)

    n1 = len(nb['BB_minus_EM'].dropna())
    n2 = len(ab['BB_minus_EM'].dropna())
    pooled_std = np.sqrt(((n1-1)*nb['BB_minus_EM'].std()**2 + (n2-1)*ab['BB_minus_EM'].std()**2) / (n1+n2-2))
    cohens_d = (nb['BB_minus_EM'].mean() - ab['BB_minus_EM'].mean()) / pooled_std if pooled_std > 0 else 0

    print(f"\n--- Interaction Test (comparing BB-EM difference across groups) ---")
    print(f"t({n1+n2-2}) = {t_stat:.4f}, p = {p_val:.4g}")
    print(f"Cohen's d = {cohens_d:.4f}")

    if p_val < 0.05:
        print(">> SIGNIFICANT INTERACTION: Abrupt cuts selectively impair BB frames more than EM frames!")
    else:
        print(">> No significant interaction: The group difference is similar for BB and EM frames.")

    # --- Also run simple effects ---
    print("\n--- Simple Effects (post-hoc) ---")
    # Group difference for BB frames
    t_bb, p_bb = stats.ttest_ind(nb['BB_accuracy'].dropna(), ab['BB_accuracy'].dropna(), equal_var=False)
    print(f"BB frames (NB vs AB): t = {t_bb:.4f}, p = {p_bb:.4g}")

    # Group difference for EM frames
    t_em, p_em = stats.ttest_ind(nb['EM_accuracy'].dropna(), ab['EM_accuracy'].dropna(), equal_var=False)
    print(f"EM frames (NB vs AB): t = {t_em:.4f}, p = {p_em:.4g}")

    # --- Visualization ---
    plot_data = pd.DataFrame({
        'Condition': ['NB'] * 2 + ['AB'] * 2,
        'Target Type': ['Before-Boundary', 'Event-Middle'] * 2,
        'Accuracy': [nb['BB_accuracy'].mean(), nb['EM_accuracy'].mean(),
                     ab['BB_accuracy'].mean(), ab['EM_accuracy'].mean()],
        'SE': [nb['BB_accuracy'].sem(), nb['EM_accuracy'].sem(),
               ab['BB_accuracy'].sem(), ab['EM_accuracy'].sem()]
    })

    fig, ax = plt.subplots(figsize=(8, 6))
    x = np.arange(2)
    width = 0.3
    nb_vals = plot_data[plot_data['Condition'] == 'NB']
    ab_vals = plot_data[plot_data['Condition'] == 'AB']

    bars1 = ax.bar(x - width/2, nb_vals['Accuracy'], width, yerr=nb_vals['SE'],
                   label='Natural Cut', color='#4c72b0', alpha=0.8, capsize=5, edgecolor='black')
    bars2 = ax.bar(x + width/2, ab_vals['Accuracy'], width, yerr=ab_vals['SE'],
                   label='Abrupt Cut', color='#c44e52', alpha=0.8, capsize=5, edgecolor='black')

    ax.set_ylabel('Recognition Accuracy', fontsize=12)
    ax.set_title('H4: Group × Target Type Interaction\non Recognition Accuracy', fontsize=14, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(['Before-Boundary', 'Event-Middle'], fontsize=11)
    ax.legend(title='Condition', fontsize=10)
    ax.set_ylim(0.75, 0.95)

    # Add interaction annotation
    interaction_text = f"Interaction: p = {p_val:.3f}"
    ax.text(0.5, 0.02, interaction_text, transform=ax.transAxes, ha='center',
            fontsize=11, style='italic',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'h4_interaction.png'), dpi=300)
    print(f"\nSaved: h4_interaction.png")


    # --- Auto-generated Extra Plots ---
    try:
        df_p = pd.read_csv('../cleaned_data/cleaned_trials.csv')
        df_s = pd.read_csv('../cleaned_data/cleaned_summary.csv')
        
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=df_s, x='group', y='BB_accuracy', palette='Set2')
        sns.swarmplot(data=df_s, x='group', y='BB_accuracy', color='k', alpha=0.5)
        plt.title('H4: Violin + Swarm of BB Accuracy')
        plt.savefig(os.path.join(plots_dir, 'h4_extra_plots_bb_accuracy.png'), dpi=300)
        plt.close()
        
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_s, x='group', y='EM_accuracy', palette='Set2')
        sns.swarmplot(data=df_s, x='group', y='EM_accuracy', color='k', alpha=0.5)
        plt.title('H4: Box + Swarm of EM Accuracy')
        plt.savefig(os.path.join(plots_dir, 'h4_extra_plots_em_accuracy.png'), dpi=300)
        plt.close()
        
        if 'rt' in df_p.columns:
            plt.figure(figsize=(10, 6))
            sns.violinplot(data=df_p, x='group', y='rt', hue='target_type', split=True, palette='muted')
            plt.title('H4: RT distributions by Group and Target Type')
            plt.ylim(0, 15)
            plt.savefig(os.path.join(plots_dir, 'h4_extra_plots_rt.png'), dpi=300)
            plt.close()
            
    except Exception as e:
        print(f"Extra plots failed: {e}")
    # ---------------------------------

if __name__ == '__main__':
    main()
