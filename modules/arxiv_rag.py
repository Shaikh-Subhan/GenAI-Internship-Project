import json
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

ARXIV_FILE = "datasets/arxiv/arxiv-metadata-oai-snapshot.jsonl"
VECTOR_DB_PATH = "vectorstores/arxiv_db"

# Better embedding model for research paper retrieval
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)


def load_arxiv_documents():
    documents = []

    with open(ARXIV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                paper = json.loads(line)

                title = paper.get("title", "")
                abstract = paper.get("abstract", "")
                category = paper.get("categories", "")

                content = f"""
Title: {title}

Category: {category}

Abstract:
{abstract}
"""

                documents.append(
                    Document(
                        page_content=content,
                        metadata={"title": title}
                    )
                )

            except Exception as e:
                print("Error reading paper:", e)

    return documents


def create_arxiv_vector_db():
    docs = load_arxiv_documents()

    vector_db = FAISS.from_documents(
        docs,
        embedding_model
    )

    vector_db.save_local(VECTOR_DB_PATH)
    print(f"Saved {len(docs)} papers.")


def retrieve_arxiv_context(query):
    db = FAISS.load_local(
        VECTOR_DB_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    # Query expansion for better retrieval
    query_lower = query.lower()

    if "transformer" in query_lower:
        query += " self attention neural network deep learning attention mechanism"
    elif "llm" in query_lower:
        query += " large language model transformer generative AI"
    elif "cnn" in query_lower:
        query += " convolutional neural network computer vision image classification"
    elif "attention" in query_lower:
        query += " deep learning transformer sequence modeling"
    elif "bert" in query_lower:
        query += " bidirectional encoder representations transformer NLP"
    elif "gpt" in query_lower:
        query += " generative pretrained transformer autoregressive language model"

    # Similarity search with score
    results = db.similarity_search_with_score(query, k=8)

    filtered_docs = []

    for doc, score in results:
        print("Score:", score, "|", doc.metadata)

        # Lower score means better similarity
        if score < 1.2:
            filtered_docs.append(doc)

    if not filtered_docs:
        return "No relevant research papers found."

    context = "\n\n".join(
        doc.page_content for doc in filtered_docs[:5]
    )

    return context