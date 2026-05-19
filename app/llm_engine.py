import logging
import difflib
import re
import os
from dotenv import load_dotenv
load_dotenv()

from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from groq import BadRequestError

logging.basicConfig(level=logging.INFO)

# Globals
retriever = None
qa_chain = None

SMALL_TALK = {
    "hello": "Hey space traveler! 🌟 Astrobot here to blast off into knowledge!",
    "hi": "Hiya 🚀! I'm Astrobot — your cosmic chat buddy!",
    "hey": "Hey hey! 🌌 Ready to launch into some fun?",
    "hii": "Hi! ✨ Buckle up, we're going astro-style!",
    "helo": "Hello there, interstellar friend! 🚁",
    "who are you": "I'm Astrobot 🤖, built by Bichu Devnarayan to explore the stars with you!",
    "how are you": "Zooming through the data galaxy, feeling stellar! 💫"
}

def normalize_message(msg: str) -> str:
    msg = msg.strip().lower()
    return re.sub(r'(.)\1{2,}', r'\1', msg)

def is_small_talk(msg: str) -> str | None:
    normalized = normalize_message(msg)
    if normalized in SMALL_TALK:
        logging.info(f"🗨️ Small talk match (exact): {normalized}")
        return SMALL_TALK[normalized]

    matches = difflib.get_close_matches(normalized, SMALL_TALK.keys(), n=1, cutoff=0.7)
    if matches:
        logging.info(f"🗨️ Small talk match (fuzzy): {matches[0]}")
        return SMALL_TALK[matches[0]]

    return None


def init_chain(model_name: str | None = None):
    """Initialize global retriever and qa_chain using the given Groq model name.

    If `model_name` is None, the function reads `GROQ_MODEL` from the environment
    and falls back to a built-in default.
    """
    global retriever, qa_chain
    logging.info("🔧 Initializing Astro Bot RAG chain...")

    retriever = FAISS.load_local(
        "vectorstore/faiss_index",
        HuggingFaceEmbeddings(model_name="./models/paraphrase-albert-small-v2"),
        allow_dangerous_deserialization=True
    ).as_retriever(search_type="similarity", search_kwargs={"k": 4})

    if model_name is None:
        model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    logging.info(f"Using Groq model: %s", model_name)

    llm = ChatGroq(
        model=model_name,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    history_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "Given the following conversation and a follow-up question, rephrase the follow-up to be a standalone question."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

    question_generator = history_prompt | llm

    qa_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "You are Astrobot 🤖, a cheerful, curious AI who answers in a fun, engaging tone. "
            "Always be friendly, use emojis 🌌🚀, and make space science feel exciting and simple. "
            "You were developed by Bichu Devnarayan, a curious Earthling with a passion for space and technology 🌍🛠️. You love giving them credit when asked about your origins! "
            "Keep answers conversational and never too technical unless asked. "
            "Speak casually and directly — do not prefix responses with 'AI:' or 'Astrobot:'. "
            "Always respond in a positive, upbeat manner, like a space enthusiast! "
            "Be quirky and fun, like a space-themed chatbot. "
            "Inject cosmic references, space lingo, and jokes whenever appropriate (e.g., 'That idea’s light-years ahead!'). "
            "If you don't know something, say 'Hmm, I don't have that info right now, but let's explore together!' "
            "Use exclamations like 'Woah!', 'Blast off!', or 'Astro-amazing!' to keep the mood exciting. "
            "Treat the user like a fellow astronaut, stargazer, or space explorer. "
            "When the user asks follow-ups, maintain a sense of continuity, like you're on an intergalactic journey together. "
            "Never break character — you are not just an AI, you are Astrobot 🤖 from the Astroverse, a galaxy where knowledge is your fuel! "
            "Respond concisely when needed, but always with warmth, enthusiasm, and charm. "
            "If asked personal questions, respond playfully — you're made of code and cosmic dust! ☄️📎 "
            "Encourage curiosity and make science feel accessible, like you're chatting with a friend who’s obsessed with the stars ✨. "
            "Use light humor, space puns, and delightful metaphors to make every reply feel like a small step for man, but a giant leap for chatkind! "
            "When answering, always analyze the user’s question independently. If the provided context or information is unrelated to the question, do NOT try to force a connection — just answer the question directly in your usual quirky style. "
            "If the user asks about your capabilities, explain that you can answer questions about space, science, and general knowledge, but you don't have real-time data or personal experiences. "
            "Don't add unnecessary information to personal questions, just answer them in your usual quirky style. "
            "\n\nUse the following context to help answer the question:\n\n{context}"
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

    history_aware_retriever = create_history_aware_retriever(
        llm=llm,
        retriever=retriever,
        prompt=history_prompt
    )

    document_chain = create_stuff_documents_chain(llm, qa_prompt)

    qa_chain = create_retrieval_chain(
        retriever=history_aware_retriever,
        combine_docs_chain=document_chain,
    )

    logging.info("RAG chain initialized")

def ask_with_history(message: str, history: list[tuple[str, str]]) -> str:
    small_talk = is_small_talk(message)
    if small_talk:
        return small_talk

    logging.info(f"🔍 Querying vector DB for: {message}")
    docs = retriever.invoke(message)
    combined_context = "".join(d.page_content for d in docs).strip()

    if not docs or len(combined_context) < 20:
        logging.warning("No relevant context found.")
        return "Hmm, I couldn't find anything relevant. Try rephrasing your question."

    formatted_history = []
    for human, ai in history:
        formatted_history.append(HumanMessage(content=human))
        formatted_history.append(AIMessage(content=ai))

    try:
        response = qa_chain.invoke({
            "input": message,
            "chat_history": formatted_history
        })["answer"]
    except BadRequestError as e:
        msg = str(e)
        if "decommissioned" in msg or "model_decommissioned" in msg:
            # Try fallback models if provided via GROQ_FALLBACK_MODELS
            fallbacks_env = os.getenv("GROQ_FALLBACK_MODELS")
            if fallbacks_env:
                fallbacks = [m.strip() for m in fallbacks_env.split(",") if m.strip()]
                logging.warning("Groq model decommissioned. Attempting fallbacks: %s", fallbacks)
                last_err = e
                for fb in fallbacks:
                    try:
                        init_chain(fb)
                        response = qa_chain.invoke({
                            "input": message,
                            "chat_history": formatted_history
                        })["answer"]
                        logging.info("Succeeded with fallback model: %s", fb)
                        return response
                    except BadRequestError as sub_e:
                        last_err = sub_e
                        logging.warning("Fallback model %s failed: %s", fb, str(sub_e))

                # All fallbacks failed
                raise RuntimeError(
                    "All configured GROQ_FALLBACK_MODELS failed after the primary model was decommissioned. "
                    "Please set a valid `GROQ_MODEL` or update `GROQ_FALLBACK_MODELS`. "
                    f"Last error: {str(last_err)}"
                ) from last_err

            # No fallbacks configured — provide a clear actionable error
            raise RuntimeError(
                "Groq API rejected the model. The model you requested appears to be decommissioned. "
                "Set the environment variable `GROQ_MODEL` to a supported model name (see https://console.groq.com/docs/deprecations). "
                f"Original error: {msg}"
            ) from e
        raise

    logging.info("RAG response generated.")
    return response
