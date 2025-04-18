from fpdf import FPDF
import textwrap
import unicodedata

def clean_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')


def add_section(pdf, title, text, pages, lines_per_page=40):
    """
Insert a section with a title and text into a fixed number of pages.
"""  
    wrapper = textwrap.TextWrapper(width=90)
    # prepare lines
    paragraphs = text.split('\n')
    lines = []
    for para in paragraphs:
        lines.extend(wrapper.wrap(clean_text(para)))
        lines.append('')  # blank line
    # split into pages
    chunks = [lines[i:i+lines_per_page] for i in range(0, len(lines), lines_per_page)]
    # ensure we have exactly 'pages' chunks
    while len(chunks) < pages:
        chunks.append([''] * lines_per_page)
    chunks = chunks[:pages]
    # add pages
    for idx, chunk in enumerate(chunks):
        pdf.add_page()
        if idx == 0 and title:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, clean_text(title), ln=True)
            pdf.set_font('Arial', '', 12)
        for line in chunk:
            pdf.cell(0, 8, line, ln=True)


def create_pdf(title, content):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)

    # 1. Portada (1 page)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 12, clean_text(title), ln=True, align='C')
    pdf.ln(20)
    pdf.set_font('Arial', '', 14)
    pdf.cell(0, 10, 'Libro generado por IA', ln=True, align='C')

    # 2. Índice (1 page)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Índice', ln=True)
    pdf.ln(5)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, '1. Introducción', ln=True)
    for i in range(10): pdf.cell(0, 8, f'{i+2}. Capítulo {i+1}', ln=True)
    pdf.cell(0, 8, '12. Ejercicios', ln=True)
    pdf.cell(0, 8, '13. Conclusión', ln=True)
    pdf.cell(0, 8, '14. Bibliografía', ln=True)

    # 3. Introducción (2 pages)
    add_section(pdf, 'Introducción', content.get('introduccion',''), pages=2)

    # 4. 10 capítulos (3 pages each)
    for cap, text in content.get('capitulos', {}).items():
        add_section(pdf, cap, text, pages=3)

    # 5. Ejercicios (3 pages)
    add_section(pdf, 'Ejercicios', content.get('ejercicios',''), pages=3)

    # 6. Conclusión (2 pages)
    add_section(pdf, 'Conclusión', content.get('conclusion',''), pages=2)

    # 7. Bibliografía (1 page)
    add_section(pdf, 'Bibliografía', content.get('bibliografia',''), pages=1)

    filename = f"{title.replace(' ','_')}_libro.pdf"
    pdf.output(filename)
    return filename