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

def check_normality(data, variable, title):
    """Run Shapiro-Wilk test and plot distributions"""
    
    ab_data = data[data['condition'] == 'AB'][variable].dropna()
    nb_data = data[data['condition'] == 'NB'][variable].dropna()
    
    # Statistical tests
    stat_ab, p_ab = stats.shapiro(ab_data)
    stat_nb, p_nb = stats.shapiro(nb_data)
    
    print("\n" + "="*50)
    print(f"Normality Check: {title}")
    print("="*50)
    print(f"Abrupt Cut (AB)   - Statistic: {stat_ab:.4f}, p-value: {p_ab:.4f} -> {'Normal' if p_ab > 0.05 else 'NOT Normal'}")
    print(f"Natural Cut (NB)  - Statistic: {stat_nb:.4f}, p-value: {p_nb:.4f} -> {'Normal' if p_nb > 0.05 else 'NOT Normal'}")
    
    # 1. Histogram / KDE plot
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    sns.histplot(data=data, x=variable, hue='condition', kde=True, palette={'AB': '#FF6B6B', 'NB': '#4ECDC4'}, bins=15)
    plt.title(f'{title} Distribution')
    
    # 2. Q-Q Plots
    plt.subplot(1, 2, 2)
    
    # Calculate probability plot data for AB
    res_ab = stats.probplot(ab_data, dist="norm")
    (osm_ab, osr_ab), (slope_ab, intercept_ab, r_ab) = res_ab
    
    # Calculate probability plot data for NB
    res_nb = stats.probplot(nb_data, dist="norm")
    (osm_nb, osr_nb), (slope_nb, intercept_nb, r_nb) = res_nb
    
    # Plot AB (Red)
    plt.plot(osm_ab, osr_ab, marker='o', linestyle='none', color='#FF6B6B', label='AB (Abrupt Cut)')
    plt.plot(osm_ab, slope_ab * osm_ab + intercept_ab, color='#FF6B6B', linestyle='-')
    
    # Plot NB (Teal)
    plt.plot(osm_nb, osr_nb, marker='o', linestyle='none', color='#4ECDC4', label='NB (Natural Cut)')
    plt.plot(osm_nb, slope_nb * osm_nb + intercept_nb, color='#4ECDC4', linestyle='-')
    
    plt.title(f'Q-Q Plot for {title}')
    plt.xlabel('Theoretical Quantiles')
    plt.ylabel('Ordered Values')
    
    # Add proper legend instead of text box
    plt.legend(loc='upper left', framealpha=0.8)
             
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'normality_{variable}.png', dpi=300)
    plt.close()

def main():
    print("Loading data and calculating participant metrics...")
    df = load_data()
    
    if df is None or df.empty:
        print("No valid data loaded")
        return
        
    print(df.groupby('condition')[['accuracy', 'median_rt', 'mean_rt']].describe())
    
    # Check H1a (Accuracy)
    check_normality(df, 'accuracy', 'Participant Mean Accuracy (%)')
    
    # Check H1b (Response Time)
    check_normality(df, 'median_rt', 'Participant Median Response Time (Correct Trials)')
    check_normality(df, 'mean_rt', 'Participant Mean Response Time (Correct Trials)')

    print(f"\nPlots saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
