import pymupdf
doc = pymupdf.open(r'p:\Projects\AIRE-TRACE\Report\report.pdf')
page = doc[0]
blocks = page.get_text('dict')['blocks']
for b in blocks:
    if 'lines' in b:
        for l in b['lines']:
            for s in l['spans']:
                text = s['text'].strip()
                if text:
                    print(f"Text: {text} | Font: {s['font']} | Size: {s['size']:.1f}")
