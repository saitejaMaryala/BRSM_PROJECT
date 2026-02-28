import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os

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
    

if __name__ == '__main__':
    main()
