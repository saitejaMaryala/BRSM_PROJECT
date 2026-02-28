import os
import glob
import pandas as pd
import numpy as np
import re

CLEANED_DATA_DIR = "../cleaned_data"

THRESHOLD_MINUTES = None #27.05

def main():
    data_dir = "../BRSM data csv"
    all_files = glob.glob(os.path.join(data_dir, "*.csv"))

    if not os.path.exists(CLEANED_DATA_DIR):
        os.makedirs(CLEANED_DATA_DIR)
    
    participants = []
    
    # Extract valid participant IDs
    for f in all_files:
        basename = os.path.basename(f)
        if basename.lower().startswith('sub'):
            sub_id_str = basename.split('_')[0].replace('sub', '')
            try:
                sub_id = int(sub_id_str)
            except:
                sub_id = sub_id_str
            participants.append((sub_id, f))
            
    # Sort by sub_id (cast to string to avoid TypeError between int and str)
    participants.sort(key=lambda x: str(x[0]))
    
    # Filter out first 13 participants
    valid_participants = [p for p in participants if (isinstance(p[0], int) and p[0] >= 14) or (not isinstance(p[0], int) and 'sub'+str(p[0]).lower() not in [f'sub{i}' for i in range(1, 14)])]
    
    data_rows = []
    trial_rows = []
    
    for sub_id, fp in valid_participants:
        df = pd.read_csv(fp)
        
        # Determine group
        basename = os.path.basename(fp)
        group = 'AB' if '_AB_' in basename else 'NB'
        
        # Final cleanup for string IDs like '41' from 'Sub41'
        try:
            clean_sub_id = int(re.search(r'\d+', str(sub_id)).group())
        except:
            clean_sub_id = sub_id
            
        # Calculate Vigilance
        if 'instruction_2.stopped' in df.columns and 'Videos.stopped' in df.columns:
            t1 = df['instruction_2.stopped'].dropna().iloc[0] if not df['instruction_2.stopped'].dropna().empty else np.nan
            t2 = df['Videos.stopped'].dropna().iloc[0] if not df['Videos.stopped'].dropna().empty else np.nan
            encoding_time_sec = t2 - t1
            encoding_time_min = encoding_time_sec / 60
        else:
            encoding_time_min = 999 
        
        if THRESHOLD_MINUTES:
            vigilance_pass = encoding_time_min <= THRESHOLD_MINUTES
        else:
            vigilance_pass = True
        
        # Get accuracy and mean RT
        if 'recogloop.resp.corr' in df.columns:
            recog_df = df.dropna(subset=['recogloop.resp.corr']).copy()
        elif 'resp.corr' in df.columns:
            recog_df = df.dropna(subset=['resp.corr']).copy()
            recog_df['recogloop.resp.corr'] = recog_df['resp.corr']
            if 'resp.rt' in df.columns:
                recog_df['recogloop.resp.rt'] = recog_df['resp.rt']
                
        if len(recog_df) > 0:
            for col in ['recogloop.resp.corr', 'recogloop.resp.rt', 'recogloop.conf_radio.response']:
                if col in recog_df.columns:
                    recog_df[col] = recog_df[col].astype(str).str.replace(r'[\[\]]', '', regex=True)
                    recog_df[col] = pd.to_numeric(recog_df[col], errors='coerce')

            accuracy = recog_df['recogloop.resp.corr'].mean()
            mean_rt = recog_df['recogloop.resp.rt'].mean()
            
            # Target Types
            recog_df['target_type'] = recog_df['target_img'].apply(lambda x: 'BB' if 'BB' in str(x) else ('EM' if 'EM' in str(x) else 'Unknown'))
            bb_acc = recog_df[recog_df['target_type'] == 'BB']['recogloop.resp.corr'].mean()
            em_acc = recog_df[recog_df['target_type'] == 'EM']['recogloop.resp.corr'].mean()
            mean_conf = recog_df['recogloop.conf_radio.response'].mean() if 'recogloop.conf_radio.response' in recog_df.columns else np.nan
            
            # Store trials
            for idx, row in recog_df.iterrows():
                trial_rows.append({
                    'participant': clean_sub_id,
                    'group': group,
                    'vigilance_pass': vigilance_pass,
                    'target_type': row['target_type'],
                    'correct': row['recogloop.resp.corr'],
                    'rt': row['recogloop.resp.rt'],
                    'confidence': row.get('recogloop.conf_radio.response', np.nan)
                })
        else:
            accuracy = mean_rt = bb_acc = em_acc = mean_conf = np.nan
        
        # In a 2AFC test without explicit "new" foils, 
        # REC and LDI simplify to overall discrimination accuracy.
        # REC = P(Hit) which is measured directly by accuracy in this setup
        # LDI similarly matches general hit rate vs lures since all distractor images are lures here
        rec_score = accuracy if not pd.isna(accuracy) else np.nan
        ldi_score = accuracy if not pd.isna(accuracy) else np.nan
            
        data_rows.append({
            'participant': clean_sub_id,
            'group': group,
            'encoding_time_min': encoding_time_min,
            'vigilance_pass': vigilance_pass,
            'accuracy': accuracy,
            'REC': rec_score,
            'LDI': ldi_score,
            'mean_rt': mean_rt,
            'BB_accuracy': bb_acc,
            'EM_accuracy': em_acc,
            'mean_confidence': mean_conf
        })
        
    summary_df = pd.DataFrame(data_rows)
    trials_df = pd.DataFrame(trial_rows)
    
    cleaned_df = summary_df[summary_df['vigilance_pass'] == True].copy()
    cleaned_trials_df = trials_df[trials_df['vigilance_pass'] == True].copy()
    
    # Merge demographic data
    try:
        demo_df = pd.read_excel('../Demographic data.xlsx')
        # Extract integer specifically since our clean_df is now all integers
        demo_df['participant'] = demo_df['Sub ID'].astype(str).str.extract(r'(\d+)')[0].astype(float)
        cleaned_df['participant'] = cleaned_df['participant'].astype(float)
        merged_df = pd.merge(cleaned_df, demo_df, on='participant', how='left')
    except Exception as e:
        print(f"Failed to merge demographics: {e}")
        merged_df = cleaned_df
        
    # Final robust sorting numerically
    merged_df = merged_df.sort_values(by='participant').reset_index(drop=True)
    cleaned_trials_df['participant'] = cleaned_trials_df['participant'].astype(float)
    cleaned_trials_df = cleaned_trials_df.sort_values(by='participant').reset_index(drop=True)
    
    # Save cleaned data
    merged_df.to_csv(os.path.join(CLEANED_DATA_DIR, 'cleaned_summary.csv'), index=False)
    cleaned_trials_df.to_csv(os.path.join(CLEANED_DATA_DIR, 'cleaned_trials.csv'), index=False)
    print("Preprocessed data saved to cleaned_summary.csv and cleaned_trials.csv")
    
if __name__ == '__main__':
    main()
