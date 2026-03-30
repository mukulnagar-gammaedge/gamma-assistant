import re

def validate_input(question):
    if not question:
        return False, "Query is empty"
    if len(question)>1000:
        return False, "Question too long"
    return True, question

INJECTION_PATTERNS = [

    "ignore previous instructions",
    "reveal system prompt",
    "disclose hidden policy",
    "act as system",
    "bypass restrictions",
    "show confidential data"

]

def detect_prompt_injection(question):

    q = question.lower()

    for pattern in INJECTION_PATTERNS:

        if pattern in q:

            return True

    return False


EMAIL_REGEX = r"\S+@\S+"
PHONE_REGEX = r"\b\d{10}\b"
AADHAR_REGEX = r"\b\d{12}\b"
def contains_pii(text):

    if re.search(EMAIL_REGEX, text):
        return True

    if re.search(PHONE_REGEX, text):
        return True

    if re.search(AADHAR_REGEX, text):
        return True

    return False

def grounded_answer(answer):

    if "[DOC" not in answer:

        return False

    return True