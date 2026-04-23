import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

def align_and_rank_h5(df, value_col, subject_col, group_col, within_col):
    """
    Performs Aligned Rank Transform (ART) for testing Interaction in a 2x2 Mixed Design.
    """
    # Calculate means
    grand_mean = df[value_col].mean()
    group_means = df.groupby(group_col)[value_col].transform('mean')
    within_means = df.groupby(within_col)[value_col].transform('mean')
    
    # Calculate aligned responses for Interaction
    df['aligned'] = df[value_col] - group_means - within_means + grand_mean
    
    # Rank aligned responses globally
    df['rank'] = df['aligned'].rank()
    return df

def analyze_h5_art():
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
        
        # Process confidence
        td = df[df['resp.corr'].notna()].copy() # Use same subset of correct trial data? Or all? Based on prior script H5 confidence uses all available?
        td['conf_radio.response'] = pd.to_numeric(td.get('conf_radio.response'), errors='coerce')
        td = td.dropna(subset=['conf_radio.response'])
        
        bb = td[td['target_img'].astype(str).str.contains('BB_T', na=False)]
        em = td[td['target_img'].astype(str).str.contains('EM_T', na=False)]
        
        if len(bb) > 0 and len(em) > 0:
            rows.append({'pid': pid, 'cond': cond, 'target': 'BB', 'conf': bb['conf_radio.response'].mean()})
            rows.append({'pid': pid, 'cond': cond, 'target': 'EM', 'conf': em['conf_radio.response'].mean()})

    long_df = pd.DataFrame(rows)
    
    # Perform ART for Interaction
    art_df = align_and_rank_h5(long_df, 'conf', 'pid', 'cond', 'target')
    
    # Compute rank differences (BB - EM) for each subject
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
    
    # Independent t-test on rank differences (equivalent to the interaction F-test)
    t_stat, p_val = stats.ttest_ind(nb_diffs, ab_diffs, equal_var=True)
    
    # PLOTTING
    out_dir = Path('../../exploration_output/art_analysis')
    out_dir.mkdir(parents=True, exist_ok=True)
    
    sns.set_theme(style="whitegrid")
    
    # Plot 1: Interaction Profile of Aligned Ranks
    plt.figure(figsize=(8, 6))
    sns.pointplot(data=art_df, x='target', y='rank', hue='cond', dodge=True, markers=['o', 's'], capsize=.1, err_kws={'linewidth': 1})
    plt.title('H5 ART Analysis: Interaction Profile of Aligned Ranks (Confidence)')
    plt.ylabel('Mean Aligned Rank')
    plt.xlabel('Target Type')
    plt.tight_layout()
    plt.savefig(out_dir / 'h5_art_interaction_profile.png', dpi=300)
    plt.close()
    
    # Plot 2: Distribution of Rank Differences
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=diff_df, x='cond', y='rank_diff', showfliers=False, color='lightblue')
    sns.stripplot(data=diff_df, x='cond', y='rank_diff', alpha=0.6, jitter=True, hue='cond', legend=False)
    plt.axhline(0, color='red', linestyle='--', alpha=0.5)
    plt.title('H5 ART Analysis: Distribution of Rank Differences (BB - EM)')
    plt.ylabel('Difference in Aligned Ranks')
    plt.xlabel('Group')
    plt.tight_layout()
    plt.savefig(out_dir / 'h5_art_rank_differences.png', dpi=300)
    plt.close()
    
    # Save Report
    with open(out_dir / 'h5_art_report.md', 'w') as f:
        f.write("# H5: Aligned Rank Transform (ART) ANOVA on Confidence\n\n")
        f.write("To test the interaction between Group (NB vs AB) and Target Type (BB vs EM) on confidence on an ordinal Likert scale, the Aligned Rank Transform (ART) non-parametric ANOVA was utilized.\n\n")
        f.write("## Methodology\n")
        f.write("1. **Alignment**: Responses (mean confidence) were aligned by extracting out the main effects of Group and Target Type to isolate the interaction variance component.\n")
        f.write("2. **Ranking**: These interaction-aligned responses were then ranked across all participants.\n")
        f.write("3. **Testing**: We computed the within-subject difference between ranked BB and EM responses ($Rank_{BB} - Rank_{EM}$) and tested this difference across groups with an independent samples t-test to evaluate the interaction effect.\n\n")
        f.write("## Results\n")
        f.write(f"- **t-statistic**: {t_stat:.4f}\n")
        f.write(f"- **p-value**: {p_val:.4f}\n\n")
        if p_val < 0.05:
            f.write("**Conclusion**: The Group x Target Type interaction on confidence is statistically significant under the more robust ART methodology, confirming differences in confidence drop across groups.\n\n")
        else:
            f.write("**Conclusion**: The Group x Target Type interaction was not significant under the ART approach.\n\n")
        f.write("## Plots\n")
        f.write("![Aligned Rank Interaction Profile](h5_art_interaction_profile.png)\n\n")
        f.write("![Rank Differences Distribution](h5_art_rank_differences.png)\n")
        
    print("H5 ART Analysis complete.")

if __name__ == "__main__":
    analyze_h5_art()
