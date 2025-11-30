from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Load API KEY from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str
    selected_text: str = ""

@app.post("/query")
def answer_question(q: Query):
    prompt = f"""
You are a helpful AI tutor.
The user selected this chapter text:

{q.selected_text}

The user question is:
{q.text}

Give a clear short answer.
"""
    try:
        # Use a compatible Gemini model
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        if response and hasattr(response, 'text'):
            answer = response.text
        else:
            answer = "Sorry, I couldn't generate a response."
    except Exception as e:
        answer = f"An error occurred: {str(e)}"

    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


