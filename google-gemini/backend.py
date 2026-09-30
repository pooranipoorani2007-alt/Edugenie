from google.genai import errors
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


# Gemini client
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")

client = genai.Client(
    api_key=api_key
)


# FastAPI application
app = FastAPI(
    title="EduGenie AI Educational Assistant"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Models
# -----------------------------

class AskRequest(BaseModel):
    question: str


class QuizRequest(BaseModel):
    topic: str


class PathRequest(BaseModel):
    topic: str


# -----------------------------
# Gemini Helper
# -----------------------------

def generate_gemini_response(
    prompt: str,
    max_output_tokens: int = 1000
) -> str:

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=max_output_tokens
            )
        )

        return response.text

    except errors.ClientError as e:

        if e.code == 429:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota has been exceeded. Please try again later."
            )

        raise HTTPException(
            status_code=500,
            detail=f"Gemini API error: {e}"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {e}"
        )


# -----------------------------
# Gemini AI - Question Answer
# -----------------------------

def answer_question(question: str) -> str:

    prompt = f"""
You are EduGenie, an AI educational assistant.

Help the student understand the following question.

Rules:
- Explain in simple language.
- Give examples when useful.
- Break difficult concepts into steps.
- Keep the answer educational and easy to understand.
- If appropriate, use headings and bullet points.

Student question:
{question}
"""

    return generate_gemini_response(
        prompt,
        max_output_tokens=1500
    )


# -----------------------------
# Gemini AI - Quiz
# -----------------------------

def generate_quiz(topic: str) -> str:

    prompt = f"""
You are EduGenie, an AI educational assistant.

Create a quiz for a student learning:

{topic}

Create exactly 5 questions.

For each question provide:

1. Question
2. Four multiple-choice options
3. Correct answer
4. Short explanation

Keep the questions educational and suitable for beginners.

Use this format:

### Question 1
Question: ...

A. ...
B. ...
C. ...
D. ...

Answer: ...
Explanation: ...

Repeat this format for all 5 questions.
"""

    return generate_gemini_response(
        prompt,
        max_output_tokens=2000
    )


# -----------------------------
# Gemini AI - Learning Path
# -----------------------------

def learning_path(topic: str) -> str:

    prompt = f"""
You are EduGenie, an AI educational assistant.

Create a personalized 4-week learning path for a student
who wants to learn:

{topic}

Structure the learning path into:

Week 1 - Beginner
Week 2 - Beginner / Intermediate
Week 3 - Intermediate
Week 4 - Advanced

For every week provide:

- Topics to learn
- What the student should practice
- A small project or exercise

Keep the plan practical and easy to follow.

Use headings and bullet points.
"""

    return generate_gemini_response(
        prompt,
        max_output_tokens=2000
    )


# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def home():

    return {
        "message": "EduGenie is running"
    }


@app.post("/ask")
def ask(request: AskRequest):

    answer = answer_question(
        request.question
    )

    return {
        "question": request.question,
        "answer": answer
    }


@app.post("/quiz")
def quiz(request: QuizRequest):

    quiz_result = generate_quiz(
        request.topic
    )

    return {
        "topic": request.topic,
        "quiz": quiz_result
    }


@app.post("/learning-path")
def path(request: PathRequest):

    learning_result = learning_path(
        request.topic
    )

    return {
        "topic": request.topic,
        "learning_path": learning_result
    }