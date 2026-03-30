
import time
from groq import Groq
from app.retrieval import search, rerank
from app.memory import get_memory, add_message
import os
from dotenv import load_dotenv
from app.guardrails import (
    validate_input,
    detect_prompt_injection,
    contains_pii,
    grounded_answer
)
from app.evaluator import judge_answer

load_dotenv() 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt_with_memory(question, context_chunks, previous_messages):
    
    # Building prompt including previous conversation context
    
    context_text = ""
    for i, chunk in enumerate(context_chunks):
        context_text += f"\n[DOC {i+1}]\n{chunk}\n"

    memory_text = ""
    for msg in previous_messages:
        memory_text += f"{msg['role'].capitalize()}: {msg['content']}\n"

    prompt = f"""
You are an assistant for a company GammaEdge Technologies .
and you are design by Mukul Nagar Associate software trainee.

Answer ONLY using the provided documents.

If the answer is not in the documents, say:
"I could not find this information in the provided documents."

Include citations using [DOC number].

Conversation so far:
{memory_text}

Documents:
{context_text}

New Question:
{question}

Answer:
"""
    return prompt


def generate_answer_with_memory(session_id, question):
# It will generate answer with memory
    valid, message = validate_input(question)
    if not valid:
        yield message
        return 
    #Check for prompt injection 
    if detect_prompt_injection(question):
        yield "Trying to injecting prompt "
        return
    #Check for any PII
    if contains_pii(question):
        yield "Prompt contain sensitive information."
        return


    previous_messages = get_memory(session_id)

    chunks1 = search(question, top_k=5)
    # Applying re-ranker to re analyze the generate result 
    chunks = rerank(question, chunks1)


    prompt = build_prompt_with_memory(question, chunks, previous_messages)

      
    full_answer = ""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        stream=True  #sse streaming allow
    )

    for chunk in completion:
       
        content = chunk.choices[0].delta.content
        if content:
            time.sleep(0.05)
            full_answer += content
            yield content
   
    # Check for answer is grounding or not 
    if not grounded_answer(full_answer):
        yield "\n\nWarning: answer may not be grounded in documents."
    

    evaluation = judge_answer(
        question,
        full_answer,
        chunks
    )
    print("Evaluation :--", evaluation)

    add_message(session_id, "user", question)
    add_message(session_id, "assistant", full_answer)