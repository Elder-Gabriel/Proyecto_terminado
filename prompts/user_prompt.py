def get_user_prompt():
    title     = input("📘 Título del libro: ").strip()
    target    = input("🎯 Público objetivo (niños, jóvenes, adultos): ").strip()
    age_range = input("📅 Rango de edad (ej: 10-14): ").strip()
    return {"title": title, "target": target, "age_range": age_range}

