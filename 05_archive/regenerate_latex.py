import re

def regenerate_latex():
    with open("AIRE-Trace_Universal_IEEE_Conference_Master.tex", "r", encoding="utf-8") as f:
        master = f.read()
    
    body_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', master, re.DOTALL)
    if not body_match:
        return
    body = body_match.group(1)
    
    # 1. Clean Title & Authors
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
    def replace_pandoc_figures(text):
        # We need to find \pandocbounded{...} inside \begin{figure}...\end{figure}
        pattern = r'\\begin\{figure\}.*?\\pandocbounded\{\\includegraphics\[.*?\]\{(.*?)\}\}.*?\\caption\{(.*?)\}.*?\\end\{figure\}'
        def repl(m):
            img_path = m.group(1)
            cap = m.group(2)
            num_match = re.search(r'Fig\.\s*(\d+)', cap)
            label = f"\\label{{fig{num_match.group(1)}}}" if num_match else ""
            return f"""\\begin{{figure*}}[htbp]
\\centerline{{\\includegraphics[width=0.8\\textwidth]{{{img_path}}}}}
\\caption{{{cap}}}
{label}
\\end{{figure*}}"""
        return re.sub(pattern, repl, text, flags=re.DOTALL)
    
    body = replace_pandoc_figures(body)
    
    # Check if there are any standalone \pandocbounded figures
    def standalone_fig_repl(m):
        cap = m.group(1)
        img_path = m.group(2)
        num_match = re.search(r'Fig\.\s*(\d+)', cap)
        label = f"\\label{{fig{num_match.group(1)}}}" if num_match else ""
        return f"""\\begin{{figure*}}[htbp]
\\centerline{{\\includegraphics[width=0.8\\textwidth]{{{img_path}}}}}
\\caption{{{cap}}}
{label}
\\end{{figure*}}"""
    body = re.sub(r'\\pandocbounded\{\\includegraphics\[keepaspectratio,alt=\{(.*?)\}\]\{(.*?)\}\}', standalone_fig_repl, body)
    
    # 5. Tables
    # Remove the wrapper {\def\LTcaptype{none} ... }
    pattern = r'\{\\def\\LTcaptype\{none\}.*?\\begin\{longtable\}\[.*?\]\{(.*?)\}(.*?)\\end\{longtable\}\s*\}'
    def repl(m):
        col_def = m.group(1).replace('\n', '')
        tbl_body = m.group(2)
        tbl_body = re.sub(r'\\(?:endhead|endfirsthead|endfoot|endlastfoot)', '', tbl_body)
        tbl_body = re.sub(r'\\tabularnewline', r'\\\\', tbl_body)
        tbl_body = re.sub(r'\\toprule|\\midrule|\\bottomrule', r'\\hline', tbl_body)
        tbl_body = '\n'.join([line for line in tbl_body.split('\n') if line.strip() != ''])
        return f"""\\begin{{table*}}[htbp]
\\begin{{center}}
\\begin{{tabular}}{{{col_def}}}
{tbl_body}
\\end{{tabular}}
\\end{{center}}
\\end{{table*}}"""
    body = re.sub(pattern, repl, body, flags=re.DOTALL)
    
    pattern2 = r'\\begin\{longtable\}\[.*?\]\{(.*?)\}(.*?)\\end\{longtable\}'
    body = re.sub(pattern2, repl, body, flags=re.DOTALL)
    
    # 6. References
    ref_split = re.split(r'\\subsection\{References\}\\label\{references\}', body)
    if len(ref_split) == 2:
        main_text = ref_split[0]
        ref_text = ref_split[1]
        refs = re.findall(r'\{\[\}(\d+)\{\]\}(.*?)(?=\{\[\}\d+\{\]\}|$)', ref_text, re.DOTALL)
        bib_str = "\\begin{thebibliography}{00}\n"
        for num, text in refs:
            text = text.replace('\n', ' ').strip()
            bib_str += f"\\bibitem{{b{num}}} {text}\n"
        bib_str += "\\end{thebibliography}\n"
        body = main_text + "\n" + bib_str

    final_tex = r"""\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts
\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{array}
\usepackage{calc}
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
    print("Regeneration complete.")

if __name__ == "__main__":
    regenerate_latex()
