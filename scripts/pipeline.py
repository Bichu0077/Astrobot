# scripts/pipeline.py (MLOps-Integrated)

from pathlib import Path
from tqdm import tqdm
from typing import List, Dict
import sys
import logging
import os

# Add project root to sys.path for module resolution
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import custom modules
from scripts.topics_loader import load_topics
from scripts.wiki_fetcher import WikiFetcher
from scripts.cleaner import clean_text
from scripts.saver import save_article
from scripts.chunker import chunk_and_save
from scripts.embedder import build_vectorstore_from_chunks
from scripts.query_engine import load_vectorstore, build_qa_chain, answer_query


def normalize_topic_title(topic: str) -> str:
    topic = topic.strip()
    topic = topic.replace("&", "and").replace("/", " ")
    topic = topic.replace("(", "").replace(")", "")
    return topic.title()


def setup_logging(log_dir="logs"):
    Path(log_dir).mkdir(exist_ok=True)
    logging.basicConfig(
        filename=Path(log_dir) / "pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def run_pipeline(
    topics_file: str = "data_topics.json",
    out_dir: str = "data",
    chunk_out_dir: str = "data/chunks",
    vectorstore_dir: str = "vectorstore/faiss_index",
    auto_query: str = None
):
    setup_logging()
    wiki = WikiFetcher()
    topics: List[Dict] = load_topics(topics_file)

    if not topics:
        logging.error("No topics loaded. Exiting pipeline.")
        return

    print(f"[INFO] Starting pipeline for {len(topics)} topics...\n")

    for topic in tqdm(topics, desc="Processing topics"):
        topic_name = normalize_topic_title(topic.get("topic", ""))
        category = topic.get("category", "Uncategorized")
        source = "Wikipedia"

        article_path = Path(out_dir) / category / f"{topic_name.replace(' ', '_')}.json"
        chunk_path = Path(chunk_out_dir) / category / f"{topic_name.replace(' ', '_')}_chunks.jsonl"

        # Skip if both article and chunk already exist
        if article_path.exists() and chunk_path.exists():
            logging.info(f"[SKIP] Data and chunks already exist: {topic_name}")
            continue

        try:
            wiki_data = wiki.fetch_page(topic_name)
            if not wiki_data:
                logging.warning(f"[SKIP] Page not found or empty: {topic_name}")
                with open("logs/skipped_topics.txt", "a", encoding="utf-8") as f:
                    f.write(f"{topic.get('topic')} → {topic_name}\n")
                continue

            raw_text = wiki_data["full_text"]
            cleaned = clean_text(raw_text)

            if not article_path.exists():
                success = save_article(
                    topic=topic_name,
                    category=category,
                    source=source,
                    raw_text=raw_text,
                    cleaned_text=cleaned,
                    out_dir=out_dir
                )
                if not success:
                    logging.error(f"[FAIL] Could not save article: {topic_name}")
                    continue

            if not chunk_path.exists():
                chunk_success = chunk_and_save(
                    cleaned_text=cleaned,
                    topic=topic_name,
                    category=category,
                    out_dir=chunk_out_dir
                )
                if not chunk_success:
                    logging.error(f"[FAIL] Chunking failed: {topic_name}")

        except Exception as e:
            logging.exception(f"[ERROR] Failed processing topic: {topic_name} | {str(e)}")

    # Embed only if FAISS index does not exist
    index_file = Path(vectorstore_dir) / "index.faiss"
    if index_file.exists():
        print("[SKIP] Vector store already exists. Skipping embedding.")
    else:
        print("[INFO] All topics processed. Starting embedding...")
        build_vectorstore_from_chunks(
            chunks_dir=chunk_out_dir,
            vectorstore_dir=vectorstore_dir
        )

    # Optional: run query if provided
    if auto_query:
        print("\n[INFO] Running query on the pipeline result:")
        retriever = load_vectorstore(vectorstore_dir=vectorstore_dir)
        qa = build_qa_chain(retriever)
        answer_query(auto_query, qa)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the full AstroRAG pipeline.")
    parser.add_argument("--query", type=str, help="Ask a question after pipeline finishes")
    args = parser.parse_args()

    run_pipeline(auto_query=args.query)
