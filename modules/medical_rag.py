from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_DB_PATH = "vectorstores/medical_db"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

medical_db = FAISS.load_local(
    VECTOR_DB_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)


def retrieve_medical_context(query, k=3):
    docs = medical_db.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])