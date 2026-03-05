"""
Generate Clean, Simple Visualizations for BRSM Project
=======================================================

Creates only the most meaningful and statistically significant plots
with clean, simple aesthetics.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set clean, minimal style
sns.set_style("white")
sns.set_context("talk")
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# Set paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'cleaned_data'
PLOTS_DIR = BASE_DIR / 'plots'

PLOTS_DIR.mkdir(exist_ok=True)

# Define clean color palette - consistent across all plots
COLORS = {
    'AB': '#3498DB',  # Blue for Abrupt
    'NB': '#E74C3C',  # Red for Natural
    'BB': '#3498DB',  # Blue for Before Boundary
    'EM': '#E74C3C',  # Red for Event Middle
}

print("="*70)
print("GENERATING CLEAN VISUALIZATIONS")
print("="*70)
print()

# Load processed data
print("Loading data...")
recognition_data = pd.read_csv(DATA_DIR / 'recognition_trials_processed.csv')
participant_summary = pd.read_csv(DATA_DIR / 'participant_summary.csv')
participant_frame_summary = pd.read_csv(DATA_DIR / 'participant_frame_summary.csv')

# Clean condition column
recognition_data['condition'] = recognition_data['condition'].str.strip()
participant_summary['condition'] = participant_summary['condition'].str.strip()
participant_frame_summary['condition'] = participant_frame_summary['condition'].str.strip()

print(f"Loaded {len(participant_summary)} participants\n")

# ============================================================================
# PLOT 1: Accuracy by Condition (Main Effect)
# ============================================================================
print("Creating Plot 1: Accuracy by Condition...")

fig, ax = plt.subplots(figsize=(7, 6))

acc_by_cond = participant_summary.groupby('condition')['accuracy'].agg(['mean', 'sem'])

x_pos = [0, 1]
colors = [COLORS['AB'], COLORS['NB']]

bars = ax.bar(x_pos, acc_by_cond['mean'], 
               alpha=0.8, color=colors, edgecolor='black', linewidth=1.5)

# Add value labels
for i, (idx, row) in enumerate(acc_by_cond.iterrows()):
    ax.text(i, row['mean'] + 0.02, f"{row['mean']:.3f}", 
            ha='center', va='bottom', fontsize=13, fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels(['Abrupt Cut', 'Natural Cut'], fontsize=13)
ax.set_ylabel('Recognition Accuracy', fontsize=14, fontweight='bold')
ax.set_title('Memory Performance by Video Condition', fontsize=15, fontweight='bold', pad=15)
ax.set_ylim(0, 1.0)
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.4, linewidth=1)

# Statistical test
ab_acc = participant_summary[participant_summary['condition'] == 'AB']['accuracy']
nb_acc = participant_summary[participant_summary['condition'] == 'NB']['accuracy']
t_stat, p_val = stats.ttest_ind(ab_acc, nb_acc)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '1_accuracy_by_condition.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved (p = {p_val:.4f})")

# ============================================================================
# PLOT 2: Accuracy by Frame Type
# ============================================================================
print("Creating Plot 2: Accuracy by Frame Type...")

fig, ax = plt.subplots(figsize=(7, 6))

participant_frame_acc = recognition_data.groupby(['subject_id', 'frame_type'])['resp.corr'].mean().reset_index()
frame_stats = participant_frame_acc.groupby('frame_type')['resp.corr'].agg(['mean', 'sem'])

x_pos = [0, 1]
colors = [COLORS['BB'], COLORS['EM']]

bars = ax.bar(x_pos, frame_stats['mean'], 
               alpha=0.8, color=colors, edgecolor='black', linewidth=1.5)

for i, (idx, row) in enumerate(frame_stats.iterrows()):
    ax.text(i, row['mean'] + 0.02, f"{row['mean']:.3f}", 
            ha='center', va='bottom', fontsize=13, fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels(['Before Boundary', 'Event Middle'], fontsize=13)
ax.set_ylabel('Recognition Accuracy', fontsize=14, fontweight='bold')
ax.set_title('Memory Performance by Frame Type', fontsize=15, fontweight='bold', pad=15)
ax.set_ylim(0, 1.0)
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.4, linewidth=1)

# Statistical test
bb_acc = participant_frame_acc[participant_frame_acc['frame_type'] == 'BB']['resp.corr']
em_acc = participant_frame_acc[participant_frame_acc['frame_type'] == 'EM']['resp.corr']
t_stat, p_val = stats.ttest_ind(bb_acc, em_acc)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '2_accuracy_by_frame_type.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved (p = {p_val:.4f})")

# ============================================================================
# PLOT 3: Condition × Frame Type Interaction
# ============================================================================
print("Creating Plot 3: Condition × Frame Type Interaction...")

fig, ax = plt.subplots(figsize=(8, 6))

cond_frame_stats = participant_frame_summary.groupby(['condition', 'frame_type'])['accuracy'].agg(
    ['mean', 'sem']
).reset_index()

x = np.arange(2)
width = 0.35
colors_interaction = [COLORS['AB'], COLORS['NB']]

for i, cond in enumerate(['AB', 'NB']):
    cond_data = cond_frame_stats[cond_frame_stats['condition'] == cond]
    means = cond_data['mean'].values
    
    bars = ax.bar(x + i*width, means, width, 
                   label=cond, alpha=0.8, 
                   color=colors_interaction[i], edgecolor='black', linewidth=1.5)
    
    for j, m in enumerate(means):
        ax.text(j + i*width, m + 0.015, f'{m:.3f}', 
                ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_xticks(x + width / 2)
ax.set_xticklabels(['Before Boundary', 'Event Middle'], fontsize=13)
ax.set_ylabel('Recognition Accuracy', fontsize=14, fontweight='bold')
ax.set_title('Condition × Frame Type Interaction', fontsize=15, fontweight='bold', pad=15)
ax.set_ylim(0, 1.0)
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.4, linewidth=1)
ax.legend(title='Condition', title_fontsize=12, fontsize=12, 
          labels=['Abrupt Cut', 'Natural Cut'], frameon=False)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '3_interaction_condition_frame.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved")

# ============================================================================
# PLOT 4: Response Time by Condition
# ============================================================================
print("Creating Plot 4: Response Time by Condition...")

fig, ax = plt.subplots(figsize=(7, 6))

correct_trials = recognition_data[recognition_data['resp.corr'] == 1].copy()
participant_rt = correct_trials.groupby(['subject_id', 'condition'])['resp.rt'].mean().reset_index()
rt_stats = participant_rt.groupby('condition')['resp.rt'].agg(['mean', 'sem'])

x_pos = [0, 1]
colors = [COLORS['AB'], COLORS['NB']]

bars = ax.bar(x_pos, rt_stats['mean'], 
               alpha=0.8, color=colors, edgecolor='black', linewidth=1.5)

for i, (idx, row) in enumerate(rt_stats.iterrows()):
    ax.text(i, row['mean'] + 0.15, f"{row['mean']:.2f}s", 
            ha='center', va='bottom', fontsize=13, fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels(['Abrupt Cut', 'Natural Cut'], fontsize=13)
ax.set_ylabel('Response Time (seconds)', fontsize=14, fontweight='bold')
ax.set_title('Response Time by Condition', fontsize=15, fontweight='bold', pad=15)

# Statistical test
ab_rt = participant_rt[participant_rt['condition'] == 'AB']['resp.rt']
nb_rt = participant_rt[participant_rt['condition'] == 'NB']['resp.rt']
t_stat, p_val = stats.ttest_ind(ab_rt, nb_rt)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '4_rt_by_condition.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved (p = {p_val:.4f})")

# ============================================================================
# PLOT 5: Confidence Ratings by Condition
# ============================================================================
print("Creating Plot 5: Confidence Ratings by Condition...")

fig, ax = plt.subplots(figsize=(7, 6))

participant_conf = recognition_data.groupby(['subject_id', 'condition'])['conf_radio.response'].mean().reset_index()
conf_stats = participant_conf.groupby('condition')['conf_radio.response'].agg(['mean', 'sem'])

x_pos = [0, 1]
colors = [COLORS['AB'], COLORS['NB']]

bars = ax.bar(x_pos, conf_stats['mean'], 
               alpha=0.8, color=colors, edgecolor='black', linewidth=1.5)

for i, (idx, row) in enumerate(conf_stats.iterrows()):
    ax.text(i, row['mean'] + 0.08, f"{row['mean']:.2f}", 
            ha='center', va='bottom', fontsize=13, fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels(['Abrupt Cut', 'Natural Cut'], fontsize=13)
ax.set_ylabel('Confidence Rating (1-5)', fontsize=14, fontweight='bold')
ax.set_title('Response Confidence by Condition', fontsize=15, fontweight='bold', pad=15)
ax.set_ylim(1, 5)
ax.axhline(y=3, color='gray', linestyle='--', alpha=0.4, linewidth=1)

# Statistical test
ab_conf = participant_conf[participant_conf['condition'] == 'AB']['conf_radio.response']
nb_conf = participant_conf[participant_conf['condition'] == 'NB']['conf_radio.response']
t_stat, p_val = stats.ttest_ind(ab_conf, nb_conf)

plt.tight_layout()
plt.savefig(PLOTS_DIR / '5_confidence_by_condition.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved (p = {p_val:.4f})")

# ============================================================================
# Generate Summary Statistics
# ============================================================================
print("\nGenerating statistical summary...")

summary = []
summary.append("="*70)
summary.append("STATISTICAL SUMMARY")
summary.append("="*70)
summary.append("")

# Overall
summary.append(f"Sample Size: {len(participant_summary)} participants")
summary.append(f"  - Abrupt Cut (AB): {(participant_summary['condition']=='AB').sum()}")
summary.append(f"  - Natural Cut (NB): {(participant_summary['condition']=='NB').sum()}")
summary.append("")

# Accuracy by Condition
summary.append("ACCURACY BY CONDITION")
summary.append("-" * 40)
ab_acc = participant_summary[participant_summary['condition'] == 'AB']['accuracy']
nb_acc = participant_summary[participant_summary['condition'] == 'NB']['accuracy']
t_stat, p_val = stats.ttest_ind(ab_acc, nb_acc)
summary.append(f"Abrupt Cut:  M = {ab_acc.mean():.4f}, SD = {ab_acc.std():.4f}")
summary.append(f"Natural Cut: M = {nb_acc.mean():.4f}, SD = {nb_acc.std():.4f}")
summary.append(f"t({len(ab_acc)+len(nb_acc)-2}) = {t_stat:.3f}, p = {p_val:.4f}")
summary.append("")

# RT by Condition
summary.append("RESPONSE TIME BY CONDITION (correct trials)")
summary.append("-" * 40)
ab_rt = participant_rt[participant_rt['condition'] == 'AB']['resp.rt']
nb_rt = participant_rt[participant_rt['condition'] == 'NB']['resp.rt']
t_stat, p_val = stats.ttest_ind(ab_rt, nb_rt)
summary.append(f"Abrupt Cut:  M = {ab_rt.mean():.4f}s, SD = {ab_rt.std():.4f}s")
summary.append(f"Natural Cut: M = {nb_rt.mean():.4f}s, SD = {nb_rt.std():.4f}s")
summary.append(f"t({len(ab_rt)+len(nb_rt)-2}) = {t_stat:.3f}, p = {p_val:.4f}")
summary.append("")

# Frame Type Effects
summary.append("ACCURACY BY FRAME TYPE")
summary.append("-" * 40)
bb_acc = participant_frame_acc[participant_frame_acc['frame_type'] == 'BB']['resp.corr']
em_acc = participant_frame_acc[participant_frame_acc['frame_type'] == 'EM']['resp.corr']
t_stat, p_val = stats.ttest_ind(bb_acc, em_acc)
summary.append(f"Before Boundary: M = {bb_acc.mean():.4f}, SD = {bb_acc.std():.4f}")
summary.append(f"Event Middle:    M = {em_acc.mean():.4f}, SD = {em_acc.std():.4f}")
summary.append(f"t({len(bb_acc)+len(em_acc)-2}) = {t_stat:.3f}, p = {p_val:.4f}")
summary.append("")

summary.append("="*70)

with open(PLOTS_DIR / 'statistical_summary.txt', 'w') as f:
    f.write('\n'.join(summary))

print(f"✓ Saved statistical summary")
print()
print("="*70)
print("ALL PLOTS GENERATED SUCCESSFULLY")
print("="*70)
print(f"\nPlots saved to: {PLOTS_DIR}")
print("Total plots: 5")
print()
