from markdown_pdf import Section, MarkdownPdf

pdf = MarkdownPdf(toc_level=2)
pdf.add_section(Section(open("AIRE-Trace_IEEE_Draft.md", "r", encoding="utf-8").read()))
pdf.save("AIRE-Trace_IEEE.pdf")
