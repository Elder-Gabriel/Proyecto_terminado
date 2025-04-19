from modules import parser, content_builder, image_generator, pdf_creator
from dotenv import load_dotenv
import re

# Cargar variables de entorno (API keys)
load_dotenv()

# Paso 1: Obtener datos del usuario
params = parser.parse_user_input()

# Paso 2: Generar el contenido del libro
print("🧠 Generando contenido...")
full_text = content_builder.build_content(params)

# Paso 3: Limpiar texto de marcadores de imagen sugerida (si aún existen)
full_text = re.sub(r"\[Imagen sugerida:.*?\]", "", full_text)

# Paso 4: Extraer capítulos para generar imágenes
def extract_chapters(text):
    chapters = []
    current = []
    for line in text.splitlines():
        if line.lower().startswith("capítulo"):
            if current:
                chapters.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        chapters.append("\n".join(current))
    return chapters

chapters = extract_chapters(full_text)

# Paso 5: Generar imágenes con DALL·E
print("🎨 Generando imágenes...")
images = image_generator.generate_images_from_chapters(chapters)

print("🖼️ URLs de las imágenes generadas:")
for url in images:
    print(url)

# Paso 6: Crear PDF final
print("📄 Creando PDF...")
pdf_creator.create_pdf(params, full_text, images)
