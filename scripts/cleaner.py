import re


def clean_text(text: str) -> str:
    """
    Cleans raw Wikipedia text by:
    - Removing citation numbers like [1], [23]
    - Removing extra whitespace and line breaks
    - Normalizing unicode characters
    - Stripping leading/trailing whitespace

    Args:
        text (str): Raw Wikipedia text.

    Returns:
        str: Cleaned and normalized text.
    """
    if not text:
        return ""

    # Remove reference-style brackets like [1], [12]
    text = re.sub(r'\[\d+\]', '', text)

    # Remove footnotes or empty brackets [citation needed]
    text = re.sub(r'\[\s*citation needed\s*\]', '', text, flags=re.IGNORECASE)

    # Normalize spacing
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
