import os
import glob
import pandas as pd
import numpy as np

data_dir = "../BRSM data csv"
all_files = glob.glob(os.path.join(data_dir, "*.csv"))
print(f"Total files found: {len(all_files)}")

# 1. Figure out the first 13 participants
# Files format: subXXX_AB_recognitionstage_...csv
# Extract XXX
participants = []
for f in all_files:
    basename = os.path.basename(f)
    if basename.startswith('sub'):
        sub_id_str = basename.split('_')[0].replace('sub', '')
        # Handle cases where sub is string or integer
        try:
            sub_id = int(sub_id_str)
        except:
            sub_id = sub_id_str
        participants.append((sub_id, f))

# Sort by sub_id if they are integers, otherwise alphabetically
try:
    participants.sort(key=lambda x: int(x[0]))
except:
    participants.sort(key=lambda x: x[0])

print("First 15 participants in the folder:")
for p in participants[:15]:
    print(f"Sub: {p[0]}, File: {os.path.basename(p[1])}")

# 2. Check variables for a participant
df = pd.read_csv(participants[15][1]) # Pick somewhat random valid participant
print("\n--- Inspecting specific columns for participant", participants[15][0], "---")

vigilance_cols = ['instruction_2.stopped', 'Videos.stopped']
print("\nVigilance columns:")
print(df[vigilance_cols].dropna().head())

# Time taken
t1 = df['instruction_2.stopped'].dropna().iloc[0]
t2 = df['Videos.stopped'].dropna().iloc[0]
print(f"Time taken for encoding: {t2 - t1} seconds ({(t2 - t1)/60:.2f} mins)")

recog_cols = [c for c in df.columns if 'lure' in c.lower() or 'target' in c.lower() or 'corr' in c.lower() or 'resp' in c.lower()]
print("\nRecognition columns related to targets/lures/corr:")
print(recog_cols)

# Print a few rows of the recognition trials
# Find where the recognition loop ran
recog_df = df.dropna(subset=['recogloop.resp.corr'])
print("\nSample recognition trials:")
print(recog_df[['target_img', 'lure_img', 'recogloop.resp.keys', 'recogloop.resp.corr', 'recogloop.conf_radio.response']].head())
