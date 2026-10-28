import re

def clean_latex():
    with open("AIRE-Trace_IEEE/main.tex", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Fix nested figures
    # The previous run added \begin{figure*} but left pandoc's \begin{figure} \centering ... \end{figure}
    # Let's replace the whole pandoc \begin{figure} block with the new clean block.
    # Actually, let's just strip \begin{figure}\n\centering\n\begin{figure*}[htbp] and so on.
    content = content.replace("\\begin{figure}\n\\centering\n\\begin{figure*}[htbp]", "\\begin{figure*}[htbp]")
    content = content.replace("\\end{figure*}\n\\caption{", "\\caption{")
    # Pandoc also had its own caption, which might now be duplicated.
    # The current state has:
    # \begin{figure*}[htbp]
    # ...
    # \end{figure*}
    # \caption{...}
    # \end{figure}
    
    # We should just regenerate main.tex from Universal_IEEE_Conference_Master.tex cleanly
    pass

if __name__ == "__main__":
    clean_latex()
