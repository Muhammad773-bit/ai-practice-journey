import os
import re
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

def create_vector_store(pdf_path):
    
    #load the pdf
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    # split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    
    # create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    #create the vector store
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store

# ASK QUESTION

def ask_question(vector_store, question, hf_token):
    repo_id = "HuggingFaceH4/zephyr-7b-beta"
    llm = HuggingFaceEndpoint (
        repo_id = repo_id
        task="conversattional",
        max_new_tokens=512,
        huggingfacehub_api_token=hf_token,
    )
    chatmodel = ChatHuggingFace(llm=llm)
    
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Keep the answer concise and professional.

    {context}

    Question: {question}
    Helpful Answer:"""
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    
    qa_chain = RetrievalQA.from_chain_type(
        chatmodel,
        retriever=vector_store.as_retriever(),
        chain_type_kwargs={"prompts": QA_CHAIN_PROMPT}
    )
    
    response = qa_chain.invoke({"query":question})
    return response["result"]


if__name__ == "__main__":
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    
    if not hf_token:
        raise ValueError("Please set HUGGINGFACEHUB_API_TOKEN in .env file")
    
    pdf_path = 'your_pdf_file.pdf'
    vector_store = create_vector_store(pdf_path)
    
    question = "What is the main topic of this document?"
    answer = ask_question(vector_store, question, hf_token)
    print("answer" , answer)