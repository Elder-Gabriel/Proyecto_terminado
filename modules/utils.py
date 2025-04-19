import unicodedata
import logging

def clean_text(text: str) -> str:
    """
    Normaliza el texto eliminando acentos y caracteres especiales no ASCII.
    También controla errores y retorna un string vacío si falla.
    """
    try:
        # Elimina acentos y caracteres especiales
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    except Exception as e:
        logging.error(f"Error en clean_text: {e}. Texto original: {text}")
        return ''
