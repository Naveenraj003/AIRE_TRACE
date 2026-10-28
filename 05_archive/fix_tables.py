import re
import os

def fix_tables():
    with open("AIRE-Trace_IEEE/main.tex", "r", encoding="utf-8") as f:
        content = f.read()

    def replace_table(match):
        col_def = match.group(1).replace('@{}', '')
        body = match.group(2)
        # Remove pandoc-specific longtable commands
        body = re.sub(r'\\(?:endhead|endfirsthead|endfoot|endlastfoot)', '', body)
        body = re.sub(r'\\tabularnewline', r'\\\\', body)
        body = re.sub(r'\\toprule|\\midrule|\\bottomrule', r'\\hline', body)
        # Wrap in table* to span columns if it's too wide, or just table.
        # Given it's a conference template, table* is often safer for long tables,
        # but let's use table* to ensure it fits.
        return f"""\\begin{{table*}}[htbp]
\\begin{{center}}
\\begin{{tabular}}{{{col_def}}}
{body}\\end{{tabular}}
\\end{{center}}
\\end{{table*}}"""

    # Non-greedy match for the longtable contents
    content = re.sub(r'\\begin\{longtable\}\[\]\{(.*?)\}(.*?)\\end\{longtable\}', replace_table, content, flags=re.DOTALL)
    
    with open("AIRE-Trace_IEEE/main.tex", "w", encoding="utf-8") as f:
        f.write(content)
        
if __name__ == "__main__":
    fix_tables()
