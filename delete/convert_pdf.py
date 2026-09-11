import os
from fpdf import FPDF
import re

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def clean_text(text):
    text = text.replace('\ufeff', '')
    text = text.replace('\u2014', '--')
    text = text.replace('\u2013', '-')
    text = text.replace('\u201c', '"')
    text = text.replace('\u201d', '"')
    text = text.replace('\u2018', "'")
    text = text.replace('\u2019', "'")
    text = text.replace('\u2265', '>=')
    text = text.replace('\u00e9', 'e')
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text

def markdown_to_pdf(md_file, pdf_file):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)

    with open(md_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = clean_text(line.strip())
            
            if line.startswith('# '):
                pdf.set_font("Helvetica", 'B', 16)
                pdf.write(10, line[2:].replace('**', '').replace('*', '') + '\n')
                pdf.set_font("Helvetica", size=12)
                pdf.ln(5)
            elif line.startswith('## '):
                pdf.set_font("Helvetica", 'B', 14)
                pdf.write(10, line[3:].replace('**', '').replace('*', '') + '\n')
                pdf.set_font("Helvetica", size=12)
                pdf.ln(4)
            elif line.startswith('### '):
                pdf.set_font("Helvetica", 'B', 12)
                pdf.write(10, line[4:].replace('**', '').replace('*', '') + '\n')
                pdf.set_font("Helvetica", size=12)
                pdf.ln(3)
            elif line.startswith('- '):
                clean_line = line.replace('**', '')
                pdf.write(8, "  * " + clean_line[2:] + '\n')
            elif line == '':
                pdf.ln(5)
            else:
                clean_line = line.replace('**', '')
                pdf.write(8, clean_line + '\n')

    pdf.output(pdf_file)
    print(f"Created {pdf_file}")

files = ["problem_statement", "data_card", "impact_statement_card", "stakeholder_engagement"]
for f in files:
    if os.path.exists(f"docs/{f}.md"):
        markdown_to_pdf(f"docs/{f}.md", f"docs/{f}.pdf")
        os.remove(f"docs/{f}.md")
