import os
import sys
import time
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

# ---------------------------
# Typing effect functions (for CLI)
# ---------------------------
def typing_effect(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def smart_typing(answer, user_message):
    emotional_keywords = [
        "stress", "anxious", "sad", "happy", "lonely",
        "depressed", "angry", "upset", "overwhelmed", "stressed"
    ]
    if any(word in user_message.lower() for word in emotional_keywords):
        typing_effect(answer, delay=0.06)
    else:
        typing_effect(answer, delay=0.02)

# ---------------------------
# Load or create vector database
# ---------------------------
def load_or_create_vectorstore(data_folder="data", vectorstore_folder="vectorstore"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    if os.path.exists(vectorstore_folder):
        print("✅ Loading existing vector database...")
        vectorstore = FAISS.load_local(vectorstore_folder, embeddings, allow_dangerous_deserialization=True)
    else:
        print("📂 Vectorstore not found. Creating new vector database from PDFs...")
        docs = []
        for filename in os.listdir(data_folder):
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(os.path.join(data_folder, filename))
                docs.extend(loader.load())
        if not docs:
            raise FileNotFoundError(f"No PDF files found in '{data_folder}' folder.")
        
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local(vectorstore_folder)
        print(f"✅ Vectorstore created and saved in '{vectorstore_folder}' folder")
    
    return vectorstore

# ---------------------------
# Build QA chain
# ---------------------------
def build_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
    )

    template = """
    You are Lumi 🌸, a warm, friendly, and supportive mental health companion.
    Speak like a caring friend who listens with empathy, not like a doctor.
    Use gentle encouragement, kind words, and emojis (🌿, 😊, 💙, 🌻).
    Share simple, practical tips. Keep answers positive and reassuring.
    If someone feels down, remind them they’re not alone 💖.

    Context: {context}
    Question: {question}
    Chat history: {chat_history}

    Answer as Lumi 🌸:
    """

    prompt = PromptTemplate(input_variables=["context", "question", "chat_history"], template=template)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        combine_docs_chain_kwargs={
            "prompt": prompt,
            "document_variable_name": "context"
        }
    )
    return qa_chain

# ---------------------------
# Helper for Streamlit UI
# ---------------------------
def get_answer(query: str, chat_history=[]):
    """Fetch Lumi’s friendly answer for UI or API use"""
    vectorstore = load_or_create_vectorstore()
    qa_chain = build_qa_chain(vectorstore)

    result = qa_chain.invoke({"question": query, "chat_history": chat_history})
    answer = result["answer"]

    # Extract sources if available
    sources = result.get("source_documents", [])
    unique_sources = {os.path.basename(doc.metadata.get("source", "")) for doc in sources if "source" in doc.metadata}

    return f"{answer}\n\n📖 Based on: {', '.join(unique_sources)}" if unique_sources else answer

# ---------------------------
# Main loop (CLI mode)
# ---------------------------
def main():
    chatbot_name = "Lumi 🌸"
    print(f"🤖 Hi! I’m {chatbot_name}, your friendly companion. I’m here for you 💙")

    vectorstore = load_or_create_vectorstore()
    qa_chain = build_qa_chain(vectorstore)
    chat_history = []

    while True:
        query = input("\n💬 You: ")
        if query.lower() == "exit":
            typing_effect("👋 Bye! Remember, you’re stronger than you think 🌸 Take care!")
            break

        result = qa_chain.invoke({"question": query, "chat_history": chat_history})
        answer = result["answer"]

        smart_typing(f"{chatbot_name}: {answer}", query)

        sources = result.get("source_documents", [])
        unique_sources = {os.path.basename(doc.metadata.get("source", "")) for doc in sources if "source" in doc.metadata}
        if unique_sources:
            print(f"\n📖 (Info based on: {', '.join(unique_sources)})")

        chat_history.append((query, answer))

if __name__ == "__main__":
    main()
