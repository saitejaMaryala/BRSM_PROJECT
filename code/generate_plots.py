"""
Generate Visualizations for BRSM Project
==========================================

This script creates meaningful plots showing patterns in the data:
- Accuracy comparisons by condition and frame type
- Response time distributions
- Confidence ratings analysis
- Participant-level variability
- Statistical comparisons
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
sns.set_palette("Set2")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11

# Set paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'cleaned_data'
PLOTS_DIR = BASE_DIR / 'plots'

PLOTS_DIR.mkdir(exist_ok=True)

print("="*70)
print("GENERATING VISUALIZATIONS FOR BRSM PROJECT")
print("="*70)
print()

# ============================================================================
# Load processed data
# ============================================================================
print("Loading processed data...")

recognition_data = pd.read_csv(DATA_DIR / 'recognition_trials_processed.csv')
participant_summary = pd.read_csv(DATA_DIR / 'participant_summary.csv')
participant_frame_summary = pd.read_csv(DATA_DIR / 'participant_frame_summary.csv')
participant_rec = pd.read_csv(DATA_DIR / 'participant_REC.csv')
participant_rec_frame = pd.read_csv(DATA_DIR / 'participant_REC_by_frame.csv')

# Clean condition column (strip whitespace)
recognition_data['condition'] = recognition_data['condition'].str.strip()
participant_summary['condition'] = participant_summary['condition'].str.strip()
participant_frame_summary['condition'] = participant_frame_summary['condition'].str.strip()
participant_rec['condition'] = participant_rec['condition'].str.strip()
participant_rec_frame['condition'] = participant_rec_frame['condition'].str.strip()

print(f"Loaded {len(recognition_data)} recognition trials")
print(f"Loaded {len(participant_summary)} participant summaries")
print()

# ============================================================================
# PLOT 1: Accuracy by Condition
# ============================================================================
print("Creating Plot 1: Accuracy by Condition...")

fig, ax = plt.subplots(figsize=(10, 6))

# Prepare data
acc_by_cond = participant_summary.groupby('condition')['accuracy'].agg(['mean', 'sem', 'count'])

# Bar plot with error bars
x_pos = np.arange(len(acc_by_cond))
bars = ax.bar(x_pos, acc_by_cond['mean'], yerr=acc_by_cond['sem'], 
               capsize=5, alpha=0.7, color=['#FF6B6B', '#4ECDC4'])

# Add value labels on bars
for i, (idx, row) in enumerate(acc_by_cond.iterrows()):
    ax.text(i, row['mean'] + row['sem'] + 0.01, f"{row['mean']:.3f}", 
            ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax.text(i, 0.02, f"n={int(row['count'])}", 
            ha='center', va='bottom', fontsize=10, color='white', fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels(['Abrupt Cut', 'Natural Cut'])
ax.set_ylabel('Mean Accuracy', fontsize=13, fontweight='bold')
ax.set_xlabel('Condition', fontsize=13, fontweight='bold')
ax.set_title('Recognition Accuracy by Video Condition', fontsize=15, fontweight='bold', pad=20)
ax.set_ylim(0, 1.0)
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Chance level')
ax.legend(loc='lower right')

# Statistical test
ab_acc = participant_summary[participant_summary['condition'] == 'AB']['accuracy']
nb_acc = participant_summary[participant_summary['condition'] == 'NB']['accuracy']
t_stat, p_val = stats.ttest_ind(ab_acc, nb_acc, nan_policy='omit')

# Add significance annotation
if p_val < 0.001:
    sig_text = '***'
elif p_val < 0.01:
    sig_text = '**'
elif p_val < 0.05:
    sig_text = '*'
else:
    sig_text = 'ns'

y_max = acc_by_cond['mean'].max() + acc_by_cond['sem'].max()
ax.plot([0, 1], [y_max + 0.05, y_max + 0.05], 'k-', linewidth=1.5)
ax.text(0.5, y_max + 0.06, sig_text, ha='center', va='bottom', fontsize=16)
ax.text(0.5, y_max + 0.10, f'p = {p_val:.4f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '01_accuracy_by_condition.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: 01_accuracy_by_condition.png (t={t_stat:.3f}, p={p_val:.4f})")

# ============================================================================
# PLOT 2: Accuracy by Frame Type
# ============================================================================
print("Creating Plot 2: Accuracy by Frame Type...")

fig, ax = plt.subplots(figsize=(10, 6))

# Aggregate at participant level first (to avoid pseudoreplication)
participant_frame_acc = recognition_data.groupby(['subject_id', 'frame_type'])['resp.corr'].mean().reset_index()
frame_stats = participant_frame_acc.groupby('frame_type')['resp.corr'].agg(['mean', 'sem', 'count'])

x_pos = np.arange(len(frame_stats))
bars = ax.bar(x_pos, frame_stats['mean'], yerr=frame_stats['sem'], 
               capsize=5, alpha=0.7, color=['#95E1D3', '#FFD93D'])

# Add value labels
for i, (idx, row) in enumerate(frame_stats.iterrows()):
    ax.text(i, row['mean'] + row['sem'] + 0.01, f"{row['mean']:.3f}", 
            ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax.text(i, 0.02, f"n={int(row['count'])}", 
            ha='center', va='bottom', fontsize=10, color='white', fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels(['Before Boundary (BB)', 'Event Middle (EM)'])
ax.set_ylabel('Mean Accuracy', fontsize=13, fontweight='bold')
ax.set_xlabel('Frame Type', fontsize=13, fontweight='bold')
ax.set_title('Recognition Accuracy by Frame Type', fontsize=15, fontweight='bold', pad=20)
ax.set_ylim(0, 1.0)
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Chance level')
ax.legend(loc='lower right')

# Statistical test
bb_acc = participant_frame_acc[participant_frame_acc['frame_type'] == 'BB']['resp.corr']
em_acc = participant_frame_acc[participant_frame_acc['frame_type'] == 'EM']['resp.corr']
t_stat, p_val = stats.ttest_ind(bb_acc, em_acc, nan_policy='omit')

# Add significance annotation
if p_val < 0.001:
    sig_text = '***'
elif p_val < 0.01:
    sig_text = '**'
elif p_val < 0.05:
    sig_text = '*'
else:
    sig_text = 'ns'

y_max = frame_stats['mean'].max() + frame_stats['sem'].max()
ax.plot([0, 1], [y_max + 0.05, y_max + 0.05], 'k-', linewidth=1.5)
ax.text(0.5, y_max + 0.06, sig_text, ha='center', va='bottom', fontsize=16)
ax.text(0.5, y_max + 0.10, f'p = {p_val:.4f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '02_accuracy_by_frame_type.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: 02_accuracy_by_frame_type.png (t={t_stat:.3f}, p={p_val:.4f})")

# ============================================================================
# PLOT 3: Accuracy by Condition and Frame Type (2x2 design)
# ============================================================================
print("Creating Plot 3: Accuracy by Condition × Frame Type...")

fig, ax = plt.subplots(figsize=(12, 7))

# Aggregate at participant level
cond_frame_stats = participant_frame_summary.groupby(['condition', 'frame_type'])['accuracy'].agg(
    ['mean', 'sem', 'count']
).reset_index()

# Set up positions
x = np.arange(2)  # BB and EM
width = 0.35
colors = ['#FF6B6B', '#4ECDC4']

# Plot bars for each condition
for i, cond in enumerate(['AB', 'NB']):
    cond_data = cond_frame_stats[cond_frame_stats['condition'] == cond]
    means = cond_data['mean'].values
    sems = cond_data['sem'].values
    
    bars = ax.bar(x + i*width, means, width, yerr=sems, 
                   capsize=5, label=cond, alpha=0.8, color=colors[i])
    
    # Add value labels
    for j, (m, s) in enumerate(zip(means, sems)):
        ax.text(j + i*width, m + s + 0.01, f'{m:.3f}', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_xticks(x + width / 2)
ax.set_xticklabels(['Before Boundary (BB)', 'Event Middle (EM)'])
ax.set_ylabel('Mean Accuracy', fontsize=13, fontweight='bold')
ax.set_xlabel('Frame Type', fontsize=13, fontweight='bold')
ax.set_title('Recognition Accuracy: Condition × Frame Type', fontsize=15, fontweight='bold', pad=20)
ax.set_ylim(0, 1.0)
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Chance')
ax.legend(title='Condition', title_fontsize=12, fontsize=11, loc='lower right')

plt.tight_layout()
plt.savefig(PLOTS_DIR / '03_accuracy_condition_x_frame.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: 03_accuracy_condition_x_frame.png")

# ============================================================================
# PLOT 4: Response Time by Condition
# ============================================================================
print("Creating Plot 4: Response Time by Condition...")

fig, ax = plt.subplots(figsize=(10, 6))

# Filter to correct responses only
correct_trials = recognition_data[recognition_data['resp.corr'] == 1].copy()

# Aggregate at participant level
participant_rt = correct_trials.groupby(['subject_id', 'condition'])['resp.rt'].mean().reset_index()
rt_stats = participant_rt.groupby('condition')['resp.rt'].agg(['mean', 'sem', 'count'])

x_pos = np.arange(len(rt_stats))
bars = ax.bar(x_pos, rt_stats['mean'], yerr=rt_stats['sem'], 
               capsize=5, alpha=0.7, color=['#FF6B6B', '#4ECDC4'])

# Add value labels
for i, (idx, row) in enumerate(rt_stats.iterrows()):
    ax.text(i, row['mean'] + row['sem'] + 0.2, f"{row['mean']:.2f}s", 
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels(['Abrupt Cut', 'Natural Cut'])
ax.set_ylabel('Mean Response Time (seconds)', fontsize=13, fontweight='bold')
ax.set_xlabel('Condition', fontsize=13, fontweight='bold')
ax.set_title('Response Time by Condition (Correct Trials Only)', fontsize=15, fontweight='bold', pad=20)

# Statistical test
ab_rt = participant_rt[participant_rt['condition'] == 'AB']['resp.rt']
nb_rt = participant_rt[participant_rt['condition'] == 'NB']['resp.rt']
t_stat, p_val = stats.ttest_ind(ab_rt, nb_rt, nan_policy='omit')

# Add significance
if p_val < 0.001:
    sig_text = '***'
elif p_val < 0.01:
    sig_text = '**'
elif p_val < 0.05:
    sig_text = '*'
else:
    sig_text = 'ns'

y_max = rt_stats['mean'].max() + rt_stats['sem'].max()
ax.plot([0, 1], [y_max + 0.5, y_max + 0.5], 'k-', linewidth=1.5)
ax.text(0.5, y_max + 0.6, sig_text, ha='center', va='bottom', fontsize=16)
ax.text(0.5, y_max + 1.2, f'p = {p_val:.4f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '04_rt_by_condition.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: 04_rt_by_condition.png (t={t_stat:.3f}, p={p_val:.4f})")

# ============================================================================
# PLOT 5: Response Time by Frame Type
# ============================================================================
print("Creating Plot 5: Response Time by Frame Type...")

fig, ax = plt.subplots(figsize=(10, 6))

participant_rt_frame = correct_trials.groupby(['subject_id', 'frame_type'])['resp.rt'].mean().reset_index()
rt_frame_stats = participant_rt_frame.groupby('frame_type')['resp.rt'].agg(['mean', 'sem', 'count'])

x_pos = np.arange(len(rt_frame_stats))
bars = ax.bar(x_pos, rt_frame_stats['mean'], yerr=rt_frame_stats['sem'], 
               capsize=5, alpha=0.7, color=['#95E1D3', '#FFD93D'])

for i, (idx, row) in enumerate(rt_frame_stats.iterrows()):
    ax.text(i, row['mean'] + row['sem'] + 0.2, f"{row['mean']:.2f}s", 
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels(['Before Boundary (BB)', 'Event Middle (EM)'])
ax.set_ylabel('Mean Response Time (seconds)', fontsize=13, fontweight='bold')
ax.set_xlabel('Frame Type', fontsize=13, fontweight='bold')
ax.set_title('Response Time by Frame Type (Correct Trials Only)', fontsize=15, fontweight='bold', pad=20)

# Statistical test
bb_rt = participant_rt_frame[participant_rt_frame['frame_type'] == 'BB']['resp.rt']
em_rt = participant_rt_frame[participant_rt_frame['frame_type'] == 'EM']['resp.rt']
t_stat, p_val = stats.ttest_ind(bb_rt, em_rt, nan_policy='omit')

if p_val < 0.001:
    sig_text = '***'
elif p_val < 0.01:
    sig_text = '**'
elif p_val < 0.05:
    sig_text = '*'
else:
    sig_text = 'ns'

y_max = rt_frame_stats['mean'].max() + rt_frame_stats['sem'].max()
ax.plot([0, 1], [y_max + 0.5, y_max + 0.5], 'k-', linewidth=1.5)
ax.text(0.5, y_max + 0.6, sig_text, ha='center', va='bottom', fontsize=16)
ax.text(0.5, y_max + 1.2, f'p = {p_val:.4f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '05_rt_by_frame_type.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: 05_rt_by_frame_type.png (t={t_stat:.3f}, p={p_val:.4f})")

# ============================================================================
# PLOT 6: RT Distribution by Condition (violin plot)
# ============================================================================
print("Creating Plot 6: RT Distribution by Condition...")

fig, ax = plt.subplots(figsize=(10, 7))

# Use trial-level data for distribution (but summarize per participant first)
parts = sns.violinplot(data=participant_rt, x='condition', y='resp.rt', 
                       palette=['#FF6B6B', '#4ECDC4'], ax=ax, inner='quartile')

# Overlay individual points with jitter
for i, cond in enumerate(['AB', 'NB']):
    cond_data = participant_rt[participant_rt['condition'] == cond]['resp.rt']
    x_jitter = np.random.normal(i, 0.04, size=len(cond_data))
    ax.scatter(x_jitter, cond_data, alpha=0.3, s=30, color='black')

ax.set_xticklabels(['Abrupt Cut', 'Natural Cut'])
ax.set_ylabel('Mean Response Time (seconds)', fontsize=13, fontweight='bold')
ax.set_xlabel('Condition', fontsize=13, fontweight='bold')
ax.set_title('Distribution of Response Times by Condition', fontsize=15, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '06_rt_distribution_by_condition.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: 06_rt_distribution_by_condition.png")

# ============================================================================
# PLOT 7: Confidence Ratings by Condition
# ============================================================================
print("Creating Plot 7: Confidence Ratings by Condition...")

fig, ax = plt.subplots(figsize=(10, 6))

participant_conf = recognition_data.groupby(['subject_id', 'condition'])['conf_radio.response'].mean().reset_index()
conf_stats = participant_conf.groupby('condition')['conf_radio.response'].agg(['mean', 'sem', 'count'])

x_pos = np.arange(len(conf_stats))
bars = ax.bar(x_pos, conf_stats['mean'], yerr=conf_stats['sem'], 
               capsize=5, alpha=0.7, color=['#FF6B6B', '#4ECDC4'])

for i, (idx, row) in enumerate(conf_stats.iterrows()):
    ax.text(i, row['mean'] + row['sem'] + 0.05, f"{row['mean']:.2f}", 
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels(['Abrupt Cut', 'Natural Cut'])
ax.set_ylabel('Mean Confidence Rating', fontsize=13, fontweight='bold')
ax.set_xlabel('Condition', fontsize=13, fontweight='bold')
ax.set_title('Confidence Ratings by Condition', fontsize=15, fontweight='bold', pad=20)
ax.set_ylim(1, 5)
ax.axhline(y=3, color='gray', linestyle='--', alpha=0.5, label='Midpoint')
ax.legend(loc='lower right')

# Statistical test
ab_conf = participant_conf[participant_conf['condition'] == 'AB']['conf_radio.response']
nb_conf = participant_conf[participant_conf['condition'] == 'NB']['conf_radio.response']
t_stat, p_val = stats.ttest_ind(ab_conf, nb_conf, nan_policy='omit')

if p_val < 0.001:
    sig_text = '***'
elif p_val < 0.01:
    sig_text = '**'
elif p_val < 0.05:
    sig_text = '*'
else:
    sig_text = 'ns'

y_max = conf_stats['mean'].max() + conf_stats['sem'].max()
ax.plot([0, 1], [y_max + 0.15, y_max + 0.15], 'k-', linewidth=1.5)
ax.text(0.5, y_max + 0.18, sig_text, ha='center', va='bottom', fontsize=16)
ax.text(0.5, y_max + 0.30, f'p = {p_val:.4f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '07_confidence_by_condition.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: 07_confidence_by_condition.png (t={t_stat:.3f}, p={p_val:.4f})")

# ============================================================================
# PLOT 8: Confidence by Accuracy and Condition
# ============================================================================
print("Creating Plot 8: Confidence by Accuracy and Condition...")

fig, ax = plt.subplots(figsize=(12, 7))

# Aggregate by participant first
conf_acc_data = recognition_data.groupby(['subject_id', 'condition', 'resp.corr']).agg({
    'conf_radio.response': 'mean'
}).reset_index()

conf_acc_stats = conf_acc_data.groupby(['condition', 'resp.corr'])['conf_radio.response'].agg(
    ['mean', 'sem']
).reset_index()

x = np.array([0, 1])  # Incorrect, Correct
width = 0.35
colors = ['#FF6B6B', '#4ECDC4']

for i, cond in enumerate(['AB', 'NB']):
    cond_data = conf_acc_stats[conf_acc_stats['condition'] == cond]
    means = cond_data['mean'].values
    sems = cond_data['sem'].values
    
    bars = ax.bar(x + i*width, means, width, yerr=sems, 
                   capsize=5, label=cond, alpha=0.8, color=colors[i])
    
    for j, (m, s) in enumerate(zip(means, sems)):
        ax.text(j + i*width, m + s + 0.05, f'{m:.2f}', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_xticks(x + width / 2)
ax.set_xticklabels(['Incorrect', 'Correct'])
ax.set_ylabel('Mean Confidence Rating', fontsize=13, fontweight='bold')
ax.set_xlabel('Response Accuracy', fontsize=13, fontweight='bold')
ax.set_title('Confidence Ratings by Accuracy and Condition', fontsize=15, fontweight='bold', pad=20)
ax.set_ylim(1, 5)
ax.legend(title='Condition', title_fontsize=12, fontsize=11)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '08_confidence_by_accuracy.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: 08_confidence_by_accuracy.png")

# ============================================================================
# PLOT 9: Participant-Level Variability (Accuracy)
# ============================================================================
print("Creating Plot 9: Participant-Level Accuracy Distribution...")

fig, ax = plt.subplots(figsize=(12, 7))

# Sort participants by accuracy within each condition
participant_summary_sorted = participant_summary.sort_values(['condition', 'accuracy'])
participant_summary_sorted['participant_rank'] = range(len(participant_summary_sorted))

colors_map = {'AB': '#FF6B6B', 'NB': '#4ECDC4'}
for cond in ['AB', 'NB']:
    cond_data = participant_summary_sorted[participant_summary_sorted['condition'] == cond]
    ax.scatter(cond_data['participant_rank'], cond_data['accuracy'], 
               label=cond, alpha=0.6, s=50, color=colors_map[cond])

ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Chance level')
ax.set_ylabel('Accuracy', fontsize=13, fontweight='bold')
ax.set_xlabel('Participant (sorted by accuracy)', fontsize=13, fontweight='bold')
ax.set_title('Participant-Level Accuracy Distribution', fontsize=15, fontweight='bold', pad=20)
ax.set_ylim(0, 1.05)
ax.legend(title='Condition', fontsize=11)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '09_participant_accuracy_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: 09_participant_accuracy_distribution.png")

# ============================================================================
# PLOT 10: REC Index by Condition
# ============================================================================
print("Creating Plot 10: REC (Recognition Memory Index) by Condition...")

fig, ax = plt.subplots(figsize=(10, 6))

rec_stats = participant_rec.groupby('condition')['REC'].agg(['mean', 'sem', 'count'])

x_pos = np.arange(len(rec_stats))
bars = ax.bar(x_pos, rec_stats['mean'], yerr=rec_stats['sem'], 
               capsize=5, alpha=0.7, color=['#FF6B6B', '#4ECDC4'])

for i, (idx, row) in enumerate(rec_stats.iterrows()):
    ax.text(i, row['mean'] + row['sem'] + 0.01, f"{row['mean']:.3f}", 
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels(['Abrupt Cut', 'Natural Cut'])
ax.set_ylabel('REC Index', fontsize=13, fontweight='bold')
ax.set_xlabel('Condition', fontsize=13, fontweight='bold')
ax.set_title('Recognition Memory Index (REC) by Condition', fontsize=15, fontweight='bold', pad=20)
ax.set_ylim(0, 1.0)
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Chance level')
ax.legend(loc='lower right')

# Statistical test
ab_rec = participant_rec[participant_rec['condition'] == 'AB']['REC']
nb_rec = participant_rec[participant_rec['condition'] == 'NB']['REC']
t_stat, p_val = stats.ttest_ind(ab_rec, nb_rec, nan_policy='omit')

if p_val < 0.001:
    sig_text = '***'
elif p_val < 0.01:
    sig_text = '**'
elif p_val < 0.05:
    sig_text = '*'
else:
    sig_text = 'ns'

y_max = rec_stats['mean'].max() + rec_stats['sem'].max()
ax.plot([0, 1], [y_max + 0.05, y_max + 0.05], 'k-', linewidth=1.5)
ax.text(0.5, y_max + 0.06, sig_text, ha='center', va='bottom', fontsize=16)
ax.text(0.5, y_max + 0.10, f'p = {p_val:.4f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '10_REC_by_condition.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: 10_REC_by_condition.png (t={t_stat:.3f}, p={p_val:.4f})")

# ============================================================================
# PLOT 11: REC by Condition and Frame Type
# ============================================================================
print("Creating Plot 11: REC by Condition × Frame Type...")

fig, ax = plt.subplots(figsize=(12, 7))

rec_frame_stats = participant_rec_frame.groupby(['condition', 'frame_type'])['REC'].agg(
    ['mean', 'sem']
).reset_index()

x = np.arange(2)
width = 0.35
colors = ['#FF6B6B', '#4ECDC4']

for i, cond in enumerate(['AB', 'NB']):
    cond_data = rec_frame_stats[rec_frame_stats['condition'] == cond]
    means = cond_data['mean'].values
    sems = cond_data['sem'].values
    
    bars = ax.bar(x + i*width, means, width, yerr=sems, 
                   capsize=5, label=cond, alpha=0.8, color=colors[i])
    
    for j, (m, s) in enumerate(zip(means, sems)):
        ax.text(j + i*width, m + s + 0.01, f'{m:.3f}', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_xticks(x + width / 2)
ax.set_xticklabels(['Before Boundary (BB)', 'Event Middle (EM)'])
ax.set_ylabel('REC Index', fontsize=13, fontweight='bold')
ax.set_xlabel('Frame Type', fontsize=13, fontweight='bold')
ax.set_title('Recognition Memory Index (REC): Condition × Frame Type', 
             fontsize=15, fontweight='bold', pad=20)
ax.set_ylim(0, 1.0)
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Chance')
ax.legend(title='Condition', title_fontsize=12, fontsize=11, loc='lower right')

plt.tight_layout()
plt.savefig(PLOTS_DIR / '11_REC_condition_x_frame.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: 11_REC_condition_x_frame.png")

# ============================================================================
# PLOT 12: Scatter Plot - Accuracy vs RT
# ============================================================================
print("Creating Plot 12: Accuracy vs Response Time...")

fig, ax = plt.subplots(figsize=(10, 7))

colors_map = {'AB': '#FF6B6B', 'NB': '#4ECDC4'}
for cond in ['AB', 'NB']:
    cond_data = participant_summary[participant_summary['condition'] == cond]
    ax.scatter(cond_data['mean_rt'], cond_data['accuracy'], 
               label=cond, alpha=0.6, s=80, color=colors_map[cond])

ax.set_xlabel('Mean Response Time (seconds)', fontsize=13, fontweight='bold')
ax.set_ylabel('Accuracy', fontsize=13, fontweight='bold')
ax.set_title('Relationship Between Accuracy and Response Time', 
             fontsize=15, fontweight='bold', pad=20)
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.3)
ax.legend(title='Condition', fontsize=11)

# Add correlation for each condition
for cond in ['AB', 'NB']:
    cond_data = participant_summary[participant_summary['condition'] == cond]
    r, p = stats.pearsonr(cond_data['mean_rt'].dropna(), 
                          cond_data['accuracy'].dropna())
    print(f"  {cond} Accuracy-RT correlation: r={r:.3f}, p={p:.4f}")

plt.tight_layout()
plt.savefig(PLOTS_DIR / '12_accuracy_vs_rt.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: 12_accuracy_vs_rt.png")

# ============================================================================
# Summary Statistics File
# ============================================================================
print("\nCreating summary statistics file...")

summary_text = []
summary_text.append("="*70)
summary_text.append("BRSM PROJECT - STATISTICAL SUMMARY")
summary_text.append("="*70)
summary_text.append("")

# Overall stats
summary_text.append("OVERALL STATISTICS")
summary_text.append("-" * 40)
summary_text.append(f"Total participants: {len(participant_summary)}")
summary_text.append(f"  - Abrupt Cut (AB): {(participant_summary['condition']=='AB').sum()}")
summary_text.append(f"  - Natural Cut (NB): {(participant_summary['condition']=='NB').sum()}")
summary_text.append(f"Total recognition trials: {len(recognition_data)}")
summary_text.append("")

# Accuracy comparisons
summary_text.append("ACCURACY COMPARISONS")
summary_text.append("-" * 40)

ab_acc = participant_summary[participant_summary['condition'] == 'AB']['accuracy']
nb_acc = participant_summary[participant_summary['condition'] == 'NB']['accuracy']
t_stat, p_val = stats.ttest_ind(ab_acc, nb_acc, nan_policy='omit')

summary_text.append(f"Accuracy by Condition:")
summary_text.append(f"  AB: M={ab_acc.mean():.4f}, SD={ab_acc.std():.4f}, n={len(ab_acc)}")
summary_text.append(f"  NB: M={nb_acc.mean():.4f}, SD={nb_acc.std():.4f}, n={len(nb_acc)}")
summary_text.append(f"  Independent t-test: t={t_stat:.3f}, p={p_val:.4f}")
summary_text.append("")

# RT comparisons
summary_text.append("RESPONSE TIME COMPARISONS (Correct Trials)")
summary_text.append("-" * 40)

participant_rt = correct_trials.groupby(['subject_id', 'condition'])['resp.rt'].mean().reset_index()
ab_rt = participant_rt[participant_rt['condition'] == 'AB']['resp.rt']
nb_rt = participant_rt[participant_rt['condition'] == 'NB']['resp.rt']
t_stat, p_val = stats.ttest_ind(ab_rt, nb_rt, nan_policy='omit')

summary_text.append(f"Response Time by Condition:")
summary_text.append(f"  AB: M={ab_rt.mean():.4f}s, SD={ab_rt.std():.4f}s, n={len(ab_rt)}")
summary_text.append(f"  NB: M={nb_rt.mean():.4f}s, SD={nb_rt.std():.4f}s, n={len(nb_rt)}")
summary_text.append(f"  Independent t-test: t={t_stat:.3f}, p={p_val:.4f}")
summary_text.append("")

# Frame type effects
summary_text.append("FRAME TYPE EFFECTS")
summary_text.append("-" * 40)

participant_frame_acc = recognition_data.groupby(['subject_id', 'frame_type'])['resp.corr'].mean().reset_index()
bb_acc = participant_frame_acc[participant_frame_acc['frame_type'] == 'BB']['resp.corr']
em_acc = participant_frame_acc[participant_frame_acc['frame_type'] == 'EM']['resp.corr']
t_stat, p_val = stats.ttest_ind(bb_acc, em_acc, nan_policy='omit')

summary_text.append(f"Accuracy by Frame Type:")
summary_text.append(f"  BB: M={bb_acc.mean():.4f}, SD={bb_acc.std():.4f}, n={len(bb_acc)}")
summary_text.append(f"  EM: M={em_acc.mean():.4f}, SD={em_acc.std():.4f}, n={len(em_acc)}")
summary_text.append(f"  Independent t-test: t={t_stat:.3f}, p={p_val:.4f}")
summary_text.append("")

# REC index
summary_text.append("RECOGNITION MEMORY INDEX (REC)")
summary_text.append("-" * 40)

ab_rec = participant_rec[participant_rec['condition'] == 'AB']['REC']
nb_rec = participant_rec[participant_rec['condition'] == 'NB']['REC']
t_stat, p_val = stats.ttest_ind(ab_rec, nb_rec, nan_policy='omit')

summary_text.append(f"REC by Condition:")
summary_text.append(f"  AB: M={ab_rec.mean():.4f}, SD={ab_rec.std():.4f}, n={len(ab_rec)}")
summary_text.append(f"  NB: M={nb_rec.mean():.4f}, SD={nb_rec.std():.4f}, n={len(nb_rec)}")
summary_text.append(f"  Independent t-test: t={t_stat:.3f}, p={p_val:.4f}")
summary_text.append("")

summary_text.append("="*70)

# Save summary
with open(PLOTS_DIR / 'statistical_summary.txt', 'w') as f:
    f.write('\n'.join(summary_text))

print(f"Saved statistical summary to {PLOTS_DIR / 'statistical_summary.txt'}")
print()

print("="*70)
print("VISUALIZATION COMPLETE!")
print("="*70)
print(f"\nAll plots saved to: {PLOTS_DIR}")
print(f"Total plots generated: 12")
print()
