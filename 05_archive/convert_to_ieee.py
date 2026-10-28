import re
import os

def convert():
    with open("AIRE-Trace_Universal_IEEE_Conference_Master.tex", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract body between \begin{document} and \end{document}
    body_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', content, re.DOTALL)
    if not body_match:
        print("Could not find document body.")
        return
    body = body_match.group(1)
    
    # 1. Title & Authors
    body = re.sub(r'\\section\{AIRE-Trace: A Standardized Prospective.*?\\label\{.*?\}', '', body, flags=re.DOTALL)
    body = re.sub(r'\\begin\{center\}\\rule.*?\\end\{center\}', '', body, flags=re.DOTALL)
    
    author_placeholder_pattern = r'\*\*\{\[}AUTHOR 1 NAME\{\]}\*\*.*?TO BE DETERMINED\{\]}'
    body = re.sub(author_placeholder_pattern, '', body, flags=re.DOTALL)
    
    # 2. Abstract & Keywords
    body = re.sub(r'\\subsection\{Abstract\}\\label\{abstract\}', r'\\begin{abstract}', body)
    body = re.sub(r'\*\*Index Terms:\*\* (.*?)\n', r'\\end{abstract}\n\n\\begin{IEEEkeywords}\n\1\n\\end{IEEEkeywords}\n', body)
    
    # 3. Sections
    body = re.sub(r'\\subsection\{[IVX]+\.\s*(.*?)\}\\label\{.*?\}', r'\\section{\1}', body)
    body = re.sub(r'\\subsubsection\{[A-Z]\.\s*(.*?)\}\\label\{.*?\}', r'\\subsection{\1}', body)
    body = re.sub(r'\\paragraph\{\d+\.\s*(.*?)\}\\label\{.*?\}', r'\\subsubsection{\1}', body)
    
    # 4. Figures
    fig_pattern = r'\\pandocbounded\{\\includegraphics\[keepaspectratio,alt=\{Fig\.\s*(\d+)\.\s*(.*?)\}\]\{figures/ieee/(.*?)\}\}'
    def fig_repl(m):
        fnum, fcap, fpath = m.groups()
        return f"""\\begin{{figure}}[htbp]
\\centerline{{\\includegraphics[width=\\columnwidth]{{figures/ieee/{fpath}}}}}
\\caption{{{fcap}}}
\\label{{fig{fnum}}}
\\end{{figure}}"""
    body = re.sub(fig_pattern, fig_repl, body)
    
    # 5. Tables
    # Pandoc longtables are complex. Let's just convert them simply or rely on string replacement.
    table_pattern = r'\\begin\{longtable\}\[.*?\]\{(@\{\}l.*?\)\})\}\n(.*?)\\end\{longtable\}'
    def tab_repl(m):
        col_def = m.group(1).replace('@{}', '').replace('()', '')
        tbl_body = m.group(2)
        # Remove endhead, endfirsthead, etc.
        tbl_body = re.sub(r'\\end(?:first)?head', '', tbl_body)
        tbl_body = re.sub(r'\\end(?:last)?foot', '', tbl_body)
        tbl_body = re.sub(r'\\toprule', '\\hline', tbl_body)
        tbl_body = re.sub(r'\\midrule', '\\hline', tbl_body)
        tbl_body = re.sub(r'\\bottomrule', '\\hline', tbl_body)
        return f"""\\begin{{table}}[htbp]
\\begin{{center}}
\\begin{{tabular}}{{{col_def}}}
{tbl_body}\\end{{tabular}}
\\end{{center}}
\\end{{table}}"""
    body = re.sub(table_pattern, tab_repl, body, flags=re.DOTALL)
    
    # 6. References
    # Find the References section and convert it to thebibliography
    ref_split = re.split(r'\\subsection\{References\}\\label\{references\}', body)
    if len(ref_split) == 2:
        main_text = ref_split[0]
        ref_text = ref_split[1]
        
        # Parse references: they are like `{[}1{]} Authors, "Title,"...`
        refs = re.findall(r'\{\[\}(\d+)\{\]\}(.*?)(?=\{\[\}\d+\{\]\}|$)', ref_text, re.DOTALL)
        
        bib_str = "\\begin{thebibliography}{00}\n"
        for num, text in refs:
            text = text.replace('\n', ' ').strip()
            bib_str += f"\\bibitem{{b{num}}} {text}\n"
        bib_str += "\\end{thebibliography}\n"
        
        body = main_text + "\n" + bib_str
    
    # Combine with IEEE template
    final_tex = r"""\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts
\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{longtable}
\def\BibTeX{{\rm B\kern-.05em{\sc i\kern-.025em b}\kern-.08em
    T\kern-.1667em\lower.7ex\hbox{E}\kern-.125emX}}

\begin{document}

\title{AIRE-Trace: A Standardized Prospective Evaluation Protocol for Online Agent-Failure Warning}

\author{\IEEEauthorblockN{[AUTHOR 1 NAME]}
\IEEEauthorblockA{\textit{[AUTHOR 1 DEPARTMENT]} \\
\textit{[AUTHOR 1 INSTITUTION]}\\
[CITY, COUNTRY] \\
[AUTHOR 1 EMAIL]}
\and
\IEEEauthorblockN{[AUTHOR 2 NAME]}
\IEEEauthorblockA{\textit{[AUTHOR 2 DEPARTMENT]} \\
\textit{[AUTHOR 2 INSTITUTION]}\\
[CITY, COUNTRY] \\
[AUTHOR 2 EMAIL]}
}

\maketitle

""" + body + "\n\\end{document}\n"
    
    with open("AIRE-Trace_IEEE/main.tex", "w", encoding="utf-8") as f:
        f.write(final_tex)
    print("Conversion complete.")

if __name__ == "__main__":
    convert()
