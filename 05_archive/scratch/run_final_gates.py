import pandas as pd
import numpy as np
from src.baselines.logistic import LogisticBaseline
from src.baselines.m4_category import M4CategoryBaseline
from src.evaluation.thresholding import select_calibration_threshold, compute_episode_far_and_recall
from src.evaluation.metrics import compute_all_metrics
import warnings

class M4DifficultyOnly(M4CategoryBaseline):
    def _extract_features(self, df: pd.DataFrame, is_fit: bool) -> np.ndarray:
        if self.feature_cols is None:
            self.feature_cols = [c for c in df.columns if str(c).startswith("feat_")]
        X_num = df[self.feature_cols].values
        episodes = df['episode_id'].values
        diff_encoded = np.zeros(len(df))
        for i, ep in enumerate(episodes):
            meta = self.meta_map.get(ep, {"difficulty": "unknown"})
            diff_encoded[i] = self.diff_failure_rates.get(meta["difficulty"], self.global_failure_rate)
        X_diff = diff_encoded.reshape(-1, 1)
        X_combined = np.hstack([X_num, X_diff])
        if is_fit:
            return self.scaler.fit_transform(X_combined)
        else:
            return self.scaler.transform(X_combined)

class M4CategoryOnly(M4CategoryBaseline):
    def _extract_features(self, df: pd.DataFrame, is_fit: bool) -> np.ndarray:
        if self.feature_cols is None:
            self.feature_cols = [c for c in df.columns if str(c).startswith("feat_")]
        X_num = df[self.feature_cols].values
        episodes = df['episode_id'].values
        cat_encoded = np.zeros(len(df))
        for i, ep in enumerate(episodes):
            meta = self.meta_map.get(ep, {"category": "unknown"})
            cat_encoded[i] = self.cat_failure_rates.get(meta["category"], self.global_failure_rate)
        X_cat = cat_encoded.reshape(-1, 1)
        X_combined = np.hstack([X_num, X_cat])
        if is_fit:
            return self.scaler.fit_transform(X_combined)
        else:
            return self.scaler.transform(X_combined)

def main():
    warnings.filterwarnings("ignore")
    
    df_tb = pd.read_parquet('data/processed/manifests/terminalbench_prefixes.parquet')
    df_tb_k = df_tb[df_tb['prefix_len'] <= 30].copy()
    
    df_train = df_tb_k[df_tb_k['split'] == 'train'].copy()
    df_calib = df_tb_k[df_tb_k['split'] == 'calibration'].copy()
    df_test = df_tb_k[df_tb_k['split'] == 'test'].copy()
    
    y_train = df_train['eventual_outcome'].values.astype(int)
    
    m4_dummy = M4CategoryBaseline()
    m4_dummy.fit(df_train, y_train)
    
    ep_df_train = df_train[['episode_id']].drop_duplicates().copy()
    ep_df_train['category'] = ep_df_train['episode_id'].apply(lambda ep: m4_dummy.meta_map.get(ep, {}).get("category", "unknown"))
    cat_counts = ep_df_train.groupby('category').size()
    supported_cats = cat_counts[cat_counts >= 10].index.tolist()
    
    df_test['category'] = df_test['episode_id'].apply(lambda ep: m4_dummy.meta_map.get(ep, {}).get("category", "unknown"))
    df_test_supported = df_test[df_test['category'].isin(supported_cats)].copy()
    
    print("--- PART 2: FOUR-WAY ABLATION (SUPPORTED TEST) ---")
    def run_eval(name, model):
        model.fit(df_train, y_train)
        y_prob_calib = model.predict_proba(df_calib)
        res = select_calibration_threshold(df_calib, y_prob_calib, target_far=0.05)
        thr = res['frozen_threshold']
        
        y_prob_test = model.predict_proba(df_test_supported)
        metrics = compute_all_metrics(df_test_supported, y_prob_test, thr, mode="prospective")
        auroc = metrics.get('AUROC', np.nan)
        _, recall, _ = compute_episode_far_and_recall(df_test_supported, y_prob_test, thr, mode="prospective")
        
        print(f"{name} | AUROC: {auroc:.4f} | Recall: {recall:.4f} | Thr: {thr:.2f} | TrainEps: {df_train['episode_id'].nunique()} | TestEps: {df_test_supported['episode_id'].nunique()}")
        return model, thr, y_prob_test

    m1, thr_m1, y_prob_test_m1 = run_eval("1. M1 History-only", LogisticBaseline())
    m_diff, thr_diff, _ = run_eval("2. M4 Difficulty-only", M4DifficultyOnly())
    m_cat, thr_cat, _ = run_eval("3. M4 Category-only", M4CategoryOnly())
    m4, thr_m4, y_prob_test_m4 = run_eval("4. M4 Category+Difficulty", M4CategoryBaseline())
    
    print("\n--- PART 4: GATE X1 DYNAMIC RISK TRACKING (M1 vs M4-full) ---")
    df_ts = df_test_supported.copy()
    df_ts['prob_m1'] = y_prob_test_m1
    df_ts['prob_m4'] = y_prob_test_m4
    
    fail_df = df_ts[df_ts['eventual_outcome'] == 1].copy()
    onset_col = pd.to_numeric(fail_df["annotation_derived_onset_step"], errors="coerce")
    valid_mask = (fail_df["onset_annotated"].astype(bool)) & (onset_col.notna()) & (fail_df["prefix_len"] <= onset_col)
    fail_valid_df = fail_df[valid_mask].copy()
    
    delta_results = []
    
    for ep_id, ep_grp in fail_valid_df.groupby('episode_id'):
        ep_grp = ep_grp.sort_values('prefix_len')
        if len(ep_grp) == 0:
            continue
        p1_m1 = ep_grp.iloc[0]['prob_m1']
        p_last_m1 = ep_grp.iloc[-1]['prob_m1']
        d_m1 = p_last_m1 - p1_m1
        
        p1_m4 = ep_grp.iloc[0]['prob_m4']
        p_last_m4 = ep_grp.iloc[-1]['prob_m4']
        d_m4 = p_last_m4 - p1_m4
        
        delta_results.append({
            'episode_id': ep_id,
            'd_m1': d_m1, 'd_m4': d_m4,
            'onset': ep_grp.iloc[0]['annotation_derived_onset_step']
        })
    
    df_delta = pd.DataFrame(delta_results)
    if len(df_delta) > 0:
        print(f"Num failing episodes evaluated: {len(df_delta)}")
        print(f"M1 DeltaP - Mean: {df_delta['d_m1'].mean():.4f}, Median: {df_delta['d_m1'].median():.4f}, Std: {df_delta['d_m1'].std():.4f}, >0: {(df_delta['d_m1'] > 0).mean():.4f}")
        print(f"M4 DeltaP - Mean: {df_delta['d_m4'].mean():.4f}, Median: {df_delta['d_m4'].median():.4f}, Std: {df_delta['d_m4'].std():.4f}, >0: {(df_delta['d_m4'] > 0).mean():.4f}")
    
    print("\n--- PART 5: TIMELINESS OUTCOME DISTRIBUTION (M1 vs M4-full) ---")
    def compute_timeliness(y_prob_col, thr):
        res = {'TIMELY': 0, 'LATE': 0, 'FALSE': 0, 'MISSED': 0}
        total_fail = df_ts['episode_id'].nunique()
        lead_times = []
        
        for ep_id, ep_grp in df_ts.groupby('episode_id'):
            ep_grp = ep_grp.sort_values('prefix_len')
            outcome = ep_grp.iloc[0]['eventual_outcome']
            has_annot = ep_grp.iloc[0]['onset_annotated']
            onset = pd.to_numeric(ep_grp.iloc[0]['annotation_derived_onset_step'])
            
            crossings = ep_grp[ep_grp[y_prob_col] >= thr]
            if len(crossings) > 0:
                k = crossings.iloc[0]['prefix_len']
                if outcome == 1:
                    if has_annot and not pd.isna(onset) and k <= onset:
                        res['TIMELY'] += 1
                        lead_times.append(onset - k)
                    else:
                        res['LATE'] += 1
                else:
                    res['FALSE'] += 1
            else:
                if outcome == 1:
                    res['MISSED'] += 1
        
        fail_count = len(df_ts[df_ts['eventual_outcome'] == 1]['episode_id'].unique())
        succ_count = len(df_ts[df_ts['eventual_outcome'] == 0]['episode_id'].unique())
        print(f"Stats (Fail={fail_count}, Succ={succ_count}):")
        print(f"TIMELY: {res['TIMELY']} ({res['TIMELY']/fail_count:.1%})")
        print(f"LATE:   {res['LATE']} ({res['LATE']/fail_count:.1%})")
        print(f"MISSED: {res['MISSED']} ({res['MISSED']/fail_count:.1%})")
        print(f"FALSE:  {res['FALSE']} ({res['FALSE']/succ_count:.1%})")
        if lead_times:
            print(f"Median Lead Time (Timely): {np.median(lead_times):.1f} steps")

    print("M1 Timeliness:")
    compute_timeliness('prob_m1', thr_m1)
    print("\nM4-full Timeliness:")
    compute_timeliness('prob_m4', thr_m4)

    print("\n--- PART 6: STATIC-PRIOR CHECK ---")
    def static_check(y_prob_col):
        stds = df_ts.groupby('episode_id')[y_prob_col].std().fillna(0)
        ranges = df_ts.groupby('episode_id')[y_prob_col].apply(lambda x: x.max() - x.min()).fillna(0)
        print(f"Mean Std: {stds.mean():.4f}, Mean Range: {ranges.mean():.4f}, Prop with range > 0.05: {(ranges > 0.05).mean():.4f}")
        
    print("M1:")
    static_check('prob_m1')
    print("M4-full:")
    static_check('prob_m4')

if __name__ == "__main__":
    main()
