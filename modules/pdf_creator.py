import re
import requests
import tempfile
from fpdf import FPDF

class BookPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(True, margin=20)
        self.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        self.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf", uni=True)

    def add_title_page(self, title: str):
     self.add_page()
     self.set_font("DejaVu", "B", 28)
     self.set_y(60)
     self.multi_cell(0, 20, title, align="C")
    
     self.ln(10)
     self.set_font("DejaVu", "", 16)
     self.multi_cell(0, 10, "Autor: Inteligencia Artificial (TEI)", align="C")
     self.multi_cell(0, 10, "Ilustrador: Generado por DALL·E 3", align="C")
 

    def add_section(self, heading: str, body: str):
        self.add_page()
        self.set_font("DejaVu", "B", 20)
        self.multi_cell(0, 10, heading)
        self.ln(5)
        self.set_font("DejaVu", "", 14)

        subsections = body.split("## ")
        for subsection in subsections:
            if not subsection.strip():
                continue
            lines = subsection.strip().split("\n", 1)
            if len(lines) == 2:
                subtitle, paragraph = lines
                self.set_font("DejaVu", "B", 16)
                self.multi_cell(0, 8, subtitle.strip())
                self.set_font("DejaVu", "", 14)
                self.multi_cell(0, 8, paragraph.strip())
                self.ln(4)
            else:
                self.multi_cell(0, 8, subsection.strip())
                self.ln(2)

    def add_image_page(self, url: str):
        if not url:
            return
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                tmp_file.write(resp.content)
                tmp_path = tmp_file.name
            self.add_page()
            self.image(tmp_path, x=25, y=40, w=160, h=160)
        except Exception as e:
            print(f"⚠️ Error al insertar imagen: {e}")

def create_pdf(params: dict, full_text: str, image_urls: list):
    full_text = re.sub(r"\[Imagen sugerida:.*?\]", "", full_text)

    pdf = BookPDF()
    pdf.add_title_page(params.get("title", "Libro Educativo"))

    sections = full_text.split("\n## ")
    chapter_blocks = []
    block = ""
    for section in sections:
        if section.strip().lower().startswith("capítulo"):
            if block:
                chapter_blocks.append(block)
            block = "## " + section.strip()
        else:
            block += "\n## " + section.strip()
    if block:
        chapter_blocks.append(block)

    image_index = 0
    for i, chapter in enumerate(chapter_blocks):
        section_title = chapter.split("\n", 1)[0].replace("##", "").strip()
        content = chapter.split("\n", 1)[1] if "\n" in chapter else ""
        pdf.add_section(section_title, content)

        # 👇 Esta línea es la clave: imagen cada 3 capítulos
        if (i + 1) % 3 == 0 and image_index < len(image_urls):
            url = image_urls[image_index]
            if url:
                pdf.add_image_page(url)
            image_index += 1

    output_path = f"{params['title'].replace(' ', '_')}.pdf"
    pdf.output(output_path)
    print(f"✅ PDF guardado como: {output_path}")
