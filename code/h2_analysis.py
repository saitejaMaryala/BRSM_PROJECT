import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path

# Set paths
CLEANED_DIR = Path("../data/individuals_cleaned")
OUTPUT_DIR = Path("../exploration_output/h2_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def load_bb_data():
    """Load all cleaned participant files and extract ONLY Before Boundary (BB) frames."""
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
            
            # Extract trial data
            trial_data = df[df['resp.corr'].notna()].copy()
            if trial_data.empty:
                continue
                
            # Filter specifically for Before Boundary (BB) frames
            # Based on target_img filenames containing 'BB_T'
            bb_trials = trial_data[trial_data['target_img'].astype(str).str.contains('BB_T', na=False)].copy()
            
            if bb_trials.empty:
                continue

            bb_trials['resp.corr'] = pd.to_numeric(bb_trials['resp.corr'], errors='coerce')
            
            # Calculate participant-level accuracy specifically for BB frames
            mean_acc_bb = bb_trials['resp.corr'].mean() * 100
            
            all_data.append({
                'participant_id': participant_id,
                'condition': condition,
                'accuracy_bb': mean_acc_bb,
                'bb_trial_count': len(bb_trials)
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
    
    # Plotting Normality Q-Q
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    sns.histplot(data=data, x=variable, hue='condition', kde=True, palette={'AB': '#FF6B6B', 'NB': '#4ECDC4'}, bins=15)
    plt.title(f'{title} Distribution')
    plt.xlabel('Accuracy (%)')
    
    # Q-Q Plots
    plt.subplot(1, 2, 2)
    res_ab = stats.probplot(ab_data, dist="norm")
    (osm_ab, osr_ab), (slope_ab, intercept_ab, r_ab) = res_ab
    
    res_nb = stats.probplot(nb_data, dist="norm")
    (osm_nb, osr_nb), (slope_nb, intercept_nb, r_nb) = res_nb
    
    plt.plot(osm_ab, osr_ab, marker='o', linestyle='none', color='#FF6B6B', label='AB (Abrupt Cut)')
    plt.plot(osm_ab, slope_ab * osm_ab + intercept_ab, color='#FF6B6B', linestyle='-')
    
    plt.plot(osm_nb, osr_nb, marker='o', linestyle='none', color='#4ECDC4', label='NB (Natural Cut)')
    plt.plot(osm_nb, slope_nb * osm_nb + intercept_nb, color='#4ECDC4', linestyle='-')
    
    plt.title(f'Q-Q Plot for {title}')
    plt.xlabel('Theoretical Quantiles')
    plt.ylabel('Ordered Values')
    plt.legend(loc='upper left', framealpha=0.8)
             
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'normality_{variable}.png', dpi=300)
    plt.close()


def perform_mann_whitney(data, variable, title):
    """Run Mann-Whitney U test and calculate effect size (Rank-Biserial Correlation)"""
    
    ab_data = data[data['condition'] == 'AB'][variable].dropna()
    nb_data = data[data['condition'] == 'NB'][variable].dropna()
    
    # Run two-sided Mann-Whitney U test
    stat, p_value = stats.mannwhitneyu(nb_data, ab_data, alternative='two-sided')
    
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

    # Plotting: Raincloud Plot
    plt.figure(figsize=(10, 6))
    
    # Needs to be imported at the top, adding it here for the scope 
    import ptitprince as pt
    
    # Create the Raincloud plot (Half-Violin + Boxplot + Strip/Scatter)
    pt.RainCloud(x='condition', y=variable, data=data, palette=['#FF6B6B', '#4ECDC4'], 
                 bw=.2, width_viol=.6,  ax=None, orient='h', alpha=.65, dodge=True, pointplot=False, move=.2)
    
    plt.title(f'{title} by Condition\nMann-Whitney U={stat}, p={p_value:.4f}')
    plt.ylabel('Condition (AB = Abrupt, NB = Natural)')
    plt.xlabel('Mean Accuracy on BB Frames (%)')
    plt.xlim(0, 110) # Using xlim because orient='h' flips the axes
    
    plt.annotate('Expected:\nNB > AB', xy=(0.85, 0.85), xycoords='axes fraction', 
                 ha='center', va='center', fontsize=12, bbox=dict(boxstyle="round", alpha=0.1))
        
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'hypothesis_{variable}_raincloud.png', dpi=300)
    plt.close()

    # Plotting: Bar Plot
    plt.figure(figsize=(6, 6))
    sns.barplot(x='condition', y=variable, hue='condition', data=data, 
                palette={'AB': '#FF6B6B', 'NB': '#4ECDC4'}, 
                estimator=np.mean, errorbar=('ci', 68), capsize=0.1, legend=False)
                
    plt.title(f'{title} by Condition\nBar Plot')
    plt.xlabel('Condition (AB = Abrupt, NB = Natural)')
    plt.ylabel('Mean Accuracy on BB Frames (%)')
    plt.ylim(0, 100)
        
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'hypothesis_{variable}_bar.png', dpi=300)
    plt.close()

def main():
    print("Loading data and filtering for Before Boundary (BB) frames...")
    df = load_bb_data()
    
    if df is None or df.empty:
        print("No valid data loaded")
        return
        
    print(f"\nAverage BB trials analyzed per participant: {df['bb_trial_count'].mean():.1f}")
    
    # Check H2 Normality 
    # check_normality(df, 'accuracy_bb', 'Participant Mean Accuracy (BB Frames)')
    
    # Test H2: Accuracy on BB frames (Is NB > AB?)
    perform_mann_whitney(df, 'accuracy_bb', 'Participant Mean Accuracy (BB Frames)')

    print(f"\nStatistical Tests complete. Plots saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
