import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plots_dir = '../plots'
os.makedirs(plots_dir, exist_ok=True)

# Set style
sns.set_theme(style="whitegrid")
sns.set_palette("colorblind")

# Load data
summary_df = pd.read_csv('../cleaned_data/cleaned_summary.csv')
trials_df = pd.read_csv('../cleaned_data/cleaned_trials.csv')
abrupt_vids = pd.read_csv('../abruptmovies.csv')
natural_vids = pd.read_csv('../naturalmovies.csv')

print("="*50)
print("DATASET DESCRIPTIVE STATISTICS")
print("="*50)

# 1. Sample Demographics
print("\n1. SAMPLE DEMOGRAPHICS")
print(f"Total participants: {len(summary_df)}")
print(f"Natural Cut group: {len(summary_df[summary_df['group']=='NB'])}")
print(f"Abrupt Cut group: {len(summary_df[summary_df['group']=='AB'])}")
print(f"Age range: {summary_df['Age'].min():.0f} - {summary_df['Age'].max():.0f} years")
print(f"Mean age: {summary_df['Age'].mean():.1f} (SD={summary_df['Age'].std():.1f})")
print(f"\nGender distribution:")
print(summary_df['Gender '].value_counts())

# 2. Video Characteristics
print("\n2. VIDEO STIMULUS CHARACTERISTICS")
abrupt_unique = abrupt_vids[abrupt_vids['is_repeat']==0]
natural_unique = natural_vids[natural_vids['is_repeat']==0]
print(f"Unique videos per condition: {len(abrupt_unique)}")
print(f"Abrupt videos duration: Mean={abrupt_unique['duration'].mean():.1f}s (SD={abrupt_unique['duration'].std():.1f})")
print(f"Natural videos duration: Mean={natural_unique['duration'].mean():.1f}s (SD={natural_unique['duration'].std():.1f})")
print(f"Repeated vigilance videos: {abrupt_vids['is_repeat'].sum()}")

# 3. Trial-level characteristics
print("\n3. TRIAL-LEVEL CHARACTERISTICS")
print(f"Total trials: {len(trials_df)}")
print(f"Trials per participant: {len(trials_df) // len(summary_df)}")
print(f"BB targets: {len(trials_df[trials_df['target_type']=='BB'])}")
print(f"EM targets: {len(trials_df[trials_df['target_type']=='EM'])}")
print(f"\nResponse Time: Mean={trials_df['rt'].mean():.2f}s (SD={trials_df['rt'].std():.2f})")
print(f"Confidence: Mean={trials_df['confidence'].mean():.2f} (SD={trials_df['confidence'].std():.2f})")

# ========== VISUALIZATIONS ==========

# Plot 1: Participant distribution by group
fig, ax = plt.subplots(1, 1, figsize=(7, 5))
group_counts = summary_df['group'].value_counts().sort_index()
colors = ['#4c72b0', '#c44e52']
bars = ax.bar(group_counts.index, group_counts.values, color=colors, alpha=0.8, edgecolor='black')
ax.set_xlabel('Experimental Condition', fontsize=12)
ax.set_ylabel('Number of Participants', fontsize=12)
ax.set_title('Participant Distribution Across Conditions', fontsize=14, pad=15)
ax.set_xticklabels(['Abrupt Cut', 'Natural Cut'])
# Add count labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'n={int(height)}', ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'participant_distribution.png'), dpi=300)
print("\nSaved: participant_distribution.png")

# Plot 2: Age distribution
fig, ax = plt.subplots(1, 1, figsize=(8, 5))
ax.hist(summary_df['Age'].dropna(), bins=10, color='#55a868', alpha=0.7, edgecolor='black')
ax.axvline(summary_df['Age'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean = {summary_df["Age"].mean():.1f}')
ax.set_xlabel('Age (years)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Age Distribution of Participants', fontsize=14, pad=15)
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'age_distribution.png'), dpi=300)
print("Saved: age_distribution.png")

# Plot 3: Video duration distribution
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].hist(abrupt_unique['duration'], bins=15, color='#c44e52', alpha=0.7, edgecolor='black')
axes[0].axvline(abrupt_unique['duration'].mean(), color='darkred', linestyle='--', linewidth=2)
axes[0].set_xlabel('Duration (seconds)', fontsize=11)
axes[0].set_ylabel('Frequency', fontsize=11)
axes[0].set_title('Abrupt Cut Videos', fontsize=12)
axes[0].text(0.95, 0.95, f'Mean={abrupt_unique["duration"].mean():.1f}s', 
             transform=axes[0].transAxes, ha='right', va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

axes[1].hist(natural_unique['duration'], bins=15, color='#4c72b0', alpha=0.7, edgecolor='black')
axes[1].axvline(natural_unique['duration'].mean(), color='darkblue', linestyle='--', linewidth=2)
axes[1].set_xlabel('Duration (seconds)', fontsize=11)
axes[1].set_ylabel('Frequency', fontsize=11)
axes[1].set_title('Natural Cut Videos', fontsize=12)
axes[1].text(0.95, 0.95, f'Mean={natural_unique["duration"].mean():.1f}s', 
             transform=axes[1].transAxes, ha='right', va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

fig.suptitle('Video Stimulus Duration Distribution', fontsize=14, y=1.00)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'video_duration_distribution.png'), dpi=300)
print("Saved: video_duration_distribution.png")

# Plot 4: Target type distribution
fig, ax = plt.subplots(1, 1, figsize=(7, 5))
target_counts = trials_df['target_type'].value_counts()
colors_targets = ['#dd8452', '#8172b2']
bars = ax.bar(target_counts.index, target_counts.values, color=colors_targets, alpha=0.8, edgecolor='black')
ax.set_xlabel('Target Frame Type', fontsize=12)
ax.set_ylabel('Number of Trials', fontsize=12)
ax.set_title('Distribution of Target Frame Types Across All Trials', fontsize=14, pad=15)
ax.set_xticklabels(['Before-Boundary', 'Event-Middle'])
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'target_type_distribution.png'), dpi=300)
print("Saved: target_type_distribution.png")

# Plot 5: Response time distribution
fig, ax = plt.subplots(1, 1, figsize=(8, 5))
ax.hist(trials_df['rt'], bins=50, color='#64b5cd', alpha=0.7, edgecolor='black')
ax.axvline(trials_df['rt'].median(), color='red', linestyle='--', linewidth=2, label=f'Median = {trials_df["rt"].median():.2f}s')
ax.axvline(trials_df['rt'].mean(), color='darkred', linestyle='-', linewidth=2, label=f'Mean = {trials_df["rt"].mean():.2f}s')
ax.set_xlabel('Response Time (seconds)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Response Time Distribution Across All Trials', fontsize=14, pad=15)
ax.legend()
ax.set_xlim(0, 30)  # Limit to reasonable range
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'rt_distribution.png'), dpi=300)
print("Saved: rt_distribution.png")

# Plot 6: Confidence rating distribution
fig, ax = plt.subplots(1, 1, figsize=(8, 5))
conf_counts = trials_df['confidence'].value_counts().sort_index()
colors_conf = sns.color_palette("YlOrRd", n_colors=5)
bars = ax.bar(conf_counts.index, conf_counts.values, color=colors_conf, alpha=0.8, edgecolor='black')
ax.set_xlabel('Confidence Rating', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Distribution of Confidence Ratings Across All Trials', fontsize=14, pad=15)
ax.set_xticks([1, 2, 3, 4, 5])
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'confidence_distribution.png'), dpi=300)
print("Saved: confidence_distribution.png")

print("\n" + "="*50)
print("All dataset descriptive plots generated successfully!")
print("="*50)
