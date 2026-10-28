file_path = r"p:\Projects\AIRE-TRACE\AIRE-Trace — Prior-Art Claim-Element Chart.md"
with open(file_path, "a", encoding="utf-8") as f:
    f.write("\n\n## RAIL (Recoverability-Aware Intervention Learning) Candidates\n")
    f.write("| Reference                      | What It Discloses                                                             | Candidate Killed       |\n")
    f.write("| ------------------------------ | ----------------------------------------------------------------------------- | ---------------------- |\n")
    f.write("| EvoUndo (arXiv:2608.28363)     | Round-trip recoverability verification (mutate → recover → check equivalence) | Candidate 1            |\n")
    f.write("| AgentRewind (arXiv:2608.14380) | Checkpoint/restore for agent recovery                                         | Candidate 1            |\n")
    f.write("| PAINT (ICML 2022)              | Reversibility estimation + proactive intervention                             | Candidate 2            |\n")
    f.write("| Doyle 1979 (TMS)               | Justification-based belief revision                                           | Candidate 4            |\n")
    f.write("| de Kleer 1986 (ATMS)           | Assumption-based truth maintenance                                            | Candidate 4            |\n")
    f.write("| BLIP (arXiv:2608.25210)        | Minimal verifiable provenance for black-box LLM                               | Candidate 5            |\n")
    f.write("| Gupta/Mumick 1993 (IVM)        | Incremental view maintenance                                                  | Candidate 6            |\n")
    f.write("| RAIL (arXiv:2608.05080)        | Recoverability-aware intervention learning                                    | Counterfactual revival |\n")
    f.write("\nFailFast (arXiv:2608.03222) — baseline for comparison\n")

print("Appended table to Claim-Element Chart")
