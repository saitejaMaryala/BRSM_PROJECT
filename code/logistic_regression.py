"""
Logistic Regression (GLM - Binomial) Analysis
==============================================
Research Question:
    To what extent do subjective confidence, frame type (Before Boundary BB vs.
    Event-Middle EM), and video editing style (NB vs. AB) predict the probability
    of correct frame recognition?

Model:
    DV  : resp.corr        (binary: 1 = correct, 0 = incorrect)
    IVs : Condition        (NB vs. AB)
          Target_Type      (BB vs. EM, extracted from target_img filename)
          Confidence       (conf_radio.response, 1-5 Likert scale)
    Interaction: Condition × Confidence  (tests boundary-advantage / confidence link)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# statsmodels for GLM
import statsmodels.formula.api as smf
import statsmodels.api as sm

# sklearn for ROC / AUC
from sklearn.metrics import (
    roc_auc_score, roc_curve,
    classification_report, confusion_matrix, ConfusionMatrixDisplay
)

# scipy for odds-ratio CIs from log-OR
from scipy import stats

# ── Paths ─────────────────────────────────────────────────────────────────────
CLEANED_DIR = Path("../data/individuals_cleaned")
OUTPUT_DIR  = Path("../exploration_output/logistic_regression")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def parse_list_value(val):
    """Parse values stored as string lists like '[9.14]'."""
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
    except Exception:
        return np.nan


def extract_target_type(img_path: str) -> str:
    """
    Extract target type from filename.
    Filenames look like: frames\\Vid33_BB_T.png  or  frames/Vid9_EM_T.png
    Returns 'BB' or 'EM', else NaN.
    """
    if pd.isna(img_path):
        return np.nan
    img_path = str(img_path).replace("\\", "/")
    fname = img_path.split("/")[-1]        # e.g. "Vid33_BB_T.png"
    parts = fname.split("_")               # ['Vid33', 'BB', 'T.png']
    for part in parts:
        if part in ("BB", "EM"):
            return part
    return np.nan


# ── Data Loading ──────────────────────────────────────────────────────────────
def build_trial_dataframe() -> pd.DataFrame:
    """
    Walk every cleaned participant CSV, extract trial-level rows, and
    return one combined long-format DataFrame ready for modelling.
    """
    csv_files = sorted(CLEANED_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {CLEANED_DIR}")

    print(f"Loading {len(csv_files)} participant files …")
    records = []

    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, low_memory=False)

            # ── participant meta ──────────────────────────────────────────────
            condition     = ('AB' if '_AB_' in csv_file.name else
                             'NB' if '_NB_' in csv_file.name else 'Unknown')
            participant_id = csv_file.stem.split('_')[0]   # e.g. 'sub14'

            # ── keep only recognition-task trial rows ─────────────────────────
            trials = df[df['resp.corr'].notna()].copy()
            if trials.empty:
                continue

            # ── parse columns ─────────────────────────────────────────────────
            trials['resp.corr']         = pd.to_numeric(trials['resp.corr'],         errors='coerce')
            trials['conf_radio.response'] = trials['conf_radio.response'].apply(parse_list_value)
            trials['resp.rt']           = trials['resp.rt'].apply(parse_list_value)

            # ── derive Target_Type ────────────────────────────────────────────
            trials['Target_Type'] = trials['target_img'].apply(extract_target_type)

            # ── assemble record per trial ─────────────────────────────────────
            for _, row in trials.iterrows():
                records.append({
                    'Participant'  : participant_id,
                    'Condition'    : condition,
                    'Target_Type'  : row['Target_Type'],
                    'Confidence'   : row['conf_radio.response'],
                    'Resp_Corr'    : row['resp.corr'],
                    'RT'           : row['resp.rt'],
                    'movie_id'     : row.get('movie_id', np.nan),
                    'target_img'   : row.get('target_img', np.nan),
                })

        except Exception as e:
            print(f"  ⚠  Error reading {csv_file.name}: {e}")

    long_df = pd.DataFrame(records)
    return long_df


# ── Pre-processing ────────────────────────────────────────────────────────────
def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and encode the long-format trial DataFrame.
    """
    print(f"\nTotal trials before cleaning : {len(df)}")

    # Drop rows missing key variables
    df = df.dropna(subset=['Resp_Corr', 'Confidence', 'Target_Type', 'Condition'])
    print(f"Total trials after dropna    : {len(df)}")

    # Ensure types
    df['Resp_Corr']  = df['Resp_Corr'].astype(int)
    df['Confidence'] = df['Confidence'].astype(float)

    # ── Dummy / treatment coding ──────────────────────────────────────────────
    # Reference levels: NB for Condition, BB for Target_Type
    df['Condition_AB']   = (df['Condition']   == 'AB').astype(int)   # 1 = AB, 0 = NB
    df['TargetType_EM']  = (df['Target_Type'] == 'EM').astype(int)   # 1 = EM, 0 = BB

    # Centre Confidence for interpretability of main effects (grand-mean centred)
    df['Confidence_c'] = df['Confidence'] - df['Confidence'].mean()

    print(f"\nCondition breakdown:")
    print(df['Condition'].value_counts())
    print(f"\nTarget_Type breakdown:")
    print(df['Target_Type'].value_counts())
    print(f"\nConfidence distribution:")
    print(df['Confidence'].describe())
    print(f"\nOverall accuracy: {df['Resp_Corr'].mean()*100:.2f}%")

    return df


# ── Logistic Regression ───────────────────────────────────────────────────────
def run_logistic_regression(df: pd.DataFrame):
    """
    Fit GLM Binomial logistic regression using statsmodels.
    Formula includes main effects + Condition × Confidence interaction.
    """
    print("\n" + "="*70)
    print("LOGISTIC REGRESSION (GLM - Binomial)")
    print("="*70)

    # Formula (statsmodels patsy-style)
    # Condition_AB coded 0/1, TargetType_EM coded 0/1, Confidence_c grand-mean centred
    formula = "Resp_Corr ~ Condition_AB + TargetType_EM + Confidence_c + Condition_AB:Confidence_c"

    model = smf.glm(
        formula = formula,
        data    = df,
        family  = sm.families.Binomial()
    )
    result = model.fit()

    print(result.summary())

    return result


# ── Odds Ratios ───────────────────────────────────────────────────────────────
def print_odds_ratios(result):
    """
    Compute and print odds ratios + 95% CIs from the fitted model.
    """
    print("\n" + "-"*60)
    print("ODDS RATIOS  (exp(β))  with 95% Confidence Intervals")
    print("-"*60)

    params    = result.params
    conf_int  = result.conf_int()     # 2.5% and 97.5%
    or_table  = pd.DataFrame({
        'OR'      : np.exp(params),
        'OR_2.5%' : np.exp(conf_int[0]),
        'OR_97.5%': np.exp(conf_int[1]),
        'p-value' : result.pvalues,
    })
    or_table['Significant'] = or_table['p-value'].apply(lambda p: '***' if p < 0.001 else
                                                          ('**'  if p < 0.01  else
                                                           ('*'   if p < 0.05  else '')))
    print(or_table.to_string(float_format="{:.4f}".format))
    return or_table


# ── Model Evaluation ──────────────────────────────────────────────────────────
def evaluate_model(df: pd.DataFrame, result, or_table: pd.DataFrame):
    """
    ROC curve, AUC, confusion matrix, classification report.
    """
    # Predicted probabilities
    df = df.copy()
    df['predicted_prob']  = result.predict(df)
    df['predicted_class'] = (df['predicted_prob'] >= 0.5).astype(int)

    auc = roc_auc_score(df['Resp_Corr'], df['predicted_prob'])
    print(f"\nAUC-ROC : {auc:.4f}")

    print("\nClassification Report (threshold = 0.5):")
    print(classification_report(df['Resp_Corr'], df['predicted_class'],
                                 target_names=['Incorrect (0)', 'Correct (1)']))

    # McFadden's Pseudo-R²
    ll_model  = result.llf
    ll_null   = result.llnull
    pseudo_r2 = 1 - (ll_model / ll_null)
    print(f"McFadden's Pseudo-R² : {pseudo_r2:.4f}")

    # ── Plot 1: ROC curve ─────────────────────────────────────────────────────
    fpr, tpr, _ = roc_curve(df['Resp_Corr'], df['predicted_prob'])
    plt.figure(figsize=(7, 6))
    plt.plot(fpr, tpr, color='#4A90D9', lw=2, label=f'ROC curve (AUC = {auc:.3f})')
    plt.plot([0, 1], [0, 1], 'k--', lw=1, label='Chance')
    plt.xlabel('False Positive Rate', fontsize=13)
    plt.ylabel('True Positive Rate', fontsize=13)
    plt.title('ROC Curve — Logistic Regression', fontsize=14, fontweight='bold')
    plt.legend(loc='lower right', fontsize=12)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'roc_curve.png', dpi=300)
    plt.close()
    print(f"  → Saved: roc_curve.png")

    # ── Plot 2: Confusion Matrix ───────────────────────────────────────────────
    cm  = confusion_matrix(df['Resp_Corr'], df['predicted_class'])
    fig, ax = plt.subplots(figsize=(5, 4))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Incorrect', 'Correct'])
    disp.plot(ax=ax, colorbar=False, cmap='Blues')
    ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'confusion_matrix.png', dpi=300)
    plt.close()
    print(f"  → Saved: confusion_matrix.png")

    # ── Plot 3: Odds Ratio Forest Plot ────────────────────────────────────────
    or_plot = or_table.drop(index='Intercept', errors='ignore').copy()
    labels  = or_plot.index.tolist()
    ors     = or_plot['OR'].values
    lo      = or_plot['OR_2.5%'].values
    hi      = or_plot['OR_97.5%'].values
    colors  = ['#E74C3C' if p < 0.05 else '#95A5A6' for p in or_plot['p-value']]

    fig, ax = plt.subplots(figsize=(9, max(4, len(labels)*1.1)))
    y_pos = np.arange(len(labels))

    ax.hlines(y_pos, lo, hi, colors=colors, linewidth=3, alpha=0.7)
    ax.scatter(ors, y_pos, color=colors, s=120, zorder=5)
    ax.axvline(x=1, color='black', linestyle='--', linewidth=1.2, label='OR = 1 (null)')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=12)
    ax.set_xlabel('Odds Ratio (log scale)', fontsize=12)
    ax.set_xscale('log')
    ax.set_title('Odds Ratios with 95% Confidence Intervals\n(red = significant p < .05)',
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'odds_ratio_forest.png', dpi=300)
    plt.close()
    print(f"  → Saved: odds_ratio_forest.png")

    return df, auc, pseudo_r2


# ── Effect Visualisation ──────────────────────────────────────────────────────
def plot_effects(df: pd.DataFrame):
    """
    Visualise how confidence and condition modulate predicted accuracy.
    """
    # ── Plot 4: Predicted probability by Confidence × Condition ───────────────
    plt.figure(figsize=(9, 6))
    palette = {'AB': '#E74C3C', 'NB': '#2ECC71'}
    sns.lineplot(
        data=df, x='Confidence', y='predicted_prob',
        hue='Condition', palette=palette,
        estimator='mean', errorbar=('ci', 95), linewidth=2.5
    )
    plt.xlabel('Confidence Rating (1–5)', fontsize=13)
    plt.ylabel('Predicted P(Correct)', fontsize=13)
    plt.title('Predicted Recognition Accuracy\nby Confidence × Condition',
              fontsize=14, fontweight='bold')
    plt.legend(title='Condition', fontsize=11)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'predicted_prob_conf_x_condition.png', dpi=300)
    plt.close()
    print(f"  → Saved: predicted_prob_conf_x_condition.png")

    # ── Plot 5: Predicted probability by Confidence × Target_Type ─────────────
    plt.figure(figsize=(9, 6))
    palette2 = {'BB': '#9B59B6', 'EM': '#F39C12'}
    sns.lineplot(
        data=df, x='Confidence', y='predicted_prob',
        hue='Target_Type', palette=palette2,
        estimator='mean', errorbar=('ci', 95), linewidth=2.5
    )
    plt.xlabel('Confidence Rating (1–5)', fontsize=13)
    plt.ylabel('Predicted P(Correct)', fontsize=13)
    plt.title('Predicted Recognition Accuracy\nby Confidence × Target Type',
              fontsize=14, fontweight='bold')
    plt.legend(title='Target Type', fontsize=11)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'predicted_prob_conf_x_targettype.png', dpi=300)
    plt.close()
    print(f"  → Saved: predicted_prob_conf_x_targettype.png")

    # ── Plot 6: Observed accuracy by Confidence × Condition (bar) ────────────
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for ax, cond, color in zip(axes, ['NB', 'AB'], ['#2ECC71', '#E74C3C']):
        sub = df[df['Condition'] == cond]
        acc_by_conf = sub.groupby('Confidence')['Resp_Corr'].mean() * 100
        ax.bar(acc_by_conf.index, acc_by_conf.values, color=color, edgecolor='white', alpha=0.85)
        ax.set_title(f'Condition: {cond}', fontsize=13, fontweight='bold')
        ax.set_xlabel('Confidence Rating', fontsize=12)
        ax.set_ylabel('Observed Accuracy (%)', fontsize=12)
        ax.set_ylim(0, 105)
        ax.axhline(y=50, color='grey', linestyle='--', linewidth=1)
        for conf, val in acc_by_conf.items():
            ax.text(conf, val + 1.5, f"{val:.0f}%", ha='center', fontsize=10)
    fig.suptitle('Observed % Correct by Confidence, Split by Condition',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'accuracy_by_confidence_condition.png', dpi=300)
    plt.close()
    print(f"  → Saved: accuracy_by_confidence_condition.png")

    # ── Plot 7: Observed accuracy by Confidence × Target_Type (bar) ──────────
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for ax, ttype, color in zip(axes, ['BB', 'EM'], ['#9B59B6', '#F39C12']):
        sub = df[df['Target_Type'] == ttype]
        acc_by_conf = sub.groupby('Confidence')['Resp_Corr'].mean() * 100
        ax.bar(acc_by_conf.index, acc_by_conf.values, color=color, edgecolor='white', alpha=0.85)
        ax.set_title(f'Target Type: {ttype}', fontsize=13, fontweight='bold')
        ax.set_xlabel('Confidence Rating', fontsize=12)
        ax.set_ylabel('Observed Accuracy (%)', fontsize=12)
        ax.set_ylim(0, 105)
        ax.axhline(y=50, color='grey', linestyle='--', linewidth=1)
        for conf, val in acc_by_conf.items():
            ax.text(conf, val + 1.5, f"{val:.0f}%", ha='center', fontsize=10)
    fig.suptitle('Observed % Correct by Confidence, Split by Target Type',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'accuracy_by_confidence_targettype.png', dpi=300)
    plt.close()
    print(f"  → Saved: accuracy_by_confidence_targettype.png")


# ── Save Outputs ──────────────────────────────────────────────────────────────
def save_outputs(df: pd.DataFrame, or_table: pd.DataFrame, result, auc, pseudo_r2):
    """
    Save the merged trial DataFrame and a summary table to CSV.
    """
    # Full trial-level dataframe
    df_out = df[['Participant', 'Condition', 'Target_Type', 'Confidence',
                  'Resp_Corr', 'RT', 'Condition_AB', 'TargetType_EM',
                  'Confidence_c', 'predicted_prob', 'predicted_class']].copy()
    df_out.to_csv(OUTPUT_DIR / 'logistic_regression_trial_data.csv', index=False)
    print(f"\n  → Saved: logistic_regression_trial_data.csv  ({len(df_out)} rows)")

    # Odds ratio table
    or_table.to_csv(OUTPUT_DIR / 'odds_ratios.csv')
    print(f"  → Saved: odds_ratios.csv")

    # Text summary
    summary_text = result.summary().as_text()
    with open(OUTPUT_DIR / 'model_summary.txt', 'w') as f:
        f.write(summary_text)
        f.write(f"\n\nAUC-ROC        : {auc:.4f}")
        f.write(f"\nMcFadden Pseudo-R2 : {pseudo_r2:.4f}")
    print(f"  → Saved: model_summary.txt")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("="*70)
    print("BRSM Study — Logistic Regression Analysis")
    print("DV: resp.corr   IVs: Condition, Target_Type, Confidence")
    print("="*70)

    # 1. Build trial-level dataframe from all cleaned CSVs
    df_raw = build_trial_dataframe()

    # 2. Preprocess & encode
    df = preprocess(df_raw)

    # 3. Run logistic regression -----------------------------------------------
    result = run_logistic_regression(df)

    # 4. Odds Ratios -----------------------------------------------------------
    or_table = print_odds_ratios(result)

    # 5. Model evaluation ------------------------------------------------------
    df, auc, pseudo_r2 = evaluate_model(df, result, or_table)

    # 6. Effect visualisations -------------------------------------------------
    print("\nGenerating effect visualisations …")
    plot_effects(df)

    # 7. Save outputs ----------------------------------------------------------
    print("\nSaving outputs …")
    save_outputs(df, or_table, result, auc, pseudo_r2)

    print(f"\n✅  All outputs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
