import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

CLEANED_DIR = Path("../data/individuals_cleaned")
OUTPUT_DIR = Path("../exploration_output/h4_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_interaction_data():
    csv_files = list(CLEANED_DIR.glob("*.csv"))
    if not csv_files: return None
    all_data = []
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, low_memory=False)
            condition = 'AB' if '_AB_' in csv_file.name else ('NB' if '_NB_' in csv_file.name else 'Unknown')
            if condition == 'Unknown':
                continue
            participant_id = csv_file.stem.split('_')[0]
            
            trial_data = df[df['resp.corr'].notna()].copy()
            if trial_data.empty: continue
            
            trial_data['resp.corr'] = pd.to_numeric(trial_data['resp.corr'], errors='coerce')

            bb_trials = trial_data[trial_data['target_img'].astype(str).str.contains('BB_T', na=False)]
            em_trials = trial_data[trial_data['target_img'].astype(str).str.contains('EM_T', na=False)]
            
            if bb_trials.empty or em_trials.empty: continue

            all_data.append({
                'participant': participant_id,
                'group': condition,
                'BB_accuracy': bb_trials['resp.corr'].mean() * 100,
                'EM_accuracy': em_trials['resp.corr'].mean() * 100
            })
        except Exception as e: pass
            
    return pd.DataFrame(all_data)


def plot_interaction_profile(df):
    """Plot group means for BB and EM accuracy so the interaction is visible directly."""
    plot_df = df[df['group'].isin(['NB', 'AB'])].copy()
    long_df = plot_df.melt(id_vars=['participant', 'group'], value_vars=['BB_accuracy', 'EM_accuracy'],
                      var_name='target_type', value_name='accuracy')
    long_df['target_type'] = long_df['target_type'].replace({'BB_accuracy': 'BB', 'EM_accuracy': 'EM'})

    plt.figure(figsize=(8, 6))
    sns.pointplot(data=long_df, x='target_type', y='accuracy', hue='group',
                  palette={'NB': '#4c72b0', 'AB': '#c44e52'}, errorbar=('ci', 68),
                  dodge=0.2, markers=['o', 's'], linestyles=['-', '--'])
    plt.title('Accuracy Interaction Profile: Group by Target Type')
    plt.xlabel('Target Type')
    plt.ylabel('Mean Accuracy (%)')
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'h4_interaction_profile.png', dpi=300)
    plt.close()


def plot_difference_distribution(df):
    """Plot the raw BB-EM difference scores for each group."""
    plot_df = df[df['group'].isin(['NB', 'AB'])].copy()
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=plot_df, x='group', y='BB_minus_EM', palette={'NB': '#4c72b0', 'AB': '#c44e52'})
    sns.stripplot(data=plot_df, x='group', y='BB_minus_EM', color='black', alpha=0.35, jitter=True)
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.title('BB - EM Accuracy Difference by Group')
    plt.xlabel('Group')
    plt.ylabel('Difference Score (%)')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'h4_difference_distribution.png', dpi=300)
    plt.close()

def main():
    df = load_interaction_data()
    if df is None or df.empty: return

    print("=" * 60)
    print("H4: GROUP × TARGET TYPE INTERACTION ON ACCURACY")
    print("=" * 60)

    nb = df[df['group'] == 'NB'].copy()
    ab = df[df['group'] == 'AB'].copy()

    nb['BB_minus_EM'] = nb['BB_accuracy'] - nb['EM_accuracy']
    ab['BB_minus_EM'] = ab['BB_accuracy'] - ab['EM_accuracy']

    print("\n--- Descriptive Statistics ---")
    print(f"NB BB accuracy: M={nb['BB_accuracy'].mean():.4f}, SD={nb['BB_accuracy'].std():.4f}")
    print(f"NB EM accuracy: M={nb['EM_accuracy'].mean():.4f}, SD={nb['EM_accuracy'].std():.4f}")
    print(f"AB BB accuracy: M={ab['BB_accuracy'].mean():.4f}, SD={ab['BB_accuracy'].std():.4f}")
    print(f"AB EM accuracy: M={ab['EM_accuracy'].mean():.4f}, SD={ab['EM_accuracy'].std():.4f}")

    # Normality
    stat_nb, p_nb = stats.shapiro(nb['BB_minus_EM'].dropna())
    stat_ab, p_ab = stats.shapiro(ab['BB_minus_EM'].dropna())
    
    print(f"\n--- Normality Test (Shapiro-Wilk) on Difference Scores (BB-EM) ---")
    print(f"NB diff: W = {stat_nb:.4f}, p = {p_nb:.4g} -> {'Normal' if p_nb > 0.05 else 'NOT Normal'}")
    print(f"AB diff: W = {stat_ab:.4f}, p = {p_ab:.4g} -> {'Normal' if p_ab > 0.05 else 'NOT Normal'}")

    normal = p_nb > 0.05 and p_ab > 0.05

    # Interaction test
    print("\n--- Interaction Test (comparing BB-EM difference across groups) ---")
    
    # Mann-Whitney U test
    u_stat, p_val = stats.mannwhitneyu(nb['BB_minus_EM'].dropna(), ab['BB_minus_EM'].dropna(), alternative='two-sided')
    n1 = len(nb['BB_minus_EM'].dropna())
    n2 = len(ab['BB_minus_EM'].dropna())
    r = 1 - (2 * u_stat) / (n1 * n2) # Rank-biserial correlation

    print(f"Mann-Whitney U = {u_stat:.1f}, p = {p_val:.4g}, effect size (r) = {r:.4f}")

    if p_val < 0.05:
        print(">> SIGNIFICANT INTERACTION: Abrupt cuts selectively impair BB frames more than EM frames!")
    else:
        print(">> No significant interaction: The group difference is similar for BB and EM frames.")

    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Q-Q plots for normality test visualization (only diff scores)
    stats.probplot(nb['BB_minus_EM'].dropna(), dist="norm", plot=axes[0])
    axes[0].get_lines()[0].set_markerfacecolor('#4c72b0')
    axes[0].get_lines()[0].set_markeredgecolor('#4c72b0')
    stats.probplot(ab['BB_minus_EM'].dropna(), dist="norm", plot=axes[0])
    axes[0].get_lines()[2].set_markerfacecolor('#c44e52')
    axes[0].get_lines()[2].set_markeredgecolor('#c44e52')
    axes[0].set_title('Q-Q Plot for BB-EM Accuracy Differences')

    # Raincloud-style plot for Difference Scores
    df['BB_minus_EM'] = df['BB_accuracy'] - df['EM_accuracy']
    sns.violinplot(data=df, x='group', y='BB_minus_EM', ax=axes[1], palette=['#4c72b0', '#c44e52'])
    axes[1].set_title('BB-EM Accuracy Differences by Group')
    axes[1].set_ylabel('Accuracy Difference (BB - EM) %')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'h4_interaction_non_parametric.png', dpi=300)
    print(f"\nSaved plot: {OUTPUT_DIR}/h4_interaction_non_parametric.png")

    plot_interaction_profile(df)
    plot_difference_distribution(df)

    md_content = f"""# Hypothesis 4: Group × Target Type Interaction on Accuracy

**Hypothesis:** The difference in recognition accuracy between Natural Cut and Abrupt Cut groups should be significantly LARGER for Before-Boundary (BB) frames than for Event-Middle (EM) frames.

## Normality Check (Shapiro-Wilk on Difference Scores)
- **Natural Cut Group (NB):** $W = {stat_nb:.4f}, p = {p_nb:.4g}$
- **Abrupt Cut Group (AB):** $W = {stat_ab:.4f}, p = {p_ab:.4g}$
- **Conclusion:** {"Data is normally distributed." if normal else "Data deviates from normality, warranting a non-parametric test."}

## Statistical Comparison (Mann-Whitney U Test)
- **Test:** Mann-Whitney U test on the accuracy difference scores (BB_Accuracy - EM_Accuracy).
- **Result:** $U = {u_stat:.1f}, p = {p_val:.4g}$, effect size (rank-biserial $r$) = ${r:.4f}$
- **Conclusion:** {"Significant Interaction" if p_val < 0.05 else "Not Significant Interaction"}
"""
    with open(OUTPUT_DIR / "h4_analysis_nonparametric.md", "w") as f:
        f.write(md_content)

if __name__ == '__main__':
    main()
