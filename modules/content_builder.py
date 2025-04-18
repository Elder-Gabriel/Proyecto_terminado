import logging
import openai
from config import OPENAI_API_KEY
from modules.web_search import search_topic

# Configurar API Key
openai.api_key = OPENAI_API_KEY


def generate_section(prompt, max_tokens=1200):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generando sección: {e}")
        return ""


def build_book_content(prompt_data):
    title     = prompt_data["title"]
    target    = prompt_data["target"]
    age_range = prompt_data["age_range"]

    # Enriquecer contexto
    items = search_topic(f"{title} para {target} {age_range} años")
    contexto = "".join(f"- {it.get('title')}: {it.get('snippet')} (Fuente: {it.get('link')})\n" for it in items)

    content = {}
    # Introducción
    intro_prompt = (
        f"Escribe una introducción para un libro titulado '{title}', dirigido a {target} de {age_range} años. "
        "Debe contener al menos 800 palabras, bien estructurado en párrafos, sin imágenes ni referencias a ellas."
        f"\nContexto:\n{contexto}"
    )
    content['introduccion'] = generate_section(intro_prompt, max_tokens=1500)

    # 10 capítulos
    content['capitulos'] = {}
    for i in range(1, 11):
        cap_prompt = (
            f"Capítulo {i}: Escribe un capítulo educativo para '{title}', dirigido a {target} de {age_range} años. "
            "Incluye un título y al menos 1000 palabras en párrafos claros, sin imágenes ni referencias a ellas."
            f"\nContexto útil:\n{contexto}"
        )
        content['capitulos'][f"Capítulo {i}"] = generate_section(cap_prompt, max_tokens=1800)

    # Ejercicios
    ej_prompt = (
        f"Crea una sección de ejercicios con preguntas y actividades basadas en los 10 capítulos del libro '{title}'. "
        "Debe ocupar unas 3 páginas (~600 palabras)."
    )
    content['ejercicios'] = generate_section(ej_prompt, max_tokens=800)

    # Conclusión
    conc_prompt = (
        f"Escribe una conclusión reflexiva y general para el libro '{title}', dirigida a {target} de {age_range} años. "
        "Debe ocupar unas 2 páginas (~400 palabras), sin repetir los capítulos."
    )
    content['conclusion'] = generate_section(conc_prompt, max_tokens=800)

    # Bibliografía
    content['bibliografia'] = (
        "Bibliografía:\n" +
        "1. Contenidos educativos generales.\n" +
        "2. Búsqueda web mediante Google CSE.\n" +
        "3. Documentación de OpenAI ChatGPT."
    )
    return content
