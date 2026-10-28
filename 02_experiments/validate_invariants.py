import re

def validate():
    with open("AIRE-Trace_IEEE/main.tex", "r", encoding="utf-8") as f:
        content = f.read()
    
    invariants = [
        "3,316", "636", "163", "57", "416", "317", "99", "257", "60",
        "K=30", "0.8294", "0.881", "H1", "H2", "H3", "H4", "M1", "S1", "S2", "B=1000"
    ]
    
    missing = []
    for inv in invariants:
        if inv not in content:
            missing.append(inv)
            
    if missing:
        print(f"FAIL: Missing invariants: {missing}")
    else:
        print("PASS: All numerical invariants found.")

if __name__ == "__main__":
    validate()
