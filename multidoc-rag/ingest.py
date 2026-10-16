"""
Ingestion Script
One-time script to load, split, embed, and store documents in Chroma vector database
Following LangChain best practices
"""

import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from loader_main.loader_router import DocumentLoaderRouter


def ingest_documents():
    """
    Main ingestion pipeline following the required architecture:
    Documents → Loaders → Text Splitter → Embeddings → Vector Store
    """

    print("\n" + "=" * 60)
    print("MULTI-DOCUMENT RAG INGESTION PIPELINE")
    print("=" * 60 + "\n")

    # Step 1: Load documents
    print("STEP 1: Loading documents...")
    loader = DocumentLoaderRouter(base_data_path="data")
    documents = loader.load_all_documents()

    if not documents:
        print("\n❌ ERROR: No documents found to ingest!")
        print("Please add PDF, DOCX, or PPTX files to the data/ directories")
        return

    # Step 2: Split text into chunks
    print("\nSTEP 2: Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)
    print(f"  ✓ Created {len(chunks)} text chunks")

    # STEP 2.1: Add metadata doc_type
    for chunk in chunks:
        source = chunk.metadata.get("source", "")
        if source.endswith(".pdf"):
            chunk.metadata["doc_type"] = "pdf"
        elif source.endswith(".docx"):
            chunk.metadata["doc_type"] = "docx"
        elif source.endswith(".pptx"):
            chunk.metadata["doc_type"] = "pptx"
        else:
            chunk.metadata["doc_type"] = "unknown"

    # Step 3: Create embeddings
    print("\nSTEP 3: Initializing embedding model...")
    print("  Model: sentence-transformers/all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("  ✓ Embedding model loaded")

    # Step 4: Store in Chroma vector database
    print("\nSTEP 4: Creating Chroma vector database...")
    persist_directory = "./chroma_db"

    # Remove existing database if present
    if os.path.exists(persist_directory):
        print(f"  Removing existing database at {persist_directory}")
        import shutil
        shutil.rmtree(persist_directory)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    print(f"  ✓ Vector database created at: {persist_directory}")
    print(f"  ✓ Total vectors stored: {len(chunks)}")

    print("\n" + "=" * 60)
    print("✅ INGESTION COMPLETE!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  - Documents loaded: {len(documents)}")
    print(f"  - Text chunks created: {len(chunks)}")
    print(f"  - Database location: {persist_directory}")
    print(f"\nYou can now run 'python main.py' to query the documents!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    ingest_documents()
