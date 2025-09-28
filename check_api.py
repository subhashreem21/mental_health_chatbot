import os

api_key = os.getenv("GROQ_API_KEY")

if api_key:
    print("✅ Groq API key is set!")
    print("API Key (partial):", api_key[:5] + "..." + api_key[-5:])
else:
    print("❌ Groq API key not found.")
