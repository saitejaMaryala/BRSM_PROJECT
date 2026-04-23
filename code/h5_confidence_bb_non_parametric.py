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
OUTPUT_DIR = Path("../exploration_output/h5_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_confidence_data():
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
            
            trial_data['conf_radio.response'] = pd.to_numeric(trial_data['conf_radio.response'], errors='coerce')

            bb_trials = trial_data[trial_data['target_img'].astype(str).str.contains('BB_T', na=False)]
            em_trials = trial_data[trial_data['target_img'].astype(str).str.contains('EM_T', na=False)]
            
            if bb_trials.empty or em_trials.empty:
                continue

            all_data.append({
                'participant': participant_id,
                'group': condition,
                'BB_conf': bb_trials['conf_radio.response'].mean(),
                'EM_conf': em_trials['conf_radio.response'].mean()
            })
            
        except Exception as e:
            pass
            
    return pd.DataFrame(all_data)


def plot_interaction_profile(df):
    """Plot group means for BB and EM confidence so the interaction is visible directly."""
    plot_df = df[df['group'].isin(['NB', 'AB'])].copy()
    long_df = plot_df.melt(id_vars=['participant', 'group'], value_vars=['BB_conf', 'EM_conf'],
                      var_name='target_type', value_name='confidence')
    long_df['target_type'] = long_df['target_type'].replace({'BB_conf': 'BB', 'EM_conf': 'EM'})

    plt.figure(figsize=(8, 6))
    sns.pointplot(data=long_df, x='target_type', y='confidence', hue='group',
                  palette={'NB': '#4c72b0', 'AB': '#c44e52'}, errorbar=('ci', 68),
                  dodge=0.2, markers=['o', 's'], linestyles=['-', '--'])
    plt.title('Confidence Interaction Profile: Group by Target Type')
    plt.xlabel('Target Type')
    plt.ylabel('Mean Confidence')
    plt.ylim(1, 5)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'h5_interaction_profile.png', dpi=300)
    plt.close()


def plot_difference_distribution(df):
    """Plot the raw BB-EM confidence difference scores for each group."""
    plot_df = df[df['group'].isin(['NB', 'AB'])].copy()
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=plot_df, x='group', y='BB_minus_EM_conf', palette={'NB': '#4c72b0', 'AB': '#c44e52'})
    sns.stripplot(data=plot_df, x='group', y='BB_minus_EM_conf', color='black', alpha=0.35, jitter=True)
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.title('BB - EM Confidence Difference by Group')
    plt.xlabel('Group')
    plt.ylabel('Difference Score')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'h5_difference_distribution.png', dpi=300)
    plt.close()

def main():
    df = load_confidence_data()
    if df is None or df.empty: return

    print("=" * 60)
    print("H5: CONFIDENCE SELECTIVELY REDUCED FOR BB IN ABRUPT GROUP")
    print("=" * 60)

    nb = df[df['group'] == 'NB'].copy()
    ab = df[df['group'] == 'AB'].copy()

    nb['BB_minus_EM_conf'] = nb['BB_conf'] - nb['EM_conf']
    ab['BB_minus_EM_conf'] = ab['BB_conf'] - ab['EM_conf']

    print("\n--- Descriptive Statistics (Mean Confidence) ---")
    print(f"NB - BB frames: M={nb['BB_conf'].mean():.4f}, SD={nb['BB_conf'].std():.4f}")
    print(f"NB - EM frames: M={nb['EM_conf'].mean():.4f}, SD={nb['EM_conf'].std():.4f}")
    print(f"AB - BB frames: M={ab['BB_conf'].mean():.4f}, SD={ab['BB_conf'].std():.4f}")
    print(f"AB - EM frames: M={ab['EM_conf'].mean():.4f}, SD={ab['EM_conf'].std():.4f}")

    # Normality
    stat_nb, p_nb = stats.shapiro(nb['BB_minus_EM_conf'].dropna())
    stat_ab, p_ab = stats.shapiro(ab['BB_minus_EM_conf'].dropna())
    
    print(f"\n--- Normality Test (Shapiro-Wilk) on Difference Scores (BB-EM Confidence) ---")
    print(f"NB conf diff: W = {stat_nb:.4f}, p = {p_nb:.4g} -> {'Normal' if p_nb > 0.05 else 'NOT Normal'}")
    print(f"AB conf diff: W = {stat_ab:.4f}, p = {p_ab:.4g} -> {'Normal' if p_ab > 0.05 else 'NOT Normal'}")
    normal = p_nb > 0.05 and p_ab > 0.05

    # Interaction Test - Mann-Whitney U Test
    u_stat, p_int = stats.mannwhitneyu(nb['BB_minus_EM_conf'].dropna(), ab['BB_minus_EM_conf'].dropna(), alternative='two-sided')
    n1 = len(nb['BB_minus_EM_conf'].dropna())
    n2 = len(ab['BB_minus_EM_conf'].dropna())
    r = 1 - (2 * u_stat) / (n1 * n2) # Rank biserial correlation

    print(f"\n--- Interaction Test (BB-EM confidence difference, Mann-Whitney U) ---")
    print(f"U = {u_stat:.1f}, p = {p_int:.4g}, r = {r:.4f}")

    # Tests for BB and EM separately, Mann Whitney U since data likely non-normal
    u_bb, p_bb = stats.mannwhitneyu(nb['BB_conf'].dropna(), ab['BB_conf'].dropna(), alternative='two-sided')
    r_bb = 1 - (2 * u_bb) / (len(nb['BB_conf'].dropna()) * len(ab['BB_conf'].dropna()))
    print(f"\n--- BB Frame Confidence (NB vs AB): U = {u_bb:.1f}, p = {p_bb:.4g}, r = {r_bb:.4f}")

    u_em, p_em = stats.mannwhitneyu(nb['EM_conf'].dropna(), ab['EM_conf'].dropna(), alternative='two-sided')
    r_em = 1 - (2 * u_em) / (len(nb['EM_conf'].dropna()) * len(ab['EM_conf'].dropna()))
    print(f"--- EM Frame Confidence (NB vs AB): U = {u_em:.1f}, p = {p_em:.4g}, r = {r_em:.4f}")

    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Q-Q plot for confidence differences
    stats.probplot(nb['BB_minus_EM_conf'].dropna(), dist="norm", plot=axes[0])
    axes[0].get_lines()[0].set_markerfacecolor('#4c72b0')
    axes[0].get_lines()[0].set_markeredgecolor('#4c72b0')
    stats.probplot(ab['BB_minus_EM_conf'].dropna(), dist="norm", plot=axes[0])
    axes[0].get_lines()[2].set_markerfacecolor('#c44e52')
    axes[0].get_lines()[2].set_markeredgecolor('#c44e52')
    axes[0].set_title('Q-Q Plot for BB-EM Confidence Diffs')

    # Raincloud-style violin plot
    df['BB_minus_EM_conf'] = df['BB_conf'] - df['EM_conf']
    sns.violinplot(data=df, x='group', y='BB_minus_EM_conf', ax=axes[1], palette=['#4c72b0', '#c44e52'])
    axes[1].set_title('BB-EM Confidence Differences by Group')
    axes[1].set_ylabel('Confidence Diff (BB - EM)')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'h5_confidence_non_parametric.png', dpi=300, bbox_inches='tight')
    print(f"\nSaved plot: {OUTPUT_DIR}/h5_confidence_non_parametric.png")

    plot_interaction_profile(df)
    plot_difference_distribution(df)
    
    md_content = f"""# Hypothesis 5: Confidence Selectively Reduced for BB

**Hypothesis:** Participants in the Abrupt Cut group should report LOWER subjective confidence specifically for BB frames compared to the Natural group.

## Normality Check (Shapiro-Wilk on Difference Scores)
- **Natural Cut Group (NB):** $W = {stat_nb:.4f}, p = {p_nb:.4g}$
- **Abrupt Cut Group (AB):** $W = {stat_ab:.4f}, p = {p_ab:.4g}$
- **Conclusion:** {"Data is normally distributed." if normal else "Data deviates from normality, warranting a non-parametric test."}

## Statistical Comparison (Mann-Whitney U Test)
- **BB Frames Confidence (NB vs AB):** $U = {u_bb:.1f}, p = {p_bb:.4g}$, $r = {r_bb:.4f}$
- **EM Frames Confidence (NB vs AB):** $U = {u_em:.1f}, p = {p_em:.4g}$, $r = {r_em:.4f}$
- **Interaction Test (BB-EM conf diff across groups):** $U = {u_stat:.1f}, p = {p_int:.4g}$, $r = {r:.4f}$
- **Result:** {"Significant Interaction" if p_int < 0.05 else "Not Significant Interaction"}
"""
    with open(OUTPUT_DIR / "h5_analysis_nonparametric.md", "w") as f:
        f.write(md_content)

if __name__ == '__main__':
    main()
