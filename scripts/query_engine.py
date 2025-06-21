from pathlib import Path
import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq  # ✅ switched from ChatOpenAI to ChatGroq
from langchain.chains import RetrievalQA
from langchain_core.retrievers import BaseRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


def load_vectorstore(vectorstore_dir: str = "vectorstore/faiss_index") -> BaseRetriever:
    """Load FAISS vector store and return a retriever."""
    embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vs_path = Path(vectorstore_dir)
    if not (vs_path / "index.faiss").exists():
        raise FileNotFoundError(f"FAISS index not found in {vectorstore_dir}")

    vectorstore = FAISS.load_local(vectorstore_dir, embed_model, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever


def build_qa_chain(retriever: BaseRetriever) -> RetrievalQA:
    """Create a QA chain using Groq LLM with Astro Bot's fun tone and retriever."""

    llm = ChatGroq(
        model="llama3-70b-8192",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )

    # Inject Astrobot's fun personality via prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are Astro Bot 🚀, a playful, curious space explorer! Answer all questions about space and science "
         "in a cheerful, friendly tone with a dash of cosmic fun. Avoid being too technical or robotic. "
         "Use emojis where it fits, and keep things simple and engaging."),
        ("human", "{question}")
    ])

    # Create a full custom chain (LLM with prompt)
    prompt_chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | llm
    )

    # Wrap prompt chain with retriever in a RetrievalQA object
    qa_chain = RetrievalQA(
        combine_documents_chain=prompt_chain,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain


def answer_query(query: str, qa_chain: RetrievalQA):
    """Answer a question using the QA chain."""
    result = qa_chain.invoke({"query": query})

    print("\n💬 Question:", query)
    print("\n📘 Answer:", result["result"])

    sources = result.get("source_documents", [])
    if not sources:
        print("\n⚠️ No relevant sources found for this query.")
        return

    print("\n🔍 Sources:")
    for doc in sources:
        print(f" - {doc.metadata.get('topic', 'Unknown')} ({doc.metadata.get('source_file', 'No file')})")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python query_engine.py 'your question here'")
        exit(1)

    user_query = sys.argv[1]
    retriever = load_vectorstore()
    qa = build_qa_chain(retriever)
    answer_query(user_query, qa)
