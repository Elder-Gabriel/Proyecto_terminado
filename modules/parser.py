def parse_user_input(user_input=None) -> dict:
    print("Ingrese los datos del libro:")
    title = input("Título: ").strip().title()
    audience = input("Público (niños, jóvenes, adultos): ").strip().lower()
    age_range = input("Rango de edad (ej: 8-12): ").strip()
    if audience not in ["niños", "jóvenes", "adultos"]:
        raise ValueError("Público inválido.")
    if "-" not in age_range:
        raise ValueError("Formato de rango inválido.")
    return {"title": title, "audience": audience, "age_range": age_range}