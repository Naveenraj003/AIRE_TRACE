import os
import json
import socket
socket.setdefaulttimeout(15)
import time
import pandas as pd
import tarfile
import zstandard as zstd
from datasets import load_dataset
from huggingface_hub import hf_hub_download
from huggingface_hub.utils import HfHubHTTPError, LocalEntryNotFoundError
from requests.exceptions import ReadTimeout, ConnectionError

def check_artifact_validity(local_path):
    """
    Returns (True, "valid") or (False, error_reason)
    """
    try:
        dctx = zstd.ZstdDecompressor()
        with open(local_path, 'rb') as ifh:
            with dctx.stream_reader(ifh) as reader:
                with tarfile.open(mode='r|', fileobj=reader) as tar:
                    for member in tar:
                        if member.name.endswith('agent-logs/mini.traj.json'):
                            f = tar.extractfile(member)
                            if f is not None:
                                data = json.load(f)
                                msgs = data.get("messages", [])
                                if msgs:
                                    return True, "valid"
                                else:
                                    return False, "empty_messages"
                            else:
                                return False, "extractfile_returned_none"
                    return False, "missing_mini_traj_json"
    except Exception as e:
        return False, f"corrupted_archive_{type(e).__name__}"

def download_with_retry(repo_id, artifact_path, max_attempts=5):
    """
    Returns (local_path, "success") or (None, failure_reason)
    """
    delay = 1
    for attempt in range(1, max_attempts + 1):
        try:
            local_path = hf_hub_download(repo_id=repo_id, repo_type="dataset", filename=artifact_path, local_files_only=False)
            return local_path, "success"
        except HfHubHTTPError as e:
            if e.response.status_code == 404:
                return None, "http_404_not_found"
            elif e.response.status_code == 429:
                reason = "http_429_rate_limit"
            else:
                reason = f"http_{e.response.status_code}_error"
        except (ReadTimeout, ConnectionError):
            reason = "connection_timeout"
        except LocalEntryNotFoundError:
            reason = "local_not_found"
        except Exception as e:
            reason = f"download_error_{type(e).__name__}"

        if attempt < max_attempts:
            print(f"    Attempt {attempt} failed ({reason}), retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        else:
            return None, reason

def main():
    print("Loading Contextbench/Tracebench metadata...")
    tb_cfg = {"hf_repo": "Contextbench/Tracebench", "split": "full"}
    tb_ds = load_dataset(tb_cfg["hf_repo"], split=tb_cfg["split"])

    print("Loading prior audit results...")
    audit_df = pd.read_csv("p:\\AIRE-TRACE\\exclusion_audit_results.csv")
    audit_map = {}
    for _, row in audit_df.iterrows():
        audit_map[str(row["traj_id"])] = {
            "status": row["status"],
            "fail_reason": row["fail_reason"]
        }

    recovery_manifest = []

    print(f"Starting recovery job for {len(tb_ds)} rows...")
    for idx, row in enumerate(tb_ds):
        traj_id = str(row.get("traj_id"))
        artifact_path = row.get("artifact_path")
        
        prior_info = audit_map.get(traj_id, {"status": "unknown", "fail_reason": "unknown"})
        prev_status = prior_info["status"]
        prev_reason = prior_info["fail_reason"]
        
        current_status = "unknown"
        current_reason = "unknown"

        if idx % 100 == 0:
            print(f"Processed {idx}/{len(tb_ds)}")

        # 1. Previously valid 636
        if prev_status == "retained":
            # Verify cached artifact
            try:
                local_path = hf_hub_download(repo_id=tb_cfg["hf_repo"], repo_type="dataset", filename=artifact_path, local_files_only=True)
                valid, rsn = check_artifact_validity(local_path)
                if valid:
                    current_status = "verified_existing"
                    current_reason = "valid"
                else:
                    current_status = "structurally_invalid"
                    current_reason = rsn
            except Exception as e:
                current_status = "still_unresolved"
                current_reason = "missing_from_cache"

        # 4. Missing artifact path
        elif prev_reason == "missing_artifact_path":
            if artifact_path:
                current_status = "recovered"
                current_reason = "artifact_path_now_present"
            else:
                current_status = "missing_artifact_path"
                current_reason = "upstream_metadata_missing"

        # 2. Network-excluded 1,457 OR 3. Structurally invalid 1,198
        else:
            if not artifact_path:
                current_status = "missing_artifact_path"
                current_reason = "upstream_metadata_missing"
            else:
                local_path, dl_rsn = download_with_retry(tb_cfg["hf_repo"], artifact_path)
                if local_path:
                    valid, chk_rsn = check_artifact_validity(local_path)
                    if valid:
                        current_status = "recovered"
                        current_reason = "valid"
                    else:
                        current_status = "structurally_invalid"
                        current_reason = chk_rsn
                else:
                    current_status = "still_unresolved"
                    current_reason = dl_rsn

        recovery_manifest.append({
            "traj_id": traj_id,
            "artifact_path": artifact_path,
            "previous_status": prev_status,
            "previous_fail_reason": prev_reason,
            "current_status": current_status,
            "current_failure_reason": current_reason
        })

    print("Saving recovery manifest...")
    df = pd.DataFrame(recovery_manifest)
    df.to_json("p:\\AIRE-TRACE\\recovery_manifest.json", orient="records", indent=2)
    
    print("\n--- RECOVERY SUMMARY ---")
    print(df["current_status"].value_counts())
    print("\nFailure reasons:")
    print(df["current_failure_reason"].value_counts())

if __name__ == "__main__":
    main()
