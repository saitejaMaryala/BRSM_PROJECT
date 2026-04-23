import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
import os
import ast

# Set paths
CLEANED_DIR = Path("../data/individuals_cleaned")
OUTPUT_DIR = Path("../exploration_output/h1_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def parse_list_value(val):
    """Parse values stored as string lists like '[9.14]'"""
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)):
        return float(val)
    try:
        val_str = str(val).strip()
        if val_str.startswith('[') and val_str.endswith(']'):
            inner = val_str[1:-1].strip()
            if inner:
                return float(inner)
        return float(val_str)
    except:
        return np.nan

def load_data():
    """Load all cleaned participant files."""
    csv_files = list(CLEANED_DIR.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {CLEANED_DIR}")
        return None

    all_data = []
    print(f"Loading {len(csv_files)} participant files...")
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, low_memory=False)
            
            # Determine condition
            condition = 'AB' if '_AB_' in csv_file.name else ('NB' if '_NB_' in csv_file.name else 'Unknown')
            if condition == 'Unknown':
                continue
            participant_id = csv_file.stem.split('_')[0]
            
            # Extract trial data (where multiple choice input exists)
            trial_data = df[df['resp.corr'].notna()].copy()
            if trial_data.empty:
                continue
                
            # Parse RT and accuracy
            trial_data['resp.rt'] = trial_data['resp.rt'].apply(parse_list_value)
            trial_data['resp.corr'] = pd.to_numeric(trial_data['resp.corr'], errors='coerce')
            
            # Filter for correct trials only to calculate RT
            correct_trials = trial_data[trial_data['resp.corr'] == 1]
            
            # Calculate participant-level metrics
            mean_acc = trial_data['resp.corr'].mean() * 100
            median_rt = correct_trials['resp.rt'].median() if not correct_trials.empty else np.nan
            mean_rt = correct_trials['resp.rt'].mean() if not correct_trials.empty else np.nan
            
            all_data.append({
                'participant_id': participant_id,
                'condition': condition,
                'accuracy': mean_acc,
                'median_rt': median_rt,
                'mean_rt': mean_rt
            })
        except Exception as e:
            print(f"Error reading {csv_file.name}: {e}")
            
    return pd.DataFrame(all_data)

def perform_mann_whitney(data, variable, title):
    """Run Mann-Whitney U test and calculate effect size (Rank-Biserial Correlation)"""
    
    ab_data = data[data['condition'] == 'AB'][variable].dropna()
    nb_data = data[data['condition'] == 'NB'][variable].dropna()
    
    # Run two-sided Mann-Whitney U test
    stat, p_value = stats.mannwhitneyu(nb_data, ab_data, alternative='two-sided')
    
    # Calculate effect size: Rank-Biserial Correlation (r)
    # r = 1 - (2U / (n1 * n2))
    n1 = len(nb_data)
    n2 = len(ab_data)
    r = 1 - (2 * stat) / (n1 * n2)
    
    print("\n" + "="*50)
    print(f"Hypothesis Testing: {title}")
    print("="*50)
    print(f"Natural Cut (NB) N = {n1}, Median = {nb_data.median():.2f}")
    print(f"Abrupt Cut (AB)  N = {n2}, Median = {ab_data.median():.2f}")
    print(f"Mann-Whitney U = {stat:.2f}")
    print(f"p-value = {p_value:.4f} {'(Significant)' if p_value < 0.05 else '(Not Significant)'}")
    print(f"Effect Size (Rank-Biserial r) = {r:.4f}")

    # Plotting: Violin Plot
    plt.figure(figsize=(10, 6))
    
    # Violin plot with overlaid box plot
    sns.violinplot(x='condition', y=variable, hue='condition', data=data, 
                   palette={'AB': '#FF6B6B', 'NB': '#4ECDC4'}, inner=None, alpha=0.5, legend=False)
    
    sns.boxplot(x='condition', y=variable, data=data, width=0.2, 
                color="white", whiskerprops={'color': 'black'}, 
                capprops={'color': 'black'}, flierprops={'marker': 'o', 'markersize': 4})
    
    # Overlay swarm plot to show all individual points
    sns.stripplot(x='condition', y=variable, hue='condition', data=data, palette={'AB': 'black', 'NB': 'black'}, alpha=0.3, jitter=True, legend=False)
    
    plt.title(f'{title} by Condition\nMann-Whitney U={stat}, p={p_value:.4f}')
    plt.xlabel('Condition (AB = Abrupt, NB = Natural)')
    
    # Adjust Y label based on variable
    if 'accuracy' in variable:
        plt.ylabel('Mean Accuracy (%)')
        plt.ylim(0, 105) # Add a little padding above 100
        # Hypothesis direction arrow
        plt.annotate(
            'Expected:\nNB > AB', 
            xy=(0.5, 0.9), xycoords='axes fraction', 
            ha='center', va='center', fontsize=12, bbox=dict(boxstyle="round", alpha=0.1))
    else:
        plt.ylabel('Response Time (seconds)')
        plt.annotate(
            'Expected:\nNB < AB (Faster)', 
            xy=(0.5, 0.9), xycoords='axes fraction', 
            ha='center', va='center', fontsize=12, bbox=dict(boxstyle="round", alpha=0.1))
        
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'hypothesis_{variable}_violin.png', dpi=300)
    plt.close()

    # Plotting: Bar Plot
    plt.figure(figsize=(6, 6))
    
    # Determine estimator (median for RT, mean for accuracy)
    est = np.median if 'rt' in variable else np.mean
    
    sns.barplot(x='condition', y=variable, hue='condition', data=data, 
                palette={'AB': '#FF6B6B', 'NB': '#4ECDC4'}, 
                estimator=est, errorbar=('ci', 68), capsize=0.1, legend=False)
                
    plt.title(f'{title} by Condition\nBar Plot')
    plt.xlabel('Condition (AB = Abrupt, NB = Natural)')
    
    if 'accuracy' in variable:
        plt.ylabel('Mean Accuracy (%)')
        plt.ylim(0, 100)
    else:
        plt.ylabel('Median Response Time (seconds)')
        
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'hypothesis_{variable}_bar.png', dpi=300)
    plt.close()


def plot_distribution_diagnostics(data, variable, title):
    """Save a histogram and Q-Q plot so the distribution shape is visible before testing."""
    plot_data = data[data['condition'].isin(['AB', 'NB'])].copy()
    ab_data = plot_data[plot_data['condition'] == 'AB'][variable].dropna()
    nb_data = plot_data[plot_data['condition'] == 'NB'][variable].dropna()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    sns.histplot(data=plot_data, x=variable, hue='condition', kde=True,
                 palette={'AB': '#FF6B6B', 'NB': '#4ECDC4'}, bins=15, ax=axes[0])
    axes[0].set_title(f'{title} Distribution')
    axes[0].set_xlabel(variable.replace('_', ' ').title())

    stats.probplot(ab_data, dist='norm', plot=axes[1])
    axes[1].get_lines()[0].set_markerfacecolor('#FF6B6B')
    axes[1].get_lines()[0].set_markeredgecolor('#FF6B6B')
    stats.probplot(nb_data, dist='norm', plot=axes[1])
    axes[1].get_lines()[2].set_markerfacecolor('#4ECDC4')
    axes[1].get_lines()[2].set_markeredgecolor('#4ECDC4')
    axes[1].set_title(f'Q-Q Plot for {title}')
    axes[1].set_xlabel('Theoretical Quantiles')
    axes[1].set_ylabel('Ordered Values')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'normality_{variable}.png', dpi=300)
    plt.close()

def main():
    print("Loading data and calculating participant metrics...")
    df = load_data()
    
    if df is None or df.empty:
        print("No valid data loaded")
        return

    plot_distribution_diagnostics(df, 'accuracy', 'Participant Mean Accuracy')
    plot_distribution_diagnostics(df, 'median_rt', 'Participant Median Response Time')
        
    # Test H1a: Accuracy (Is NB > AB?)
    perform_mann_whitney(df, 'accuracy', 'Participant Mean Accuracy')
    
    # Test H1b: Response Time (Is NB < AB?)
    perform_mann_whitney(df, 'median_rt', 'Participant Median Response Time')

    print(f"\nStatistical Tests complete. Plots saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
