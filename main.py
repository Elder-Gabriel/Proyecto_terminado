from modules.content_builder import build_book_content
from modules.pdf_creator import create_pdf
from prompts.user_prompt import get_user_prompt

def main():
    datos = get_user_prompt()
    contenido = build_book_content(datos)
    ruta = create_pdf(datos['title'], contenido)
    print(f"\n✅ Libro generado correctamente: {ruta}")

if __name__ == '__main__':
    main()
