import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader

# Set your Groq API key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Embedding model (free, open-source, top-performing for retrieval)
embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large-instruct",
    model_kwargs={"device": "cpu"}  # change to "cuda" if you have NVIDIA GPU
)
# Vector store setup (persistent in ./chroma_db)
vector_store_dir = "./chroma_db"
vectorstore = Chroma(
    collection_name="multi_doc_collection",
    embedding_function=embeddings,
    persist_directory=vector_store_dir
)

# Function to load documents based on file type
def load_document(file_path):
    if file_path.endswith(".pdf"):
        return PyPDFLoader(file_path).load()
    elif file_path.endswith(".docx"):
        return Docx2txtLoader(file_path).load()
    elif file_path.endswith(".pptx") or file_path.endswith(".ppt"):
        return UnstructuredPowerPointLoader(file_path).load()
    else:
        print(f"Skipping unsupported file: {file_path}")
        return []

# Scan data folder and load all supported files
data_folder = "data"
documents = []
for root, _, files in os.walk(data_folder):
    for file in files:
        file_path = os.path.join(root, file)
        docs = load_document(file_path)
        documents.extend(docs)

# Split documents into chunks (optimal for retrieval: 1000 chars, 200 overlap)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = text_splitter.split_documents(documents)

# Add to vector store (embed and index)
vectorstore.add_documents(split_docs)
print(f"Indexed {len(split_docs)} chunks from {len(documents)} documents.")
