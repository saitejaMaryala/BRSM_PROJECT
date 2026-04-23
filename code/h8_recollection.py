"""
Hypothesis 8: Abrupt Cuts Selectively Impair High-Confidence (Recollective) Memory
===================================================================================

Dual-process memory theory distinguishes between:
  - RECOLLECTION: vivid, detail-rich memory (associated with HIGH confidence)
  - FAMILIARITY: weaker, gist-based memory (associated with LOW confidence)

If abrupt cuts at event boundaries disrupt the coherent event model that
supports rich episodic encoding, then the manipulation should selectively
impair RECOLLECTION (high-confidence correct responses) while leaving
FAMILIARITY (low-confidence correct responses) relatively intact.

Prediction: The proportion of high-confidence correct trials (confidence >= 4)
is lower in the Abrupt Cut group vs Natural Cut group, whereas the proportion
of low-confidence correct trials (confidence <= 3) does not differ across groups.

Test: Compare high-confidence hit rates and low-confidence hit rates between groups.
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

plots_dir = '../exploration_output/h8_analysis'
os.makedirs(plots_dir, exist_ok=True)

def main():
    trials = pd.read_csv('../cleaned_data/cleaned_trials.csv')

    print("=" * 60)
    print("H8: RECOLLECTION vs FAMILIARITY — DUAL-PROCESS ANALYSIS")
    print("=" * 60)

    # Classify trials
    trials['memory_type'] = np.where(trials['confidence'] >= 4, 'High-Confidence', 'Low-Confidence')

    # Per participant: proportion of trials that are high-conf correct AND low-conf correct
    participant_stats = []
    for (pid, grp), pdf in trials.groupby(['participant', 'group']):
        total = len(pdf)
        high_conf_correct = len(pdf[(pdf['memory_type'] == 'High-Confidence') & (pdf['correct'] == 1)])
        low_conf_correct = len(pdf[(pdf['memory_type'] == 'Low-Confidence') & (pdf['correct'] == 1)])
        high_conf_incorrect = len(pdf[(pdf['memory_type'] == 'High-Confidence') & (pdf['correct'] == 0)])
        low_conf_incorrect = len(pdf[(pdf['memory_type'] == 'Low-Confidence') & (pdf['correct'] == 0)])

        participant_stats.append({
            'participant': pid,
            'group': grp,
            'recollection_rate': high_conf_correct / total,  # high-conf hits
            'familiarity_rate': low_conf_correct / total,     # low-conf hits
            'high_conf_errors': high_conf_incorrect / total,
            'low_conf_errors': low_conf_incorrect / total
        })

    pstats = pd.DataFrame(participant_stats)
    nb = pstats[pstats['group'] == 'NB']
    ab = pstats[pstats['group'] == 'AB']

    print("\n--- Descriptive Statistics ---")
    print(f"\nRecollection (high-conf correct):")
    print(f"  NB: M={nb['recollection_rate'].mean():.4f}, SD={nb['recollection_rate'].std():.4f}")
    print(f"  AB: M={ab['recollection_rate'].mean():.4f}, SD={ab['recollection_rate'].std():.4f}")

    print(f"\nFamiliarity (low-conf correct):")
    print(f"  NB: M={nb['familiarity_rate'].mean():.4f}, SD={nb['familiarity_rate'].std():.4f}")
    print(f"  AB: M={ab['familiarity_rate'].mean():.4f}, SD={ab['familiarity_rate'].std():.4f}")

    # Test 1: Recollection difference
    t_rec, p_rec = stats.ttest_ind(nb['recollection_rate'], ab['recollection_rate'], equal_var=False)
    n1, n2 = len(nb), len(ab)
    pooled_std = np.sqrt(((n1-1)*nb['recollection_rate'].std()**2 + (n2-1)*ab['recollection_rate'].std()**2) / (n1+n2-2))
    d_rec = (nb['recollection_rate'].mean() - ab['recollection_rate'].mean()) / pooled_std if pooled_std > 0 else 0

    print(f"\n--- Recollection: NB vs AB ---")
    print(f"t = {t_rec:.4f}, p = {p_rec:.4g}, d = {d_rec:.4f}")
    if p_rec < 0.05:
        print(">> SIGNIFICANT: Recollection (vivid memory) is impaired in Abrupt group!")
    else:
        print(">> No significant difference in recollection.")

    # Test 2: Familiarity difference
    t_fam, p_fam = stats.ttest_ind(nb['familiarity_rate'], ab['familiarity_rate'], equal_var=False)
    pooled_std_f = np.sqrt(((n1-1)*nb['familiarity_rate'].std()**2 + (n2-1)*ab['familiarity_rate'].std()**2) / (n1+n2-2))
    d_fam = (nb['familiarity_rate'].mean() - ab['familiarity_rate'].mean()) / pooled_std_f if pooled_std_f > 0 else 0

    print(f"\n--- Familiarity: NB vs AB ---")
    print(f"t = {t_fam:.4f}, p = {p_fam:.4g}, d = {d_fam:.4f}")
    if p_fam < 0.05:
        print(">> SIGNIFICANT: Even familiarity differs between groups.")
    else:
        print(">> No significant difference in familiarity (as predicted).")

    # Dissociation test: is recollection more impaired than familiarity?
    nb['rec_minus_fam'] = nb['recollection_rate'] - nb['familiarity_rate']
    ab['rec_minus_fam'] = ab['recollection_rate'] - ab['familiarity_rate']
    t_diss, p_diss = stats.ttest_ind(nb['rec_minus_fam'], ab['rec_minus_fam'], equal_var=False)
    print(f"\n--- Dissociation Test (Rec-Fam difference across groups) ---")
    print(f"NB (Rec - Fam): M={nb['rec_minus_fam'].mean():.4f}")
    print(f"AB (Rec - Fam): M={ab['rec_minus_fam'].mean():.4f}")
    print(f"t = {t_diss:.4f}, p = {p_diss:.4g}")

    # --- Also break down by target type ---
    print("\n--- Recollection by Target Type ---")
    for tt in ['BB', 'EM']:
        tt_trials = trials[trials['target_type'] == tt]
        tt_stats = []
        for (pid, grp), pdf in tt_trials.groupby(['participant', 'group']):
            total = len(pdf)
            hc = len(pdf[(pdf['memory_type'] == 'High-Confidence') & (pdf['correct'] == 1)])
            tt_stats.append({'participant': pid, 'group': grp, 'recollection_rate': hc / total})
        tt_df = pd.DataFrame(tt_stats)
        nb_tt = tt_df[tt_df['group'] == 'NB']['recollection_rate']
        ab_tt = tt_df[tt_df['group'] == 'AB']['recollection_rate']
        t_tt, p_tt = stats.ttest_ind(nb_tt, ab_tt, equal_var=False)
        print(f"  {tt}: NB M={nb_tt.mean():.4f}, AB M={ab_tt.mean():.4f}, t={t_tt:.4f}, p={p_tt:.4g}")

    # --- Visualization ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Panel A: Stacked comparison
    ax1 = axes[0]
    x = np.arange(2)
    width = 0.35
    rec_vals = [nb['recollection_rate'].mean(), ab['recollection_rate'].mean()]
    fam_vals = [nb['familiarity_rate'].mean(), ab['familiarity_rate'].mean()]
    rec_se = [nb['recollection_rate'].sem(), ab['recollection_rate'].sem()]
    fam_se = [nb['familiarity_rate'].sem(), ab['familiarity_rate'].sem()]

    bars1 = ax1.bar(x - width/2, rec_vals, width, yerr=rec_se, label='Recollection\n(High-Conf Correct)',
                    color='#4c72b0', alpha=0.8, capsize=5, edgecolor='black')
    bars2 = ax1.bar(x + width/2, fam_vals, width, yerr=fam_se, label='Familiarity\n(Low-Conf Correct)',
                    color='#dd8452', alpha=0.8, capsize=5, edgecolor='black')
    ax1.set_xticks(x)
    ax1.set_xticklabels(['Natural Cut', 'Abrupt Cut'], fontsize=11)
    ax1.set_ylabel('Proportion of Trials', fontsize=12)
    ax1.set_title('Recollection vs Familiarity by Condition', fontsize=13, pad=10)
    ax1.legend(fontsize=9)

    # Add significance stars
    if p_rec < 0.05:
        ax1.annotate('*', xy=(x[0] - width/2, rec_vals[0] + rec_se[0] + 0.01),
                     fontsize=16, ha='center', color='red')

    # Panel B: By target type
    ax2 = axes[1]
    high_conf_data = trials[(trials['memory_type'] == 'High-Confidence') & (trials['correct'] == 1)]
    hc_summary = high_conf_data.groupby(['participant', 'group', 'target_type']).size().reset_index(name='count')
    # Normalize by participant total trials per target type
    total_per = trials.groupby(['participant', 'group', 'target_type']).size().reset_index(name='total')
    hc_merged = hc_summary.merge(total_per, on=['participant', 'group', 'target_type'])
    hc_merged['rate'] = hc_merged['count'] / hc_merged['total']
    hc_merged['target_type'] = hc_merged['target_type'].map({'BB': 'Before-Boundary', 'EM': 'Event-Middle'})

    sns.barplot(data=hc_merged, x='target_type', y='rate', hue='group',
                palette=['#4c72b0', '#c44e52'], ax=ax2, errorbar='ci', capsize=0.1)
    ax2.set_title('Recollection Rate by Target Type', fontsize=13, pad=10)
    ax2.set_ylabel('Proportion High-Conf Correct', fontsize=12)
    ax2.set_xlabel('')
    ax2.legend(title='Condition')

    fig.suptitle('H8: Does Boundary Disruption Selectively Impair Recollection?', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'h8_recollection.png'), dpi=300, bbox_inches='tight')
    print(f"\nSaved: h8_recollection.png")


    # --- Auto-generated Extra Plots ---
    try:
        df_p = pd.read_csv('../cleaned_data/cleaned_trials.csv')
        df_s = pd.read_csv('../cleaned_data/cleaned_summary.csv')
        
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=df_s, x='group', y='BB_accuracy', palette='Set2')
        sns.swarmplot(data=df_s, x='group', y='BB_accuracy', color='k', alpha=0.5)
        plt.title('H8: Violin + Swarm of BB Accuracy')
        plt.savefig(os.path.join(plots_dir, 'h8_extra_plots_bb_accuracy.png'), dpi=300)
        plt.close()
        
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_s, x='group', y='EM_accuracy', palette='Set2')
        sns.swarmplot(data=df_s, x='group', y='EM_accuracy', color='k', alpha=0.5)
        plt.title('H8: Box + Swarm of EM Accuracy')
        plt.savefig(os.path.join(plots_dir, 'h8_extra_plots_em_accuracy.png'), dpi=300)
        plt.close()
        
        if 'rt' in df_p.columns:
            plt.figure(figsize=(10, 6))
            sns.violinplot(data=df_p, x='group', y='rt', hue='target_type', split=True, palette='muted')
            plt.title('H8: RT distributions by Group and Target Type')
            plt.ylim(0, 15)
            plt.savefig(os.path.join(plots_dir, 'h8_extra_plots_rt.png'), dpi=300)
            plt.close()
            
    except Exception as e:
        print(f"Extra plots failed: {e}")
    # ---------------------------------

if __name__ == '__main__':
    main()
