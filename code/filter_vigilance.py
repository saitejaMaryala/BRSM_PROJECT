"""
Script to filter participants based on vigilance check.
Moves files of participants who pass the vigilance check to individuals_cleaned folder.

Vigilance criteria:
Time between instruction_2.stopped and Videos.stopped should be <= 27.05 minutes (1623 seconds)
"""

import pandas as pd
import os
import shutil
from pathlib import Path

# Define paths
DATA_DIR = Path("../data/individual")
OUTPUT_DIR = Path("../data/individuals_cleaned")
FAILED_DIR = Path("../data/individuals_failed")  # Optional: to store failed files

# Create output directories if they don't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FAILED_DIR.mkdir(parents=True, exist_ok=True)

# Vigilance threshold in seconds (27.05 minutes)
VIGILANCE_THRESHOLD = 27.05 * 60  # 1623 seconds

def extract_vigilance_times(csv_path):
    """
    Extract instruction_2.stopped and Videos.stopped times from CSV file.
    These values are typically in the 4th row (index 3) of the data.
    
    Returns:
        tuple: (instruction_2_stopped, videos_stopped) or (None, None) if not found
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_path, low_memory=False)
        
        # The times are typically in row index 3 (4th row)
        # instruction_2.stopped is column index 43
        # Videos.stopped is column index 50
        
        # Find columns
        instruction_col = 'instruction_2.stopped'
        videos_col = 'Videos.stopped'
        
        if instruction_col not in df.columns or videos_col not in df.columns:
            print(f"Warning: Required columns not found in {csv_path.name}")
            return None, None
        
        # Extract values - looking for non-null values
        instruction_times = df[instruction_col].dropna()
        videos_times = df[videos_col].dropna()
        
        if len(instruction_times) == 0 or len(videos_times) == 0:
            print(f"Warning: No valid times found in {csv_path.name}")
            return None, None
        
        # Get the first valid time for each
        instruction_stopped = float(instruction_times.iloc[0])
        videos_stopped = float(videos_times.iloc[0])
        
        return instruction_stopped, videos_stopped
        
    except Exception as e:
        print(f"Error reading {csv_path.name}: {e}")
        return None, None

def calculate_encoding_duration(instruction_stopped, videos_stopped):
    """
    Calculate the encoding duration (Videos.stopped - instruction_2.stopped).
    
    Returns:
        float: Duration in seconds
    """
    if instruction_stopped is None or videos_stopped is None:
        return None
    
    duration = videos_stopped - instruction_stopped
    return duration

def passes_vigilance_check(duration):
    """
    Check if participant passes vigilance check.
    
    Args:
        duration: Encoding duration in seconds
        
    Returns:
        bool: True if passes (duration <= 27.05 minutes), False otherwise
    """
    if duration is None:
        return False
    
    return duration <= VIGILANCE_THRESHOLD

def main():
    """
    Main function to process all participant files.
    """
    # Get all CSV files in the individual directory
    csv_files = list(DATA_DIR.glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {DATA_DIR}")
        return
    
    print(f"Found {len(csv_files)} participant files")
    print(f"Vigilance threshold: {VIGILANCE_THRESHOLD} seconds ({VIGILANCE_THRESHOLD/60:.2f} minutes)")
    print("-" * 80)
    
    passed_count = 0
    failed_count = 0
    error_count = 0
    
    # Count by condition
    passed_ab_count = 0
    passed_nb_count = 0
    failed_ab_count = 0
    failed_nb_count = 0
    error_ab_count = 0
    error_nb_count = 0
    
    results = []
    
    for csv_file in sorted(csv_files):
        # Extract times
        instruction_stopped, videos_stopped = extract_vigilance_times(csv_file)
        
        # Determine condition (AB or NB)
        condition = 'AB' if '_AB_' in csv_file.name else ('NB' if '_NB_' in csv_file.name else 'Unknown')
        
        # Calculate duration
        duration = calculate_encoding_duration(instruction_stopped, videos_stopped)
        
        if duration is None:
            print(f"❌ ERROR: {csv_file.name} - Could not extract times")
            # Move error files to failed directory
            destination = FAILED_DIR / csv_file.name
            shutil.copy2(csv_file, destination)
            error_count += 1
            if condition == 'AB':
                error_ab_count += 1
            elif condition == 'NB':
                error_nb_count += 1
            
            # Store results for error cases
            participant_id = csv_file.stem.split('_')[0]
            results.append({
                'participant_id': participant_id,
                'filename': csv_file.name,
                'condition': condition,
                'encoding_duration_sec': None,
                'encoding_duration_min': None,
                'passed': False
            })
            continue
        
        # Convert duration to minutes for display
        duration_minutes = duration / 60
        
        # Check vigilance
        passed = passes_vigilance_check(duration)
        
        # Store results
        participant_id = csv_file.stem.split('_')[0]  # Extract sub100, sub101, etc.
        results.append({
            'participant_id': participant_id,
            'filename': csv_file.name,
            'condition': condition,
            'encoding_duration_sec': duration,
            'encoding_duration_min': duration_minutes,
            'passed': passed
        })
        
        if passed:
            # Move to individuals_cleaned
            destination = OUTPUT_DIR / csv_file.name
            shutil.copy2(csv_file, destination)
            print(f"✓ PASS: {csv_file.name} - {duration_minutes:.2f} min -> moved to individuals_cleaned")
            passed_count += 1
            if condition == 'AB':
                passed_ab_count += 1
            elif condition == 'NB':
                passed_nb_count += 1
        else:
            # Move to failed directory
            destination = FAILED_DIR / csv_file.name
            shutil.copy2(csv_file, destination)
            print(f"✗ FAIL: {csv_file.name} - {duration_minutes:.2f} min (exceeds {VIGILANCE_THRESHOLD/60:.2f} min)")
            failed_count += 1
            if condition == 'AB':
                failed_ab_count += 1
            elif condition == 'NB':
                failed_nb_count += 1
    
    print("-" * 80)
    print(f"\nSummary:")
    print(f"  Total files processed: {len(csv_files)}")
    print(f"  Passed vigilance check: {passed_count}")
    print(f"    - Abrupt Cut (AB): {passed_ab_count}")
    print(f"    - Natural Cut (NB): {passed_nb_count}")
    print(f"  Failed vigilance check: {failed_count}")
    print(f"    - Abrupt Cut (AB): {failed_ab_count}")
    print(f"    - Natural Cut (NB): {failed_nb_count}")
    print(f"  Errors: {error_count}")
    print(f"    - Abrupt Cut (AB): {error_ab_count}")
    print(f"    - Natural Cut (NB): {error_nb_count}")
    print(f"\nPassing files copied to: {OUTPUT_DIR}")
    print(f"Failing files copied to: {FAILED_DIR}")
    
    # Count files in all directories
    total_in_original = len(list(DATA_DIR.glob("*.csv")))
    total_in_cleaned = len(list(OUTPUT_DIR.glob("*.csv")))
    total_in_failed = len(list(FAILED_DIR.glob("*.csv")))
    
    print(f"\nFile counts in directories:")
    print(f"  {DATA_DIR}: {total_in_original} files")
    print(f"  {OUTPUT_DIR}: {total_in_cleaned} files")
    print(f"  {FAILED_DIR}: {total_in_failed} files")

if __name__ == "__main__":
    main()
