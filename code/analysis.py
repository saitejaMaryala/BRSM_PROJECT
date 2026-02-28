import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os

plots_dir = '../plots'

def perform_ttest(group1, group2, metric_name):
    # Drop NaNs
    g1_clean = group1.dropna()
    g2_clean = group2.dropna()
    
    t_stat, p_val = stats.ttest_ind(g1_clean, g2_clean, equal_var=False)
    
    mean1, std1 = g1_clean.mean(), g1_clean.std()
    mean2, std2 = g2_clean.mean(), g2_clean.std()
    
    # Cohen's d for effect size
    n1, n2 = len(g1_clean), len(g2_clean)
    pooled_var = ((n1-1)*std1**2 + (n2-1)*std2**2) / (n1 + n2 - 2)
    cohens_d = (mean1 - mean2) / np.sqrt(pooled_var) if pooled_var > 0 else 0
    
    print(f"\n--- {metric_name} ---")
    print(f"Natural Cut (NB) [n={n1}]: Mean = {mean1:.4f}, SD = {std1:.4f}")
    print(f"Abrupt Cut (AB)  [n={n2}]: Mean = {mean2:.4f}, SD = {std2:.4f}")
    print(f"T-Statistic = {t_stat:.4f}, p-value = {p_val:.4g}")
    print(f"Cohen's d = {cohens_d:.4f}")
    
    if p_val < 0.05:
        print(">> SIGNIFICANT DIFFERENCE DETECTED (p < 0.05)")
    else:
        print(">> No significant difference.")

def main():
    df = pd.read_csv('../cleaned_data/cleaned_summary.csv')
    
    nb_group = df[df['group'] == 'NB']
    ab_group = df[df['group'] == 'AB']
    
    print("="*50)
    print("STATISTICAL ANALYSIS: NATURAL CUT vs ABRUPT CUT")
    print("="*50)
    
    print("\n1. OVERALL RECOGNITION ACCURACY (REC/LDI proxy)")
    perform_ttest(nb_group['accuracy'], ab_group['accuracy'], "Overall Accuracy")
    
    print("\n2. BEFORE BOUNDARY (BB) FRAMES ACCURACY")
    perform_ttest(nb_group['BB_accuracy'], ab_group['BB_accuracy'], "BB Frame Accuracy")
    
    print("\n3. EVENT MIDDLE (EM) FRAMES ACCURACY")
    perform_ttest(nb_group['EM_accuracy'], ab_group['EM_accuracy'], "EM Frame Accuracy")
    
    print("\n4. OVERALL RESPONSE TIMES (RT in seconds)")
    perform_ttest(nb_group['mean_rt'], ab_group['mean_rt'], "Response Times (RT)")
    
    print("\n5. CONFIDENCE RATINGS")
    perform_ttest(nb_group['mean_confidence'], ab_group['mean_confidence'], "Confidence")
    
    # -----------------------------------------------------
    # Visualization Generation
    # -----------------------------------------------------
    print("\nGenerating Visualizations...")
    
    # Set style
    sns.set_theme(style="whitegrid")
    
    # 1. Bar Plot for Accuracies (Overall, BB, EM)
    # Melt the dataframe so we can plot multiple accuracy types side-by-side
    acc_df = df[['group', 'accuracy', 'BB_accuracy', 'EM_accuracy']].melt(
        id_vars='group', 
        var_name='Metric', 
        value_name='Accuracy'
    )
    
    # Rename for cleaner plot labels
    acc_df['Metric'] = acc_df['Metric'].replace({
        'accuracy': 'Overall (REC/LDI)',
        'BB_accuracy': 'Before Boundary',
        'EM_accuracy': 'Event Middle'
    })
    
    # Create directory if it doesn't exist
    os.makedirs(plots_dir, exist_ok=True)
    acc_barplot_path = os.path.join(plots_dir, 'accuracy_barplot.png')
    plt.figure(figsize=(10, 6))
    sns.barplot(data=acc_df, x='Metric', y='Accuracy', hue='group', palette=['#4c72b0', '#c44e52'], errorbar='ci')
    plt.title('Recognition Memory Accuracy by Frame Type\n(Natural Cut vs. Abrupt Cut)', fontsize=14, pad=15)
    plt.ylabel('Proportion Correct')
    plt.xlabel('')
    plt.ylim(0.7, 1.0) # Start y-axis at 0.7 to highlight the differences better since baseline is high
    plt.legend(title='Condition', loc='upper right')
    plt.tight_layout()
    plt.savefig(acc_barplot_path, dpi=300)
    print(f"Saved: {acc_barplot_path}")
    
    # 2. Box Plot for Response Times
    rt_boxplot_path = os.path.join(plots_dir, 'rt_boxplot.png')
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x='group', y='mean_rt', palette=['#4c72b0', '#c44e52'])
    plt.title('Average Response Time during Recognition\n(Natural Cut vs. Abrupt Cut)', fontsize=14, pad=15)
    plt.ylabel('Response Time (seconds)')
    plt.xlabel('Condition')
    plt.tight_layout()
    plt.savefig(rt_boxplot_path, dpi=300)
    print(f"Saved: {rt_boxplot_path}")
    
    print("\nAnalysis Complete!")

if __name__ == '__main__':
    main()
