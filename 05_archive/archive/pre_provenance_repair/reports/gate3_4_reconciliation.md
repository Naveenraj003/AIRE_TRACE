# Gate 3.4 Mode A / Mode B Metric Separation & Onset Strictness Reconciliation

## 1. Issue Reconciliation
The defect in thresholding.py allowed failures without explicit onset annotations or with malformed missing onsets to be treated as valid prospective metrics (falling back to Raw Recall implicitly). This was reconciled by enforcing `mode='prospective'` and `mode='raw'` downstream from the `MasterEvaluator`, and structurally segregating the metric keys.

## 2. Downstream Consumer Audit Evidence
The following raw `ripgrep` / `grep` search validates that no consumers of `Recall_at_FAR` or `Raw_Recall` have been orphaned by the metric key separation.

```text
p:\AIRE-TRACE\tests\evaluation\test_pdc.py:6:    mA = {"AUROC": 0.8, "AUPRC": 0.7, "Recall_at_FAR": 0.3, "ECE": 0.15}
p:\AIRE-TRACE\tests\evaluation\test_pdc.py:7:    mB = {"AUROC": 0.7, "AUPRC": 0.6, "Recall_at_FAR": 0.4, "ECE": 0.05} # mB has higher recall and lower ECE (better ECE)
p:\AIRE-TRACE\tests\evaluation\test_pdc.py:17:        "H1": {"AUROC": 0.6, "AUPRC": 0.5, "Recall_at_FAR": 0.2, "ECE": 0.2},
p:\AIRE-TRACE\tests\evaluation\test_pdc.py:18:        "M1": {"AUROC": 0.7, "AUPRC": 0.6, "Recall_at_FAR": 0.4, "ECE": 0.1},
p:\AIRE-TRACE\tests\evaluation\test_pdc.py:19:        "S1": {"AUROC": 0.8, "AUPRC": 0.7, "Recall_at_FAR": 0.5, "ECE": 0.08}
p:\AIRE-TRACE\tests\evaluation\test_metrics.py:33:    assert "Recall_at_FAR" in m_dict
p:\AIRE-TRACE\tests\evaluation\test_metrics.py:38:    assert "Raw_Recall" in m_dict_raw
p:\AIRE-TRACE\tests\evaluation\test_metrics.py:39:    assert "Recall_at_FAR" not in m_dict_raw
p:\AIRE-TRACE\src\run_gate3_experiments.py:105:            "Recall_at_FAR": mode_a[m_id]["Recall_at_FAR"],
p:\AIRE-TRACE\src\run_gate3_experiments.py:106:            "Recall_95CI": f"[{cis[m_id]['Recall_at_FAR']['ci_lower']:.4f}, {cis[m_id]['Recall_at_FAR']['ci_upper']:.4f}]",
p:\AIRE-TRACE\src\run_gate3_experiments.py:112:            "tau2_Raw_Recall": mode_b[m_id]["Raw_Recall"],
p:\AIRE-TRACE\src\run_gate3_experiments.py:144:| **H1** | Tool Error Count Threshold | {threshs['H1']['frozen_threshold']} | {mode_a['H1']['AUROC']} [{cis['H1']['AUROC']['ci_lower']}, {cis['H1']['AUROC']['ci_upper']}] | {mode_a['H1']['AUPRC']} [{cis['H1']['AUPRC']['ci_lower']}, {cis['H1']['AUPRC']['ci_upper']}] | {mode_a['H1']['Recall_at_FAR']} [{cis['H1']['Recall_at_FAR']['ci_lower']}, {cis['H1']['Recall_at_FAR']['ci_upper']}] | {mode_a['H1']['FAR']} | {mode_a['H1']['Brier']} | {mode_a['H1']['ECE']} |
p:\AIRE-TRACE\src\run_gate3_experiments.py:145:| **H2** | Retry Count Threshold | {threshs['H2']['frozen_threshold']} | {mode_a['H2']['AUROC']} [{cis['H2']['AUROC']['ci_lower']}, {cis['H2']['AUROC']['ci_upper']}] | {mode_a['H2']['AUPRC']} [{cis['H2']['AUPRC']['ci_lower']}, {cis['H2']['AUPRC']['ci_upper']}] | {mode_a['H2']['Recall_at_FAR']} [{cis['H2']['Recall_at_FAR']['ci_lower']}, {cis['H2']['Recall_at_FAR']['ci_upper']}] | {mode_a['H2']['FAR']} | {mode_a['H2']['Brier']} | {mode_a['H2']['ECE']} |
p:\AIRE-TRACE\src\run_gate3_experiments.py:146:| **H3** | Repeated Action Threshold | {threshs['H3']['frozen_threshold']} | {mode_a['H3']['AUROC']} [{cis['H3']['AUROC']['ci_lower']}, {cis['H3']['AUROC']['ci_upper']}] | {mode_a['H3']['AUPRC']} [{cis['H3']['AUPRC']['ci_lower']}, {cis['H3']['AUPRC']['ci_upper']}] | {mode_a['H3']['Recall_at_FAR']} [{cis['H3']['Recall_at_FAR']['ci_lower']}, {cis['H3']['Recall_at_FAR']['ci_upper']}] | {mode_a['H3']['FAR']} | {mode_a['H3']['Brier']} | {mode_a['H3']['ECE']} |
p:\AIRE-TRACE\src\run_gate3_experiments.py:147:| **H4** | Combined Heuristic Score | {threshs['H4']['frozen_threshold']} | {mode_a['H4']['AUROC']} [{cis['H4']['AUROC']['ci_lower']}, {cis['H4']['AUROC']['ci_upper']}] | {mode_a['H4']['AUPRC']} [{cis['H4']['AUPRC']['ci_lower']}, {cis['H4']['AUPRC']['ci_upper']}] | {mode_a['H4']['Recall_at_FAR']} [{cis['H4']['Recall_at_FAR']['ci_lower']}, {cis['H4']['Recall_at_FAR']['ci_upper']}] | {mode_a['H4']['FAR']} | {mode_a['H4']['Brier']} | {mode_a['H4']['ECE']} |
p:\AIRE-TRACE\src\run_gate3_experiments.py:148:| **M1** | Logistic Regression | {threshs['M1']['frozen_threshold']} | **{mode_a['M1']['AUROC']}** [{cis['M1']['AUROC']['ci_lower']}, {cis['M1']['AUROC']['ci_upper']}] | **{mode_a['M1']['AUPRC']}** [{cis['M1']['AUPRC']['ci_lower']}, {cis['M1']['AUPRC']['ci_upper']}] | **{mode_a['M1']['Recall_at_FAR']}** [{cis['M1']['Recall_at_FAR']['ci_lower']}, {cis['M1']['Recall_at_FAR']['ci_upper']}] | {mode_a['M1']['FAR']} | {mode_a['M1']['Brier']} | {mode_a['M1']['ECE']} |
p:\AIRE-TRACE\src\run_gate3_experiments.py:149:| **S1** | Random Forest | {threshs['S1']['frozen_threshold']} | **{mode_a['S1']['AUROC']}** [{cis['S1']['AUROC']['ci_lower']}, {cis['S1']['AUROC']['ci_upper']}] | **{mode_a['S1']['AUPRC']}** [{cis['S1']['AUPRC']['ci_lower']}, {cis['S1']['AUPRC']['ci_upper']}] | **{mode_a['S1']['Recall_at_FAR']}** [{cis['S1']['Recall_at_FAR']['ci_lower']}, {cis['S1']['Recall_at_FAR']['ci_upper']}] | {mode_a['S1']['FAR']} | **{mode_a['S1']['Brier']}** | **{mode_a['S1']['ECE']}** |
p:\AIRE-TRACE\src\run_gate3_experiments.py:160:| **H1** | {threshs['H1']['frozen_threshold']} | {mode_b['H1']['AUROC']} | {mode_b['H1']['AUPRC']} | {mode_b['H1']['Raw_Recall']} | {mode_b['H1']['FAR']} | {mode_b['H1']['Brier']} | {mode_b['H1']['ECE']} |
p:\AIRE-TRACE\src\run_gate3_experiments.py:161:| **H2** | {threshs['H2']['frozen_threshold']} | {mode_b['H2']['AUROC']} | {mode_b['H2']['AUPRC']} | {mode_b['H2']['Raw_Recall']} | {mode_b['H2']['FAR']} | {mode_b['H2']['Brier']} | {mode_b['H2']['ECE']} |
p:\AIRE-TRACE\src\run_gate3_experiments.py:162:| **H3** | {threshs['H3']['frozen_threshold']} | {mode_b['H3']['AUROC']} | {mode_b['H3']['AUPRC']} | {mode_b['H3']['Raw_Recall']} | {mode_b['H3']['FAR']} | {mode_b['H3']['Brier']} | {mode_b['H3']['ECE']} |
p:\AIRE-TRACE\src\run_gate3_experiments.py:163:| **H4** | {threshs['H4']['frozen_threshold']} | {mode_b['H4']['AUROC']} | {mode_b['H4']['AUPRC']} | {mode_b['H4']['Raw_Recall']} | {mode_b['H4']['FAR']} | {mode_b['H4']['Brier']} | {mode_b['H4']['ECE']} |
p:\AIRE-TRACE\src\run_gate3_experiments.py:164:| **M1** | {threshs['M1']['frozen_threshold']} | {mode_b['M1']['AUROC']} | {mode_b['M1']['AUPRC']} | {mode_b['M1']['Raw_Recall']} | {mode_b['M1']['FAR']} | {mode_b['M1']['Brier']} | {mode_b['M1']['ECE']} |
p:\AIRE-TRACE\src\run_gate3_experiments.py:165:| **S1** | {threshs['S1']['frozen_threshold']} | {mode_b['S1']['AUROC']} | {mode_b['S1']['AUPRC']} | {mode_b['S1']['Raw_Recall']} | {mode_b['S1']['FAR']} | {mode_b['S1']['Brier']} | {mode_b['S1']['ECE']} |
p:\AIRE-TRACE\src\run_gate3_experiments.py:182:| **S1 (Random Forest)** | Recall @ FAR $\le 5\%$ | {sensitivity_results['K_10']['mode_a_terminalbench_test']['S1']['Recall_at_FAR']} | {sensitivity_results['K_20']['mode_a_terminalbench_test']['S1']['Recall_at_FAR']} | {sensitivity_results['K_30']['mode_a_terminalbench_test']['S1']['Recall_at_FAR']} |
p:\AIRE-TRACE\src\run_gate3_experiments.py:184:| **M1 (Logistic Reg)** | Recall @ FAR $\le 5\%$ | {sensitivity_results['K_10']['mode_a_terminalbench_test']['M1']['Recall_at_FAR']} | {sensitivity_results['K_20']['mode_a_terminalbench_test']['M1']['Recall_at_FAR']} | {sensitivity_results['K_30']['mode_a_terminalbench_test']['M1']['Recall_at_FAR']} |
p:\AIRE-TRACE\src\evaluation\pdc.py:45:        metrics_to_compare = ["AUROC", "AUPRC", "Recall_at_FAR", "ECE"]
p:\AIRE-TRACE\src\evaluation\metrics.py:116:        results["Recall_at_FAR"] = round(recall, 4)
p:\AIRE-TRACE\src\evaluation\metrics.py:118:        results["Raw_Recall"] = round(recall, 4)
p:\AIRE-TRACE\src\evaluation\bootstrap.py:84:    recall_key = "Recall_at_FAR" if mode == "prospective" else "Raw_Recall"
p:\AIRE-TRACE\scratch\forensic_gate3_3.py:22:    print(f"  {m_id}: AUROC={m_dict['AUROC']:.4f}, AUPRC={m_dict['AUPRC']:.4f}, Recall@FAR={m_dict['Recall_at_FAR']:.4f}, FAR={m_dict['FAR']:.4f}, Brier={m_dict['Brier']:.4f}, ECE={m_dict['ECE']:.4f}")
p:\AIRE-TRACE\scratch\forensic_gate3_3.py:27:print(df_csv[["method", "dataset", "AUROC", "AUPRC", "Recall_at_FAR", "FAR", "Brier", "ECE"]])
p:\AIRE-TRACE\scratch\audit_gate3_1_verify_all.py:23:    print(f"  {m_id:4s} | AUROC: {metrics['AUROC']:.4f} | AUPRC: {metrics['AUPRC']:.4f} | Recall@FAR: {metrics['Recall_at_FAR']:.4f} | ECE: {metrics['ECE']:.4f}")
```
*(Note: Excluded `results/*.json` to filter raw metric output artifact data from the codebase consumer results)*
