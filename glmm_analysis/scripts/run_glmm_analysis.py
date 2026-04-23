import pandas as pd
import statsmodels.formula.api as smf
import seaborn as sns
import matplotlib.pyplot as plt
import os
import json

# Ensure we're running from the scripts/ directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Define output directories
PLOTS_DIR = '../outputs/plots'
RESULTS_DIR = '../outputs/results'
os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# 1. LOAD AND PREPROCESS DATA
print("Loading data...")
df = pd.read_csv('../../cleaned_data/cleaned_trials.csv')

# Drop 'Unknown' group to avoid modeling issues
df = df[df['group'] != 'Unknown']

# The data is at trial level, let's aggregate to participant-level %.
# We need it in long format: participant, group, target, accuracy, confidence
agg_df = df.groupby(['participant', 'group', 'target_type']).agg({
    'resp.corr': 'mean',
    'confidence': 'mean'
}).reset_index()

# Rename columns for easier access in formulas
agg_df = agg_df.rename(columns={
    'resp.corr': 'accuracy',
    'target_type': 'target'
})

print("Aggregated Data Sample:")
print(agg_df.head())


# Function to extract coefficients to CSV
def save_model_tables(model_result, name):
    # Save the full summary
    with open(f'{RESULTS_DIR}/{name}_model_summary.txt', 'w') as f:
        f.write(model_result.summary().as_text())
    
    # Save extracted JSON
    pvalues = model_result.pvalues
    coefs = model_result.params
    bse = model_result.bse
    
    results_dict = {}
    for idx in coefs.index:
        results_dict[idx] = {
            'coefficient': coefs[idx],
            'std_error': bse[idx],
            'p_value': pvalues[idx]
        }
        
    with open(f'{RESULTS_DIR}/{name}_structured_results.json', 'w') as f:
        json.dump(results_dict, f, indent=4)


# 2. RUN GLMM FOR H4 (Accuracy)
print("\n--- Fitting H4: Accuracy GLMM ---")
# We use linear mixed model on the percentage accuracy
m_h4 = smf.mixedlm("accuracy ~ group * target", agg_df, groups=agg_df["participant"])
res_h4 = m_h4.fit()
save_model_tables(res_h4, 'h4')

# 3. RUN GLMM FOR H5 (Confidence)
print("\n--- Fitting H5: Confidence GLMM ---")
m_h5 = smf.mixedlm("confidence ~ group * target", agg_df, groups=agg_df["participant"])
res_h5 = m_h5.fit()
save_model_tables(res_h5, 'h5')

# 4. PLOTTING

# Style settings
sns.set_theme(style="whitegrid")
colors = ["#4c72b0", "#dd8452"]  # AB vs NB approx

# Helper to avoid repetitive code
def generate_plots(data, y_var, name_prefix):
    # (A) Interaction Plot
    plt.figure(figsize=(6, 5))
    sns.pointplot(data=data, x='target', y=y_var, hue='group', errorbar='se', palette=colors, dodge=True, markers=['o', 's'], capsize=0.1)
    plt.title(f'{name_prefix.upper()} Interaction Plot: {y_var.capitalize()} by Group and Target')
    plt.ylabel(y_var.capitalize())
    plt.xlabel('Target Type (BB vs EM)')
    plt.legend(title='Group')
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/{name_prefix}_interaction_plot.png', dpi=300)
    plt.close()

    # (B) Boxplot
    plt.figure(figsize=(6, 5))
    sns.boxplot(data=data, x='target', y=y_var, hue='group', palette=colors)
    plt.title(f'{name_prefix.upper()} Boxplot: {y_var.capitalize()} by Group and Target')
    plt.ylabel(y_var.capitalize())
    plt.xlabel('Target Type')
    plt.legend(title='Group')
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/{name_prefix}_boxplot.png', dpi=300)
    plt.close()

    # (C) Difference Score Plot (BB - EM)
    # Pivot dataset for difference calculation
    pivot_df = data.pivot(index=['participant', 'group'], columns='target', values=y_var).reset_index()
    pivot_df['delta'] = pivot_df['BB'] - pivot_df['EM']
    
    plt.figure(figsize=(6, 5))
    sns.kdeplot(data=pivot_df, x='delta', hue='group', fill=True, common_norm=False, palette=colors)
    # Add a zero line
    plt.axvline(0, color='black', linestyle='--', alpha=0.5)
    plt.title(f'{name_prefix.upper()} Difference Score (BB - EM)')
    plt.xlabel(f'Δ {y_var.capitalize()} (BB - EM)')
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/{name_prefix}_delta_plot.png', dpi=300)
    plt.close()

print("\nGenerating plots for H4...")
generate_plots(agg_df, 'accuracy', 'h4')

print("Generating plots for H5...")
generate_plots(agg_df, 'confidence', 'h5')

print("\nAnalysis complete! Outputs generated in glmm_analysis/outputs/")
