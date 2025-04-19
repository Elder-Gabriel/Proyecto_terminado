from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_images_from_chapters(chapters: list) -> list:
    images = []
    for i in range(0, len(chapters), 3):
        context = " ".join(chapters[i:i+3])[:400]
        prompt = (
            f"Ilustración educativa sin texto, clara y centrada, "
            f"basada en el siguiente contexto: {context}"
        )

        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            image_url = response.data[0].url
            print(f"✅ Imagen generada: {image_url}")
            images.append(image_url)
        except Exception as e:
            print(f"⚠️ Error al generar imagen: {e}")
            images.append(None)
    return images
