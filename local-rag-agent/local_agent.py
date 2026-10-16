import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding   # optional

# No need for OpenAI key anymore
# load_dotenv()   # you can remove this if you want

# Load documents from 'data' folder
documents = SimpleDirectoryReader("data").load_data()

# Create index
# Optional: use Ollama embeddings too (better coherence, still free)
embed_model = OllamaEmbedding(model_name="llama3.2:3b")   # or "nomic-embed-text" if you pull it
index = VectorStoreIndex.from_documents(
    documents,
    embed_model=embed_model,   # remove this line if you want to keep default (HuggingFace)
)

# Query engine tool
query_engine_tool = QueryEngineTool(
    query_engine=index.as_query_engine(),
    metadata=ToolMetadata(
        name="llama_index_docs",
        description="Useful for answering questions about LlamaIndex documentation from multiple files."
    )
)

# Use local Ollama LLM
llm = Ollama(
    model="llama3.2:3b",          # ← change to whichever model you pulled
    request_timeout=120.0,        # seconds – increase if model is slow
    temperature=0.1,              # low = more deterministic answers
)

# Create ReAct agent
agent = ReActAgent.from_tools(
    [query_engine_tool],
    llm=llm,
    verbose=True
)

# Simple query loop
while True:
    query = input("\nAsk about LlamaIndex documentation (or 'exit'): ")
    if query.lower() in ['exit', 'quit', 'q']:
        break
    response = agent.chat(query)
    print("\nAnswer:", response, "\n")