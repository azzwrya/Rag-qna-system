from google import genai
from dotenv import load_dotenv
import os

# Recommended: use environment variable
# setx GOOGLE_API_KEY "YOUR_API_KEY"   (Windows)
# export GOOGLE_API_KEY="YOUR_API_KEY" (Linux/Mac)

load_dotenv()

# 3️⃣ Create Gemini client
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
)

def generate_answer(question: str, context_chunks: list[str]):
    context_text = "\n\n".join(context_chunks)

    prompt = f"""
You are a helpful assistant. Answer the question using ONLY the provided context.
If the answer isn't in the context, say "I don't have enough information in the uploaded documents."

CONTEXT:
{context_text}

QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
