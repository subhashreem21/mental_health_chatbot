# backend.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import load_or_create_vectorstore, build_qa_chain

app = FastAPI(title="Lumi 🌸 Chatbot API")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

vectorstore = load_or_create_vectorstore()
qa_chain = build_qa_chain(vectorstore)
chat_history = []

class Query(BaseModel):
    message: str

@app.post("/chat")
def chat(query: Query):
    global chat_history
    result = qa_chain.invoke({"question": query.message, "chat_history": chat_history})
    answer = result["answer"]
    chat_history.append((query.message, answer))
    return {"answer": answer}
