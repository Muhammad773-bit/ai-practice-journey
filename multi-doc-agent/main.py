import os
# import os
# import uuid
# from typing import List

# # ────────────────────────────────────────────────
# # NEW IMPORTS for CORS
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# # ────────────────────────────────────────────────

# from pydantic import BaseModel
# from groq import Groq
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np
# from docx import Document
# import PyPDF2
# from pptx import Presentation

# # Environment setup
# os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
# groq_client = Groq()
# embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# CHUNK_SIZE = 500
# VECTOR_DIM = 384

# # In-memory storage (for simplicity; use persistent in prod)
# documents = {}  # {doc_id: {"chunks": [text_chunks], "embeddings": np.array}}
# index = faiss.IndexFlatL2(VECTOR_DIM)

# app = FastAPI(title="Multi-Document Retrieval Agent")

# # ────────────────────────────────────────────────
# # ADD CORS MIDDLEWARE HERE (very important for browser requests)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],                    # ← For development: allow all origins
#     allow_credentials=True,
#     allow_methods=["*"],                    # GET, POST, OPTIONS, etc.
#     allow_headers=["*"],                    # Content-Type, Authorization, etc.
# )
# # ────────────────────────────────────────────────

# class QueryRequest(BaseModel):
#     query: str
#     doc_ids: List[str]

# def parse_document(file: UploadFile) -> List[str]:
#     filename = file.filename.lower()
#     content = file.file.read()
#     chunks = []
    
#     if filename.endswith('.docx'):
#         doc = Document(content)
#         text = '\n'.join([para.text for para in doc.paragraphs])
#     elif filename.endswith('.pdf'):
#         pdf_reader = PyPDF2.PdfReader(content)
#         text = ''.join([page.extract_text() or "" for page in pdf_reader.pages])
#     elif filename.endswith('.pptx'):
#         prs = Presentation(content)
#         text = '\n'.join([shape.text for slide in prs.slides for shape in slide.shapes if hasattr(shape, 'text')])
#     else:
#         raise ValueError("Unsupported file type")
    
#     for i in range(0, len(text), CHUNK_SIZE):
#         chunks.append(text[i:i + CHUNK_SIZE])
#     return chunks

# @app.post("/upload")
# async def upload_document(file: UploadFile = File(...)):
#     try:
#         chunks = parse_document(file)
#         if not chunks:
#             raise ValueError("No content extracted from document")
        
#         embeddings = embedding_model.encode(chunks)
#         embeddings_np = np.array(embeddings).astype('float32')
        
#         doc_id = str(uuid.uuid4())
#         documents[doc_id] = {"chunks": chunks, "embeddings": embeddings_np}
        
#         # Simple ID mapping (improve later with proper metadata/index)
#         ids = np.array([int(doc_id, 16) % (2**64) for _ in chunks])
#         index.add_with_ids(embeddings_np, ids)
        
#         return JSONResponse({"doc_id": doc_id, "message": "Document processed successfully"})
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.post("/query")
# async def query_documents(request: QueryRequest):
#     if not request.doc_ids:
#         raise HTTPException(status_code=400, detail="At least one doc_id required")
    
#     query_embedding = embedding_model.encode([request.query])[0].astype('float32').reshape(1, -1)
    
#     k = 5
#     distances, indices = index.search(query_embedding, k)
    
#     retrieved_chunks = []
#     for idx in indices[0]:
#         if idx == -1: continue
#         for doc_id, data in documents.items():
#             if idx < len(data["chunks"]):
#                 retrieved_chunks.append(data["chunks"][idx])
#                 break
    
#     if not retrieved_chunks:
#         return JSONResponse({"answer": "No relevant information found in the documents."})
    
#     context = "\n\n".join(retrieved_chunks)
#     prompt = f"Answer the query based only on the following context. Be precise and factual:\n\nContext: {context}\n\nQuery: {request.query}"
    
#     completion = groq_client.chat.completions.create(
#         messages=[{"role": "user", "content": prompt}],
#         model="llama3-70b-8192",
#         temperature=0.1,
#         max_tokens=500
#     )
    
#     answer = completion.choices[0].message.content.strip()
#     return JSONResponse({"answer": answer, "retrieved_chunks": retrieved_chunks})

# # Tip: run with → uvicorn main:app --reload