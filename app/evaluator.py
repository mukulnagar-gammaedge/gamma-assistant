from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv() 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def judge_answer(question, answer, context):
    context_text = "\n".join(context)

   
    prompt = f"""
    You are evaluating an AI answer.

    Question:
    {question}

    Answer:
    {answer}

    Documents:
    {context_text}

    Evaluate:
    1. Is answer supported by documents?
    2. Is answer relevant?
    3. Any hallucination?

    Return JSON:
    {{
        "grounded": true/false,
        "relevant": true/false,
        "hallucination": true/false
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
