import re

def fix_latex():
    # Start fresh from the pandoc generated tex
    with open("AIRE-Trace_Universal_IEEE_Conference_Master.tex", "r", encoding="utf-8") as f:
        master = f.read()
    
    # Extract body
    body_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', master, re.DOTALL)
    if not body_match:
        print("Could not find document body.")
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
    
    # 4. Figures (removing the pandoc wrapper and replacing with table*)
    # Pandoc wraps figures in \begin{figure}\centering ... \end{figure} 
    # but the image itself is \pandocbounded{\includegraphics[...]{...}}
    # We want to replace the whole \begin{figure}...\end{figure} block or just the includegraphics.
    # Let's find all pandoc figures. Pandoc generates:
    # \begin{figure}
    # \centering
    # \pandocbounded{\includegraphics[keepaspectratio,alt={...}]{figures/ieee/fig...}}
    # \caption{...}
    # \end{figure}
    
    def fig_repl(m):
        content = m.group(0)
        # Extract the image path and caption
        img_match = re.search(r'\\includegraphics\[.*?\]\{(.*?)\}', content)
        cap_match = re.search(r'\\caption\{(.*?)\}', content, re.DOTALL)
        
        if img_match and cap_match:
            img_path = img_match.group(1)
            caption = cap_match.group(1)
            # Find figure number to create a label
            num_match = re.search(r'Fig\.\s*(\d+)', caption)
            label = f"\\label{{fig{num_match.group(1)}}}" if num_match else ""
            
            return f"""\\begin{{figure*}}[htbp]
\\centerline{{\\includegraphics[width=0.8\\textwidth]{{{img_path}}}}}
\\caption{{{caption}}}
{label}
\\end{{figure*}}"""
        return content

    body = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', fig_repl, body, flags=re.DOTALL)
    
    # Wait, some figures in pandoc might not be wrapped in \begin{figure} if they are inline.
    # Let's just catch \pandocbounded{\includegraphics...} that are standalone.
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
    # Instead of parsing the longtable args with regex, just replace \begin{longtable}[]{...} with table*
    # We will find the exact string \begin{longtable} and \end{longtable}
    # Because pandoc longtables might use \begin{longtable}[]{@{}lll@{}}, we can match up to the end of the line
    def table_repl(m):
        # m.group(1) is the column definition, m.group(2) is the body
        col_def = m.group(1)
        tbl_body = m.group(2)
        tbl_body = re.sub(r'\\(?:endhead|endfirsthead|endfoot|endlastfoot)', '', tbl_body)
        tbl_body = re.sub(r'\\tabularnewline', r'\\\\', tbl_body)
        tbl_body = re.sub(r'\\toprule|\\midrule|\\bottomrule', r'\\hline', tbl_body)
        return f"""\\begin{{table*}}[htbp]
\\begin{{center}}
\\begin{{tabular}}{{{col_def}}}
{tbl_body}\\end{{tabular}}
\\end{{center}}
\\end{{table*}}"""

    # Better regex: match \begin{longtable}[...] followed by {col_def} where col_def is everything up to the first \toprule or \hline or similar, OR just match braces.
    # Actually, the simplest is to match \begin{longtable} followed by [anything] then {anything} up to the newline.
    # But col definition can span multiple lines!
    # Let's extract blocks by counting braces or simply replacing \begin{longtable}[...] with \begin{table*}[htbp]\begin{center}\begin{tabular}
    # and \end{longtable} with \end{tabular}\end{center}\end{table*}
    
    # Let's process line by line to replace \begin{longtable}[xxx]{yyy} with tabular
    new_lines = []
    in_table = False
    for line in body.split('\n'):
        if line.startswith(r'\begin{longtable}'):
            # It might have [] and {} on the same line or next lines.
            # We will just replace it. We know it starts with \begin{longtable}.
            # Let's just substitute the \begin{longtable} part.
            line = re.sub(r'\\begin\{longtable\}\[.*?\]', r'\\begin{table*}[htbp]\n\\begin{center}\n\\begin{tabular}', line)
            in_table = True
            new_lines.append(line)
        elif line.startswith(r'\end{longtable}'):
            new_lines.append(r'\end{tabular}')
            new_lines.append(r'\end{center}')
            new_lines.append(r'\end{table*}')
            in_table = False
        elif in_table:
            line = re.sub(r'\\(?:endhead|endfirsthead|endfoot|endlastfoot)', '', line)
            line = re.sub(r'\\tabularnewline', r'\\\\', line)
            line = re.sub(r'\\toprule|\\midrule|\\bottomrule', r'\\hline', line)
            if line.strip() != "":
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    body = "\n".join(new_lines)

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
    
    # Add necessary packages for Pandoc tables (calc, array, etc.)
    # and escape fixes if necessary.
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

    # Fix escaping of %, _, &, #, $, {, } - Pandoc already handles most of this.
    # Let's ensure t_onset in text is t\_onset. Pandoc outputs t\_onset. If any unescaped _ exists outside math, fix it.
    # Actually, just leave what Pandoc did, it's usually correct for escaping.
    
    with open("AIRE-Trace_IEEE/main.tex", "w", encoding="utf-8") as f:
        f.write(final_tex)
    print("Fix applied.")

if __name__ == "__main__":
    fix_latex()
