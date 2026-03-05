"""
Initial Data Exploration for BRSM Project
==========================================

This script performs initial data exploration including:
- Loading and preprocessing participant data
- Applying vigilance criterion
- Computing REC and LDI indices
- Calculating mean accuracy and RT by condition and frame type
- Generating participant-level and trial-level summaries
"""

import pandas as pd
import numpy as np
import os
import glob
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data' / 'individual'
OUTPUT_DIR = BASE_DIR / 'cleaned_data'
PLOTS_DIR = BASE_DIR / 'plots'

# Create output directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
PLOTS_DIR.mkdir(exist_ok=True)

print("="*70)
print("BRSM PROJECT - INITIAL DATA EXPLORATION")
print("="*70)
print()

# ============================================================================
# STEP 1: Load all participant data
# ============================================================================
print("Step 1: Loading participant data...")

all_files = sorted(glob.glob(str(DATA_DIR / "sub*.csv")))
print(f"Found {len(all_files)} participant files")

# Filter out subjects 1-13 (though they shouldn't exist in the data)
all_files = [f for f in all_files if not any(
    f"sub{i}_" in os.path.basename(f) for i in range(1, 14)
)]
print(f"After excluding subjects 1-13: {len(all_files)} files")

# Load data
data_list = []
vigilance_summary = []

for file_path in all_files:
    filename = os.path.basename(file_path)
    
    # Extract subject ID and condition from filename
    parts = filename.split('_')
    subject_id = parts[0]
    condition = parts[1]  # AB or NB
    
    # Read the file
    df = pd.read_csv(file_path, low_memory=False)
    
    # Skip first two header rows and process the actual data
    df = df.iloc[2:].reset_index(drop=True)
    
    # Add subject info
    df['subject_id'] = subject_id
    df['condition'] = condition.strip()  # Remove whitespace from condition
    
    data_list.append(df)

# Combine all data
print("Combining all data...")
all_data = pd.concat(data_list, ignore_index=True)

# Clean condition column (strip whitespace)
all_data['condition'] = all_data['condition'].str.strip()

print(f"Total rows loaded: {len(all_data)}")
print(f"Unique subjects: {all_data['subject_id'].nunique()}")
print()

# ============================================================================
# STEP 2: Apply vigilance criterion
# ============================================================================
print("Step 2: Applying vigilance criterion...")

# Convert timing columns to numeric
timing_cols = ['instruction_2.stopped', 'Videos.stopped']
for col in timing_cols:
    if col in all_data.columns:
        all_data[col] = pd.to_numeric(all_data[col], errors='coerce')

# Calculate encoding duration per subject
vigilance_check = all_data.groupby('subject_id').agg({
    'instruction_2.stopped': 'first',
    'Videos.stopped': 'max',
    'condition': 'first'
}).reset_index()

vigilance_check['encoding_duration_sec'] = (
    vigilance_check['Videos.stopped'] - vigilance_check['instruction_2.stopped']
)
vigilance_check['encoding_duration_min'] = vigilance_check['encoding_duration_sec'] / 60

# Apply vigilance criterion (≤ 27.05 minutes)
VIGILANCE_THRESHOLD = 27.05
vigilance_check['passes_vigilance'] = vigilance_check['encoding_duration_min'] <= VIGILANCE_THRESHOLD

print(f"Vigilance threshold: {VIGILANCE_THRESHOLD} minutes")
print(f"Subjects passing vigilance: {vigilance_check['passes_vigilance'].sum()}")
print(f"Subjects failing vigilance: {(~vigilance_check['passes_vigilance']).sum()}")

# Get list of subjects who pass vigilance
valid_subjects = vigilance_check[vigilance_check['passes_vigilance']]['subject_id'].tolist()

# Filter data to only include valid subjects
all_data = all_data[all_data['subject_id'].isin(valid_subjects)].copy()

print(f"Data after vigilance filtering: {len(all_data)} rows, {len(valid_subjects)} subjects")
print()

# Save vigilance summary
vigilance_check.to_csv(OUTPUT_DIR / 'vigilance_summary.csv', index=False)
print(f"Saved vigilance summary to {OUTPUT_DIR / 'vigilance_summary.csv'}")
print()

# ============================================================================
# STEP 3: Process recognition trial data
# ============================================================================
print("Step 3: Processing recognition trial data...")

# Filter to only recognition trials (those with movie_id)
recognition_data = all_data[all_data['movie_id'].notna()].copy()

# Convert key columns to appropriate types
recognition_data['movie_id'] = pd.to_numeric(recognition_data['movie_id'], errors='coerce')
recognition_data['resp.corr'] = pd.to_numeric(recognition_data['resp.corr'], errors='coerce')
recognition_data['conf_radio.response'] = pd.to_numeric(recognition_data['conf_radio.response'], errors='coerce')

# Handle RT data - it's stored in recogloop.resp.rt as string representation of list
def extract_rt(rt_str):
    """Extract RT value from string representation of list"""
    if pd.isna(rt_str):
        return np.nan
    try:
        # Remove brackets and convert to float
        rt_str = str(rt_str).strip()
        if rt_str.startswith('[') and rt_str.endswith(']'):
            rt_str = rt_str[1:-1]  # Remove brackets
            if rt_str:
                return float(rt_str)
    except:
        pass
    return np.nan

# Try to extract RT from the appropriate column
if 'recogloop.resp.rt' in recognition_data.columns:
    recognition_data['resp.rt'] = recognition_data['recogloop.resp.rt'].apply(extract_rt)
else:
    recognition_data['resp.rt'] = pd.to_numeric(recognition_data['resp.rt'], errors='coerce')

# Extract frame type from target_img (BB = Before Boundary, EM = Event Middle)
def extract_frame_type(img_name):
    if pd.isna(img_name):
        return None
    if '_BB_' in img_name:
        return 'BB'
    elif '_EM_' in img_name:
        return 'EM'
    return None

recognition_data['frame_type'] = recognition_data['target_img'].apply(extract_frame_type)

# Remove rows with missing critical data
recognition_data = recognition_data.dropna(subset=['movie_id', 'resp.corr', 'frame_type'])

print(f"Recognition trials: {len(recognition_data)}")
print(f"Trials by condition:")
print(recognition_data['condition'].value_counts())
print()
print(f"Trials by frame type:")
print(recognition_data['frame_type'].value_counts())
print()

# ============================================================================
# STEP 4: Compute summary statistics
# ============================================================================
print("Step 4: Computing summary statistics...")

# Overall accuracy by condition
accuracy_by_condition = recognition_data.groupby('condition').agg({
    'resp.corr': ['mean', 'std', 'count']
}).round(4)
accuracy_by_condition.columns = ['mean_accuracy', 'std_accuracy', 'n_trials']

print("Accuracy by Condition:")
print(accuracy_by_condition)
print()

# Accuracy by frame type
accuracy_by_frame = recognition_data.groupby('frame_type').agg({
    'resp.corr': ['mean', 'std', 'count']
}).round(4)
accuracy_by_frame.columns = ['mean_accuracy', 'std_accuracy', 'n_trials']

print("Accuracy by Frame Type:")
print(accuracy_by_frame)
print()

# Accuracy by condition and frame type
accuracy_by_cond_frame = recognition_data.groupby(['condition', 'frame_type']).agg({
    'resp.corr': ['mean', 'std', 'count']
}).round(4)
accuracy_by_cond_frame.columns = ['mean_accuracy', 'std_accuracy', 'n_trials']

print("Accuracy by Condition and Frame Type:")
print(accuracy_by_cond_frame)
print()

# Response time analysis (only for correct responses)
rt_by_condition = recognition_data[recognition_data['resp.corr'] == 1].groupby('condition').agg({
    'resp.rt': ['mean', 'median', 'std', 'count']
}).round(4)
rt_by_condition.columns = ['mean_rt', 'median_rt', 'std_rt', 'n_trials']

print("Response Time by Condition (correct trials only):")
print(rt_by_condition)
print()

# RT by frame type
rt_by_frame = recognition_data[recognition_data['resp.corr'] == 1].groupby('frame_type').agg({
    'resp.rt': ['mean', 'median', 'std', 'count']
}).round(4)
rt_by_frame.columns = ['mean_rt', 'median_rt', 'std_rt', 'n_trials']

print("Response Time by Frame Type (correct trials only):")
print(rt_by_frame)
print()

# RT by condition and frame type
rt_by_cond_frame = recognition_data[recognition_data['resp.corr'] == 1].groupby(
    ['condition', 'frame_type']
).agg({
    'resp.rt': ['mean', 'median', 'std', 'count']
}).round(4)
rt_by_cond_frame.columns = ['mean_rt', 'median_rt', 'std_rt', 'n_trials']

print("Response Time by Condition and Frame Type (correct trials only):")
print(rt_by_cond_frame)
print()

# ============================================================================
# STEP 5: Participant-level summaries
# ============================================================================
print("Step 5: Computing participant-level summaries...")

participant_summary = recognition_data.groupby(['subject_id', 'condition']).agg({
    'resp.corr': ['mean', 'count'],
    'resp.rt': 'mean',
    'conf_radio.response': 'mean'
}).round(4)
participant_summary.columns = ['accuracy', 'n_trials', 'mean_rt', 'mean_confidence']
participant_summary = participant_summary.reset_index()

print("Participant-level summary (first 10):")
print(participant_summary.head(10))
print()

# Participant summary by frame type
participant_frame_summary = recognition_data.groupby(['subject_id', 'condition', 'frame_type']).agg({
    'resp.corr': ['mean', 'count'],
    'resp.rt': 'mean'
}).round(4)
participant_frame_summary.columns = ['accuracy', 'n_trials', 'mean_rt']
participant_frame_summary = participant_frame_summary.reset_index()

print(f"Participant-frame type summary (first 10 rows):")
print(participant_frame_summary.head(10))
print()

# ============================================================================
# STEP 6: Compute REC and LDI indices
# ============================================================================
print("Step 6: Computing REC (Recognition Memory Index) and LDI (Lure Discrimination Index)...")

# NOTE: Based on the experiment design:
# - All trials present a target (previously seen) and a lure (unseen)
# - Participants choose left or right
# - resp.corr = 1 means they correctly identified the target
# - We need to infer whether they responded "old" (target) or not

# For REC computation:
# REC = P("old"|Target) - P("old"|Foil)
# In this design, "old" response means correctly identifying the target
# So REC is essentially the hit rate (proportion correct)

# Computing per-participant REC
participant_rec = recognition_data.groupby(['subject_id', 'condition']).agg({
    'resp.corr': 'mean'  # This is the hit rate
}).round(4)
participant_rec.columns = ['REC']
participant_rec = participant_rec.reset_index()

print("REC by Participant (first 10):")
print(participant_rec.head(10))
print()

# REC by condition
rec_by_condition = participant_rec.groupby('condition')['REC'].agg(['mean', 'std', 'count']).round(4)
print("Mean REC by Condition:")
print(rec_by_condition)
print()

# REC by frame type and condition
participant_rec_frame = recognition_data.groupby(['subject_id', 'condition', 'frame_type']).agg({
    'resp.corr': 'mean'
}).round(4)
participant_rec_frame.columns = ['REC']
participant_rec_frame = participant_rec_frame.reset_index()

rec_by_cond_frame = participant_rec_frame.groupby(['condition', 'frame_type'])['REC'].agg(
    ['mean', 'std', 'count']
).round(4)
print("Mean REC by Condition and Frame Type:")
print(rec_by_cond_frame)
print()

# Note: LDI computation requires "similar" responses which aren't explicitly coded in this data
# LDI = P("similar"|Lure) - P("similar"|Foil)
# This might require confidence ratings or additional response categories
# For now, we'll use confidence as a proxy for similarity judgments

print("Note: LDI calculation requires 'similar' response coding which is not explicit in the data.")
print("Using confidence ratings as a proxy for response certainty instead.")
print()

# ============================================================================
# STEP 7: Confidence analysis
# ============================================================================
print("Step 7: Analyzing confidence ratings...")

confidence_by_condition = recognition_data.groupby('condition').agg({
    'conf_radio.response': ['mean', 'std', 'count']
}).round(4)
confidence_by_condition.columns = ['mean_confidence', 'std_confidence', 'n_trials']

print("Confidence by Condition:")
print(confidence_by_condition)
print()

# Confidence by accuracy
confidence_by_accuracy = recognition_data.groupby(['condition', 'resp.corr']).agg({
    'conf_radio.response': ['mean', 'std', 'count']
}).round(4)
confidence_by_accuracy.columns = ['mean_confidence', 'std_confidence', 'n_trials']

print("Confidence by Condition and Accuracy:")
print(confidence_by_accuracy)
print()

# ============================================================================
# STEP 8: Save processed data
# ============================================================================
print("Step 8: Saving processed data...")

# Save full recognition data
recognition_data.to_csv(OUTPUT_DIR / 'recognition_trials_processed.csv', index=False)
print(f"Saved recognition trials to {OUTPUT_DIR / 'recognition_trials_processed.csv'}")

# Save participant-level summary
participant_summary.to_csv(OUTPUT_DIR / 'participant_summary.csv', index=False)
print(f"Saved participant summary to {OUTPUT_DIR / 'participant_summary.csv'}")

# Save participant-frame-level summary
participant_frame_summary.to_csv(OUTPUT_DIR / 'participant_frame_summary.csv', index=False)
print(f"Saved participant-frame summary to {OUTPUT_DIR / 'participant_frame_summary.csv'}")

# Save REC data
participant_rec.to_csv(OUTPUT_DIR / 'participant_REC.csv', index=False)
print(f"Saved participant REC to {OUTPUT_DIR / 'participant_REC.csv'}")

participant_rec_frame.to_csv(OUTPUT_DIR / 'participant_REC_by_frame.csv', index=False)
print(f"Saved participant REC by frame to {OUTPUT_DIR / 'participant_REC_by_frame.csv'}")

# Create summary statistics file
summary_stats = {
    'n_subjects_total': len(all_files),
    'n_subjects_after_vigilance': len(valid_subjects),
    'n_subjects_AB': len([s for s in valid_subjects if 'AB' in all_data[all_data['subject_id']==s]['condition'].iloc[0]]),
    'n_subjects_NB': len([s for s in valid_subjects if 'NB' in all_data[all_data['subject_id']==s]['condition'].iloc[0]]),
    'n_recognition_trials': len(recognition_data),
    'overall_accuracy': recognition_data['resp.corr'].mean(),
    'overall_mean_rt': recognition_data['resp.rt'].mean(),
    'overall_mean_confidence': recognition_data['conf_radio.response'].mean()
}

summary_df = pd.DataFrame([summary_stats])
summary_df.to_csv(OUTPUT_DIR / 'overall_summary_stats.csv', index=False)
print(f"Saved overall summary stats to {OUTPUT_DIR / 'overall_summary_stats.csv'}")

print()
print("="*70)
print("DATA EXPLORATION COMPLETE!")
print("="*70)
print(f"\nProcessed data saved to: {OUTPUT_DIR}")
print("\nKey findings:")
print(f"  - Valid subjects: {len(valid_subjects)}")
print(f"  - Overall accuracy: {summary_stats['overall_accuracy']:.4f}")
print(f"  - Overall mean RT: {summary_stats['overall_mean_rt']:.4f} seconds")
print(f"  - Overall mean confidence: {summary_stats['overall_mean_confidence']:.4f}")
print()
