"""
QA Agent
Retrieval-Augmented Generation agent using modern LangChain (LCEL)
Answers questions based only on ingested documents
"""

import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import Chroma

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load environment variables
load_dotenv()


class QAAgent:
    """Question-Answering agent using retrieval from Chroma vector store"""

    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.retriever = None
        self.chain = None
        self._initialize_agent()

    def _initialize_agent(self):
        """Initialize retriever + LLM + LCEL chain"""

        print("\n" + "=" * 60)
        print("INITIALIZING QA AGENT")
        print("=" * 60 + "\n")

        # Check vector DB
        if not os.path.exists(self.persist_directory):
            raise FileNotFoundError(
                f"Vector database not found at {self.persist_directory}\n"
                "Please run 'python ingest.py' first."
            )

        # STEP 1: Embeddings
        print("STEP 1: Loading embeddings model...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        print("  ✓ Embeddings loaded")

        # STEP 2: Vector store
        print("\nSTEP 2: Loading Chroma vector database...")
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=embeddings,
        )
        print(f"  ✓ Database loaded from: {self.persist_directory}")

        # STEP 3: Retriever
        print("\nSTEP 3: Creating retriever...")
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4},
        )
        print("  ✓ Retriever configured (k=4)")

        # STEP 4: Local LLM
        print("\nSTEP 4: Initializing local LLM (flan-t5-base)...")

        model_id = "google/flan-t5-base"

        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

        hf_pipeline = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=512,
            temperature=0.7,
        )

        llm = HuggingFacePipeline(pipeline=hf_pipeline)

        print("  ✓ Local LLM initialized")

        # STEP 5: Prompt + LCEL Chain
        print("\nSTEP 5: Building LCEL RAG chain...")

        prompt = ChatPromptTemplate.from_template(
            """
You are a helpful AI assistant.
Answer the question using ONLY the provided context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""
        )

        self.chain = (
            {
                "context": RunnablePassthrough(),
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )

        print("  ✓ LCEL RAG chain ready")

        print("\n" + "=" * 60)
        print("✅ QA AGENT INITIALIZED")
        print("=" * 60 + "\n")

    def ask(self, question: str):
        """Ask a question and return answer + sources"""

        print("\n" + "=" * 60)
        print(f"QUESTION: {question}")
        print("=" * 60 + "\n")

        # Retrieve docs (k=4)
        docs = self.vectorstore.similarity_search(question, k=4)

        # Build context from retrieved docs
        context = "\n\n".join([doc.page_content for doc in docs])

        # Ask LLM using context
        answer = self.chain.invoke({
            "context": context,
            "question": question
        })

        return {
            "result": answer,
            "source_documents": docs,
        }

    def format_response(self, response: dict):
        """Format and display the response"""

        print("ANSWER:")
        print("-" * 60)
        print(response["result"])
        print("-" * 60)

        if response.get("source_documents"):
            print(f"\n📚 SOURCES ({len(response['source_documents'])} documents):")
            print("-" * 60)

            for i, doc in enumerate(response["source_documents"], 1):
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "N/A")

                print(f"\n[{i}] Source: {source}")
                if page != "N/A":
                    print(f"    Page: {page}")
                print(f"    Preview: {doc.page_content[:150]}...")

            print("-" * 60)


if __name__ == "__main__":
    agent = QAAgent()
    response = agent.ask("What is this document about?")
    agent.format_response(response)
