import json
from pathlib import Path

def save_article(
    topic: str,
    category: str,
    source: str,
    raw_text: str,
    cleaned_text: str,
    out_dir: str = "data"
) -> bool:
    """
    Saves an article to a structured JSON file.

    Args:
        topic (str): Topic title.
        category (str): Topic category.
        source (str): Source used (e.g., Wikipedia).
        raw_text (str): Raw retrieved content.
        cleaned_text (str): Cleaned version of the text.
        out_dir (str): Output directory path (default: 'data').

    Returns:
        bool: True if saved successfully, False otherwise.
    """
    try:
        safe_filename = topic.replace(" ", "_").replace("/", "_") + ".json"
        category_dir = Path(out_dir) / category
        category_dir.mkdir(parents=True, exist_ok=True)

        output_path = category_dir / safe_filename

        data = {
            "topic": topic,
            "category": category,
            "source": source,
            "raw_text": raw_text,
            "cleaned_text": cleaned_text
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"[INFO] Saved: {output_path}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to save {topic}: {e}")
        return False
