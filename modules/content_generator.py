# modules/content_generator.py

from modules.web_search import search_web_duckduckgo

def generate_book_content(prompt):
    print("\n🔍 Buscando información relacionada en la web...")
    web_data = search_web_duckduckgo(prompt)
    
    print("\n✍️ Generando contenido del libro...")
    book_content = f"""
# Libro generado
## Prompt: {prompt}

## Contenido basado en búsqueda web:
{web_data}
    """
    return book_content
