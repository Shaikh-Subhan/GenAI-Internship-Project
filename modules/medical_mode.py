import os
import xml.etree.ElementTree as ET
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

MEDQUAD_PATH = "datasets/medquad"
VECTOR_DB_PATH = "vectorstores/medical_db"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def load_medquad_data():
    documents = []

    print("Scanning MedQuAD dataset...")

    for root, dirs, files in os.walk(MEDQUAD_PATH):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)

                try:
                    tree = ET.parse(file_path)
                    root_xml = tree.getroot()

                    focus = root_xml.find("Focus")
                    disease_name = (
                        focus.text.strip()
                        if focus is not None and focus.text
                        else "Unknown"
                    )

                    qa_pairs = root_xml.find("QAPairs")

                    if qa_pairs is not None:
                        for qa in qa_pairs.findall("QAPair"):
                            question = qa.find("Question")
                            answer = qa.find("Answer")

                            if (
                                question is not None
                                and answer is not None
                                and question.text
                                and answer.text
                            ):
                                content = f"""
                                    Disease: {disease_name}

                                    Question: {question.text.strip()}

                                    Answer: {answer.text.strip()}
                                    """

                                documents.append(
                                    Document(
                                        page_content=content,
                                        metadata={"source": file}
                                    )
                                )

                                # Show progress every 1000 docs
                                if len(documents) % 1000 == 0:
                                    print(f"Processed {len(documents)} documents...")

                except Exception as e:
                    print(f"Error parsing {file}: {e}")

    return documents


def create_medical_vector_db():
    docs = load_medquad_data()

    print(f"\nTotal parsed docs: {len(docs)}")
    print("Creating embeddings... This may take a long time.\n")

    vector_db = FAISS.from_documents(
        docs,
        embedding_model
    )

    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    vector_db.save_local(VECTOR_DB_PATH)

    print(f"\nSaved {len(docs)} medical documents to {VECTOR_DB_PATH}")


if __name__ == "__main__":
    create_medical_vector_db()