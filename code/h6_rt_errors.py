"""
Hypothesis 6: Incorrect Responses are Slower, Especially for BB Frames in the Abrupt Group
===========================================================================================

When participants make errors (selecting the lure instead of the target), this
typically reflects greater deliberation or confusion. If abrupt cuts degrade
memory representations specifically near event boundaries, then:

- Incorrect trials should generally be SLOWER than correct trials (reflecting
  uncertainty and deliberation).
- This RT cost of errors should be LARGER for BB frames in the Abrupt Cut
  group, because the degraded boundary representation creates more ambiguity,
  forcing longer deliberation before an ultimately incorrect decision.

Test: 2×2×2 analysis (Group × Target Type × Correctness) on RT,
      with focused comparisons on incorrect trial RTs.
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

plots_dir = '../exploration_output/h6_analysis'
os.makedirs(plots_dir, exist_ok=True)

def main():
    trials = pd.read_csv('../cleaned_data/cleaned_trials.csv')

    print("=" * 60)
    print("H6: RT COST OF ERRORS × GROUP × TARGET TYPE")
    print("=" * 60)

    # Overall: correct vs incorrect RT
    correct_rt = trials[trials['correct'] == 1]['rt']
    incorrect_rt = trials[trials['correct'] == 0]['rt']
    t_overall, p_overall = stats.ttest_ind(correct_rt, incorrect_rt, equal_var=False)

    print("\n--- Overall Correct vs Incorrect RT ---")
    print(f"Correct trials:   M={correct_rt.mean():.3f}s (SD={correct_rt.std():.3f})")
    print(f"Incorrect trials: M={incorrect_rt.mean():.3f}s (SD={incorrect_rt.std():.3f})")
    print(f"t = {t_overall:.4f}, p = {p_overall:.4g}")

    # Compute per-participant RT for each condition
    rt_by_cond = trials.groupby(['participant', 'group', 'target_type', 'correct'])['rt'].mean().reset_index()

    # Focus: RT for INCORRECT BB trials across groups
    incorrect_bb = rt_by_cond[(rt_by_cond['target_type'] == 'BB') & (rt_by_cond['correct'] == 0)]
    nb_incorrect_bb = incorrect_bb[incorrect_bb['group'] == 'NB']['rt']
    ab_incorrect_bb = incorrect_bb[incorrect_bb['group'] == 'AB']['rt']

    t_bb_err, p_bb_err = stats.ttest_ind(nb_incorrect_bb.dropna(), ab_incorrect_bb.dropna(), equal_var=False)
    print(f"\n--- Incorrect BB Frame RT: NB vs AB ---")
    print(f"NB incorrect BB RT: M={nb_incorrect_bb.mean():.3f}s (n={len(nb_incorrect_bb)})")
    print(f"AB incorrect BB RT: M={ab_incorrect_bb.mean():.3f}s (n={len(ab_incorrect_bb)})")
    print(f"t = {t_bb_err:.4f}, p = {p_bb_err:.4g}")

    # Focus: RT for INCORRECT EM trials across groups
    incorrect_em = rt_by_cond[(rt_by_cond['target_type'] == 'EM') & (rt_by_cond['correct'] == 0)]
    nb_incorrect_em = incorrect_em[incorrect_em['group'] == 'NB']['rt']
    ab_incorrect_em = incorrect_em[incorrect_em['group'] == 'AB']['rt']

    t_em_err, p_em_err = stats.ttest_ind(nb_incorrect_em.dropna(), ab_incorrect_em.dropna(), equal_var=False)
    print(f"\n--- Incorrect EM Frame RT: NB vs AB ---")
    print(f"NB incorrect EM RT: M={nb_incorrect_em.mean():.3f}s (n={len(nb_incorrect_em)})")
    print(f"AB incorrect EM RT: M={ab_incorrect_em.mean():.3f}s (n={len(ab_incorrect_em)})")
    print(f"t = {t_em_err:.4f}, p = {p_em_err:.4g}")

    # RT cost of errors (incorrect - correct) per participant per target type
    rt_pivot = rt_by_cond.pivot_table(index=['participant', 'group', 'target_type'],
                                       columns='correct', values='rt').reset_index()
    rt_pivot.columns = ['participant', 'group', 'target_type', 'rt_incorrect', 'rt_correct']
    rt_pivot['rt_cost'] = rt_pivot['rt_incorrect'] - rt_pivot['rt_correct']

    bb_cost = rt_pivot[rt_pivot['target_type'] == 'BB']
    nb_bb_cost = bb_cost[bb_cost['group'] == 'NB']['rt_cost'].dropna()
    ab_bb_cost = bb_cost[bb_cost['group'] == 'AB']['rt_cost'].dropna()

    t_cost, p_cost = stats.ttest_ind(nb_bb_cost, ab_bb_cost, equal_var=False)
    print(f"\n--- Error RT Cost for BB Frames: NB vs AB ---")
    print(f"NB BB error cost: M={nb_bb_cost.mean():.3f}s")
    print(f"AB BB error cost: M={ab_bb_cost.mean():.3f}s")
    print(f"t = {t_cost:.4f}, p = {p_cost:.4g}")

    # --- Visualization ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Panel A: RT by correctness and group
    ax1 = axes[0]
    plot_df = trials.copy()
    plot_df['Outcome'] = plot_df['correct'].map({1.0: 'Correct', 0.0: 'Incorrect'})
    sns.barplot(data=plot_df, x='Outcome', y='rt', hue='group',
                palette=['#4c72b0', '#c44e52'], ax=ax1, errorbar='ci', capsize=0.1)
    ax1.set_title('Response Time by Accuracy & Condition', fontsize=13, pad=10)
    ax1.set_ylabel('Response Time (seconds)', fontsize=12)
    ax1.set_xlabel('')
    ax1.legend(title='Condition')

    # Panel B: RT by correctness × target type × group (focused on BB)
    ax2 = axes[1]
    bb_trials = trials[trials['target_type'] == 'BB'].copy()
    bb_trials['Outcome'] = bb_trials['correct'].map({1.0: 'Correct', 0.0: 'Incorrect'})
    sns.barplot(data=bb_trials, x='Outcome', y='rt', hue='group',
                palette=['#4c72b0', '#c44e52'], ax=ax2, errorbar='ci', capsize=0.1)
    ax2.set_title('RT for Before-Boundary Frames Only', fontsize=13, pad=10)
    ax2.set_ylabel('Response Time (seconds)', fontsize=12)
    ax2.set_xlabel('')
    ax2.legend(title='Condition')

    fig.suptitle('H6: Error-Related RT Costs Across Conditions', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'h6_rt_errors.png'), dpi=300, bbox_inches='tight')
    print(f"\nSaved: h6_rt_errors.png")


    # --- Auto-generated Extra Plots ---
    try:
        df_p = pd.read_csv('../cleaned_data/cleaned_trials.csv')
        df_s = pd.read_csv('../cleaned_data/cleaned_summary.csv')
        
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=df_s, x='group', y='BB_accuracy', palette='Set2')
        sns.swarmplot(data=df_s, x='group', y='BB_accuracy', color='k', alpha=0.5)
        plt.title('H6: Violin + Swarm of BB Accuracy')
        plt.savefig(os.path.join(plots_dir, 'h6_extra_plots_bb_accuracy.png'), dpi=300)
        plt.close()
        
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_s, x='group', y='EM_accuracy', palette='Set2')
        sns.swarmplot(data=df_s, x='group', y='EM_accuracy', color='k', alpha=0.5)
        plt.title('H6: Box + Swarm of EM Accuracy')
        plt.savefig(os.path.join(plots_dir, 'h6_extra_plots_em_accuracy.png'), dpi=300)
        plt.close()
        
        if 'rt' in df_p.columns:
            plt.figure(figsize=(10, 6))
            sns.violinplot(data=df_p, x='group', y='rt', hue='target_type', split=True, palette='muted')
            plt.title('H6: RT distributions by Group and Target Type')
            plt.ylim(0, 15)
            plt.savefig(os.path.join(plots_dir, 'h6_extra_plots_rt.png'), dpi=300)
            plt.close()
            
    except Exception as e:
        print(f"Extra plots failed: {e}")
    # ---------------------------------

if __name__ == '__main__':
    main()
