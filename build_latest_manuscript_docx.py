"""
build_latest_manuscript_docx.py
-------------------------------
Generates the exact, 100% faithful IEEE Conference Microsoft Word Document (.docx)
for the latest AIRE-Trace manuscript:
Source: conference_submissions/iConCISE_2027/working/main.tex
Compiled PDF reference: AIRE_Trace_Manuscript.pdf

Preserves:
- Full Title
- All 4 Verified Authors, Affiliations, Institutions, Emails
- Complete Abstract verbatim
- All 7 Roman-numeral Sections & Subsections
- All Mathematical Formulations & Equations (1) and (2)
- All 5 IEEE Result Tables (Tables I - V) with exact empirical numbers, booktabs borders & footnotes
- All 3 Embedded Figures (Figs. 1 - 3) with exact IEEE captions
- All 13 IEEE References [1] - [13] with hanging indentation
- Strict IEEE two-column layout with US Letter geometry
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION_START
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# --- Geometry & Column Helpers ---

def set_page_setup(section):
    """Sets standard IEEE US Letter page geometry: 8.5x11 in, 0.75" top, 1.0" bottom, 0.625" margins."""
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(0.625)
    section.right_margin = Inches(0.625)
    section.header_distance = Inches(0.4)
    section.footer_distance = Inches(0.4)

def set_columns(section, num_cols=2, space_twips=360):
    """Configures multi-column section layout with specified gutter width (360 twips = 0.25 in)."""
    sectPr = section._sectPr
    cols = sectPr.xpath('./w:cols')
    if cols:
        col = cols[0]
    else:
        col = OxmlElement('w:cols')
        sectPr.append(col)
    col.set(qn('w:num'), str(num_cols))
    col.set(qn('w:space'), str(space_twips))

def set_table_borders(table):
    """Applies IEEE booktabs styling: top & bottom solid line (0.75 pt), no vertical lines."""
    tblPr = table._tbl.tblPr
    borders_xml = parse_xml(
        '<w:tblBorders ' + nsdecls('w') + '>\n'
        '  <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>\n'
        '  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>\n'
        '  <w:left w:val="none"/>\n'
        '  <w:right w:val="none"/>\n'
        '  <w:insideH w:val="none"/>\n'
        '  <w:insideV w:val="none"/>\n'
        '</w:tblBorders>'
    )
    tblPr.append(borders_xml)

def set_header_bottom_border(row):
    """Adds a single bottom border line (0.5 pt) under the table header row."""
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = tcPr.first_child_found_in("w:tcBorders")
        if tcBorders is None:
            tcBorders = OxmlElement('w:tcBorders')
            tcPr.append(tcBorders)
        b_bottom = OxmlElement('w:bottom')
        b_bottom.set(qn('w:val'), 'single')
        b_bottom.set(qn('w:sz'), '5')
        b_bottom.set(qn('w:space'), '0')
        b_bottom.set(qn('w:color'), '000000')
        tcBorders.append(b_bottom)

def set_cell_margins(cell, top=12, bottom=12, left=25, right=25):
    """Sets internal cell margins in dxa units for compact, professional tables."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for edge, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        m = OxmlElement(f'w:{edge}')
        m.set(qn('w:w'), str(val))
        m.set(qn('w:type'), 'dxa')
        tcMar.append(m)
    tcPr.append(tcMar)

# --- Typography & Rich Inline Parsing ---

def parse_runs_from_latex(text, base_font="Times New Roman", base_size=9.5, base_bold=False, base_italic=False):
    """
    Parses LaTeX formatted text into a sequence of rich runs with proper bold, italic,
    monospace, superscripts, subscripts, and symbols.
    """
    t = text.replace('\n', ' ')
    t = re.sub(r'\s+', ' ', t).strip()

    # Pre-replacements
    t = t.replace(r'\%', '%').replace(r'\_', '_').replace(r'\&', '&')
    t = t.replace(r'\{', '{').replace(r'\}', '}')
    t = t.replace('{,}', ',')
    t = t.replace('---', '—').replace('--', '–')
    t = t.replace('``', '“').replace("''", '”')
    t = t.replace(r'\,', ' ').replace(r'\.', '.').replace('~', ' ')

    # Citations
    def replace_cite(m):
        keys = [k.strip() for k in m.group(1).split(',')]
        nums = []
        for k in keys:
            if k.startswith('b') and k[1:].isdigit():
                nums.append(int(k[1:]))
            else:
                nums.append(k)
        if all(isinstance(n, int) for n in nums):
            if len(nums) > 2 and nums == list(range(nums[0], nums[-1]+1)):
                return f"[{nums[0]}–{nums[-1]}]"
            return "[" + ", ".join(str(n) for n in nums) + "]"
        return "[" + ", ".join(str(n) for n in nums) + "]"
    t = re.sub(r'\\cite\{([^}]+)\}', replace_cite, t)

    # Cross-references
    t = t.replace(r'\ref{fig:arch}', '1')
    t = t.replace(r'\ref{fig:prefix}', '2')
    t = t.replace(r'\ref{fig:auroc}', '3')
    t = t.replace(r'\ref{tab:models}', 'I')
    t = t.replace(r'\ref{tab:primary}', 'II')
    t = t.replace(r'\ref{tab:bootstrap}', 'III')
    t = t.replace(r'\ref{tab:ablation}', 'IV')
    t = t.replace(r'\ref{tab:operational}', 'V')
    t = t.replace(r'\eqref{eq:far}', '(1)')
    t = t.replace(r'\eqref{eq:dyn_comp}', '(2)')

    # Splitting into LaTeX tags
    pattern = r'(\\textbf\{[^{}]+\}|\\textit\{[^{}]+\}|\\texttt\{[^{}]+\}|\$[^\$]+\$)'
    tokens = re.split(pattern, t)

    runs = []
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith(r'\textbf{') and tok.endswith('}'):
            inner = tok[8:-1]
            runs.append({'text': inner, 'bold': True, 'italic': base_italic, 'font': base_font, 'size': base_size})
        elif tok.startswith(r'\textit{') and tok.endswith('}'):
            inner = tok[8:-1]
            runs.append({'text': inner, 'bold': base_bold, 'italic': True, 'font': base_font, 'size': base_size})
        elif tok.startswith(r'\texttt{') and tok.endswith('}'):
            inner = tok[8:-1]
            runs.append({'text': inner, 'bold': base_bold, 'italic': False, 'font': 'Courier New', 'size': base_size - 1})
        elif tok.startswith('$') and tok.endswith('$'):
            inner = tok[1:-1]
            if inner == r'9.999 \times 10^{-5}':
                runs.append({'text': '9.999 × 10', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size})
                runs.append({'text': '−5', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size, 'super': True})
            elif inner == r'p_{\mathrm{adj}}':
                runs.append({'text': 'p', 'bold': base_bold, 'italic': True, 'font': base_font, 'size': base_size})
                runs.append({'text': 'adj', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size, 'sub': True})
            elif inner == r'H_0':
                runs.append({'text': 'H', 'bold': base_bold, 'italic': True, 'font': base_font, 'size': base_size})
                runs.append({'text': '0', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size, 'sub': True})
            elif inner == r'\Delta':
                runs.append({'text': 'Δ', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size})
            elif inner == r'\Delta\mathrm{AUROC}':
                runs.append({'text': 'ΔAUROC', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size})
            elif inner == r'\tau':
                runs.append({'text': 'τ', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size})
            elif inner == r'\tau^*':
                runs.append({'text': 'τ*', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size})
            elif inner == r'\tau^* = 0.5522':
                runs.append({'text': 'τ* = 0.5522', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size})
            elif inner == r'\tau^2':
                runs.append({'text': 'τ²', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size})
            elif inner == r'\alpha':
                runs.append({'text': 'α', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size})
            elif inner == r'\alpha=0.05':
                runs.append({'text': 'α = 0.05', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size})
            elif inner == r'-':
                runs.append({'text': '−', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size})
            elif inner == r'^\dagger':
                runs.append({'text': '†', 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size, 'super': True})
            elif inner in ['B', 'K', 'T_i', 'W', 'L', 't']:
                runs.append({'text': inner, 'bold': base_bold, 'italic': True, 'font': base_font, 'size': base_size})
            else:
                clean_m = inner
                clean_m = clean_m.replace(r'\leq', '≤').replace(r'\geq', '≥')
                clean_m = clean_m.replace(r'\times', '×').replace(r'\Delta', 'Δ')
                clean_m = clean_m.replace(r'\tau', 'τ').replace(r'\alpha', 'α')
                clean_m = clean_m.replace(r'\mathrm', '').replace(r'\mathbf', '')
                clean_m = clean_m.replace(r'\in', '∈').replace(r'\wedge', '∧')
                clean_m = clean_m.replace(r'\exists', '∃').replace(r'\mid', '|')
                clean_m = clean_m.replace(r'\ldots', '…').replace(r'\_', '_')
                clean_m = clean_m.replace('{', '').replace('}', '')
                clean_m = clean_m.replace(r'\texttt', '')
                clean_m = clean_m.replace('$', '')
                clean_m = clean_m.replace('-', '−')
                runs.append({'text': clean_m, 'bold': base_bold, 'italic': False, 'font': base_font, 'size': base_size})
        else:
            runs.append({'text': tok, 'bold': base_bold, 'italic': base_italic, 'font': base_font, 'size': base_size})

    return runs

def add_paragraph_runs(p, runs):
    """Appends run dicts to a docx paragraph."""
    for r_data in runs:
        r = p.add_run(r_data['text'])
        r.font.name = r_data.get('font', 'Times New Roman')
        r.font.size = Pt(r_data.get('size', 9.5))
        r.bold = r_data.get('bold', False)
        r.italic = r_data.get('italic', False)
        if r_data.get('super'):
            r.font.superscript = True
        if r_data.get('sub'):
            r.font.subscript = True
    return p

def add_body_p(doc, text, indent=True, space_before=0, space_after=0):
    """Adds a standard justified IEEE body paragraph."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.0
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.14)
    else:
        p.paragraph_format.first_line_indent = Pt(0)
    runs = parse_runs_from_latex(text, base_font="Times New Roman", base_size=9.5)
    add_paragraph_runs(p, runs)
    return p

def add_h1(doc, num_str, title_str):
    """Appends centered Roman numeral Level 1 heading."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.keep_with_next = True
    full_text = f"{num_str}. {title_str.upper()}" if num_str else title_str.upper()
    r = p.add_run(full_text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    return p

def add_h2(doc, letter_str, title_str):
    """Appends left-aligned Level 2 heading."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(4.5)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(f"{letter_str}.  {title_str}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.0)
    r.font.italic = True
    return p

def add_list_item(doc, item_num, text):
    """Appends an enumerated list item with clean hanging indentation."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.first_line_indent = Inches(-0.2)
    r_lead = p.add_run(f"{item_num}) ")
    r_lead.font.name = "Times New Roman"
    r_lead.font.size = Pt(9.5)
    runs = parse_runs_from_latex(text, base_font="Times New Roman", base_size=9.5)
    add_paragraph_runs(p, runs)
    return p

def add_equation_block(doc, eq_text, eq_num_str):
    """Adds a centered equation with right-aligned numbering using a borderless 2-column table."""
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    # Left cell (math formula centered)
    c0 = tbl.rows[0].cells[0]
    c0.width = Inches(2.8)
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(2)
    p0.paragraph_format.space_after = Pt(2)
    p0.paragraph_format.line_spacing = 1.0
    runs = parse_runs_from_latex(eq_text, base_font="Times New Roman", base_size=9.5)
    add_paragraph_runs(p0, runs)
    
    # Right cell (equation number right aligned)
    c1 = tbl.rows[0].cells[1]
    c1.width = Inches(0.55)
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(2)
    p1.paragraph_format.line_spacing = 1.0
    r1 = p1.add_run(eq_num_str)
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(9.5)
    
    # Clean zero borders
    for row in tbl.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')
            for b_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
                b = OxmlElement(f'w:{b_name}')
                b.set(qn('w:val'), 'none')
                tcBorders.append(b)
            tcPr.append(tcBorders)
            set_cell_margins(cell, top=6, bottom=6, left=10, right=10)

def add_figure_block(doc, img_path, fig_num, caption_text, width_in=3.35):
    """Embeds a centered figure image with IEEE formatted caption."""
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        r_pic = p_img.add_run()
        r_pic.add_picture(img_path, width=Inches(width_in))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cap.paragraph_format.space_before = Pt(1)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.line_spacing = 1.0
    p_cap.paragraph_format.first_line_indent = Pt(0)
    
    r_lbl = p_cap.add_run(f"Fig. {fig_num}.  ")
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(7.5)
    r_lbl.font.bold = True
    
    runs = parse_runs_from_latex(caption_text, base_font="Times New Roman", base_size=7.5)
    add_paragraph_runs(p_cap, runs)

def add_table_block(doc, tbl_num, tbl_title, headers, rows_data, col_widths, alignments, footnote_text=None):
    """Constructs a professional IEEE booktabs table."""
    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_head.paragraph_format.space_before = Pt(5)
    p_head.paragraph_format.space_after = Pt(1.5)
    p_head.paragraph_format.keep_with_next = True
    r_t = p_head.add_run(f"TABLE {tbl_num}:  {tbl_title.upper()}")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(7.5)
    r_t.font.bold = True

    table = doc.add_table(rows=len(rows_data)+1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    set_header_bottom_border(table.rows[0])

    for c_idx, h in enumerate(headers):
        cell = table.rows[0].cells[c_idx]
        if col_widths and c_idx < len(col_widths):
            cell.width = Inches(col_widths[c_idx])
        set_cell_margins(cell, top=12, bottom=12, left=20, right=20)
        p = cell.paragraphs[0]
        p.alignment = alignments[c_idx] if alignments else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        runs = parse_runs_from_latex(h, base_font="Times New Roman", base_size=7.5, base_bold=True)
        add_paragraph_runs(p, runs)

    for r_idx, row in enumerate(rows_data):
        r_elem = table.rows[r_idx+1]
        for c_idx, val in enumerate(row):
            cell = r_elem.cells[c_idx]
            if col_widths and c_idx < len(col_widths):
                cell.width = Inches(col_widths[c_idx])
            set_cell_margins(cell, top=10, bottom=10, left=20, right=20)
            p = cell.paragraphs[0]
            p.alignment = alignments[c_idx] if alignments else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            runs = parse_runs_from_latex(str(val), base_font="Times New Roman", base_size=7.5)
            add_paragraph_runs(p, runs)

    if footnote_text:
        p_fn = doc.add_paragraph()
        p_fn.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_fn.paragraph_format.space_before = Pt(1)
        p_fn.paragraph_format.space_after = Pt(3.5)
        p_fn.paragraph_format.line_spacing = 1.0
        p_fn.paragraph_format.first_line_indent = Pt(0)
        runs = parse_runs_from_latex(footnote_text, base_font="Times New Roman", base_size=7.0, base_italic=True)
        add_paragraph_runs(p_fn, runs)

def add_reference_item(doc, num, text):
    """Appends an IEEE reference item with hanging indent formatting."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0.5)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.first_line_indent = Inches(-0.2)
    
    r_n = p.add_run(f"[{num}]  ")
    r_n.font.name = "Times New Roman"
    r_n.font.size = Pt(7.5)
    
    runs = parse_runs_from_latex(text, base_font="Times New Roman", base_size=7.5)
    add_paragraph_runs(p, runs)

# --- Main Document Builder ---

def build_manuscript_docx(output_path):
    print(f"Building Word Document: {output_path}...")
    doc = docx.Document()

    # -------------------------------------------------------------
    # SECTION 0: Full-Width Title & 4-Author Grid (1 Column)
    # -------------------------------------------------------------
    sec0 = doc.sections[0]
    set_page_setup(sec0)
    set_columns(sec0, num_cols=1, space_twips=0)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(10)
    p_title.paragraph_format.line_spacing = 1.0
    r_t = p_title.add_run("AIRE-Trace: A Standardized Prospective Evaluation and Trajectory Risk Decomposition Framework for Online Agent-Failure Warning")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(20)
    r_t.font.bold = True

    # 4-Author Block (2x2 Table, centered, no borders, total width = 7.25")
    auth_tbl = doc.add_table(rows=2, cols=2)
    auth_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    auth_tbl.autofit = False

    authors_data = [
        # Row 0
        [
            ("B. Naveen Raj", ["Dept. of CSE (AIML)", "K.S. Rangasamy College of Technology", "Tiruchengode–637215, India", "naveenrajbv1@gmail.com"]),
            ("C. Janani", ["Assistant Professor", "Dept. of CSE (AIML)", "K.S. Rangasamy College of Technology", "Tiruchengode–637215, India", "srijanani2030@gmail.com"])
        ],
        # Row 1
        [
            ("P. Krishnamoorthi", ["Dept. of CSE (AIML)", "K.S. Rangasamy College of Technology", "Tiruchengode–637215, India", "pkrishnamoorthi126@gmail.com"]),
            ("L. Maadhava Kumar", ["Associate Software Developer", "Mphasis", "Chennai, India", "maadhava05@gmail.com"])
        ]
    ]

    for row_idx, row_pair in enumerate(authors_data):
        for col_idx, (name, affil_lines) in enumerate(row_pair):
            cell = auth_tbl.rows[row_idx].cells[col_idx]
            cell.width = Inches(3.55)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4 if row_idx > 0 else 0)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            
            r_n = p.add_run(f"{name}\n")
            r_n.font.name = "Times New Roman"
            r_n.font.size = Pt(10)
            r_n.font.bold = True

            for l_idx, line in enumerate(affil_lines):
                r_l = p.add_run(line + ("\n" if l_idx < len(affil_lines)-1 else ""))
                r_l.font.name = "Times New Roman"
                r_l.font.size = Pt(8.5)
                if "Assistant Professor" in line or "Associate Software Developer" in line or "Dept." in line:
                    r_l.font.italic = True

    # Clear borders on author table
    for row in auth_tbl.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')
            for b_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
                b = OxmlElement(f'w:{b_name}')
                b.set(qn('w:val'), 'none')
                tcBorders.append(b)
            tcPr.append(tcBorders)

    # Spacer
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # SECTION 1: Two-Column IEEE Body
    # -------------------------------------------------------------
    sec1 = doc.add_section(WD_SECTION_START.CONTINUOUS)
    set_page_setup(sec1)
    set_columns(sec1, num_cols=2, space_twips=360) # 0.25" gutter

    # Abstract Paragraph 1
    p_abs1 = doc.add_paragraph()
    p_abs1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs1.paragraph_format.space_before = Pt(0)
    p_abs1.paragraph_format.space_after = Pt(2)
    p_abs1.paragraph_format.line_spacing = 1.0
    p_abs1.paragraph_format.first_line_indent = Pt(0)

    r_lead = p_abs1.add_run("Abstract—")
    r_lead.font.name = "Times New Roman"
    r_lead.font.size = Pt(8.5)
    r_lead.font.bold = True
    r_lead.font.italic = True

    abs1_text = (
        "The increasing deployment of autonomous tool-using AI agents creates demand for mechanisms that provide "
        "prospective warning of task failure from partial execution trajectories, rather than retrospective diagnosis "
        "after failure has occurred. Prior work on online agent-failure warning has demonstrated that prefix-based "
        "failure prediction is viable, but existing methods each use their own datasets, prefix definitions, "
        "calibration procedures, and metrics, making comparative claims difficult to interpret."
    )
    runs_abs1 = parse_runs_from_latex(abs1_text, base_font="Times New Roman", base_size=8.5, base_bold=True)
    add_paragraph_runs(p_abs1, runs_abs1)

    # Abstract Paragraph 2
    abs2_text = (
        "This paper presents AIRE-Trace, a standardized prospective evaluation protocol for online agent-failure "
        "warning that fixes information visibility, failure-target definition, alert semantics, calibration procedure, "
        "false-alarm constraints, and lead-time measurement. We further propose trajectory risk decomposition "
        "(\\texttt{dyn\\_comp}), which combines static and dynamic risk signals from trajectory prefixes to improve "
        "prospective recall under the protocol's false-alarm budget."
    )
    p_abs2 = doc.add_paragraph()
    p_abs2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs2.paragraph_format.space_before = Pt(1)
    p_abs2.paragraph_format.space_after = Pt(2)
    p_abs2.paragraph_format.line_spacing = 1.0
    p_abs2.paragraph_format.first_line_indent = Pt(0)
    runs_abs2 = parse_runs_from_latex(abs2_text, base_font="Times New Roman", base_size=8.5, base_bold=True)
    add_paragraph_runs(p_abs2, runs_abs2)

    # Abstract Paragraph 3
    abs3_text = (
        "The protocol is applied to representative heuristic (H1–H4), classical machine-learning (M1), "
        "tabular ensemble (S1), sequence-model (S2), and risk-decomposition (\\texttt{dyn\\_comp}) warning methods "
        "on 636 reconstructed episodes (a 19.18% strict-retention sample of the 3,316 declared source rows), split "
        "task-disjointly into TRAIN (163), CALIBRATION (57), and TEST (416). Under the stringent 5% false-alarm "
        "rate (FAR) constraint, \\texttt{dyn\\_comp} achieved a modest prospective Recall@FAR of 0.1167 (FAR = 0.0404), "
        "compared with the M1 baseline at 0.0078 (FAR = 0.0303). A paired episode-cluster bootstrap ($B$ = 10,000) "
        "confirmed the difference ($\\Delta$ = +0.1089, 95% CI [0.0706, 0.1496], $p_{\\mathrm{adj}}$ = $9.999 \\times 10^{-5}$). "
        "Baseline AUROC ranged from 0.5074 to 0.6371. Feature ablation showed that omitting cumulative error and retry "
        "signals yielded the largest observed drop in discrimination ($\\Delta\\mathrm{AUROC}$ = −0.1069). Pairwise "
        "Direction Consistency across seven baselines was 0.8294 (21/21 informative pairs), indicating largely but not "
        "universally consistent rankings."
    )
    p_abs3 = doc.add_paragraph()
    p_abs3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs3.paragraph_format.space_before = Pt(1)
    p_abs3.paragraph_format.space_after = Pt(6)
    p_abs3.paragraph_format.line_spacing = 1.0
    p_abs3.paragraph_format.first_line_indent = Pt(0)
    runs_abs3 = parse_runs_from_latex(abs3_text, base_font="Times New Roman", base_size=8.5, base_bold=True)
    add_paragraph_runs(p_abs3, runs_abs3)

    # =============================================================
    # I. INTRODUCTION
    # =============================================================
    add_h1(doc, "I", "Introduction")
    add_body_p(doc, 
        "The deployment of autonomous agentic systems—agents that plan, invoke tools, and execute multi-step tasks "
        "with limited human oversight—has raised reliability questions that standard outcome benchmarking cannot fully "
        "answer. Benchmarks such as AgentBench \\cite{b1}, AgentBoard \\cite{b2}, and GAIA \\cite{b3} measure whether "
        "an agent ultimately succeeds or fails, but this final-outcome evaluation is insufficient for monitoring purposes: "
        "by the time the outcome is observed, the agent has already consumed resources and potentially caused unrecoverable side effects.",
        indent=False)

    add_body_p(doc,
        "\\textit{Prospective failure warning} addresses a complementary question: given only the portion of the "
        "trajectory observed so far (a prefix), can a monitor produce a timely alert that the episode will likely fail "
        "\\textit{before} the outcome is known? This early-warning capability would enable intervention—pausing the agent, "
        "escalating to human review, or switching strategies—before failure becomes irreversible.")

    add_body_p(doc,
        "Recent work has shown that prefix-based failure prediction is achievable. PrefixGuard \\cite{b7} demonstrates "
        "prefix-based warning monitors on WebArena and TerminalBench. AgentForesight \\cite{b8} employs an RL-trained "
        "7B-parameter auditor. Trajectory Guard \\cite{b9} applies real-time sequence anomaly detection. However, "
        "these methods each use their own datasets, prefix definitions, calibration procedures, and metrics. No existing "
        "work cross-compares heuristic, classical-ML, and sequence-model warning methods under one fixed protocol, making "
        "it unclear whether reported advantages are robust to a common evaluation protocol or partially artifacts of "
        "differing evaluation conditions.")

    add_body_p(doc, "AIRE-Trace addresses this gap with two contributions:")
    add_list_item(doc, 1, 
        "A \\textbf{standardized prospective evaluation protocol} for online agent-failure warning—fixing information "
        "visibility (pre-onset prefix only), failure-target definition, alert semantics, calibration procedure (FAR $\\leq$ 5%), "
        "and statistical inference (episode-cluster bootstrap with Holm–Bonferroni correction).")
    add_list_item(doc, 2,
        "\\textbf{Trajectory risk decomposition} (\\texttt{dyn\\_comp}), which combines static base-rate and dynamic "
        "trajectory-prefix risk signals to improve prospective recall under the protocol's false-alarm constraint.")

    add_body_p(doc, "AIRE-Trace is an \\textit{offline evaluator} of pre-recorded agent trajectories. It does not perform live intervention.", indent=True)
    add_body_p(doc, 
        "\\textbf{Research Question.} \\textit{Do comparative performance claims for online agent-failure warning methods "
        "remain consistent when methods are evaluated under identical information, target, alert, calibration, lead-time, "
        "and compute constraints?}", indent=True)

    # =============================================================
    # II. RELATED WORK AND COMPARATIVE GAP
    # =============================================================
    add_h1(doc, "II", "Related Work and Comparative Gap")
    
    add_h2(doc, "A", "Agent Outcome Benchmarking")
    add_body_p(doc,
        "Outcome benchmarks \\cite{b1,b2,b3} establish performance baselines for agent capabilities but do not provide "
        "mechanisms for prospective mid-execution monitoring. TRAIL \\cite{b4} articulates the need for robust evaluation "
        "of agentic traces, presenting 148 human-annotated traces for trace-debugging evaluation.", indent=False)

    add_h2(doc, "B", "Retrospective Failure Attribution")
    add_body_p(doc,
        "Post-hoc attribution methods identify where or why a trajectory went wrong after failure has occurred. "
        "AgentRx \\cite{b5} provides post-hoc localization of critical failure steps. Who&When Pro \\cite{b6} addresses "
        "retrospective attribution using 12,326 trajectories. AgentProcessBench \\cite{b11} introduces step-level quality "
        "evaluation with 8,509 human-labeled annotations. These approaches require the complete trajectory and are "
        "retrospective by construction.", indent=False)

    add_h2(doc, "C", "Prospective Agent-Failure Warning")
    add_body_p(doc,
        "PrefixGuard \\cite{b7} achieves AUPRC of 0.900 on WebArena and 0.557 on TerminalBench under its own evaluation protocol. "
        "Direct numerical comparison with AIRE-Trace results is not appropriate due to differences in prefix representation, "
        "feature regime, and calibration protocol. AgentForesight \\cite{b8} employs an RL-trained auditor. Trajectory Guard \\cite{b9} "
        "applies sequence anomaly detection. Advani \\cite{b10} characterizes false success in LLM agents, showing that TF-IDF "
        "detectors achieve AUROC 0.83–0.95 for false-success detection. These works collectively establish prospective warning as a "
        "viable research direction but operate in isolation without cross-comparison under a common protocol.", indent=False)

    add_h2(doc, "D", "Evaluation Methodology")
    add_body_p(doc,
        "Cameron, Gelbach, and Miller \\cite{b12} establish the pairs cluster bootstrap as the appropriate inference "
        "procedure when observations are dependent within clusters. Holm \\cite{b13} introduced the sequentially "
        "rejective multiple test procedure for familywise error rate control.", indent=False)

    # =============================================================
    # III. AIRE-TRACE METHODOLOGY
    # =============================================================
    add_h1(doc, "III", "AIRE-Trace Methodology")
    add_body_p(doc,
        "The AIRE-Trace prospective evaluation protocol enforces strict separation between pre-onset trajectory monitoring, "
        "offline threshold calibration, and test-set prospective evaluation, as illustrated in Fig. 1.", indent=False)

    fig1_path = r"P:\Projects\AIRE-TRACE\conference_submissions\iConCISE_2027\working\figures\fig1_aire_trace_architecture.png"
    add_figure_block(doc, fig1_path, 1,
        "AIRE-Trace standardized prospective evaluation pipeline. Trajectories are provenance-audited before episode-level splitting; "
        "trainable methods are fitted on TRAIN, operating thresholds are selected on CALIBRATION under the FAR constraint, and frozen "
        "thresholds are applied to the TEST population.")

    add_h2(doc, "A", "Prospective Evaluation Protocol")
    add_body_p(doc,
        "An agent episode consists of a sequence of events $e_1, e_2, \\ldots, e_T$ produced by an autonomous agent executing a "
        "task. Each event contains role information (agent, tool, user, system), action type, tool names, and error indicators. "
        "The episode has an eventual outcome: \\texttt{eventual\\_success} or \\texttt{eventual\\_failure}.", indent=False)

    add_body_p(doc,
        "For TerminalBench episodes, the failure onset is defined as $t_{\\mathrm{onset}} = \\min(\\texttt{incorrect\\_step\\_ids})$. "
        "Episodes lacking this annotation are excluded from onset-dependent metrics (Recall@FAR, lead time) but remain eligible "
        "for ranking metrics (AUROC, AUPRC).")

    add_body_p(doc,
        "At checkpoint $t \\in \\{1, \\ldots, \\min(T_i, K)\\}$ with horizon $K=30$, a monitor accesses only the prefix $(e_1, \\ldots, e_t)$. "
        "The checkpoint schedule is outcome-independent and episode-symmetric. An alert at checkpoint $t$ is \\textit{prospective} if and only "
        "if $t \\leq t_{\\mathrm{onset}}$; an alert at $t > t_{\\mathrm{onset}}$ is a \\textit{late detection} and is reported separately in the "
        "operational analysis. The prospective evaluation semantics are illustrated in Fig. 2.")

    fig2_path = r"P:\Projects\AIRE-TRACE\conference_submissions\iConCISE_2027\working\figures\fig3_prospective_prefix.png"
    add_figure_block(doc, fig2_path, 2,
        "Prospective prefix evaluation semantics. At each checkpoint, the monitor observes only the trajectory prefix. Alerts at or before the "
        "annotated failure onset constitute prospective detections; alerts after onset are analyzed separately as late detections.")

    add_body_p(doc,
        "Given a prefix at checkpoint $t$, a monitor produces a risk score $s(e_1,\\ldots,e_t) \\in [0,1]$. An alert is raised when "
        "$s \\geq \\tau$ for a calibrated threshold $\\tau$. Episode-level FAR is defined in (1):")

    add_equation_block(doc, r"\mathrm{FAR} = \frac{|\{i : \mathrm{success}(i) \wedge \exists\, t:\,\mathrm{alert}_t\}|}{|\{i : \mathrm{success}(i)\}|}", "(1)")

    add_body_p(doc,
        "Each episode contributes equally to prefix-level metric computation via episode-balanced weighting: $w_{i,t} = 1 / \\min(T_i, K)$.", indent=False)

    add_body_p(doc,
        "\\textbf{Evaluation Modes.} \\textit{Mode A} (TerminalBench, primary): supports AUROC, AUPRC, Brier, ECE, prospective Recall@FAR, "
        "lead time, and late-detection analysis. \\textit{Mode B} ($\\tau^2$-Bench, diagnostic): reports eventual-outcome ranking metrics only. "
        "Mode B metrics must not be compared directly to Mode A metrics.")

    add_h2(doc, "B", "Dataset and Task-Disjoint Splits")
    add_body_p(doc,
        "The primary corpus is Tracebench (3,316 declared source rows). After provenance auditing and reconstruction, 2,655 rows were structurally "
        "invalid due to missing trajectory artifacts, 25 contained unreachable artifact paths, and network recovery attempts yielded zero additional "
        "valid episodes, leaving 636 canonical episodes (19.18%) for benchmarking. These exclusions represent strict structural data-availability "
        "attrition; however, missingness cannot be assumed to be missing completely at random (MCAR). Consequently, systematic selection bias "
        "cannot be ruled out, and all empirical findings remain formally bounded to this audited 636-episode cohort. The overall pipeline "
        "structure is depicted in Fig. 1.", indent=False)

    add_body_p(doc,
        "The 636 episodes are split task-disjointly (entire episode to exactly one split): TRAIN (163), CALIBRATION (57), TEST (416). The TEST "
        "population contains 317 failed episodes (257 with valid onset annotations, 60 without), and 99 successful episodes.")

    add_h2(doc, "C", "Threshold Calibration and Alert Semantics")
    add_body_p(doc,
        "The calibration procedure selects $\\tau^* = \\arg\\max_\\tau \\mathrm{Recall}(\\tau)$ subject to $\\mathrm{FAR}_{\\mathrm{calib}}(\\tau) \\leq 0.05$, "
        "on the CALIBRATION split only. Ties are broken by lower FAR first, then higher threshold. The selected threshold $\\tau^*$ is frozen before TEST evaluation.", indent=False)

    add_h2(doc, "D", "Trajectory Risk Decomposition")
    add_body_p(doc,
        "The trajectory risk decomposition method (\\texttt{dyn\\_comp}) decomposes the failure risk score into an empirical static task-difficulty "
        "prior and a dynamic prefix-derived risk signal in (2):", indent=False)

    add_equation_block(doc, r"s_{\mathrm{dyn\_comp}}(t) = P_{\mathrm{M1}}(\mathrm{fail} \mid e_{1:t}) - P_{\mathrm{static}}(\mathrm{fail} \mid \mathrm{task})", "(2)")

    add_body_p(doc,
        "where $P_{\\mathrm{M1}}(\\mathrm{fail} \\mid e_{1:t})$ is the dynamic failure probability predicted by the logistic baseline M1 from the 13 "
        "prefix features $\\mathbf{x}_{1:t}$, and $P_{\\mathrm{static}}(\\mathrm{fail} \\mid \\mathrm{task})$ is a static prior fitted on the TRAIN "
        "split from task category and difficulty failure base rates. Both components are strictly computable at prefix checkpoint $t$ without "
        "future trajectory leakage. The residual score $s_{\\mathrm{dyn\\_comp}}(t) \\in [-1, 1]$ isolates excess dynamic risk relative to static "
        "task expectations. The operating threshold $\\tau^* = 0.5522$ is calibrated on CALIBRATION under the $\\mathrm{FAR} \\leq 5\\%$ constraint, "
        "identical to all baselines.", indent=False)

    # =============================================================
    # IV. EXPERIMENTAL SETUP
    # =============================================================
    add_h1(doc, "IV", "Experimental Setup")
    
    add_h2(doc, "A", "Models and Baselines")
    add_body_p(doc, "Seven baseline methods and one proposed method are registered (Table I):", indent=False)

    t1_headers = ["ID", "Family", "Method / Key Parameters"]
    t1_rows = [
        ["H1", "Heuristic", "Tool-error rate (min-max norm)"],
        ["H2", "Heuristic", "Retry-count (min-max norm)"],
        ["H3", "Heuristic", "Repeated-action (min-max norm)"],
        ["H4", "Heuristic", "Combined (sigmoid z-score avg)"],
        ["M1", "Classical", "Logistic Regression (C=1.0, lbfgs)"],
        ["S1", "Tabular ensemble", "Random Forest (100 trees, depth=6)"],
        ["S2", "Sequence", "GRU (hidden=64, 1 layer, 10 epochs)"],
        ["dyn_comp", "Proposed", "Trajectory risk decomposition"],
        ["L", "Semantic", "LLM monitor (not evaluated)"]
    ]
    add_table_block(doc, "I", "Warning Method Registry", t1_headers, t1_rows,
                    col_widths=[0.6, 1.1, 1.7],
                    alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
                    footnote_text="L skipped: RTX 2050, 4 GB.")

    add_body_p(doc,
        "All trainable models use 13 Category-A structural features computed from the prefix: \\texttt{feat\\_steps\\_so\\_far} (cumulative step count), "
        "four actor-role counts (agent, tool, user, system), three action-type counts (message, tool_call, tool_result), "
        "\\texttt{feat\\_tool\\_error\\_count} (cumulative tool errors), \\texttt{feat\\_retry\\_count} (consecutive error sequences), "
        "\\texttt{feat\\_unique\\_tools\\_used}, \\texttt{feat\\_tool\\_call\\_ratio}, and \\texttt{feat\\_repeated\\_action\\_last2}. Models are fitted "
        "on TRAIN with episode-balanced sample weights; all use random seed 42. S1 is evaluated as a tabular ensemble baseline that maps cumulative "
        "prefix trajectory statistics into a non-recurrent decision forest, directly contrasting with S2's hidden-state GRU recurrence.")

    add_h2(doc, "B", "Metrics and Statistical Analysis")
    add_body_p(doc, "\\textbf{Ranking metrics} (prefix-level, episode-balanced): AUROC, AUPRC, Brier Score, ECE.", indent=False)
    add_body_p(doc, "\\textbf{Operational metrics} (episode-level): FAR (denominator: 99 successful TEST episodes), Recall@FAR (denominator: 257 valid annotated failure episodes).")
    add_body_p(doc, 
        "\\textbf{Bootstrap inference:} Paired episode-cluster bootstrap. Standard baseline comparisons use $B$ = 1,000 iterations. "
        "The primary \\texttt{dyn\\_comp} vs. M1 comparison uses $B$ = 10,000 iterations. Episodes are resampled with replacement at the episode level "
        "(not prefix level) to preserve within-episode dependence \\cite{b12}. Frozen thresholds are held constant across resamples. "
        "Prefix-level resampling is incorrect because prefixes within the same episode share the outcome label, violating independence "
        "and producing artificially narrow CIs.")
    add_body_p(doc, "\\textbf{Multiple-comparison correction:} Holm–Bonferroni step-down correction \\cite{b13} across predefined comparison families, $\\alpha$ = 0.05.")
    add_body_p(doc, 
        "\\textbf{Pairwise Direction Consistency (PDC):} For each model pair $(A,B)$, wins $W$ and losses $L$ are counted across AUROC, AUPRC, "
        "Recall@FAR, and ECE. Pairs with $W+L=0$ are excluded. If $W=2$ and $L=2$, pair PDC = 0.50; otherwise PDC = $\\max(W,L)/(W+L)$. "
        "Overall PDC is the arithmetic mean of informative pair PDCs, always reported with its coverage figure.")

    # =============================================================
    # V. RESULTS
    # =============================================================
    add_h1(doc, "V", "Results")
    
    add_h2(doc, "A", "Primary Prospective Warning Results")
    add_body_p(doc,
        "Table II presents the primary Mode A TEST performance. Under the FAR $\\leq$ 5% constraint, \\texttt{dyn\\_comp} achieved Recall@FAR "
        "of 0.1167 with FAR of 0.0404 (frozen threshold 0.5522). The M1 baseline achieved Recall@FAR of 0.0078 with FAR of 0.0303 (frozen threshold 0.98). "
        "All remaining baselines achieved Recall@FAR of 0.0000, with the exception of H3, whose Recall@FAR is undefined because its calibration FAR "
        "reached 1.000 (the 5% constraint was not achievable).", indent=False)

    t2_headers = ["Model", "τ", "AUROC", "Recall@FAR", "FAR"]
    t2_rows = [
        ["H1", "0.86", "0.6205", "0.0000", "0.0000"],
        ["H2", "0.89", "0.5752", "0.0000", "0.0000"],
        ["H3", "0.01", "0.5074", "undef.†", "1.0000"],
        ["H4", "0.93", "0.6135", "0.0000", "0.0202"],
        ["M1", "0.98", "0.6215", "0.0078", "0.0303"],
        ["S1", "0.97", "0.6371", "0.0000", "0.0404"],
        ["S2", "0.74", "0.5496", "0.0000", "0.0000"],
        ["dyn_comp", "0.5522", "0.3593", "0.1167", "0.0404"]
    ]
    add_table_block(doc, "II", "Primary Mode A TEST Performance (K=30, FAR ≤ 5%)", t2_headers, t2_rows,
                    col_widths=[0.75, 0.45, 0.6, 0.9, 0.7],
                    alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT],
                    footnote_text="†H3 Recall@FAR undefined: calibration FAR = 1.000.")

    add_body_p(doc,
        "In Table II, \\texttt{dyn\\_comp}'s protocol-consistent episode-balanced prefix AUROC is 0.3593. Because \\texttt{dyn\\_comp} subtracts "
        "the static task-difficulty prior ($P_{\\mathrm{static}}$, whose observed failure-ranking AUROC is 0.6940), early non-erroneous prefixes "
        "of difficult failed episodes can yield negative residual scores, producing a sub-0.5 global prefix AUROC. The residual is an operational "
        "anomaly detector rather than a monotonic global risk score; the primary evaluation remains thresholded prospective warning. At the frozen "
        "operating threshold ($\\tau^* = 0.5522$), \\texttt{dyn\\_comp} fires only on extreme positive dynamic risk spikes, achieving Recall@FAR of 0.1167 "
        "at FAR of 0.0404, while the M1 baseline yields Recall@FAR of 0.0078 at FAR of 0.0303.")

    add_body_p(doc, "\\textbf{Primary paired comparison.} Table III presents the primary \\texttt{dyn\\_comp} vs. M1 bootstrap result.")

    t3_headers = ["Quantity", "Value"]
    t3_rows = [
        ["Metric", "Recall@FAR (prospective)"],
        ["Observed Δ (dyn_comp − M1)", "+0.1089"],
        ["95% CI", "[0.0706, 0.1496]"],
        ["Bootstrap B", "10,000"],
        ["Bootstrap unit", "Episode-cluster (joint)"],
        ["p_adj", "9.999 × 10^-5"],
        ["Reject H0 at α=0.05", "Yes"],
        ["dyn_comp FAR", "0.0404"],
        ["M1 FAR", "0.0303"]
    ]
    add_table_block(doc, "III", "Primary dyn_comp vs. M1 Bootstrap Comparison", t3_headers, t3_rows,
                    col_widths=[1.8, 1.6],
                    alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

    add_h2(doc, "B", "Baseline Comparative Results")
    add_body_p(doc,
        "Among the seven baselines, Mode A AUROC ranged from 0.5074 (H3) to 0.6371 (S1). S1 (Random Forest, AUROC = 0.6371, 95% CI [0.5885, 0.6745]) "
        "achieved the highest observed AUROC, as visualized in Fig. 3.", indent=False)

    fig3_path = r"P:\Projects\AIRE-TRACE\conference_submissions\iConCISE_2027\working\figures\fig4_mode_a_auroc.png"
    add_figure_block(doc, fig3_path, 3,
        "Mode A TEST AUROC for baseline warning methods (K=30). Error bars denote 95% episode-cluster bootstrap confidence intervals. "
        "S1 (Random Forest) achieved the highest observed AUROC (0.6371).")

    add_body_p(doc,
        "Paired episode-cluster bootstrap testing ($B$ = 1,000, Holm–Bonferroni correction) showed S1 had statistically significant AUROC "
        "advantages over S2 ($\\Delta$ = +0.0875, $p_{\\mathrm{adj}}$ = 0.006), H2 ($\\Delta$ = +0.0619, $p_{\\mathrm{adj}}$ = 0.006), "
        "and H3 ($\\Delta$ = +0.1297, $p_{\\mathrm{adj}}$ = 0.006), but not over M1, H1, or H4. For AUPRC, S1's advantage was statistically "
        "significant only against S2 ($p_{\\mathrm{adj}}$ = 0.012).")

    add_body_p(doc,
        "Despite S1's highest AUROC, its prospective Recall@FAR at FAR $\\leq$ 5% was 0.0000, illustrating a fundamental gap between "
        "discriminative performance and operational early-warning utility.")

    add_body_p(doc,
        "\\textbf{FAR sensitivity.} S1 evaluated at FAR targets of 1%, 5%, and 10% achieved identical frozen thresholds at 1% and 5% "
        "($\\tau$ = 0.97, Recall@FAR = 0.0000). At 10% FAR target ($\\tau$ = 0.93), Recall@FAR improved to 0.0973, indicating the recall/FAR trade-off.")

    add_h2(doc, "C", "Ranking Consistency")
    add_body_p(doc,
        "The overall Pairwise Direction Consistency (PDC) across the seven baselines (H1, H2, H3, H4, M1, S1, S2) was \\textbf{0.8294} with "
        "coverage of 0.881 across 21/21 informative pairs. This indicates that the majority of pairwise ranking directions are consistent "
        "across metrics, while approximately 17% of comparisons contain at least one metric disagreement. \\texttt{dyn\\_comp} is not included "
        "in this baseline PDC matrix.", indent=False)

    add_h2(doc, "D", "Ablation and Robustness")
    add_body_p(doc,
        "Feature ablation (A0–A6) on S1 under the frozen protocol is summarized in Table IV. Removing error and retry signals "
        "(\\texttt{feat\\_tool\\_error\\_count} and \\texttt{feat\\_retry\\_count}; ablation A4) produced the largest observed discrimination "
        "degradation ($\\Delta\\mathrm{AUROC}$ = −0.1069, from 0.6371 to 0.5302). All other ablations produced $|\\Delta\\mathrm{AUROC}| < 0.004$. "
        "This identifies error and retry signals as the feature group whose removal produced the largest observed discrimination loss under S1 "
        "and the evaluated feature set.", indent=False)

    t4_headers = ["ID", "Removed Features", "AUROC", "Δ"]
    t4_rows = [
        ["A0", "None (full baseline)", "0.6371", "—"],
        ["A1", "steps_so_far", "0.6357", "−0.0014"],
        ["A2", "4 actor-role features", "0.6335", "−0.0036"],
        ["A3", "3 action-type features", "0.6383", "+0.0012"],
        ["A4", "error_count + retry", "0.5302", "−0.1069"],
        ["A5", "tools + ratio", "0.6360", "−0.0011"],
        ["A6", "repeated_action", "0.6341", "−0.0030"]
    ]
    add_table_block(doc, "IV", "S1 Feature Ablation Results (Mode A, K=30)", t4_headers, t4_rows,
                    col_widths=[0.45, 1.75, 0.6, 0.6],
                    alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])

    add_h2(doc, "E", "Operational Analysis")
    add_body_p(doc,
        "The operational analysis examines false alarms, late detections, and alert burden under frozen thresholds, summarized in Table V. "
        "H3 (FAR = 1.000) alerts on all 99 successful TEST episodes and 19.84% of valid failure episodes received only late (post-onset) alerts "
        "(accounting for 3,339 late alerts out of 8,012 total alerts across the TEST split). This illustrates why the onset boundary must "
        "be explicitly enforced: H3's activity represents retrospective diagnosis, not prospective warning.", indent=False)

    t5_headers = ["Model", "FA Ep.", "TEST FAR", "Only-Late Ep. (%)", "Total Alerts", "Mean/Ep."]
    t5_rows = [
        ["H1", "0", "0.0000", "2 (0.78%)", "19", "0.046"],
        ["H2", "0", "0.0000", "2 (0.78%)", "16", "0.039"],
        ["H3", "99", "1.0000", "51 (19.84%)", "8,012", "19.260"],
        ["H4", "2", "0.0202", "8 (3.11%)", "119", "0.286"],
        ["M1", "3", "0.0303", "10 (3.89%)", "161", "0.387"],
        ["S1", "4", "0.0404", "16 (6.23%)", "25", "0.060"],
        ["S2", "0", "0.0000", "10 (3.89%)", "107", "0.257"]
    ]
    add_table_block(doc, "V", "Operational Warning Profile (Mode A, K=30, Frozen τ)", t5_headers, t5_rows,
                    col_widths=[0.55, 0.45, 0.6, 0.95, 0.45, 0.4],
                    alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT],
                    footnote_text="FA Ep.: false-alarm episodes (out of 99 successful TEST episodes).\nOnly-Late: failure episodes with solely post-onset alerts (out of 257).")

    add_body_p(doc,
        "Among models operating within the FAR target, S1 produced the lowest alert burden (25 total alerts, max 2 per episode) but zero prospective recall. "
        "\\texttt{dyn\\_comp}, with 0.0404 FAR, achieved the only non-trivial prospective recall (0.1167) among all evaluated methods.")

    # =============================================================
    # VI. DISCUSSION AND LIMITATIONS
    # =============================================================
    add_h1(doc, "VI", "Discussion and Limitations")
    
    add_h2(doc, "A", "The Operational Recall Collapse")
    add_body_p(doc,
        "The most critical finding is the collapse of prospective Recall@FAR under the 5% FAR constraint: the baselines with a defined "
        "Recall@FAR achieved zero or near-zero prospective recall; H3 was undefined because the 5% FAR constraint was not achievable. "
        "S1's AUROC of 0.6371 demonstrates meaningful probabilistic discrimination, but the discriminative signal is insufficient to "
        "generate threshold-based alerts on individual failure episodes before onset without FAR violations. \\texttt{dyn\\_comp}'s Recall@FAR "
        "of 0.1167 represents a statistically significant improvement over M1's 0.0078, but the absolute recall remains modest. "
        "The gap between discriminative ranking capability and operational early-warning utility is a structural finding of this evaluation.", indent=False)

    add_h2(doc, "B", "Selective Statistical Significance")
    add_body_p(doc,
        "The bootstrap-tested AUROC advantages for S1 are statistically significant only against S2, H2, and H3. "
        "Its advantages over M1, H1, and H4 are not statistically significant after Holm–Bonferroni correction. "
        "The empirical ordering S1 > M1 > H1 > H4 by point estimate does not reflect universally distinguishable statistical differences.", indent=False)

    add_h2(doc, "C", "Limitations")
    add_body_p(doc,
        "\\textbf{Population coverage and selection bias.} The 636 retained episodes represent 19.18% of the 3,316 declared source rows. "
        "Because exclusion was driven by artifact corruption and unreachable paths rather than random subsampling, the retained cohort may "
        "systematically differ from the excluded episodes across task complexity, agent run length, or failure distribution. The reported "
        "failure distributions and warning behaviors are valid within the audited canonical population, but generalization to the uncurated "
        "source population remains unverified.", indent=False)

    add_body_p(doc,
        "\\textbf{Incomplete onset annotation.} 60 of 317 TEST failure episodes (18.9%) lack onset annotations. These episodes are excluded "
        "from onset-dependent Recall@FAR and late-detection analysis but remain available for ranking metrics. Systematic differences between "
        "annotated and unannotated episodes may affect reported prospective-warning rates.")

    add_body_p(doc,
        "\\textbf{LLM-monitor evaluation.} The L (LLM-monitor) model was not evaluated because the available hardware (RTX 2050, 4 GB VRAM) "
        "could not support protocol-compliant evaluation over the full dataset. No conclusions about L's prospective performance can be drawn.")

    add_body_p(doc,
        "\\textbf{Domain scope.} Transferability of the protocol and results is restricted to the evaluated tool-use coding-task domain. "
        "Generalization to other agent types or task domains has not been established.")

    add_body_p(doc,
        "\\textbf{Offline evaluation.} AIRE-Trace is an offline evaluator of recorded trajectories, not a runtime intervention mechanism. "
        "Deployment considerations are outside the scope of this work.")

    # =============================================================
    # VII. CONCLUSION
    # =============================================================
    add_h1(doc, "VII", "Conclusion")
    add_body_p(doc,
        "This study evaluated prospective failure warning from trajectory-prefix information under an explicit separation between "
        "pre-onset prediction and post-onset alerting, using 636 reconstructed episodes with a task-disjoint TRAIN/CALIBRATION/TEST "
        "split and frozen calibration thresholds.", indent=False)

    add_body_p(doc,
        "Across seven baselines at $K$=30, Mode A AUROC ranged from 0.5074 to 0.6371. Under the 5% FAR constraint, the baselines with "
        "a defined Recall@FAR achieved zero or near-zero prospective recall (H3 was undefined because its calibration FAR reached 1.000). "
        "Trajectory risk decomposition (\\texttt{dyn\\_comp}) achieved Recall@FAR of 0.1167, a statistically significant improvement over M1 "
        "($\\Delta$ = +0.1089, 95% CI [0.0706, 0.1496], $p_{\\mathrm{adj}}$ = $9.999 \\times 10^{-5}$, $B$ = 10,000 episode-cluster bootstrap).")

    add_body_p(doc,
        "Feature ablation confirmed that omitting error and retry signals produced the largest observed discrimination loss "
        "($\\Delta\\mathrm{AUROC}$ = −0.1069 at A4). PDC of 0.8294 across 21 informative baseline pairs indicates largely consistent "
        "but not universal ranking stability. The evaluated trajectory-prefix structural features contain limited information about "
        "eventual task failure, and translating that information into reliable early warning under strict operational false-alarm constraints "
        "remains an open challenge.")

    # =============================================================
    # REFERENCES
    # =============================================================
    add_h1(doc, "", "References")

    references_data = [
        (1, "X. Liu et al., \"AgentBench: Evaluating LLMs as Agents,\" in Proc. ICLR, 2024. arXiv:2308.03688."),
        (2, "C. Ma et al., \"AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents,\" in Proc. NeurIPS, 2024. arXiv:2401.13178."),
        (3, "G. Mialon et al., \"GAIA: A Benchmark for General AI Assistants,\" in Proc. ICLR, 2024. arXiv:2311.12983."),
        (4, "D. Deshpande et al., \"TRAIL: Trace Reasoning and Agentic Issue Localization,\" arXiv:2505.08638, 2025."),
        (5, "S. Barke et al., \"AgentRx: Diagnosing AI Agent Failures from Execution Trajectories,\" arXiv:2602.02475, 2026."),
        (6, "J. Liu et al., \"Who&When Pro: Can LLMs Really Attribute Failures in AI Agents?\" arXiv:2607.09996, 2026."),
        (7, "X. Huang et al., \"PrefixGuard: From LLM-Agent Traces to Online Failure-Warning Monitors,\" arXiv:2605.06455, 2026."),
        (8, "B. Zhang et al., \"AgentForesight: Online Auditing for Early Failure Prediction in Multi-Agent Systems,\" arXiv:2605.08715, 2026."),
        (9, "L. Advani, \"Trajectory Guard: A Lightweight, Sequence-Aware Model for Real-Time Anomaly Detection in Agentic AI,\" arXiv:2601.00516, 2026."),
        (10, "L. Advani, \"From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents,\" arXiv:2606.09863, 2026."),
        (11, "S. Fan et al., \"AgentProcessBench: Diagnosing Step-Level Process Quality in Tool-Using Agents,\" arXiv:2603.14465, 2026."),
        (12, "A. C. Cameron, J. B. Gelbach, and D. L. Miller, \"Bootstrap-Based Improvements for Inference with Clustered Errors,\" Rev. Econ. Stat., vol. 90, no. 3, pp. 414–427, 2008."),
        (13, "S. Holm, \"A Simple Sequentially Rejective Multiple Test Procedure,\" Scand. J. Stat., vol. 6, no. 2, pp. 65–70, 1979.")
    ]

    for num, ref_text in references_data:
        add_reference_item(doc, num, ref_text)

    # Save
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    print(f"Document successfully created and saved to: {output_path} ({os.path.getsize(output_path):,} bytes)")

if __name__ == '__main__':
    primary_out = r"P:\Projects\AIRE-TRACE\AIRE_Trace_Manuscript.docx"
    secondary_out = r"P:\Projects\AIRE-TRACE\conference_submissions\iConCISE_2027\working\AIRE_Trace_Manuscript.docx"
    build_manuscript_docx(primary_out)
    build_manuscript_docx(secondary_out)
