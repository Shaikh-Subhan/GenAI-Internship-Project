from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vectorstores/medical_db",
    embedding_model,
    allow_dangerous_deserialization=True
)

query = "What are symptoms of leukemia?"

docs = db.similarity_search(query, k=2)

for i, doc in enumerate(docs, 1):
    print(f"\n--- Result {i} ---")
    print(doc.page_content[:1000])