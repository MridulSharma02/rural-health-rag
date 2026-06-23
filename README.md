<div align="center">

# 🩺 सेहत साथी — Sehat Sathi

### Rural Health Assistant powered by RAG

<img src="https://readme-typing-svg.demolab.com?font=Fraunces&size=22&pause=1000&color=3DDC97&center=true&vCenter=true&width=600&lines=Trusted+answers%2C+in+plain+language.;Grounded+in+government+guidelines.;English+%E2%80%A2+Hindi+%E2%80%A2+Punjabi+supported." alt="Typing SVG" />

<br>

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Hugging%20Face%20Spaces-3DDC97?style=for-the-badge)](https://huggingface.co/spaces/MridulSharma02/Sehat-Sathi)
[![Python](https://img.shields.io/badge/Python-3.11-5EEAD4?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF8A5C?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-8FA998?style=for-the-badge)](LICENSE)

</div>

---

## 🎯 What is this?

**Sehat Sathi** is an AI health assistant built for rural India — it answers health questions in **English, Hindi, and Punjabi**, grounded entirely in verified sources: government health guidelines (NHM, WHO, Ayushman Bharat) and trusted medical datasets.

Unlike a generic chatbot, every answer is labeled:

| Badge | Meaning |
|---|---|
| `✓ VERIFIED SOURCE` | Pulled directly from official documents — with citation |
| `⌁ GENERAL KNOWLEDGE` | No verified match found — clearly flagged as general info, with a doctor visit recommended |

No hallucinated statistics. No false confidence. Just honest, sourced healthcare guidance — built specifically for places where the nearest doctor might be hours away.

<div align="center">
<img src="https://img.shields.io/badge/🏛️_Govt._Verified-Sources-3DDC97?style=flat-square" />
<img src="https://img.shields.io/badge/🔍_RAG-Retrieval_Powered-5EEAD4?style=flat-square" />
<img src="https://img.shields.io/badge/🌍_Multilingual-EN_|_HI_|_PA-FF8A5C?style=flat-square" />
<img src="https://img.shields.io/badge/💰_100%25-Free_%26_Open-8FA998?style=flat-square" />
</div>

---

## ✨ Features

- 🩺 **Verified RAG answers** — grounded in 8 government PDFs + 25 health datasets
- 🌍 **Multilingual** — detects and responds in English, Hindi, or Punjabi automatically
- 🧠 **Conversation memory** — understands follow-ups ("How is *it* treated?")
- 🩹 **Symptom Checker Mode** — structured urgency assessment (LOW / MEDIUM / HIGH)
- 🔒 **Honest by design** — never fabricates statistics; says "I don't know" when it doesn't know
- ⚡ **Rate-limited & resilient** — built for real-world reliability, not just a demo

---

## 🧬 How it works

```
   User Question
        │
        ▼
┌───────────────────┐
│  Vector Search     │  ──►  93,000+ chunks from PDFs + CSVs
│  (ChromaDB)        │       embedded with sentence-transformers
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Relevance Check    │  ──►  Found good match? → ✓ Verified
│                     │       No match?         → ⌁ General Knowledge
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Groq (Llama 3.1)   │  ──►  Generates final answer,
│                     │       in the question's own language
└───────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | [Groq](https://groq.com/) — Llama 3.1 8B (free, fast inference) |
| Embeddings | [sentence-transformers](https://www.sbert.net/) `all-MiniLM-L6-v2` |
| Vector DB | [ChromaDB](https://www.trychroma.com/) |
| Orchestration | [LangChain](https://www.langchain.com/) |
| Frontend | [Streamlit](https://streamlit.io/) |
| Deployment | [Hugging Face Spaces](https://huggingface.co/spaces) |

---

## 📚 Knowledge Sources

<details>
<summary><b>🏛️ Government Guidelines (8 PDFs)</b></summary>
<br>

- National Health Mission — Free Drugs Service Guidelines
- National Health Mission — Hemoglobinopathies Guidelines
- National Health Mission — NCD Guidelines
- National Health Mission — Telemedicine Guidelines
- National Health Authority — Ayushman Bharat (PM-JAY) STG
- WHO — Diabetes Guidelines
- WHO — Maternal Health Guidelines
- WHO — Tuberculosis Guidelines

</details>

<details>
<summary><b>📊 Health Statistics (25 Datasets)</b></summary>
<br>

- India Primary Health Care infrastructure data (PHCs, CHCs, sub-centres)
- Staff shortage statistics (doctors, nurses, pharmacists, surgeons)
- Infant mortality rates by state
- Rural population coverage per health facility
- Comprehensive Medical Q&A dataset
- Multilingual patient records (English, Hindi, Punjabi)

</details>

---

## 🚀 Run it locally

```bash
# 1. Clone the repo
git clone https://github.com/MridulSharma02/rural-health-rag.git
cd rural-health-rag

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your free Groq API key to .env
echo "GROQ_API_KEY=your_key_here" > .env

# 4. Build the knowledge base (one-time)
python src/ingest.py

# 5. Launch
streamlit run src/app.py
```

> Get a free Groq API key at [console.groq.com](https://console.groq.com)

---

## ⚠️ Disclaimer

Sehat Sathi provides **general health information** based on official guidelines. It is **not a substitute for professional medical advice**. For emergencies or serious symptoms, please visit your nearest health center or call emergency services immediately.

---

<div align="center">

**Built with care for places where the nearest doctor is hours away.**

[![Live Demo](https://img.shields.io/badge/Try_it_now-Sehat_Sathi-3DDC97?style=for-the-badge)](https://huggingface.co/spaces/MridulSharma02/Sehat-Sathi)

</div>
