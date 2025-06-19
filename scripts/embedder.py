# scripts/embedder.py

import os
import json
from pathlib import Path
from typing import List

from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from tqdm import tqdm
import logging


def load_chunks_from_jsonl(chunk_path: Path) -> List[Document]:
    """Load and parse chunks from a .jsonl file."""
    docs = []
    with open(chunk_path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            doc = Document(
                page_content=record["content"],
                metadata={
                    "topic": record.get("topic"),
                    "category": record.get("category"),
                    "chunk_id": record.get("chunk_id"),
                    "source_file": chunk_path.name,
                },
            )
            docs.append(doc)
    return docs


def build_vectorstore_from_chunks(
    chunks_dir: str = "data/chunks",
    vectorstore_dir: str = "vectorstore/faiss_index"
):
    """Embeds all chunked .jsonl files and saves them to a FAISS index."""

    embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    all_docs = []

    chunks_dir = Path(chunks_dir)
    for jsonl_file in tqdm(list(chunks_dir.rglob("*.jsonl")), desc="Reading chunks"):
        try:
            docs = load_chunks_from_jsonl(jsonl_file)
            all_docs.extend(docs)
        except Exception as e:
            logging.error(f"[ERROR] Failed to load {jsonl_file}: {e}")

    print(f"[INFO] Total documents to embed: {len(all_docs)}")

    if not all_docs:
        raise ValueError("No documents found to embed.")

    print("[INFO] Generating embeddings and building FAISS index...")
    vectorstore = FAISS.from_documents(all_docs, embed_model)
    Path(vectorstore_dir).mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(vectorstore_dir)
    print(f"[SUCCESS] Vector store saved to: {vectorstore_dir}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    build_vectorstore_from_chunks()
