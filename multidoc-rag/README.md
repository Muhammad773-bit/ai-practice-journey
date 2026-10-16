# Multi-Document RAG Agent

A Retrieval-Augmented Generation system built with LangChain that processes PDF, DOCX, and PPTX documents.

## 📋 Architecture

```
Documents
  ↓
Loaders (PDF, DOCX, PPT)
  ↓
Text Splitter
  ↓
Embeddings
  ↓
Vector Store (Chroma)
  ↓
Retriever
  ↓
Retrieval Chain
  ↓
Answer
```

## 🗂️ Project Structure

```
antigravity_RAG/
├── data/
│   ├── pdfs/          # Place PDF files here
│   ├── docs/          # Place DOCX files here
│   └── ppts/          # Place PPTX files here
│
├── loader_main/
│   └── loader_router.py    # Document loader router
│
├── agent/
│   └── qa_agent.py         # QA agent implementation
│
├── ingest.py               # One-time ingestion script
├── main.py                 # Query execution interface
├── requirements.txt        # Dependencies
└── chroma_db/             # Vector database (created after ingestion)
```

## 🚀 Setup

### 1. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

**Note**: First installation will download:
- Hugging Face models (~900MB for LLM, ~80MB for embeddings)
- PyTorch and other dependencies

### 3. Add Documents

Place your documents in the appropriate folders:
- **PDF files** → `data/pdfs/`
- **DOCX files** → `data/docs/`
- **PPTX files** → `data/ppts/`

## 📥 Ingestion

Run the ingestion script to process and store documents:

```powershell
python ingest.py
```

This will:
1. Load all documents from `data/` directories
2. Split text into chunks
3. Create embeddings using `sentence-transformers/all-MiniLM-L6-v2`
4. Store in Chroma vector database at `./chroma_db`

## 💬 Query

Start the query interface:

```powershell
python main.py
```

Ask questions about your documents. The system will:
1. Retrieve relevant document chunks
2. Generate answers using `google/flan-t5-base` LLM
3. Show source documents for verification

**Commands**:
- Type your question naturally
- `help` - Show help information
- `quit` or `exit` - Exit the program

## 🛠️ Tech Stack

- **Framework**: LangChain
- **Vector Database**: Chroma
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **LLM**: google/flan-t5-base
- **Backend**: PyTorch
- **Document Loaders**: PyPDF, python-docx, python-pptx

## 📝 Example Usage

```powershell
# 1. Activate venv
.\venv\Scripts\Activate.ps1

# 2. Add your documents to data/ folders

# 3. Ingest documents
python ingest.py

# 4. Query the system
python main.py
```

## ⚠️ Important Notes

- The system answers **only** from ingested documents
- Re-run `ingest.py` after adding new documents
- First run downloads models automatically (~1GB total)
- Subsequent runs use cached models
