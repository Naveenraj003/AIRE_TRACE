import pandas as pd
import numpy as np
from scipy.stats import pointbiserialr

def get_k_data(df, k):
    df_k = df[df["prefix_len"] <= k]
    return df_k.sort_values("prefix_len").groupby("episode_id").last().reset_index()

def main():
    tb_path = "p:/Projects/AIRE-TRACE/data/processed/manifests/terminalbench_prefixes_new.parquet"
    df_tb = pd.read_parquet(tb_path)
    df_train = df_tb[df_tb["split"] == "train"].copy()
    
    df_15 = get_k_data(df_train, 15)
    df_30 = get_k_data(df_train, 30)
    
    unique_episodes = df_train["episode_id"].unique()
    
    B = 1000
    corrs_15 = []
    corrs_30 = []
    
    np.random.seed(42)
    for i in range(B):
        sample_eps = np.random.choice(unique_episodes, size=len(unique_episodes), replace=True)
        
        def sample_df(df_target):
            df_idx = df_target.set_index("episode_id")
            # Using .loc with an array of indices correctly handles duplicates
            return df_idx.loc[sample_eps]
            
        samp_15 = sample_df(df_15)
        samp_30 = sample_df(df_30)
        
        def calc_corr(samp):
            x = samp["feat_unique_tools_used"].values
            y = samp["eventual_outcome"].values
            if np.std(x) == 0:
                return 0.0
            return pointbiserialr(x, y)[0]
            
        corrs_15.append(calc_corr(samp_15))
        corrs_30.append(calc_corr(samp_30))
        
    ci_15 = np.percentile(corrs_15, [2.5, 97.5])
    ci_30 = np.percentile(corrs_30, [2.5, 97.5])
    
    print(f"K=15 CI: [{ci_15[0]:.4f}, {ci_15[1]:.4f}]")
    print(f"K=30 CI: [{ci_30[0]:.4f}, {ci_30[1]:.4f}]")

if __name__ == "__main__":
    main()
