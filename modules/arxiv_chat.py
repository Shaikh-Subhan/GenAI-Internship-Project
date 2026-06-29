import os
from dotenv import load_dotenv
from google import genai
from modules.arxiv_rag import retrieve_arxiv_context

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_arxiv_bot(query):
    query_lower = query.lower().strip()

    # Handle greetings / casual chat
    greetings = [
        "hi", "hello", "hey", "hii",
        "good morning", "good evening", "good afternoon"
    ]

    if query_lower in greetings:
        return """

    Hello! 👋 I am your Research Expert Assistant.

    I can help you with:
    • AI research papers
    • Paper summaries
    • Transformer / LLM concepts
    • Latest AI trends

    Try asking:

    * What is transformer architecture?
    * Explain self-attention
    * Recent trends in AI research
    """

    context = retrieve_arxiv_context(query)

    if context == "No relevant research papers found.":
        return """
        I couldn't find relevant research papers for your query.

        Try asking about:
        • Machine Learning
        • Deep Learning
        • NLP
        • Computer Vision
        • Transformers / LLMs
        """

    prompt = f"""

    You are an expert AI research assistant specializing in Computer Science papers.

    Rules:

    * Answer using the research papers provided.
    * Explain complex concepts in simple language.
    * If user asks for paper summary, summarize clearly.
    * If information is missing, say so honestly.
    * Support follow-up questions.

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
    except Exception as e:
        print(e)
        return "Research model is busy right now. Please try again."
