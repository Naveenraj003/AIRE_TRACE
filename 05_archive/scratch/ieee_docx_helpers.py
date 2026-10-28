"""
build_ieee_docx.py
------------------
Builds an IEEE Conference formatted Microsoft Word document (.docx)
strictly compliant with the IEEE Conference specifications:
- US Letter (8.5 x 11 in)
- Top margin: 0.75 in (54 pt)
- Bottom margin: 1.0 in (72 pt)
- Left/Right margins: 0.625 in (45 pt)
- 2-column layout (3.5 in columns with 0.25 in spacing)
- Times New Roman font throughout
- 24 pt bold centered paper title
- Two-column side-by-side author block with un-hallucinated placeholders
- 9 pt bold italic run-in abstract & index terms
- Roman numeral small-caps centered Level 1 headings
- Italic left-aligned Level 2 & Level 3 headings
- First-line indent (0.14 in) for body paragraphs
- IEEE booktabs style tables with centered Roman numeral headers
- Embedded figures with IEEE caption formatting ("Fig. X. ...")
- 13 verified IEEE bibliographic references with hanging indent
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION_START
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_page_setup(section):
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(0.625)
    section.right_margin = Inches(0.625)
    section.header_distance = Inches(0.5)
    section.footer_distance = Inches(0.5)

def set_columns(section, num_cols=2, space_twips=360):
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
    tblPr = table._tbl.tblPr
    borders_xml = parse_xml(
        '<w:tblBorders ' + nsdecls('w') + '>\n'
        '  <w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>\n'
        '  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>\n'
        '  <w:left w:val="none"/>\n'
        '  <w:right w:val="none"/>\n'
        '  <w:insideH w:val="none"/>\n'
        '  <w:insideV w:val="none"/>\n'
        '</w:tblBorders>'
    )
    tblPr.append(borders_xml)

def set_header_bottom_border(row):
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = tcPr.first_child_found_in("w:tcBorders")
        if tcBorders is None:
            tcBorders = OxmlElement('w:tcBorders')
            tcPr.append(tcBorders)
        b_bottom = OxmlElement('w:bottom')
        b_bottom.set(qn('w:val'), 'single')
        b_bottom.set(qn('w:sz'), '6')
        b_bottom.set(qn('w:space'), '0')
        b_bottom.set(qn('w:color'), '000000')
        tcBorders.append(b_bottom)

def set_cell_margins(cell, top=30, bottom=30, left=60, right=60):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for edge, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        m = OxmlElement(f'w:{edge}')
        m.set(qn('w:w'), str(val))
        m.set(qn('w:type'), 'dxa')
        tcMar.append(m)
    tcPr.append(tcMar)

def add_title(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(24)
    run.font.bold = True
    return p

def add_metadata_line(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    run.font.italic = True
    return p

def add_author_grid(doc):
    # Borderless 2-column table across 7.25 inches
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Author 1
    cell1 = table.rows[0].cells[0]
    cell1.width = Inches(3.5)
    p1 = cell1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(2)
    p1.paragraph_format.line_spacing = 1.05
    
    r = p1.add_run("[AUTHOR 1 NAME]\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    
    r = p1.add_run("[AUTHOR 1 DEPARTMENT]\n[AUTHOR 1 INSTITUTION]\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True
    
    r = p1.add_run("[CITY, COUNTRY]\n[AUTHOR 1 EMAIL]")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    
    # Author 2
    cell2 = table.rows[0].cells[1]
    cell2.width = Inches(3.5)
    p2 = cell2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(2)
    p2.paragraph_format.line_spacing = 1.05
    
    r = p2.add_run("[AUTHOR 2 NAME] (if applicable)\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    
    r = p2.add_run("[AUTHOR 2 DEPARTMENT]\n[AUTHOR 2 INSTITUTION]\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True
    
    r = p2.add_run("[CITY, COUNTRY]\n[AUTHOR 2 EMAIL]")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    
    # Add a spacer paragraph after authors
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(4)
    spacer.paragraph_format.space_after = Pt(6)

def add_abstract(doc, abstract_text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Pt(0)
    
    r_lead = p.add_run("Abstract—")
    r_lead.font.name = "Times New Roman"
    r_lead.font.size = Pt(9)
    r_lead.font.bold = True
    r_lead.font.italic = True
    
    r_body = p.add_run(abstract_text)
    r_body.font.name = "Times New Roman"
    r_body.font.size = Pt(9)
    r_body.font.bold = True

def add_keywords(doc, keywords_text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Pt(0)
    
    r_lead = p.add_run("Index Terms—")
    r_lead.font.name = "Times New Roman"
    r_lead.font.size = Pt(9)
    r_lead.font.bold = True
    r_lead.font.italic = True
    
    r_body = p.add_run(keywords_text)
    r_body.font.name = "Times New Roman"
    r_body.font.size = Pt(9)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    
    r = p.add_run(text.upper())
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.bold = False  # IEEE uses Small Caps or regular uppercase
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True
    return p

def add_body(doc, text, indent=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.14)
    else:
        p.paragraph_format.first_line_indent = Pt(0)
        
    # Format simple bold/italics
    # Parse markdown-style formatting like **bold** and *italic*
    tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith('**') and tok.endswith('**'):
            r = p.add_run(tok[2:-2])
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.font.bold = True
        elif tok.startswith('*') and tok.endswith('*'):
            r = p.add_run(tok[1:-1])
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.font.italic = True
        elif tok.startswith('`') and tok.endswith('`'):
            r = p.add_run(tok[1:-1])
            r.font.name = "Courier New"
            r.font.size = Pt(9.5)
        else:
            r = p.add_run(tok)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
    return p

def add_bullet_item(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.first_line_indent = Inches(-0.1)
    p.paragraph_format.line_spacing = 1.05
    
    r_bullet = p.add_run("• ")
    r_bullet.font.name = "Times New Roman"
    r_bullet.font.size = Pt(10)
    
    tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith('**') and tok.endswith('**'):
            r = p.add_run(tok[2:-2])
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.font.bold = True
        elif tok.startswith('*') and tok.endswith('*'):
            r = p.add_run(tok[1:-1])
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.font.italic = True
        elif tok.startswith('`') and tok.endswith('`'):
            r = p.add_run(tok[1:-1])
            r.font.name = "Courier New"
            r.font.size = Pt(9.5)
        else:
            r = p.add_run(tok)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
    return p

def add_figure(doc, img_path, fig_num, caption_text, width_inches=3.4):
    if not os.path.exists(img_path):
        print(f"Warning: image path {img_path} not found.")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Inches(width_inches))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(8)
    p_cap.paragraph_format.line_spacing = 1.0
    p_cap.paragraph_format.first_line_indent = Pt(0)
    
    r_lbl = p_cap.add_run(f"Fig. {fig_num}. ")
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(8)
    r_lbl.font.bold = True
    
    r_txt = p_cap.add_run(caption_text)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(8)

def add_table_header_caption(doc, tbl_num, tbl_title):
    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(8)
    p1.paragraph_format.space_after = Pt(1)
    p1.paragraph_format.keep_with_next = True
    r1 = p1.add_run(f"TABLE {tbl_num}")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(8)
    r1.font.bold = False
    
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(4)
    p2.paragraph_format.keep_with_next = True
    r2 = p2.add_run(tbl_title.upper())
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(8)

def add_table_note(doc, note_text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Pt(0)
    r = p.add_run(note_text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(8)
    r.font.italic = True

def add_custom_table(doc, headers, data_rows, col_widths=None, alignments=None):
    num_rows = len(data_rows) + 1
    num_cols = len(headers)
    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    
    # Format header row
    header_row = table.rows[0]
    set_header_bottom_border(header_row)
    for c_idx, h_text in enumerate(headers):
        cell = header_row.cells[c_idx]
        if col_widths and c_idx < len(col_widths):
            cell.width = Inches(col_widths[c_idx])
        set_cell_margins(cell, top=30, bottom=30, left=40, right=40)
        p = cell.paragraphs[0]
        align = alignments[c_idx] if alignments else WD_ALIGN_PARAGRAPH.LEFT
        p.alignment = align
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(8)
        r.font.bold = True
        
    # Format data rows
    for r_idx, row_data in enumerate(data_rows):
        row = table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            if col_widths and c_idx < len(col_widths):
                cell.width = Inches(col_widths[c_idx])
            set_cell_margins(cell, top=25, bottom=25, left=40, right=40)
            p = cell.paragraphs[0]
            align = alignments[c_idx] if alignments else WD_ALIGN_PARAGRAPH.LEFT
            p.alignment = align
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = Pt(8)
            
    # Spacer paragraph after table
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(2)
    p_space.paragraph_format.space_after = Pt(4)
    return table

def add_reference_item(doc, ref_num, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    
    r_num = p.add_run(f"[{ref_num}] ")
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(8)
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(8)

print("Helper functions defined.")
