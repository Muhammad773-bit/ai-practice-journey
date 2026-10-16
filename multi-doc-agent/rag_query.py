import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load embeddings and vector store (from previous indexing)
embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-large-instruct")
vectorstore = Chroma(
    collection_name="multi_doc_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# Retriever setup (top 5 relevant chunks)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Groq LLM (use a strong model like llama3-70b)
llm = ChatGroq(model="llama3-70b-8192")  # Or "mixtral-8x7b-32768" for variety

# Prompt template for RAG
template = """You are a helpful assistant. Use the following context to answer the question:

Context: {context}

Question: {question}

Answer:"""
prompt = PromptTemplate.from_template(template)

# RAG chain: retrieve -> format -> generate
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Example usage
query = "What is the summary of the key points in all documents?"
response = rag_chain.invoke(query)
print(response)