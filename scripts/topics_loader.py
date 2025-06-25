import json
from typing import List, Dict, Optional
from pathlib import Path


def load_topics(json_path: str = "data_topics.json") -> List[Dict]:
    """
    Load and validate topic entries from a JSON file.

    Args:
        json_path (str): Path to the data_topics.json file.

    Returns:
        List[Dict]: List of validated topic entries.
    """
    path = Path(json_path).resolve()

    if not path.exists():
        print(f"[ERROR] File not found: {path}")
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Expected a list of topic dictionaries.")

            valid_topics = []
            for i, item in enumerate(data):
                if not isinstance(item, dict):
                    print(f"[WARNING] Skipped non-dictionary at index {i}")
                    continue
                if not all(key in item for key in ("topic", "category")):
                    print(f"[WARNING] Missing required keys in item: {item}")
                    continue
                valid_topics.append(item)

            print(f"[INFO] Loaded {len(valid_topics)} valid topics from {path.name}")
            return valid_topics

    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON: {e}")
        return []
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return []


def filter_topics(
    topics: List[Dict],
    category: Optional[str] = None,
    source: Optional[str] = None,
    difficulty: Optional[str] = None,
) -> List[Dict]:
    """
    Filter topics by category, source, or difficulty.

    Args:
        topics (List[Dict]): List of topic dictionaries.
        category (str, optional): Category filter.
        source (str, optional): Source filter (e.g., "Wikipedia").
        difficulty (str, optional): Difficulty level filter.

    Returns:
        List[Dict]: Filtered list of topics.
    """
    filtered = topics

    if category:
        filtered = [t for t in filtered if t.get("category") == category]

    if source:
        filtered = [t for t in filtered if source in t.get("sources", [])]

    if difficulty:
        filtered = [t for t in filtered if t.get("difficulty") == difficulty]

    return filtered
