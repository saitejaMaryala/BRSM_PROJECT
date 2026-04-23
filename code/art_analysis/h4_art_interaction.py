import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

def align_and_rank(df, value_col, subject_col, group_col, within_col):
    """
    Performs Aligned Rank Transform (ART) for testing Interaction in a 2x2 Mixed Design.
    """
    # Calculate means
    grand_mean = df[value_col].mean()
    group_means = df.groupby(group_col)[value_col].mean()
    within_means = df.groupby(within_col)[value_col].mean()
    
    # Calculate aligned responses for Interaction
    df['aligned'] = df.apply(
        lambda row: row[value_col] - group_means[row[group_col]] - within_means[row[within_col]] + grand_mean,
        axis=1
    )
    
    # Rank aligned responses
    df['rank'] = df['aligned'].rank()
    return df

def analyze_h4_art():
    base_dir = Path('../../data/individuals_cleaned')
    csv_files = list(base_dir.glob('*.csv'))

    rows = []
    for current_file in csv_files:
        if '_AB_' in current_file.name:
            cond = 'AB'
        elif '_NB_' in current_file.name:
            cond = 'NB'
        else:
            continue
            
        pid = current_file.stem.split('_')[0]
        df = pd.read_csv(current_file, low_memory=False)
        
        # Process accuracy
        td = df[df['resp.corr'].notna()].copy()
        td['resp.corr'] = pd.to_numeric(td['resp.corr'], errors='coerce')
        
        bb = td[td['target_img'].astype(str).str.contains('BB_T', na=False)]
        em = td[td['target_img'].astype(str).str.contains('EM_T', na=False)]
        
        if len(bb) > 0 and len(em) > 0:
            rows.append({'pid': pid, 'cond': cond, 'target': 'BB', 'acc': bb['resp.corr'].mean() * 100})
            rows.append({'pid': pid, 'cond': cond, 'target': 'EM', 'acc': em['resp.corr'].mean() * 100})

    long_df = pd.DataFrame(rows)
    
    # Perform ART for Interaction
    art_df = align_and_rank(long_df, 'acc', 'pid', 'cond', 'target')
    
    # To test interaction on 2x2 mixed design using ranks, we compute the difference of the ranks
    # for each subject between the two within-subject conditions, and do an independent t-test.
    # Difference = Rank(BB) - Rank(EM)
    diff_rows = []
    for pid, grp in art_df.groupby('pid'):
        if len(grp) == 2:
            rank_bb = grp[grp['target'] == 'BB']['rank'].values[0]
            rank_em = grp[grp['target'] == 'EM']['rank'].values[0]
            cond = grp['cond'].values[0]
            diff_rows.append({'pid': pid, 'cond': cond, 'rank_diff': rank_bb - rank_em})
            
    diff_df = pd.DataFrame(diff_rows)
    
    nb_diffs = diff_df[diff_df['cond'] == 'NB']['rank_diff']
    ab_diffs = diff_df[diff_df['cond'] == 'AB']['rank_diff']
    
    # Independent t-test on rank differences (equivalent to the interaction F-test in ANOVA of ranks)
    t_stat, p_val = stats.ttest_ind(nb_diffs, ab_diffs, equal_var=True)
    
    # PLOTTING
    out_dir = Path('../../exploration_output/art_analysis')
    out_dir.mkdir(parents=True, exist_ok=True)
    
    sns.set_theme(style="whitegrid")
    
    # Plot 1: Interaction Profile of Aligned Ranks
    plt.figure(figsize=(8, 6))
    sns.pointplot(data=art_df, x='target', y='rank', hue='cond', dodge=True, markers=['o', 's'], capsize=.1, err_kws={'linewidth': 1})
    plt.title('H4 ART Analysis: Interaction Profile of Aligned Ranks (Accuracy)')
    plt.ylabel('Mean Aligned Rank')
    plt.xlabel('Target Type')
    plt.tight_layout()
    plt.savefig(out_dir / 'h4_art_interaction_profile.png', dpi=300)
    plt.close()
    
    # Plot 2: Distribution of Rank Differences
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=diff_df, x='cond', y='rank_diff', showfliers=False, color='lightgray')
    sns.stripplot(data=diff_df, x='cond', y='rank_diff', alpha=0.6, jitter=True, hue='cond', legend=False)
    plt.axhline(0, color='red', linestyle='--', alpha=0.5)
    plt.title('H4 ART Analysis: Distribution of Rank Differences (BB - EM)')
    plt.ylabel('Difference in Aligned Ranks')
    plt.xlabel('Group')
    plt.tight_layout()
    plt.savefig(out_dir / 'h4_art_rank_differences.png', dpi=300)
    plt.close()
    
    # Save Report
    with open(out_dir / 'h4_art_report.md', 'w') as f:
        f.write("# H4: Aligned Rank Transform (ART) ANOVA on Accuracy\n\n")
        f.write("To robustly test the interaction between Group (NB vs AB) and Target Type (BB vs EM) on non-normal, bounded accuracy data, we implemented the Aligned Rank Transform (ART) for non-parametric ANOVA.\n\n")
        f.write("## Methodology\n")
        f.write("1. **Alignment**: Data were aligned to isolate the interaction effect by removing the main effect of Group, the main effect of Target Type, and the grand mean.\n")
        f.write("2. **Ranking**: The aligned responses were ranked globally across all participants and conditions.\n")
        f.write("3. **Testing**: To test the interaction in this 2x2 mixed design, we computed the within-subject difference of the aligned ranks (BB - EM) and performed an independent samples t-test on these differences between the NB and AB groups. This procedure yields an exact equivalent to the F-test for interaction in a mixed ANOVA on ranks.\n\n")
        f.write("## Results\n")
        f.write(f"- **t-statistic**: {t_stat:.4f}\n")
        f.write(f"- **p-value**: {p_val:.4f}\n\n")
        if p_val < 0.05:
            f.write("**Conclusion**: The Group x Target Type interaction on accuracy is statistically significant using the ART approach.\n\n")
        else:
            f.write("**Conclusion**: We failed to find a significant Group x Target Type interaction on accuracy using the ART approach. This aligns with the previous simple Mann-Whitney analysis on unranked difference scores.\n\n")
        f.write("## Plots\n")
        f.write("![Aligned Rank Interaction Profile](h4_art_interaction_profile.png)\n\n")
        f.write("![Rank Differences Distribution](h4_art_rank_differences.png)\n")
        
    print("H4 ART Analysis complete.")

if __name__ == "__main__":
    analyze_h4_art()
