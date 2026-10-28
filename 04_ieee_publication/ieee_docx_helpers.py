"""
ieee_docx_helpers.py
--------------------
Provides standardized, reusable IEEE Conference Microsoft Word (.docx) formatting utilities:
- Two-column layout with 0.25" gutter and US Letter geometry
- Times New Roman typography with IEEE type scale
- Booktabs table borders and cell margin formatting
- Captioning for figures and tables
- Un-hallucinated author blocks and hanging-indent references
"""

import os
import re
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_page_setup(section):
    """Sets standard IEEE US Letter page geometry with proper margins."""
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
    """Applies IEEE booktabs styling (top and bottom horizontal borders, no vertical borders)."""
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
    """Adds a single bottom border line under the table header row."""
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

def add_title(doc, text):
    """Appends centered 20 pt bold paper title."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(20)
    run.font.bold = True
    return p

def add_metadata_line(doc, text):
    """Appends centered 9 pt italic conference/venue metadata line."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(9)
    run.font.italic = True
    return p

def add_author_grid(doc):
    """Creates a 2-column side-by-side author block with un-hallucinated placeholders."""
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell1 = table.rows[0].cells[0]
    cell1.width = Inches(3.5)
    p1 = cell1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(1)
    p1.paragraph_format.line_spacing = 1.0
    
    r = p1.add_run("[AUTHOR 1 NAME]\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.bold = True
    
    r = p1.add_run("[AUTHOR 1 DEPARTMENT], [AUTHOR 1 INSTITUTION]\n[CITY, COUNTRY] -- [AUTHOR 1 EMAIL]")
    r.font.name = "Times New Roman"
    r.font.size = Pt(8.5)
    
    cell2 = table.rows[0].cells[1]
    cell2.width = Inches(3.5)
    p2 = cell2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(1)
    p2.paragraph_format.line_spacing = 1.0
    
    r = p2.add_run("[AUTHOR 2 NAME] (if applicable)\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.bold = True
    
    r = p2.add_run("[AUTHOR 2 DEPARTMENT], [AUTHOR 2 INSTITUTION]\n[CITY, COUNTRY] -- [AUTHOR 2 EMAIL]")
    r.font.name = "Times New Roman"
    r.font.size = Pt(8.5)
    
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(1)
    spacer.paragraph_format.space_after = Pt(3)

def add_abstract(doc, text):
    """Appends justified 8.5 pt bold abstract with run-in header."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Pt(0)
    
    r_lead = p.add_run("Abstract—")
    r_lead.font.name = "Times New Roman"
    r_lead.font.size = Pt(8.5)
    r_lead.font.bold = True
    r_lead.font.italic = True
    
    r_body = p.add_run(text)
    r_body.font.name = "Times New Roman"
    r_body.font.size = Pt(8.5)
    r_body.font.bold = True

def add_keywords(doc, text):
    """Appends justified 8.5 pt keywords with run-in header."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Pt(0)
    
    r_lead = p.add_run("Index Terms—")
    r_lead.font.name = "Times New Roman"
    r_lead.font.size = Pt(8.5)
    r_lead.font.bold = True
    r_lead.font.italic = True
    
    r_body = p.add_run(text)
    r_body.font.name = "Times New Roman"
    r_body.font.size = Pt(8.5)

def add_h1(doc, text):
    """Appends centered 9.5 pt bold uppercase Level 1 heading."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text.upper())
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    return p

def add_h2(doc, text):
    """Appends left-aligned 9 pt italic Level 2 heading."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(9)
    r.font.italic = True
    return p

def add_h3(doc, text):
    """Appends left-aligned 8.5 pt italic Level 3 heading."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(8.5)
    r.font.italic = True
    return p

def add_p(doc, text, indent=True):
    """Appends justified 9.5 pt body paragraph with markdown bold/italic formatting."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.12)
    else:
        p.paragraph_format.first_line_indent = Pt(0)
        
    tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith('**') and tok.endswith('**'):
            r = p.add_run(tok[2:-2])
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.font.bold = True
        elif tok.startswith('*') and tok.endswith('*'):
            r = p.add_run(tok[1:-1])
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.font.italic = True
        elif tok.startswith('`') and tok.endswith('`'):
            r = p.add_run(tok[1:-1])
            r.font.name = "Courier New"
            r.font.size = Pt(8.5)
        else:
            r = p.add_run(tok)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
    return p

def add_bullet(doc, text):
    """Appends bulleted item with hanging indentation."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0.5)
    p.paragraph_format.space_after = Pt(0.5)
    p.paragraph_format.left_indent = Inches(0.15)
    p.paragraph_format.first_line_indent = Inches(-0.1)
    p.paragraph_format.line_spacing = 1.0
    
    r = p.add_run("• ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    
    tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith('**') and tok.endswith('**'):
            r = p.add_run(tok[2:-2])
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.font.bold = True
        elif tok.startswith('*') and tok.endswith('*'):
            r = p.add_run(tok[1:-1])
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.font.italic = True
        elif tok.startswith('`') and tok.endswith('`'):
            r = p.add_run(tok[1:-1])
            r.font.name = "Courier New"
            r.font.size = Pt(8.5)
        else:
            r = p.add_run(tok)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
    return p

def add_fig(doc, img_path, fig_num, caption, width_inches=3.3):
    """Embeds an image centered in a column with proper IEEE captioning."""
    if not os.path.exists(img_path):
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(3)
    p_img.paragraph_format.space_after = Pt(1)
    p_img.paragraph_format.keep_with_next = True
    r = p_img.add_run()
    r.add_picture(img_path, width=Inches(width_inches))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cap.paragraph_format.space_before = Pt(1)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.line_spacing = 1.0
    p_cap.paragraph_format.first_line_indent = Pt(0)
    
    r_lbl = p_cap.add_run(f"Fig. {fig_num}. ")
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(7.5)
    r_lbl.font.bold = True
    
    r_txt = p_cap.add_run(caption)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(7.5)

def add_tbl_header(doc, num, title):
    """Appends centered small-caps IEEE table header caption."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(f"TABLE {num}: {title.upper()}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(7.5)
    r.font.bold = True

def add_tbl(doc, headers, data, col_widths=None, alignments=None):
    """Constructs an IEEE booktabs table with customizable column widths and alignments."""
    table = doc.add_table(rows=len(data)+1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    set_header_bottom_border(table.rows[0])
    
    for c_idx, h in enumerate(headers):
        cell = table.rows[0].cells[c_idx]
        if col_widths and c_idx < len(col_widths):
            cell.width = Inches(col_widths[c_idx])
        set_cell_margins(cell, top=12, bottom=12, left=25, right=25)
        p = cell.paragraphs[0]
        p.alignment = alignments[c_idx] if alignments else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(7.5)
        r.font.bold = True
        
    for r_idx, row in enumerate(data):
        r_elem = table.rows[r_idx+1]
        for c_idx, val in enumerate(row):
            cell = r_elem.cells[c_idx]
            if col_widths and c_idx < len(col_widths):
                cell.width = Inches(col_widths[c_idx])
            set_cell_margins(cell, top=10, bottom=10, left=25, right=25)
            p = cell.paragraphs[0]
            p.alignment = alignments[c_idx] if alignments else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = Pt(7.5)
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(1)
    p_sp.paragraph_format.space_after = Pt(3)

def add_ref(doc, num, text):
    """Appends an IEEE reference item with hanging indent formatting."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0.5)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.first_line_indent = Inches(-0.2)
    
    r_n = p.add_run(f"[{num}] ")
    r_n.font.name = "Times New Roman"
    r_n.font.size = Pt(7.5)
    
    r_t = p.add_run(text)
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(7.5)

# Aliases for backwards compatibility with generate_ieee_docx.py
add_heading_1 = add_h1
add_heading_2 = add_h2
add_heading_3 = add_h3
add_body = add_p
add_bullet_item = add_bullet
add_figure = add_fig
add_table_header_caption = add_tbl_header
add_custom_table = add_tbl
add_reference_item = add_ref
def add_table_note(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(7.5)
    r.font.italic = True
    return p
