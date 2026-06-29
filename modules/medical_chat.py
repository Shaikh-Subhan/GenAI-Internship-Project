import os
from dotenv import load_dotenv
from google import genai
from modules.medical_rag import retrieve_medical_context

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def ask_medical_bot(query):
    q = query.lower().strip()

    # Handle casual conversation
    greetings = ["hi", "hello", "hey"]
    identity = ["who are you", "what are you"]
    thanks = ["thanks", "thank you"]

    if q in greetings:
        return """
Hello! I'm your AI Medical Assistant 👨‍⚕️

You can ask me about:
• Symptoms of diseases
• Causes
• Treatments
• Medications

Example:
What are symptoms of diabetes?
"""

    if q in identity:
        return """
I am an AI Medical Assistant 👨‍⚕️

I answer health-related questions using a medical knowledge base.

Please note:
• Educational information only  
• Not a replacement for doctors  
• Always consult a healthcare professional for diagnosis
"""

    if q in thanks:
        return "You're welcome! Stay healthy 😊"

    # Retrieve medical knowledge
    context = retrieve_medical_context(query)

    if not context.strip():
        return """
I couldn't find relevant medical information for your question.

Please ask about a disease, symptom, medication, or treatment.
"""

    prompt = f"""
You are a medical assistant.

Rules:
- Answer ONLY from medical knowledge provided.
- Do not invent medical facts.
- Mention that user should consult a doctor for diagnosis.
- This is educational, not medical advice.

MEDICAL KNOWLEDGE:
{context}

QUESTION:
{query}

ANSWER:
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        print(e)

        if "503" in str(e) or "UNAVAILABLE" in str(e):
            return """
⚠️ Medical AI service is busy right now.

Please try again in 30–60 seconds.
"""

        return """
⚠️ Something went wrong while processing your request.

Please try again.
"""