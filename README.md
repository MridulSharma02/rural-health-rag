---
title: Sehat Sathi - Rural Health Assistant
emoji: 🩺
colorFrom: green
colorTo: yellow
sdk: streamlit
sdk_version: "1.36.0"
app_file: src/app.py
pinned: false
---

# 🩺 Sehat Sathi — Rural Health Assistant

An AI assistant that answers health questions using verified government
guidelines and medical datasets — built with free, open tools, powered by RAG.

## 🛠️ Tech Stack
- **LLM:** Groq (Llama 3.1) — free, fast cloud inference
- **Embeddings:** HuggingFace sentence-transformers (local, free)
- **Vector DB:** ChromaDB (local, free)
- **Framework:** LangChain
- **Frontend:** Streamlit

## 📁 Project Structure
```
rural-health-rag/
├── data/
│   ├── pdfs/          ← government health PDFs
│   └── datasets/       ← Kaggle CSV datasets
├── src/
│   ├── ingest.py       ← processes documents into vector store
│   ├── rag.py          ← core RAG logic
│   └── app.py          ← Streamlit web app
├── vectorstore/         ← auto-created after running ingest.py
├── requirements.txt
├── packages.txt         ← system packages for Hugging Face (OCR support)
└── .env                 ← your Groq API key (local only, not committed)
```

## 🚀 Local Setup Instructions

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your Groq API key
Open `.env` and replace with your actual key:
```
GROQ_API_KEY=your_actual_key_here
```

### 3. (For scanned/image PDFs) Install OCR tools locally
- **Tesseract OCR:** https://github.com/UB-Mannheim/tesseract/wiki
- **Poppler:** https://github.com/oschwartz10612/poppler-windows/releases
  (Add the `bin` folder to your System PATH)

### 4. Run ingestion (processes all your documents)
```bash
python src/ingest.py
```

### 5. Launch the app locally
```bash
streamlit run src/app.py
```

## 🌐 Deploying on Hugging Face Spaces
1. Create a new Space at https://huggingface.co/new-space (choose **Streamlit** SDK)
2. Push this project's files to the Space's repo
3. Go to **Settings → Repository secrets** → add `GROQ_API_KEY`
4. The Space auto-installs everything from `requirements.txt` and `packages.txt`
5. Your permanent live link: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

## ⚠️ Disclaimer
This assistant provides general health information based on official guidelines.
It is not a substitute for professional medical advice.
