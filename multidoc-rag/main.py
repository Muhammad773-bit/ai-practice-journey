# main.py
"""
Main Query Script
CLI interface for querying the Multi-Document RAG system
"""

from agent.qa_agent import QAAgent


def main():
    """Main query loop"""
    
    print("\n" + "="*60)
    print("MULTI-DOCUMENT RAG QUERY INTERFACE")
    print("="*60)
    print("\nInitializing agent (this may take a moment)...\n")
    
    try:
        # Initialize QA agent
        agent = QAAgent()
        
        print("\n💡 Tips:")
        print("  - Ask questions about the content in your documents")
        print("  - Type 'quit' or 'exit' to stop")
        print("  - Type 'help' for more information")
        print("\n" + "="*60 + "\n")
        
        # Query loop
        while True:
            try:
                # Get user question
                question = input("\n❓ Your question: ").strip()
                
                # Handle special commands
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!\n")
                    break
                
                if question.lower() == 'help':
                    print("\n" + "="*60)
                    print("HELP")
                    print("="*60)
                    print("\nThis RAG system answers questions based ONLY on the")
                    print("documents you've ingested (PDF, DOCX, PPTX files).")
                    print("\nHow it works:")
                    print("  1. Your question is converted to an embedding")
                    print("  2. The system finds relevant document chunks")
                    print("  3. An LLM generates an answer from those chunks")
                    print("\nCommands:")
                    print("  - Type your question naturally")
                    print("  - 'quit' or 'exit' - Exit the program")
                    print("  - 'help' - Show this help message")
                    print("="*60)
                    continue
                
                if not question:
                    print("⚠️  Please enter a question")
                    continue
                
                # Get answer from agent
                response = agent.ask(question)
                
                # Display formatted response
                agent.format_response(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error processing question: {e}\n")
    
    except FileNotFoundError as e:
        print("\n" + "="*60)
        print("❌ ERROR: Vector Database Not Found")
        print("="*60)
        print(f"\n{e}")
        print("\nPlease follow these steps:")
        print("  1. Add documents to data/pdfs/, data/docs/, or data/ppts/")
        print("  2. Run: python ingest.py")
        print("  3. Then run: python main.py")
        print("="*60 + "\n")
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
