"""
rag.py
─────────────────────────────────────────────
Core RAG (Retrieval Augmented Generation) pipeline.
Loads the vector store, retrieves relevant chunks for a query,
and uses Groq's free Llama 3 API to generate an answer.

Includes:
- Improved retrieval (more chunks, relevance scoring)
- Fallback to general medical knowledge when verified docs
  don't have enough info — clearly labeled either way.
─────────────────────────────────────────────
"""

import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Relevance threshold — Chroma returns L2 distance (lower = more similar).
# Chunks above this distance are considered "not relevant enough" to trust.
RELEVANCE_DISTANCE_THRESHOLD_ENGLISH = 1.25
RELEVANCE_DISTANCE_THRESHOLD_OTHER = 1.15

# ─────────────────────────────────────────────
#  PROMPT — grounded answer (verified sources found)
# ─────────────────────────────────────────────
GROUNDED_PROMPT = """You are a helpful Rural Healthcare Assistant. Answer the question using \
ONLY the verified context below, which comes from government health guidelines and medical \
knowledge sources.

Rules:
1. Answer clearly and simply — assume the person may not have medical knowledge.
2. Keep answers concise but complete — use simple language, avoid jargon.
3. For anything serious or urgent, always recommend visiting the nearest health center or doctor.
4. Respond in the same language the question was asked in.
5. Do not mention "the context" or "the document" explicitly — just answer naturally.
6. Always respond in the same language as the question shown above (in the "Question:" line below) — typically English unless the question itself contains Hindi or another language.

Conversation so far:
{history}

Context:
{context}

Question: {question}

Answer:"""

# ─────────────────────────────────────────────
#  PROMPT — general fallback (no good verified match found)
# ─────────────────────────────────────────────
FALLBACK_PROMPT = """You are a helpful Rural Healthcare Assistant. The verified knowledge base \
does NOT contain enough information to answer this question, so you must answer using your own \
general medical knowledge instead.

Rules:
1. Answer clearly and simply — assume the person may not have medical knowledge.
2. Keep answers concise but complete.
3. Always recommend visiting the nearest health center or doctor for confirmation, since this \
answer is not from a verified local source.
4. Respond in the same language the question was asked in.
5. Be accurate and conservative — if you are not confident, say so honestly.
6. Always respond in the same language as the question shown above (in the "Question:" line below) — typically English unless the question itself contains Hindi or another language.

Conversation so far:
{history}

Question: {question}

Answer:"""


def load_vectorstore():
    """Load the persisted Chroma vector store."""
    if not os.path.exists(VECTORSTORE_DIR):
        raise FileNotFoundError(
            "Vector store not found! Please run 'python src/ingest.py' first."
        )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectordb = Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embeddings
    )
    return vectordb


def get_llm():
    """Initialize the free Groq-hosted Llama 3 model."""
    if not GROQ_API_KEY or GROQ_API_KEY == "paste_your_groq_api_key_here":
        raise ValueError(
            "GROQ_API_KEY not set! Please add your key to the .env file."
        )

    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0.3,
        max_tokens=600,
    )


def answer_question(query, vectordb, llm, chat_history=None, k=20):
    """
    Retrieve relevant chunks for the query and generate an answer.
    Falls back to general knowledge (clearly labeled) if no chunk is relevant enough.

    Returns: (answer_text, list_of_source_documents, is_verified: bool)
    """

    history_text = ""
    import re
    current_is_hindi = bool(re.search(r'[\u0900-\u097F\u0A00-\u0A7F]', query))
    followup_signals = ["it", "this", "that", "they", "them", "इसे", "यह", "वह", "ਇਹ", "ਉਹ"]
    is_likely_followup = any(f" {word} " in f" {query.lower()} " for word in followup_signals) or len(query.split()) <= 4

    if chat_history and is_likely_followup:
        for h in chat_history[-2:]:
            msg_is_hindi = bool(re.search(r'[\u0900-\u097F\u0A00-\u0A7F]', h.get("content", "")))
            if msg_is_hindi == current_is_hindi:
                role = "User" if h["role"] == "user" else "Assistant"
                history_text += f"{role}: {h['content']}\n"

    # Step 1: Retrieve relevant chunks WITH relevance scores
    import re
    has_non_latin = bool(re.search(r'[\u0900-\u097F\u0A00-\u0A7F]', query))
    results = vectordb.similarity_search_with_score(query, k=k)
    if not has_non_latin:
        results = [(doc, score) for doc, score in results
                   if doc.metadata.get("category") != "patient_record"]

    # Step 2: Filter to only chunks that pass the relevance threshold
    threshold = RELEVANCE_DISTANCE_THRESHOLD_OTHER if has_non_latin else RELEVANCE_DISTANCE_THRESHOLD_ENGLISH
    relevant_results = [(doc, score) for doc, score in results if score <= threshold]

    if not relevant_results:
        # ── FALLBACK: no good match found in verified docs ──
        try:
            prompt = ChatPromptTemplate.from_template(FALLBACK_PROMPT)
            chain = prompt | llm
            response = chain.invoke({"question": query, "history": history_text})
            return response.content, [], False
        except Exception as e:
            return "⚠️ The service is temporarily busy. Please try again in a moment.", [], None

    # ── GROUNDED: build context from relevant chunks ──
    context_parts = []
    sources = []
    for doc, score in relevant_results[:5]:
        context_parts.append(doc.page_content)
        source_name = doc.metadata.get("source", "Unknown")
        if source_name not in sources:
            sources.append(source_name)

    context = "\n\n---\n\n".join(context_parts)

    try:
        prompt = ChatPromptTemplate.from_template(GROUNDED_PROMPT)
        chain = prompt | llm

        response = chain.invoke({
            "context": context,
            "question": query,
            "history": history_text
        })

        return response.content, sources, True
    except Exception as e:
        return "⚠️ The service is temporarily busy. Please try again in a moment.", [], None

SYMPTOM_CHECKER_PROMPT = """You are a careful Rural Healthcare symptom-checker assistant. \
Based on the symptoms described below, provide a structured assessment.

Rules:
1. List 2-3 possible (NOT definitive) conditions that match these symptoms.
2. Rate urgency as: LOW, MEDIUM, or HIGH.
3. Give clear next-step advice (home care vs see doctor vs emergency).
4. Always state this is NOT a diagnosis.
5. Respond in the same language as the input.

Symptoms described: {symptoms}

Provide your assessment in this format:
**Possible considerations:** ...
**Urgency level:** ...
**Recommended action:** ...
"""

def check_symptoms(symptoms_text, llm):
    """Structured symptom assessment — separate from general Q&A."""
    prompt = ChatPromptTemplate.from_template(SYMPTOM_CHECKER_PROMPT)
    chain = prompt | llm
    response = chain.invoke({"symptoms": symptoms_text})
    return response.content

if __name__ == "__main__":
    # Quick test mode — run this file directly to test in terminal
    print("🔧 Loading vector store...")
    vectordb = load_vectorstore()
    print("🔧 Loading LLM...")
    llm = get_llm()

    print("\n✅ Ready! Ask a health question (type 'quit' to exit)\n")

    while True:
        query = input("🙋 You: ")
        if query.lower() in ["quit", "exit"]:
            break

        answer, sources, is_verified = answer_question(query, vectordb, llm)
        tag = "✅ VERIFIED" if is_verified else "🌐 GENERAL KNOWLEDGE"
        print(f"\n🤖 [{tag}] Assistant: {answer}")
        if sources:
            print(f"\n📚 Sources: {', '.join(sources)}")
        print()
        