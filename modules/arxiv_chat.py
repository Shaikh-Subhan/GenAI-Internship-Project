import os
from dotenv import load_dotenv
from google import genai
from modules.arxiv_rag import retrieve_arxiv_context

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def ask_arxiv_bot(query):
    context = retrieve_arxiv_context(query)

    prompt = f"""
You are an expert AI research assistant specializing in Computer Science papers.

Rules:
- Answer using the research papers provided.
- Explain complex concepts in simple language.
- If user asks for paper summary, summarize clearly.
- If information is missing, say so honestly.
- Support follow-up questions.
- If context is irrelevant, say no relevant paper found.


RESEARCH PAPERS:
{context}

USER QUESTION:
{query}

ANSWER:
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except:
        return "Research model is busy right now. Please try again."