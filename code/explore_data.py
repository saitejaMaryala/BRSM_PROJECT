"""
Data Exploration Script for Cleaned Individual Data
Analyzes ONLY participants who passed vigilance check (from individuals_cleaned/).
Generates descriptive statistics, plots, and tables for trial and demographic data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Define paths
CLEANED_DIR = Path("../data/individuals_cleaned")
DEMOGRAPHIC_FILE = Path("../data/demographic_data.xlsx")
OUTPUT_DIR = Path("../exploration_output")
PLOTS_DIR = OUTPUT_DIR / "plots"
TABLES_DIR = OUTPUT_DIR / "tables"

# Create output directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

def load_all_participants():
    """
    Load all participant data from cleaned directory.
    Returns combined dataframe with all trials.
    """
    csv_files = list(CLEANED_DIR.glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {CLEANED_DIR}")
        return None
    
    print(f"Loading {len(csv_files)} participant files...")
    
    all_data = []
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, low_memory=False)
            
            # Extract participant info
            participant_id = csv_file.stem.split('_')[0]
            condition = 'AB' if '_AB_' in csv_file.name else ('NB' if '_NB_' in csv_file.name else 'Unknown')
            
            # Add metadata columns
            df['participant_id'] = participant_id
            df['condition'] = condition
            df['filename'] = csv_file.name
            
            all_data.append(df)
        except Exception as e:
            print(f"Error loading {csv_file.name}: {e}")
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        print(f"Loaded {len(combined_df)} total rows from {len(all_data)} participants")
        return combined_df
    
    return None

def load_demographics():
    """
    Load demographic data from Excel file.
    """
    try:
        if DEMOGRAPHIC_FILE.exists():
            demo_df = pd.read_excel(DEMOGRAPHIC_FILE)
            print(f"Loaded demographic data: {len(demo_df)} participants")
            return demo_df
        else:
            print(f"Demographic file not found: {DEMOGRAPHIC_FILE}")
            return None
    except Exception as e:
        print(f"Error loading demographics: {e}")
        return None

def extract_trial_data(df):
    """
    Extract only trial data (rows with actual recognition trials).
    """
    # Filter rows with recognition trial data (has resp.corr values)
    trial_data = df[df['resp.corr'].notna()].copy()
    
    # Convert numeric columns
    # Note: resp.rt and resp.keys are stored as strings with brackets like "[9.14]" or "['r']"
    # We need to parse these
    
    # Handle resp.rt - stored as "[value]" strings
    if 'resp.rt' in trial_data.columns:
        def parse_list_value(val):
            """Parse values stored as string lists like "[9.14]" """
            if pd.isna(val):
                return np.nan
            if isinstance(val, (int, float)):
                return float(val)
            try:
                # Try to parse as string list
                val_str = str(val).strip()
                if val_str.startswith('[') and val_str.endswith(']'):
                    # Remove brackets and parse
                    inner = val_str[1:-1].strip()
                    if inner:
                        return float(inner)
                return float(val_str)
            except:
                return np.nan
        
        trial_data['resp.rt'] = trial_data['resp.rt'].apply(parse_list_value)
    
    # Convert other numeric columns
    numeric_cols = ['resp.corr', 'conf_radio.response']
    for col in numeric_cols:
        if col in trial_data.columns:
            trial_data[col] = pd.to_numeric(trial_data[col], errors='coerce')
    
    print(f"Extracted {len(trial_data)} recognition trials")
    print(f"Response time stats: min={trial_data['resp.rt'].min():.2f}s, max={trial_data['resp.rt'].max():.2f}s, mean={trial_data['resp.rt'].mean():.2f}s")
    
    return trial_data

def analyze_trial_performance(trial_data):
    """
    Analyze trial-level performance metrics.
    """
    print("\n" + "="*80)
    print("TRIAL PERFORMANCE ANALYSIS")
    print("="*80)
    
    # Overall accuracy
    overall_accuracy = trial_data['resp.corr'].mean() * 100
    print(f"\nOverall Accuracy: {overall_accuracy:.2f}%")
    
    # Accuracy by condition
    accuracy_by_condition = trial_data.groupby('condition')['resp.corr'].agg(['mean', 'std', 'count'])
    accuracy_by_condition['mean'] = accuracy_by_condition['mean'] * 100
    accuracy_by_condition['std'] = accuracy_by_condition['std'] * 100
    print("\nAccuracy by Condition:")
    print(accuracy_by_condition)
    
    # Response time statistics
    print("\nResponse Time (RT) Statistics:")
    rt_stats = trial_data.groupby('condition')['resp.rt'].describe()
    print(rt_stats)
    
    # Confidence ratings
    print("\nConfidence Rating Statistics:")
    conf_stats = trial_data.groupby('condition')['conf_radio.response'].describe()
    print(conf_stats)
    
    # Save summary table
    summary_table = pd.DataFrame({
        'Metric': ['Accuracy (%)', 'Mean RT (s)', 'Mean Confidence'],
        'Abrupt Cut (AB)': [
            trial_data[trial_data['condition']=='AB']['resp.corr'].mean() * 100,
            trial_data[trial_data['condition']=='AB']['resp.rt'].mean(),
            trial_data[trial_data['condition']=='AB']['conf_radio.response'].mean()
        ],
        'Natural Cut (NB)': [
            trial_data[trial_data['condition']=='NB']['resp.corr'].mean() * 100,
            trial_data[trial_data['condition']=='NB']['resp.rt'].mean(),
            trial_data[trial_data['condition']=='NB']['conf_radio.response'].mean()
        ]
    })
    summary_table.to_csv(TABLES_DIR / "trial_performance_summary.csv", index=False)
    print(f"\nSaved summary table to: {TABLES_DIR / 'trial_performance_summary.csv'}")
    
    return accuracy_by_condition, rt_stats, conf_stats

def plot_trial_performance(trial_data):
    """
    Create visualizations for trial performance.
    """
    print("\nGenerating trial performance plots...")
    
    # 1. Accuracy comparison
    plt.figure(figsize=(8, 6))
    accuracy_by_condition = trial_data.groupby('condition')['resp.corr'].mean() * 100
    plt.bar(accuracy_by_condition.index, accuracy_by_condition.values, color=['#FF6B6B', '#4ECDC4'])
    plt.ylabel('Accuracy (%)')
    plt.title('Recognition Accuracy by Condition')
    plt.ylim([0, 100])
    plt.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='Chance')
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "accuracy_by_condition.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {PLOTS_DIR / 'accuracy_by_condition.png'}")
    plt.close()
    
    # 2. Response time boxplot
    plt.figure(figsize=(8, 6))
    trial_data.boxplot(column='resp.rt', by='condition')
    plt.ylabel('Response Time (seconds)')
    plt.title('Response Time by Condition')
    plt.xlabel('Condition')
    plt.suptitle('')  # Remove the automatic title
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "rt_by_condition.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {PLOTS_DIR / 'rt_by_condition.png'}")
    plt.close()
    
    # 3. Confidence ratings boxplot
    plt.figure(figsize=(8, 6))
    trial_data.boxplot(column='conf_radio.response', by='condition')
    plt.ylabel('Confidence Rating (1-5)')
    plt.title('Confidence by Condition')
    plt.xlabel('Condition')
    plt.suptitle('')  # Remove the automatic title
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "confidence_by_condition.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {PLOTS_DIR / 'confidence_by_condition.png'}")
    plt.close()
    
    # 4. Accuracy distribution
    plt.figure(figsize=(8, 6))
    for condition in ['AB', 'NB']:
        data = trial_data[trial_data['condition']==condition]['resp.corr'] * 100
        plt.hist(data, alpha=0.6, label=condition, bins=2, edgecolor='black')
    plt.xlabel('Accuracy (%)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Trial Accuracy')
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "accuracy_distribution.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {PLOTS_DIR / 'accuracy_distribution.png'}")
    plt.close()
    
    # 5. RT distribution
    plt.figure(figsize=(8, 6))
    for condition in ['AB', 'NB']:
        data = trial_data[trial_data['condition']==condition]['resp.rt'].dropna()
        plt.hist(data, alpha=0.6, label=condition, bins=30, edgecolor='black')
    plt.xlabel('Response Time (s)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Response Times')
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "rt_distribution.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {PLOTS_DIR / 'rt_distribution.png'}")
    plt.close()
    
    # 6. Confidence distribution
    plt.figure(figsize=(8, 6))
    for condition in ['AB', 'NB']:
        data = trial_data[trial_data['condition']==condition]['conf_radio.response'].dropna()
        plt.hist(data, alpha=0.6, label=condition, bins=5, edgecolor='black', range=(0.5, 5.5))
    plt.xlabel('Confidence Rating')
    plt.ylabel('Frequency')
    plt.title('Distribution of Confidence Ratings')
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "confidence_distribution.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {PLOTS_DIR / 'confidence_distribution.png'}")
    plt.close()
    
    # 7. Accuracy by confidence
    plt.figure(figsize=(8, 6))
    conf_accuracy = trial_data.groupby(['condition', 'conf_radio.response'])['resp.corr'].mean() * 100
    conf_accuracy = conf_accuracy.reset_index()
    for condition in ['AB', 'NB']:
        data = conf_accuracy[conf_accuracy['condition']==condition]
        plt.plot(data['conf_radio.response'], data['resp.corr'], marker='o', label=condition, linewidth=2)
    plt.xlabel('Confidence Rating')
    plt.ylabel('Accuracy (%)')
    plt.title('Accuracy by Confidence Level')
    plt.legend()
    plt.xticks([1, 2, 3, 4, 5])
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "accuracy_by_confidence.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {PLOTS_DIR / 'accuracy_by_confidence.png'}")
    plt.close()

def analyze_participant_level(trial_data):
    """
    Analyze data at participant level (aggregated).
    """
    print("\n" + "="*80)
    print("PARTICIPANT-LEVEL ANALYSIS")
    print("="*80)
    
    # Aggregate by participant
    participant_stats = trial_data.groupby(['participant_id', 'condition']).agg({
        'resp.corr': ['mean', 'std', 'count'],
        'resp.rt': ['mean', 'median', 'std'],
        'conf_radio.response': ['mean', 'std']
    }).reset_index()
    
    # Flatten column names
    participant_stats.columns = ['_'.join(col).strip('_') for col in participant_stats.columns.values]
    participant_stats.rename(columns={
        'participant_id': 'participant_id',
        'condition': 'condition',
        'resp.corr_mean': 'accuracy',
        'resp.corr_count': 'n_trials',
        'resp.rt_mean': 'mean_rt',
        'resp.rt_median': 'median_rt',
        'conf_radio.response_mean': 'mean_confidence'
    }, inplace=True)
    
    # Convert accuracy to percentage
    participant_stats['accuracy'] = participant_stats['accuracy'] * 100
    
    print(f"\nParticipant-level summary (n={len(participant_stats)}):")
    print(participant_stats.groupby('condition')[['accuracy', 'mean_rt', 'mean_confidence']].describe())
    
    # Save participant-level data
    participant_stats.to_csv(TABLES_DIR / "participant_level_stats.csv", index=False)
    print(f"\nSaved: {TABLES_DIR / 'participant_level_stats.csv'}")
    
    return participant_stats

def plot_participant_distributions(participant_stats):
    """
    Plot participant-level distributions.
    """
    print("\nGenerating participant-level plots...")
    
    # 1. Accuracy distribution by condition
    plt.figure(figsize=(8, 6))
    for condition in ['AB', 'NB']:
        data = participant_stats[participant_stats['condition']==condition]['accuracy'].dropna()
        if len(data) > 0:
            plt.hist(data, alpha=0.6, label=condition, bins=15, edgecolor='black')
    plt.xlabel('Accuracy (%)')
    plt.ylabel('Number of Participants')
    plt.title('Distribution of Participant Accuracy')
    plt.axvline(x=50, color='gray', linestyle='--', alpha=0.5, label='Chance')
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "participant_accuracy_distribution.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {PLOTS_DIR / 'participant_accuracy_distribution.png'}")
    plt.close()
    
    # 2. Mean RT distribution
    plt.figure(figsize=(8, 6))
    for condition in ['AB', 'NB']:
        data = participant_stats[participant_stats['condition']==condition]['mean_rt'].dropna()
        if len(data) > 0:
            plt.hist(data, alpha=0.6, label=condition, bins=15, edgecolor='black')
    plt.xlabel('Mean Response Time (s)')
    plt.ylabel('Number of Participants')
    plt.title('Distribution of Mean RT per Participant')
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "participant_rt_distribution.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {PLOTS_DIR / 'participant_rt_distribution.png'}")
    plt.close()
    
    # 3. Mean confidence distribution
    plt.figure(figsize=(8, 6))
    for condition in ['AB', 'NB']:
        data = participant_stats[participant_stats['condition']==condition]['mean_confidence'].dropna()
        if len(data) > 0:
            plt.hist(data, alpha=0.6, label=condition, bins=15, edgecolor='black')
    plt.xlabel('Mean Confidence Rating')
    plt.ylabel('Number of Participants')
    plt.title('Distribution of Mean Confidence per Participant')
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "participant_confidence_distribution.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {PLOTS_DIR / 'participant_confidence_distribution.png'}")
    plt.close()
    
    # 4. Violin plot for accuracy
    plt.figure(figsize=(8, 6))
    data_ab = participant_stats[participant_stats['condition']=='AB']['accuracy'].dropna()
    data_nb = participant_stats[participant_stats['condition']=='NB']['accuracy'].dropna()
    
    if len(data_ab) > 0 and len(data_nb) > 0:
        data_to_plot = [data_ab, data_nb]
        parts = plt.violinplot(data_to_plot, positions=[1, 2], showmeans=True, showmedians=True)
        plt.ylabel('Accuracy (%)')
        plt.title('Accuracy Distribution by Condition (Violin Plot)')
        plt.xticks([1, 2], ['AB', 'NB'])
        plt.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / "participant_accuracy_violin.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {PLOTS_DIR / 'participant_accuracy_violin.png'}")
    plt.close()

def analyze_demographics(demo_df, participant_stats):
    """
    Analyze demographic information.
    Filter to only include participants who passed vigilance check.
    """
    if demo_df is None:
        print("\nNo demographic data available.")
        return None
    
    print("\n" + "="*80)
    print("DEMOGRAPHIC ANALYSIS (Cleaned Participants Only)")
    print("="*80)
    
    # Get list of cleaned participants
    cleaned_participants = participant_stats['participant_id'].unique()
    print(f"\nTotal participants in cleaned data: {len(cleaned_participants)}")
    
    # Find the participant ID column in demographics
    # Try different possible column names
    participant_col = None
    for col in demo_df.columns:
        if 'participant' in col.lower() or 'subject' in col.lower() or 'id' in col.lower():
            participant_col = col
            break
    
    if participant_col is None:
        print("Warning: Could not identify participant ID column in demographics.")
        print("Available columns:", list(demo_df.columns))
        # Try to match by index or row number
        print("\nUsing all demographic data (cannot filter by participant ID)")
        demo_filtered = demo_df
    else:
        print(f"Using participant ID column: {participant_col}")
        
        # Standardize participant IDs for matching (lowercase, remove spaces)
        demo_df['_temp_id'] = demo_df[participant_col].astype(str).str.lower().str.strip()
        cleaned_ids_lower = [str(pid).lower().strip() for pid in cleaned_participants]
        
        # Filter demographics to only include cleaned participants
        demo_filtered = demo_df[demo_df['_temp_id'].isin(cleaned_ids_lower)].copy()
        demo_filtered = demo_filtered.drop(columns=['_temp_id'])
        
        print(f"Demographics matched for {len(demo_filtered)} cleaned participants")
        
        if len(demo_filtered) < len(cleaned_participants):
            print(f"Warning: {len(cleaned_participants) - len(demo_filtered)} cleaned participants not found in demographics")
    
    # Basic demographics
    print("\nDemographic Summary (Cleaned Participants):")
    print(demo_filtered.describe(include='all'))
    
    # Save demographic summary
    demo_summary = demo_filtered.describe(include='all')
    demo_summary.to_csv(TABLES_DIR / "demographic_summary.csv")
    print(f"\nSaved: {TABLES_DIR / 'demographic_summary.csv'}")
    
    # Save full demographic data for cleaned participants
    demo_filtered.to_csv(TABLES_DIR / "demographics_cleaned_participants.csv", index=False)
    print(f"Saved: {TABLES_DIR / 'demographics_cleaned_participants.csv'}")
    
    return demo_filtered

def plot_demographics(demo_df):
    """
    Create demographic visualizations.
    """
    if demo_df is None:
        return
    
    print("\nGenerating demographic plots...")
    
    # Determine which columns exist
    possible_cols = ['age', 'Age', 'gender', 'Gender', 'condition', 'Condition']
    available_cols = [col for col in possible_cols if col in demo_df.columns]
    
    if not available_cols:
        print("No standard demographic columns found.")
        return
    
    # Age distribution
    age_col = next((col for col in demo_df.columns if 'age' in col.lower()), None)
    if age_col:
        plt.figure(figsize=(8, 6))
        demo_df[age_col].hist(bins=15, edgecolor='black')
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        plt.title('Age Distribution')
        plt.axvline(demo_df[age_col].mean(), color='red', linestyle='--', 
                   label=f'Mean: {demo_df[age_col].mean():.1f}')
        plt.legend()
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / "demographics_age.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {PLOTS_DIR / 'demographics_age.png'}")
        plt.close()
    
    # Gender distribution
    gender_col = next((col for col in demo_df.columns if 'gender' in col.lower()), None)
    if gender_col:
        plt.figure(figsize=(8, 6))
        gender_counts = demo_df[gender_col].value_counts()
        plt.bar(gender_counts.index, gender_counts.values, edgecolor='black')
        plt.xlabel('Gender')
        plt.ylabel('Count')
        plt.title('Gender Distribution')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / "demographics_gender.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {PLOTS_DIR / 'demographics_gender.png'}")
        plt.close()

def generate_summary_report(trial_data, participant_stats, demo_df):
    """
    Generate a comprehensive summary report.
    """
    print("\n" + "="*80)
    print("GENERATING SUMMARY REPORT")
    print("="*80)
    
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("DATA EXPLORATION SUMMARY REPORT")
    report_lines.append("For Participants Who Passed Vigilance Check (individuals_cleaned/)")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # Dataset overview
    report_lines.append("DATASET OVERVIEW")
    report_lines.append("-" * 80)
    report_lines.append(f"Total Participants (Passed Vigilance): {len(participant_stats)}")
    report_lines.append(f"  - Abrupt Cut (AB): {len(participant_stats[participant_stats['condition']=='AB'])}")
    report_lines.append(f"  - Natural Cut (NB): {len(participant_stats[participant_stats['condition']=='NB'])}")
    report_lines.append(f"Total Recognition Trials: {len(trial_data)}")
    report_lines.append("")
    report_lines.append("Note: This analysis includes ONLY participants from individuals_cleaned/")
    report_lines.append("      (those who passed vigilance check and had no data errors)")
    report_lines.append("")
    
    # Performance summary
    report_lines.append("PERFORMANCE SUMMARY")
    report_lines.append("-" * 80)
    
    for condition in ['AB', 'NB']:
        condition_name = "Abrupt Cut" if condition == 'AB' else "Natural Cut"
        data = participant_stats[participant_stats['condition']==condition]
        
        report_lines.append(f"\n{condition_name} ({condition}):")
        report_lines.append(f"  Mean Accuracy: {data['accuracy'].mean():.2f}% (SD: {data['accuracy'].std():.2f})")
        report_lines.append(f"  Mean RT: {data['mean_rt'].mean():.2f}s (SD: {data['mean_rt'].std():.2f})")
        report_lines.append(f"  Mean Confidence: {data['mean_confidence'].mean():.2f} (SD: {data['mean_confidence'].std():.2f})")
    
    report_lines.append("")
    
    # Demographics
    if demo_df is not None:
        report_lines.append("DEMOGRAPHICS (Cleaned Participants Only)")
        report_lines.append("-" * 80)
        report_lines.append(f"Demographic data available for {len(demo_df)} participants")
        report_lines.append("(matched with individuals_cleaned/ directory)")
        
        age_col = next((col for col in demo_df.columns if 'age' in col.lower()), None)
        if age_col:
            report_lines.append(f"  Age: M={demo_df[age_col].mean():.1f}, SD={demo_df[age_col].std():.1f}, Range={demo_df[age_col].min():.0f}-{demo_df[age_col].max():.0f}")
        

def main():
    """
    Main execution function.
    """
    # Load data
    print("\n1. Loading participant data from individuals_cleaned/...")
    all_data = load_all_participants()
    
    if all_data is None:
        print("Failed to load participant data. Exiting.")
        return
    
    print("\n2. Loading demographic data...")
    demo_df = load_demographics()
    
    # Extract trial data
    print("\n3. Extracting trial data...")
    trial_data = extract_trial_data(all_data)
    
    # Trial-level analysis
    print("\n4. Analyzing trial performance...")
    analyze_trial_performance(trial_data)
    plot_trial_performance(trial_data)
    
    # Participant-level analysis
    print("\n5. Analyzing participant-level data...")
    participant_stats = analyze_participant_level(trial_data)
    plot_participant_distributions(participant_stats)
    
    # Demographic analysis
    print("\n6. Analyzing demographics...")
    demo_filtered = analyze_demographics(demo_df, participant_stats)
    plot_demographics(demo_filtered)
    
    # Generate summary report
    print("\n7. Generating summary report...")
    generate_summary_report(trial_data, participant_stats, demo_filtered)
    
    print("\n" + "=" * 80)
    print("EXPLORATION COMPLETE!")
    print("=" * 80)
    print(f"\nAll outputs saved to: {OUTPUT_DIR}")
    print(f"  - Plots: {PLOTS_DIR}")
    print(f"  - Tables: {TABLES_DIR}")

if __name__ == "__main__":
    main()
