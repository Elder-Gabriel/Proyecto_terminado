from flask import Flask, request, send_file, render_template_string
import os, re
from modules.parser import parse_user_input  # O parsea tú mismo desde request.form
from modules.content_builder import build_content
from modules.image_generator import generate_images_from_chapters
from modules.pdf_creator import create_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'outputs'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Página de formulario
HTML_FORM = """
<!doctype html>
<title>Generador de Libros IA</title>
<h1>Generar Libro Educativo</h1>
<form method=post>
  <label>Título: <input name=title required></label><br>
  <label>Público:
    <select name=audience>
      <option>niños</option><option>jóvenes</option><option>adultos</option>
    </select>
  </label><br>
  <label>Rango de edad: <input name=age_range placeholder="8-12" required></label><br>
  <button type=submit>Generar PDF</button>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        params = {
            "title": request.form["title"],
            "audience": request.form["audience"],
            "age_range": request.form["age_range"]
        }
        # 1) Generar contenido
        texto = build_content(params)
        # 2) Limpiar marcadores y extraer capítulos
        texto = re.sub(r"\[Imagen sugerida:.*?\]", "", texto)
        chapters = []
        curr = []
        for line in texto.splitlines():
            if line.lower().startswith("capítulo"):
                if curr: chapters.append("\n".join(curr))
                curr = [line]
            else:
                curr.append(line)
        if curr: chapters.append("\n".join(curr))
        # 3) Generar imágenes
        images = generate_images_from_chapters(chapters)
        # 4) Crear PDF
        filename = f"{params['title'].replace(' ', '_')}.pdf"
        out_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        create_pdf(params, texto, images)  # ajusta este create_pdf para recibir out_path
        return send_file(out_path, as_attachment=True)
    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
