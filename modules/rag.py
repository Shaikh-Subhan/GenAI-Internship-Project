import pandas as pd
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

CSV_PATH = "datasets/custom_docs/dataset.csv"
CHROMA_PATH = "vector_store"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_vector_db():
    df = pd.read_csv(CSV_PATH, encoding="cp1252")

    documents = []

    for _, row in df.iterrows():
        question = str(row["prompt"])
        answer = str(row["response"])

        content = f"""
        Customer Question: {question}
        Support Answer: {answer}
        """

        doc = Document(
            page_content=content,
            metadata={"question": question}
        )

        documents.append(doc)

    db = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=CHROMA_PATH
    )

    db.persist()
    return db


def load_vector_db():
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model
    )
    return db


def retrieve_context(query, k=3):
    db = load_vector_db()
    docs = db.similarity_search(query, k=k)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context