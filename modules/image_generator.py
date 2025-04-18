import openai
import os
from openai import OpenAI
from config import load_config

config = load_config()
openai.api_key = config.get("OPENAI_API_KEY", "tu-api-key-aquí")
client = OpenAI(api_key=openai.api_key)

def generate_image(prompt):
    """
    Genera una imagen utilizando la API de OpenAI y la guarda localmente.
    Devuelve la ruta al archivo guardado.
    """
    try:
        response = client.images.generate(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response.data[0].url

        # Descargar y guardar la imagen
        import requests
        from PIL import Image
        from io import BytesIO

        img_data = requests.get(image_url).content
        image = Image.open(BytesIO(img_data))

        # Crea el directorio si no existe
        os.makedirs("generated_images", exist_ok=True)

        # Guarda la imagen con un nombre descriptivo
        image_path = os.path.join("generated_images", f"{prompt[:50].replace(' ', '_')}.png")
        image.save(image_path)

        return image_path  # Devuelve la ruta al archivo

    except Exception as e:
        print(f"Error al generar la imagen: {e}")
        return None
