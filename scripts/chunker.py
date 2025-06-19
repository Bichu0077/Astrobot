from typing import List
from sentence_transformers import SentenceTransformer, util
import nltk
import numpy as np
import json
from pathlib import Path
import logging

nltk.download("punkt")

# Load a lightweight sentence-transformer model (you can later switch to better ones)
model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_chunk(
    text: str,
    max_chunk_tokens: int = 100,
    similarity_threshold: float = 0.75
) -> List[str]:
    """
    Split text semantically using sentence embeddings + similarity.

    Args:
        text (str): Full cleaned text.
        max_chunk_tokens (int): Max tokens per semantic chunk.
        similarity_threshold (float): Cosine similarity threshold for clustering.

    Returns:
        List[str]: List of semantically grouped chunks.
    """
    sentences = nltk.sent_tokenize(text)
    embeddings = model.encode(sentences, convert_to_tensor=True)

    chunks = []
    current_chunk = []
    current_tokens = 0

    for i, sent in enumerate(sentences):
        current_chunk.append(sent)
        current_tokens += len(sent.split())

        # Try to group similar nearby sentences into one chunk
        if (
            i < len(sentences) - 1
            and current_tokens < max_chunk_tokens
            and util.cos_sim(embeddings[i], embeddings[i + 1]) > similarity_threshold
        ):
            continue  # add more

        # Else save current chunk
        chunks.append(" ".join(current_chunk))
        current_chunk = []
        current_tokens = 0

    # Catch remaining
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# Modify this line to use semantic_chunk()
def split_text(text: str) -> List[str]:
    return semantic_chunk(text)



def chunk_and_save(
    cleaned_text: str,
    topic: str,
    category: str,
    out_dir: str = "data/chunks"
) -> bool:
    try:
        chunks = split_text(cleaned_text)

        topic_slug = topic.replace(" ", "_").replace("/", "_")
        category_dir = Path(out_dir) / category
        category_dir.mkdir(parents=True, exist_ok=True)

        out_path = category_dir / f"{topic_slug}_chunks.jsonl"

        with open(out_path, "w", encoding="utf-8") as f:
            for idx, chunk in enumerate(chunks):
                record = {
                    "topic": topic,
                    "category": category,
                    "chunk_id": idx,
                    "content": chunk
                }
                json.dump(record, f)
                f.write("\n")

        logging.info(f"[CHUNKED] {len(chunks)} chunks saved → {out_path}")
        return True

    except Exception as e:
        logging.error(f"[ERROR] Failed to chunk/save {topic}: {e}")
        return False
