def parse_prompt(data):
    return {
        "title": data["title"],
        "audience": data["audience"],
        "age_range": data["age_range"],
        "total_pages": data["total_pages"]
    }
