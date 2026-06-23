"""
ingest.py
─────────────────────────────────────────────
Loads all PDFs (from data/pdfs/) and datasets (from data/datasets/)
Splits them into chunks, creates embeddings, and stores them
in a local ChromaDB vector store for later retrieval.

Handles BOTH text-based PDFs AND scanned/image-only PDFs (via OCR).

Run this ONCE (or whenever you add new documents):
    python src/ingest.py
─────────────────────────────────────────────
"""

import os
import glob
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# OCR imports (for scanned/image PDFs)
from pdf2image import convert_from_path
import pytesseract

# ─────────────────────────────────────────────
#  PATHS
# ─────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR      = os.path.join(BASE_DIR, "data", "pdfs")
DATASET_DIR  = os.path.join(BASE_DIR, "data", "datasets")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")

MIN_TEXT_LENGTH_PER_PAGE = 40  # if extracted text is shorter than this, treat as "image-only" page


# ─────────────────────────────────────────────
#  OCR FALLBACK — extract text from scanned/image pages
# ─────────────────────────────────────────────
def ocr_pdf(pdf_path, filename):
    """Convert each page to an image and run OCR to extract text."""
    documents = []
    try:
        print(f"  🔍 Running OCR on {filename} (this can take a while)...")
        images = convert_from_path(pdf_path, dpi=200)

        for i, img in enumerate(images):
            text = pytesseract.image_to_string(img)
            if text.strip():
                documents.append(Document(
                    page_content=text,
                    metadata={"source": filename, "type": "government_pdf_ocr", "page": i + 1}
                ))
        print(f"  ✅ OCR extracted text from {len(documents)} pages")
    except Exception as e:
        print(f"  ❌ OCR failed for {filename}: {e}")
        print(f"  💡 Make sure Tesseract OCR is installed (see setup instructions)")
    return documents


# ─────────────────────────────────────────────
#  LOAD PDFs (text-based, with automatic OCR fallback)
# ─────────────────────────────────────────────
def load_pdfs():
    documents = []
    pdf_files = glob.glob(os.path.join(PDF_DIR, "*.pdf"))

    print(f"📄 Found {len(pdf_files)} PDF files")

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        try:
            loader = PyPDFLoader(pdf_path)
            pages  = loader.load()

            # Check how much real text was extracted
            total_text_len = sum(len(p.page_content.strip()) for p in pages)
            avg_text_per_page = total_text_len / max(len(pages), 1)

            if avg_text_per_page < MIN_TEXT_LENGTH_PER_PAGE:
                # Looks like a scanned/image-only PDF — use OCR instead
                print(f"  ⚠️  {filename} seems to be scanned/image-based (little text found)")
                ocr_docs = ocr_pdf(pdf_path, filename)
                documents.extend(ocr_docs)
            else:
                # Normal text-based PDF
                for page in pages:
                    page.metadata["source"] = filename
                    page.metadata["type"]   = "government_pdf"
                    page.metadata["category"] = "government_doc"
                    documents.append(page)
                print(f"  ✅ Loaded: {filename} ({len(pages)} pages, text-based)")

        except Exception as e:
            print(f"  ❌ Failed to load {filename}: {e}")

    return documents


# ─────────────────────────────────────────────
#  LOAD CSV DATASETS (Kaggle datasets)
# ─────────────────────────────────────────────
def row_to_sentence(row, columns, state_col=None):
    """Convert a statistical row into a natural-language sentence for better embedding."""
    parts = []
    subject = None

    # Try to find the "subject" of the row (e.g. State/UT name)
    if state_col and pd.notna(row.get(state_col)):
        subject = str(row[state_col]).strip()

    for col in columns:
        val = row[col]
        if pd.isna(val) or str(val).strip() == "" or col == state_col:
            continue
        clean_col = col.replace("_", " ").replace("-", " ").strip()
        parts.append(f"{clean_col} is {val}")

    if not parts:
        return None

    if subject:
        sentence = f"For {subject}: " + "; ".join(parts) + "."
    else:
        sentence = "; ".join(parts) + "."

    return sentence


def load_datasets():
    documents = []
    # Use recursive glob to find CSVs in subfolders too
    csv_files = glob.glob(os.path.join(DATASET_DIR, "**", "*.csv"), recursive=True)

    print(f"📊 Found {len(csv_files)} CSV dataset files (including subfolders)")

    for csv_path in csv_files:
        filename = os.path.basename(csv_path)
        try:
            df = pd.read_csv(csv_path, encoding="utf-8", on_bad_lines="skip")
            print(f"  📋 {filename}: columns = {list(df.columns)}")

            columns = list(df.columns)

            # Detect if this looks like a Q&A style dataset (has Question/Answer cols)
            qa_cols = [c for c in columns if c.lower() in ("question", "answer", "qtype")]

            # Detect a "subject" column for statistical tables (e.g. State/UT)
            state_col = next((c for c in columns if "state" in c.lower() or "ut" in c.lower()), None)

            if len(qa_cols) >= 2:
                # ── Q&A STYLE DATASET (e.g. medical Q&A, diagnosis records) ──
                df = df.drop_duplicates(subset=[c for c in ['Diagnosis', 'Remarks'] if c in columns], keep='first')
                text_cols = [c for c in columns if df[c].dtype == object]
                for idx, row in df.iterrows():
                    content_parts = []
                    for col in text_cols:
                        val = row[col]
                        if pd.notna(val) and str(val).strip():
                            content_parts.append(f"{col}: {val}")
                    if content_parts:
                        content = "\n".join(content_parts)
                        is_patient_record = "AI_HINDI" in filename or "AI_PUNJABI" in filename or "BERT" in filename
                        doc_category = "patient_record" if is_patient_record else "medical_qa"
                        documents.append(Document(
                            page_content=content,
                            metadata={"source": filename, "type": "qa_dataset", "category": doc_category, "row": idx}
                        ))
                    if idx >= 5000:
                        print(f"  ⚠️ Limiting {filename} to first 5000 rows")
                        break
                print(f"  ✅ Processed (Q&A style): {filename} ({min(len(df), 5001)} rows)")

            else:
                # ── STATISTICAL TABLE (e.g. health infrastructure stats) ──
                # Convert each row to a natural sentence for better semantic matching
                sentences = []
                for idx, row in df.iterrows():
                    sentence = row_to_sentence(row, columns, state_col)
                    if sentence:
                        sentences.append(sentence)

                table_title = filename.replace(".csv", "").replace("_", " ").replace("-", " ")
                for sentence in sentences:
                    documents.append(Document(
                        page_content=f"From {table_title} data: {sentence}",
                        metadata={"source": filename, "type": "stat_table", "category": "statistics"}
                    ))
                print(f"  ✅ Processed (statistical table): {filename} ({len(sentences)} rows → {len(sentences)} individual documents)")

        except Exception as e:
            print(f"  ❌ Failed to load {filename}: {e}")

    return documents


# ─────────────────────────────────────────────
#  MAIN INGESTION PIPELINE
# ─────────────────────────────────────────────
def main():
    print("🚀 Starting ingestion pipeline...\n")

    # Step 1: Load all documents
    pdf_docs     = load_pdfs()
    dataset_docs = load_datasets()
    all_docs     = pdf_docs + dataset_docs

    if not all_docs:
        print("\n❌ No documents found! Make sure PDFs are in data/pdfs/ and CSVs in data/datasets/")
        return

    print(f"\n📚 Total documents loaded: {len(all_docs)}")

    # Step 2: Split into chunks
    print("\n✂️  Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(all_docs)
    print(f"✅ Created {len(chunks)} chunks")

    # Step 3: Create embeddings (free, runs locally, no API needed)
    print("\n🧠 Loading embedding model (first time may take a minute)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Step 4: Create & persist vector store (in batches to avoid ChromaDB limit)
    print("\n💾 Creating vector store (this may take a few minutes)...")

    BATCH_SIZE = 4000  # safely under ChromaDB's max batch size of 5461

    vectordb = None
    total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        print(f"  📦 Processing batch {batch_num}/{total_batches} ({len(batch)} chunks)...")

        if vectordb is None:
            vectordb = Chroma.from_documents(
                documents=batch,
                embedding=embeddings,
                persist_directory=VECTORSTORE_DIR
            )
        else:
            vectordb.add_documents(batch)

    print(f"\n🎉 Done! Vector store saved to: {VECTORSTORE_DIR}")
    print(f"📊 Total chunks indexed: {len(chunks)}")
    print("\n✅ You can now run: streamlit run src/app.py")


if __name__ == "__main__":
    main()