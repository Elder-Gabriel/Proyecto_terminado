from openai import OpenAI
from prompts.user_prompt import build_user_prompt
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_content(params: dict) -> str:
    prompt = build_user_prompt(
        params["title"], params["audience"], params["age_range"]
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un generador experto de libros educativos para diferentes edades."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=4096
    )

    return response.choices[0].message.content
