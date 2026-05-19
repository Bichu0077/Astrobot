from pathlib import Path
import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq  
from groq import BadRequestError
from langchain.chains import RetrievalQA
from langchain_core.retrievers import BaseRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

def load_vectorstore(vectorstore_dir: str = "vectorstore/faiss_index") -> BaseRetriever:
    """Load FAISS vector store and return a retriever."""
    embed_model = HuggingFaceEmbeddings(model_name="./models/paraphrase-albert-small-v2")
    vs_path = Path(vectorstore_dir)
    if not (vs_path / "index.faiss").exists():
        raise FileNotFoundError(f"FAISS index not found in {vectorstore_dir}")

    vectorstore = FAISS.load_local(vectorstore_dir, embed_model, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever


def build_qa_chain(retriever: BaseRetriever, model_name: str | None = None) -> RetrievalQA:
    """Create a QA chain using Groq LLM with Astro Bot's fun tone and retriever."""

    if model_name is None:
        model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    llm = ChatGroq(
        model=model_name,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )

    #Astrobot's fun personality via prompt.
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are Astro Bot 🚀, a playful, curious space explorer! Answer all questions about space and science "
         "in a cheerful, friendly tone with a dash of cosmic fun. Avoid being too technical or robotic. "
         "Use emojis where it fits, and keep things simple and engaging."),
        ("human", "{question}")
    ])

   
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
    try:
        result = qa_chain.invoke({"query": query})
    except BadRequestError as e:
        msg = str(e)
        if "decommissioned" in msg or "model_decommissioned" in msg:
            fallbacks_env = os.getenv("GROQ_FALLBACK_MODELS")
            if fallbacks_env:
                fallbacks = [m.strip() for m in fallbacks_env.split(",") if m.strip()]
                last_err = e
                for fb in fallbacks:
                    try:
                        qa_chain = build_qa_chain(retriever, model_name=fb)
                        result = qa_chain.invoke({"query": query})
                        print("\n✅ Succeeded with fallback model:", fb)
                        break
                    except BadRequestError as sub_e:
                        last_err = sub_e
                        print(f"Fallback model {fb} failed: {sub_e}")
                else:
                    raise RuntimeError(
                        "All configured GROQ_FALLBACK_MODELS failed after the primary model was decommissioned. "
                        "Please set a valid `GROQ_MODEL` or update `GROQ_FALLBACK_MODELS`. "
                        f"Last error: {last_err}"
                    ) from last_err
            else:
                raise RuntimeError(
                    "Groq API rejected the model. The model you requested appears to be decommissioned. "
                    "Set the environment variable `GROQ_MODEL` to a supported model name (see https://console.groq.com/docs/deprecations). "
                    f"Original error: {msg}"
                ) from e
        else:
            raise

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
