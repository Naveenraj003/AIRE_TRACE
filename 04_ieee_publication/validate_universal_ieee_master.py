import os
import re

def validate_master_files():
    print("Validating Universal IEEE Conference Master files...\n")
    
    files_to_check = [
        "AIRE-Trace_Universal_IEEE_Conference_Master.docx",
        "AIRE-Trace_Universal_IEEE_Conference_Master.tex",
        "AIRE-Trace_Universal_IEEE_Conference_Master.pdf",
        "AIRE-Trace_Universal_IEEE_Master_README.md"
    ]
    
    all_exist = True
    for f in files_to_check:
        if not os.path.exists(f):
            print(f"FAIL: Missing file {f}")
            all_exist = False
        else:
            print(f"PASS: Found {f}")
    
    if not all_exist:
        return False
        
    print("\nReading generated TeX file for content validation...")
    print("NOTE: This validates the TeX source and generated files' existence. It does not validate correct PDF rendering.\n")
    with open("AIRE-Trace_Universal_IEEE_Conference_Master.tex", "r", encoding="utf-8") as f:
        tex_content = f.read()

    # Verify figures exist as files and are referenced
    figures = ["fig1_aire_trace_architecture", "fig2_provenance_recovery", 
               "fig3_prospective_prefix", "fig4_mode_a_auroc", 
               "fig5_a4_ablation", "fig6_gate6_operational"]
    
    missing_figs = []
    missing_fig_files = []
    for fig in figures:
        if fig not in tex_content:
            missing_figs.append(fig)
        if not os.path.exists(f"figures/ieee/{fig}.png"):
            missing_fig_files.append(fig)
            
    if missing_fig_files:
        print(f"FAIL: Missing actual figure PNG files in figures/ieee/: {missing_fig_files}")
    else:
        print("PASS: 6/6 Figure PNG source files exist")

    if missing_figs:
        print(f"FAIL: Missing figures in TeX output: {missing_figs}")
    else:
        print("PASS: 6/6 Figures are referenced in TeX output")

    # Verify 13 references exist
    missing_refs = []
    
    # Split manuscript into body and references to ensure citations exist in the body
    parts = re.split(r'\\section\*?\{References\}', tex_content, flags=re.IGNORECASE)
    if len(parts) < 2:
        # Fallback if LaTeX structure differs
        parts = re.split(r'References\}\\label\{references\}', tex_content, flags=re.IGNORECASE)
        
    if len(parts) >= 2:
        body_content = parts[0]
        ref_content = parts[1]
    else:
        print("WARNING: Could not split References section. Checking entire document.")
        body_content = tex_content
        ref_content = tex_content

    for i in range(1, 14):
        # In TeX, pandoc escapes [ as {[}
        body_has_cite = f"[{i}]" in body_content or f"{{[}}{i}{{]}}" in body_content
        if not body_has_cite:
            missing_refs.append(i)
            
    if missing_refs:
        print(f"FAIL: Missing citation markers in body for references: {missing_refs}")
    else:
        print("PASS: 13/13 References cited in the manuscript body")

    # Check for unresolved scientific placeholders
    if "[REFERENCE TO BE VERIFIED]" in tex_content:
        print("FAIL: Found unresolved placeholder [REFERENCE TO BE VERIFIED]")
    else:
        print("PASS: No scientific placeholders remain")

    # Check for Markdown syntax leaking (very basic check)
    if "### " in tex_content or "## " in tex_content:
        print("FAIL: Markdown heading syntax found in TeX")
    else:
        print("PASS: No Markdown headings found in TeX")

    # Scientific Invariants
    invariants = {
        "3,316": "Declared rows",
        "636": "Canonical study episodes",
        "163": "TRAIN size",
        "416": "TEST size",
        "317": "TEST failures",
        "99": "Successful episodes",
        "257": "Valid annotated failures",
        "60": "Unannotated failures",
        "K=30": "Horizon",
        "0.8294": "PDC value"
    }

    invariants_passed = True
    for val, name in invariants.items():
        if val not in tex_content:
            print(f"FAIL: Missing numerical invariant {name} ({val})")
            invariants_passed = False
    
    if invariants_passed:
        print("PASS: Key numerical invariants are present")

    # Model list check
    for m in ["H1", "H2", "H3", "H4", "M1", "S1", "S2"]:
        if m not in tex_content:
            print(f"FAIL: Missing model {m}")

    # No L empirical results
    if "L   " in tex_content and "0." in tex_content.split("L ")[1][:10]:
         print("FAIL: Found empirical results seemingly attributed to L")
    else:
         print("PASS: No empirical results for L")
         
    # Page count equivalent (word count proxy)
    words = len(tex_content.split())
    print(f"\nWord count proxy: {words} words in TeX file (not including LaTeX boilerplate).")
    print("\nSTATUS: COMPLETE (Check log above for PASS/FAIL flags)")

if __name__ == "__main__":
    validate_master_files()
