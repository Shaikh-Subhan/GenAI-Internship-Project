# 🤖 Multi-Mode AI Assistant

### Internship Project — ElevanceSkills

**Developed by:** Subhan Shaikh

---

## 📌 Problem Statement

Traditional chatbots usually handle only simple text queries and struggle with:

* Dynamic knowledge updates
* Multi-modal inputs (text + images)
* Medical Q&A
* Emotional understanding
* Multilingual conversations
* Research-level question answering

This project extends a basic AI Customer Service chatbot into a **Multi-Mode AI Assistant** capable of handling customer support, medical Q&A, and scientific research queries using Retrieval-Augmented Generation (RAG), multimodal reasoning, sentiment analysis, and multilingual support.

---

# 🚀 Features / Internship Tasks

## Task 1 — Dynamic Knowledge Base Expansion

Implemented a system that dynamically updates the customer service chatbot knowledge base when source documents change.

### Technologies

* ChromaDB
* LangChain
* Gemini API

### Outcome

The chatbot automatically incorporates new company knowledge without manual retraining.

---

## Task 2 — Multi-Modal AI Assistant

Built an assistant capable of understanding:

* Text input
* Image input (screenshots)

### Features

* Screenshot analysis
* Visual reasoning
* Context-aware response generation
* Evidence-based technical support

### Technologies

* Gemini Vision
* Streamlit
* PIL / OpenCV

---

## Task 3 — Medical Q&A Chatbot

Developed a medical question-answering chatbot using the MedQuAD dataset.

### Features

* Medical question answering
* Symptom-based retrieval
* Disease context retrieval
* Educational medical responses

### Dataset

MedQuAD Dataset

### Technologies

* FAISS
* Sentence Transformers
* LangChain
* Gemini API

---

## Task 4 — Research Expert Chatbot

Developed a domain expert chatbot trained on AI-related arXiv papers.

### Features

* Paper retrieval
* Concept explanation
* Research summarization
* Complex technical query answering

### Dataset

arXiv Dataset (AI subset)

### Technologies

* FAISS
* HuggingFace Embeddings
* RAG Pipeline
* Gemini API

---

## Task 5 — Sentiment Analysis

Integrated sentiment analysis to detect user emotions.

### Supported Sentiments

* Positive
* Negative
* Neutral

### Response Adaptation

* Negative → Empathetic responses
* Positive → Warm responses
* Neutral → Professional responses

### Outcome

Improved chatbot emotional intelligence and customer experience.

---

## Task 6 — Multilingual Support

Extended chatbot to support multilingual conversations.

### Supported Languages

* English
* Hindi
* Gujarati
* Urdu

### Features

* Automatic language detection
* Translation pipeline
* Mixed-language support
* Context preservation across language switches

---

# 🛠 Tech Stack

## Frontend

* Streamlit

## Backend

* Python

## AI / ML

* Gemini API
* LangChain
* Sentence Transformers
* HuggingFace

## Vector Databases

* ChromaDB
* FAISS

## NLP Libraries

* langdetect
* deep-translator

---

# 📂 Project Structure

```bash
GenAI-Internship-Project/
│
├── modules/
├── datasets/
├── tests/
├── scripts/
├── vector_store/
├── vectorstores/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 📊 Datasets Used

## MedQuAD

Medical question-answer dataset containing disease-specific Q&A.

## arXiv Dataset

Used AI-related scientific papers for research chatbot.

## customer-service Dataset

Dataset links are provided in submission.

---

# ⚙ Setup

Clone this repository to your local machine using:

```bash
  git clone https://github.com/Shaikh-Subhan/GenAI-Internship-Project
```

## 🔐 Environment Setup

Create a .env file in the root directory and run below command.

```bash
copy .env.example .env
```
Then add your actual API keys in .env.

## Install Dependencies

```bash
pip install -r requirements.txt
```

## 📥 Dataset Download & Setup

This project uses external datasets which are not included in the GitHub repository due to large file sizes.

Google Drive Dataset Link
```bash
https://drive.google.com/drive/folders/1DFHgWsJM7RnDLLcS-ojKHe52CtrSnBXA?usp=sharing
```
Download datasets and put inside main folder

## 📜Scripts

## Run below scripts
```bash
python build_customer_db.py
```
```bash
python build_medical_db.py 
```
```bash
python build_arxiv_db.py
```
## Run App
```bash
streamlit run app.py
```
---

# 🧪 Test

Testing files are available in:

```bash
tests/
```

# 🧠 Chat Interface Usage

Once the app opens, you can interact with the AI assistant in multiple ways:

1️⃣ Text-Based Chat
* Type any question in the chat input box

2️⃣ Image Input (Multimodal Feature)
* Upload a screenshot or image
*Ask questions related to it

3️⃣ Medical Q&A Mode
* change the mode to Medical Q&A from left pannel
* Ask health-related questions

4️⃣ Research Assistant Mode (arXiv)
* change the mode to Research Expert from left pannel
* Ask AI/ML research questions

Includes:

* Medical tests
* Sentiment tests
* Multilingual tests
* RAG tests
* Research chatbot tests

---

# 📈 Results

Successfully developed a unified AI assistant capable of:

✅ Customer Support
✅ Medical Q&A
✅ Research Assistance
✅ Sentiment-aware responses
✅ Multilingual conversations
✅ Image understanding

---

# Challenges Faced

* Large dataset preprocessing (5GB arXiv dataset)
* Slow vector database creation
* Retrieval relevance issues
* Multilingual ambiguity handling
* Model rate limit errors

---

# Solutions Implemented

* Created AI-only arXiv subset
* Added query expansion for better retrieval
* Added model fallback system
* Optimized vector storage using FAISS

---

# Future Improvements

* Voice input support
* Better research summarization
* PDF paper upload support
* Advanced evaluation metrics

---

# Conclusion

This internship project successfully transformed a simple chatbot into a powerful multi-mode AI assistant capable of handling complex real-world scenarios across multiple domains.


