import docx
from docx.shared import Inches, Pt
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()
table = doc.add_table(rows=3, cols=3)
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

for cell in table.rows[0].cells:
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    b_bottom = OxmlElement('w:bottom')
    b_bottom.set(qn('w:val'), 'single')
    b_bottom.set(qn('w:sz'), '6')
    b_bottom.set(qn('w:space'), '0')
    b_bottom.set(qn('w:color'), '000000')
    tcBorders.append(b_bottom)
    tcPr.append(tcBorders)

doc.save('scratch/table_test.docx')
print('Table border test passed successfully!')
