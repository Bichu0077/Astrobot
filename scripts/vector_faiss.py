    
import os
import json
from pathlib import Path
from tqdm import tqdm

from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# ✅ Configuration
CHUNKS_DIR = Path("data/chunks")
INDEX_DIR = "vectorstore/faiss_index"
EMBED_MODEL = "paraphrase-albert-small-v2"

# ✅ Load chunked documents
def load_chunks():
    docs = []
    for file in tqdm(CHUNKS_DIR.rglob("*.jsonl"), desc="🔍 Loading .jsonl chunks"):
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    content = data.get("content") or next(iter(data.values()))
                    if content.strip():
                        docs.append(Document(
                            page_content=content,
                            metadata={
                                "source_file": file.name,
                                "topic": file.parent.name
                            }
                        ))
                except json.JSONDecodeError as e:
                    print(f"⚠️ Skipped malformed line in {file.name}: {e}")
    return docs

# ✅ Build and save vectorstore
def build_vectorstore():
    print(f"🚀 Using embedding model: {EMBED_MODEL}")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    docs = load_chunks()
    if not docs:
        print("❌ No valid chunks found in data/chunks/")
        return

    print(f"📦 Indexing {len(docs)} chunks...")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(INDEX_DIR)
    print(f"✅ FAISS vectorstore saved to: {INDEX_DIR}")

if __name__ == "__main__":
    build_vectorstore()
