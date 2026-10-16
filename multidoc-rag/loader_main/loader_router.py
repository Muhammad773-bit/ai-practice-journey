# loader_main/loader_router.py
"""
Document Loader Router
Loads PDF, DOCX, and PPTX documents from data directories
Following LangChain best practices
"""

import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader
)


class DocumentLoaderRouter:
    """Routes and loads documents based on file type"""
    
    def __init__(self, base_data_path: str = "data"):
        self.base_data_path = base_data_path
        self.pdf_path = os.path.join(base_data_path, "pdfs")
        self.docx_path = os.path.join(base_data_path, "docs")
        self.pptx_path = os.path.join(base_data_path, "ppts")
    
    def load_pdfs(self) -> List[Document]:
        """Load all PDF documents"""
        documents = []
        if not os.path.exists(self.pdf_path):
            print(f"Warning: {self.pdf_path} does not exist")
            return documents
        
        pdf_files = [f for f in os.listdir(self.pdf_path) if f.endswith('.pdf')]
        print(f"Loading {len(pdf_files)} PDF files...")
        
        for pdf_file in pdf_files:
            file_path = os.path.join(self.pdf_path, pdf_file)
            try:
                loader = PyPDFLoader(file_path)
                docs = loader.load()
                documents.extend(docs)
                print(f"  ✓ Loaded: {pdf_file} ({len(docs)} pages)")
            except Exception as e:
                print(f"  ✗ Error loading {pdf_file}: {e}")
        
        return documents
    
    def load_docx(self) -> List[Document]:
        """Load all DOCX documents"""
        documents = []
        if not os.path.exists(self.docx_path):
            print(f"Warning: {self.docx_path} does not exist")
            return documents
        
        docx_files = [f for f in os.listdir(self.docx_path) if f.endswith('.docx')]
        print(f"Loading {len(docx_files)} DOCX files...")
        
        for docx_file in docx_files:
            file_path = os.path.join(self.docx_path, docx_file)
            try:
                loader = Docx2txtLoader(file_path)
                docs = loader.load()
                documents.extend(docs)
                print(f"  ✓ Loaded: {docx_file}")
            except Exception as e:
                print(f"  ✗ Error loading {docx_file}: {e}")
        
        return documents
    
    def load_pptx(self) -> List[Document]:
        """Load all PPTX documents"""
        documents = []
        if not os.path.exists(self.pptx_path):
            print(f"Warning: {self.pptx_path} does not exist")
            return documents
        
        pptx_files = [f for f in os.listdir(self.pptx_path) if f.endswith('.pptx')]
        print(f"Loading {len(pptx_files)} PPTX files...")
        
        for pptx_file in pptx_files:
            file_path = os.path.join(self.pptx_path, pptx_file)
            try:
                loader = UnstructuredPowerPointLoader(file_path)
                docs = loader.load()
                documents.extend(docs)
                print(f"  ✓ Loaded: {pptx_file}")
            except Exception as e:
                print(f"  ✗ Error loading {pptx_file}: {e}")
        
        return documents
    
    def load_all_documents(self) -> List[Document]:
        """Load all documents from all supported formats"""
        print("\n" + "="*60)
        print("LOADING DOCUMENTS")
        print("="*60 + "\n")
        
        all_documents = []
        
        # Load all document types
        all_documents.extend(self.load_pdfs())
        all_documents.extend(self.load_docx())
        all_documents.extend(self.load_pptx())
        
        print(f"\n{'='*60}")
        print(f"TOTAL DOCUMENTS LOADED: {len(all_documents)}")
        print(f"{'='*60}\n")
        
        return all_documents


if __name__ == "__main__":
    # Test the loader
    loader = DocumentLoaderRouter()
    docs = loader.load_all_documents()
    
    if docs:
        print(f"\nSample document preview:")
        print(f"Content: {docs[0].page_content[:200]}...")
        print(f"Metadata: {docs[0].metadata}")
