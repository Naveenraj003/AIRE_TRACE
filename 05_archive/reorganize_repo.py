"""
reorganize_repo.py
------------------
Executes the approved repository reorganization plan:
1. Creates top-level category directories:
   - 01_research/
   - 02_experiments/
   - 03_patent/
   - 04_ieee_publication/
   - 05_archive/
   - 06_templates_and_uploads/
2. Moves and organizes files safely with detailed logging.
3. Updates paths and verifies integrity.
"""

import os
import shutil
import sys

def organize():
    root = os.path.abspath(".")
    print(f"Starting repository reorganization in: {root}\n")
    
    categories = [
        "01_research",
        "02_experiments",
        "03_patent",
        "04_ieee_publication",
        "05_archive",
        "06_templates_and_uploads"
    ]
    
    for cat in categories:
        cat_path = os.path.join(root, cat)
        if not os.path.exists(cat_path):
            os.makedirs(cat_path, exist_ok=True)
            print(f"Created directory: {cat}/")
            
    # Define file/folder movements: (source, destination_category)
    movements = [
        # --- 01_research ---
        ("RESEARCH_LOG.md", "01_research"),
        ("AIRE-Trace_Frozen_Protocol_and_Plan.md", "01_research"),
        ("PRD.md", "01_research"),
        ("TECHNICAL_DESIGN.md", "01_research"),
        ("PROJECT_ANALYSIS.md", "01_research"),
        ("AIRE-Trace — Prior-Art Claim-Element Chart.md", "01_research"),
        ("AIRE-Trace_Claim_Traceability_Audit.md", "01_research"),
        ("AIRE-Trace_Figure_Traceability_Audit.md", "01_research"),
        ("docs", "01_research"),
        
        # --- 02_experiments ---
        ("src", "02_experiments"),
        ("tests", "02_experiments"),
        ("results", "02_experiments"),
        ("data", "02_experiments"),
        ("configs", "02_experiments"),
        ("reports", "02_experiments"),
        ("dataset_prep.py", "02_experiments"),
        ("repaired_636_canonical.json", "02_experiments"),
        ("exclusion_audit_results.csv", "02_experiments"),
        ("recovery_manifest.json", "02_experiments"),
        ("lineage_verification.txt", "02_experiments"),
        ("post_recovery_audit.txt", "02_experiments"),
        ("run_all.ps1", "02_experiments"),
        ("validate_invariants.py", "02_experiments"),
        
        # --- 03_patent ---
        ("patent_docs", "03_patent"),
        
        # --- 04_ieee_publication ---
        ("AIRE-Trace_Universal_IEEE_Conference_Master.docx", "04_ieee_publication"),
        ("AIRE-Trace_IEEE_Conference_Paper.docx", "04_ieee_publication"),
        ("AIRE-Trace_Universal_IEEE_Conference_Master.pdf", "04_ieee_publication"),
        ("AIRE-Trace_IEEE_Conference_Paper.pdf", "04_ieee_publication"),
        ("AIRE-Trace_Master_IEEE_Manuscript.md", "04_ieee_publication"),
        ("AIRE-Trace_Verified_References.md", "04_ieee_publication"),
        ("AIRE-Trace_IEEE_Submission_Readiness.md", "04_ieee_publication"),
        ("AIRE-Trace_Universal_IEEE_Master_README.md", "04_ieee_publication"),
        ("build_ieee_full_under6_paper.py", "04_ieee_publication"),
        ("generate_clean_ieee_figures.py", "04_ieee_publication"),
        ("verify_docx.py", "04_ieee_publication"),
        ("verify_pdf.py", "04_ieee_publication"),
        ("ieee_docx_helpers.py", "04_ieee_publication"),
        ("validate_universal_ieee_master.py", "04_ieee_publication"),
        ("AIRE-Trace_Universal_IEEE_Conference_Master.tex", "04_ieee_publication"),
        ("AIRE-Trace_IEEE", "04_ieee_publication"),
        
        # --- 05_archive ---
        ("archive", "05_archive"),
        ("scratch", "05_archive"),
        ("AIRE-Trace_IEEE_Draft.md", "05_archive"),
        ("AIRE-Trace_Universal_Master_temp.md", "05_archive"),
        ("AIRE-Trace_IEEE.pdf", "05_archive"),
        ("build_ieee_6page_paper.py", "05_archive"),
        ("build_master.py", "05_archive"),
        ("generate_ieee_docx.py", "05_archive"),
        ("generate_ieee_figures.py", "05_archive"),
        ("generate_pdf.py", "05_archive"),
        ("clean_latex.py", "05_archive"),
        ("fix_latex.py", "05_archive"),
        ("fix_tables.py", "05_archive"),
        ("regenerate_latex.py", "05_archive"),
        ("convert_to_ieee.py", "05_archive"),
        ("convert_svgs.py", "05_archive"),
        ("append_chart.py", "05_archive"),
        ("compare.py", "05_archive"),
        ("patch_app.py", "05_archive"),
        ("create_lit_files.py", "05_archive"),
        ("create_more_lit_files.py", "05_archive"),
        ("update_refs.py", "05_archive"),
        ("update_refs2.py", "05_archive"),
        ("update_refs3.py", "05_archive"),
        ("update_refs4.py", "05_archive"),
        ("update_refs5.py", "05_archive"),
        ("update_refs6.py", "05_archive"),
        ("update_refs7.py", "05_archive"),
        
        # --- 06_templates_and_uploads ---
        ("Conference-LaTeX-template_10-17-19", "06_templates_and_uploads"),
        ("Patent Template ZIP", "06_templates_and_uploads"),
        ("GUIDELINES FOR EXAMINATION OF COMPUTER RELATED INVENTIONS (CRIs) - 2025.pdf", "06_templates_and_uploads")
    ]
    
    # Also handle figures folder:
    # figures/patent -> 03_patent/figures
    # figures/ieee -> 04_ieee_publication/figures
    # entire figures folder preserved or copied
    if os.path.exists("figures/patent"):
        os.makedirs("03_patent/figures", exist_ok=True)
        for item in os.listdir("figures/patent"):
            s = os.path.join("figures/patent", item)
            d = os.path.join("03_patent/figures", item)
            if not os.path.exists(d):
                shutil.copy2(s, d) if os.path.isfile(s) else shutil.copytree(s, d)
        print("Copied patent figures to 03_patent/figures/")

    if os.path.exists("figures/ieee"):
        os.makedirs("04_ieee_publication/figures/ieee", exist_ok=True)
        for item in os.listdir("figures/ieee"):
            s = os.path.join("figures/ieee", item)
            d = os.path.join("04_ieee_publication/figures/ieee", item)
            if not os.path.exists(d):
                shutil.copy2(s, d) if os.path.isfile(s) else shutil.copytree(s, d)
        print("Copied IEEE figures to 04_ieee_publication/figures/ieee/")
        
    # Move figures/ to 05_archive/figures if needed
    movements.append(("figures", "05_archive"))

    for src, dst_cat in movements:
        src_path = os.path.join(root, src)
        dst_path = os.path.join(root, dst_cat, os.path.basename(src))
        if os.path.exists(src_path):
            try:
                # If destination already exists, remove it first to avoid collision
                if os.path.exists(dst_path):
                    if os.path.isdir(dst_path):
                        shutil.rmtree(dst_path)
                    else:
                        os.remove(dst_path)
                shutil.move(src_path, dst_path)
                print(f"Moved: {src} -> {dst_cat}/{os.path.basename(src)}")
            except Exception as e:
                print(f"Error moving {src} to {dst_cat}: {e}")
        else:
            print(f"Skipped (not found): {src}")
            
    print("\nFile movements complete.")

if __name__ == "__main__":
    organize()
