import os
import time
from dotenv import load_dotenv
from google import genai
from modules.rag import retrieve_context
from modules.sentiment import detect_sentiment
from modules.multilingual import (
    detect_language,
    translate_to_english,
    translate_from_english
)

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """
You are an AI Customer Service Assistant.

General Rules:
- Never invent company policies or information.
- Be polite, helpful, and professional.
- If image analysis is provided, use it as evidence.
- Combine visual evidence with user question.
- Reason carefully before answering.
"""

def needs_knowledge_lookup(query):
    keywords = [
        "what", "how", "when", "where",
        "refund", "return", "policy",
        "shipping", "delivery", "order",
        "track", "payment", "cancel"
    ]

    query_lower = query.lower()
    return any(word in query_lower for word in keywords)


def ask_gemini(query, original_query=None, force_no_rag=False):
    # ---------- MULTILINGUAL PROCESSING ----------
    original_lang = detect_language(query)
    english_query = translate_to_english(query, original_lang)

    # ---------- RAG DECISION ----------
    if force_no_rag:
        use_rag = False
    else:
        use_rag = needs_knowledge_lookup(english_query)

    # ---------- SENTIMENT ----------
    sentiment_input = original_query if original_query else english_query
    sentiment, score = detect_sentiment(sentiment_input)

    if use_rag:
        sentiment = "NEUTRAL"
    elif score < 0.75:
        sentiment = "NEUTRAL"

    # ---------- KNOWLEDGE RETRIEVAL ----------
    if use_rag:
        context = retrieve_context(english_query)

        knowledge_prompt = f"""
KNOWLEDGE BASE:
{context}

Answer ONLY using the knowledge base.
If answer is not found, say:
'I don't know based on current company knowledge.'
"""
    else:
        knowledge_prompt = """
This is a conversational message.
Respond naturally without using knowledge base.
"""

    # ---------- FINAL PROMPT ----------
    prompt = f"""
{SYSTEM_PROMPT}

CUSTOMER SENTIMENT:
{sentiment}
Confidence: {score:.2f}

Response Behavior:
- NEGATIVE → Be empathetic, apologetic, calm
- POSITIVE → Be warm and appreciative
- NEUTRAL → Be professional and direct

{knowledge_prompt}

CUSTOMER MESSAGE:
{english_query}

ANSWER:
"""

    models = ["gemini-2.5-flash", "gemini-2.0-flash"]

    for model_name in models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            final_answer = translate_from_english(
                response.text,
                original_lang
            )

            return final_answer, sentiment

        except Exception as e:
            print(f"{model_name} failed: {e}")
            time.sleep(3)

    fallback = "Model is busy right now. Please try again in a minute."
    fallback = translate_from_english(fallback, original_lang)

    return fallback, sentiment