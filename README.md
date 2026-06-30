---
title: Sehat Sathi
emoji: 🩺
colorFrom: green
colorTo: yellow
sdk: streamlit
sdk_version: "1.36.0"
app_file: src/app.py
pinned: false
---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0A0E0D,50:1B4D3E,100:3DDC97&height=200&section=header&text=सेहत%20साथी%20·%20Sehat%20Sathi&fontSize=42&fontColor=ffffff&fontAlignY=38&desc=Rural%20Health%20Assistant%20·%20Powered%20by%20RAG&descAlignY=58&descSize=18&descColor=5EEAD4" width="100%"/>

<br>

<img src="https://readme-typing-svg.demolab.com?font=Fraunces&size=20&pause=1200&color=3DDC97&center=true&vCenter=true&width=650&lines=Trusted+answers%2C+in+plain+language.;Grounded+in+verified+government+guidelines.;English+%E2%80%A2+Hindi+%E2%80%A2+Punjabi+supported.;No+hallucinations.+No+false+confidence.+Just+truth." alt="Typing SVG" />

<br><br>

[![🚀 Live Demo](https://img.shields.io/badge/🚀_Live_on-Hugging%20Face%20Spaces-3DDC97?style=for-the-badge&labelColor=0A0E0D)](https://huggingface.co/spaces/MridulSharma02/Sehat-Sathi)
[![GitHub](https://img.shields.io/badge/GitHub-Source%20Code-5EEAD4?style=for-the-badge&logo=github&logoColor=white&labelColor=0A0E0D)](https://github.com/MridulSharma02/rural-health-rag)
[![Python](https://img.shields.io/badge/Python-3.11-FF8A5C?style=for-the-badge&logo=python&logoColor=white&labelColor=0A0E0D)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-8FA998?style=for-the-badge&labelColor=0A0E0D)](LICENSE)

<br>

![Problems](https://img.shields.io/badge/📄_Documents-8%20PDFs%20+%2025%20Datasets-3DDC97?style=flat-square&labelColor=1B4D3E)
![Chunks](https://img.shields.io/badge/🧩_Knowledge%20Chunks-93%2C000+-5EEAD4?style=flat-square&labelColor=1B4D3E)
![Languages](https://img.shields.io/badge/🌍_Languages-English%20·%20Hindi%20·%20Punjabi-FF8A5C?style=flat-square&labelColor=1B4D3E)
![Cost](https://img.shields.io/badge/💰_Cost-100%25%20Free-8FA998?style=flat-square&labelColor=1B4D3E)

</div>

---

## 🌾 The Problem

> *In rural India, the nearest doctor can be hours away. People make critical health decisions based on word of mouth, outdated information, or nothing at all.*

**Sehat Sathi** bridges this gap — a RAG-powered health assistant that answers questions using only **verified government guidelines and trusted medical datasets**, in the user's own language.

---

## 🩺 What Makes It Different

Most health chatbots either make things up or give generic advice. Sehat Sathi is different in two fundamental ways:

### 1. Every answer is labeled for honesty

| Badge | What it means |
|:---:|:---|
| `✓ VERIFIED SOURCE` | Answer pulled directly from official documents, with citation shown |
| `⌁ GENERAL KNOWLEDGE` | No verified match found — honestly flagged, doctor visit always recommended |

### 2. It knows what it doesn't know
When the knowledge base doesn't have the answer, it **says so clearly** instead of inventing information. In healthcare, this isn't a limitation — it's a safety feature.

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

**🔍 RAG-Powered Retrieval**
Searches 93,000+ chunks from government PDFs and health datasets before generating any answer

**🌍 True Multilingual Support**
Automatically detects and responds in English, Hindi, or Punjabi — no language selection needed

**🧠 Conversation Memory**
Understands follow-up questions — ask "How is *it* treated?" and it knows what "it" refers to

</td>
<td width="50%">

**🩹 Symptom Checker Mode**
Structured triage assessment with urgency levels: `LOW` / `MEDIUM` / `HIGH`

**🔒 Honest by Design**
Never fabricates statistics or invents medical information

**⚡ Rate-Limited & Resilient**
Built for real-world reliability with graceful error handling

</td>
</tr>
</table>

---

## 🧬 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   User asks a health question (any language)               │
│                           │                                 │
│                           ▼                                 │
│   ┌─────────────────────────────────────────┐              │
│   │   ChromaDB Vector Search                 │              │
│   │   93,000+ embedded chunks                │              │
│   │   from PDFs + CSVs                       │              │
│   └──────────────────┬──────────────────────┘              │
│                      │                                      │
│          ┌───────────▼───────────┐                         │
│          │   Relevance Check      │                         │
│          │                        │                         │
│     Good match?              No match?                      │
│          │                        │                         │
│          ▼                        ▼                         │
│   ✓ Verified Source        ⌁ General Knowledge             │
│   (with citations)         (clearly labeled)               │
│          │                        │                         │
│          └───────────┬────────────┘                         │
│                      │                                      │
│                      ▼                                      │
│   ┌─────────────────────────────────────────┐              │
│   │   Groq (Llama 3.1)                       │              │
│   │   Generates answer in question's          │              │
│   │   own language                            │              │
│   └─────────────────────────────────────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|:---:|:---:|:---|
| 🤖 LLM | [Groq](https://groq.com/) · Llama 3.1 8B | Fast, free cloud inference |
| 🧠 Embeddings | `sentence-transformers/all-MiniLM-L6-v2` | Local semantic search |
| 🗄️ Vector DB | [ChromaDB](https://www.trychroma.com/) | Persistent knowledge store |
| ⚙️ Framework | [LangChain](https://www.langchain.com/) | RAG orchestration |
| 🎨 Frontend | [Streamlit](https://streamlit.io/) | Interactive chat UI |
| ☁️ Deployment | [Hugging Face Spaces](https://huggingface.co/spaces) | Free, permanent hosting |

---

## 📚 Knowledge Base

<details>
<summary><b>🏛️ Government Guidelines — 8 PDFs</b></summary>
<br>

| Source | Document |
|:---:|:---|
| 🏥 NHM | Free Drugs Service Guidelines |
| 🏥 NHM | Hemoglobinopathies Guidelines |
| 🏥 NHM | NCD (Non-Communicable Disease) Guidelines |
| 🏥 NHM | Telemedicine Guidelines |
| 🏛️ NHA | Ayushman Bharat (PM-JAY) Standard Treatment Guidelines |
| 🌍 WHO | Diabetes Guidelines |
| 🌍 WHO | Maternal Health Guidelines |
| 🌍 WHO | Tuberculosis Guidelines |

</details>

<details>
<summary><b>📊 Health Datasets — 25 CSVs</b></summary>
<br>

| Category | Data |
|:---:|:---|
| 🏗️ Infrastructure | PHC, CHC, Sub-Centre counts by state |
| 👨‍⚕️ Staffing | Doctor, nurse, pharmacist shortage data |
| 👶 Health Metrics | Infant mortality rates (state-wise, rural vs urban) |
| 🌾 Coverage | Rural population per health facility |
| ❓ Medical Q&A | 5,000+ verified medical question-answer pairs |
| 🌍 Multilingual | Patient records in English, Hindi, and Punjabi |

</details>

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/MridulSharma02/rural-health-rag.git
cd rural-health-rag

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your free Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# 4. Build the knowledge base (one-time, takes ~20 min)
python src/ingest.py

# 5. Launch
streamlit run src/app.py
```

> 🔑 Get a free Groq API key at [console.groq.com](https://console.groq.com) — no credit card needed

---

## 🔐 Security & Production Readiness

| Feature | Implementation |
|:---:|:---|
| 🔑 API Key Security | Stored in HF Secrets, never in code or git history |
| 🚦 Rate Limiting | 15 questions per session to protect API quota |
| 🛡️ Resilience | Graceful error handling for API failures |
| 📝 Gitignore | `.env` and `vectorstore/` excluded from all commits |

---

## ⚠️ Disclaimer

Sehat Sathi provides **general health information** based on official government guidelines. It is **not a substitute for professional medical advice, diagnosis, or treatment**. For emergencies or serious symptoms, please visit your nearest health center or call emergency services immediately.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:3DDC97,50:1B4D3E,100:0A0E0D&height=120&section=footer&text=Built%20for%20the%20people%20who%20need%20it%20most&fontSize=16&fontColor=ffffff&fontAlignY=65" width="100%"/>

[![Try Sehat Sathi](https://img.shields.io/badge/🩺_Try_Sehat_Sathi_Now-3DDC97?style=for-the-badge&labelColor=0A0E0D)](https://huggingface.co/spaces/MridulSharma02/Sehat-Sathi)

*Made with ❤️ for rural India*

</div>