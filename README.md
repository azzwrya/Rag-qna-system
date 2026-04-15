# RAG-Based Question Answering System

## Project Overview
This project is a lightweight, high-performance **Retrieval-Augmented Generation (RAG) API**.  
It allows users to upload documents (`.pdf` / `.txt`), which are indexed into a local vector store.  
Users can then ask natural language questions, and the system retrieves the most relevant document segments to generate grounded, factual answers using the **Google Gemini LLM**.

---

## Features
- **Asynchronous Document Ingestion**  
  Background tasks process documents without blocking API responses.

- **Multi-format Support**  
  Native parsing for `.txt` and `.pdf` files.

- **Local Vector Storage**  
  High-speed similarity search using **FAISS (Facebook AI Similarity Search)**.

- **Semantic Search**  
  Text is embedded into high-dimensional vectors using **Sentence-Transformers (all-MiniLM-L6-v2)**.

- **Metric-Aware Retrieval**  
  Returns similarity scores (L2 distances) for each retrieved chunk.

- **API Protection**  
  Built-in rate limiting to manage costs and prevent abuse.

---

## Tech Stack
- **Framework:** FastAPI  
- **LLM API:** Google Gemini (Generative AI)  
- **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)  
- **Vector Store:** FAISS  
- **PDF Processing:** `pypdf`  
- **Rate Limiting:** SlowAPI  

---

## Folder Structure
```plaintext
rag-qa-system/
├── api/                # API routes, rate limiter, and LLM logic
├── background_jobs/    # Asynchronous document ingestion logic
├── data/               # Persistent storage for uploads and FAISS index
├── docs/               # System design notes and analysis
├── embeddings/         # Embedding generation utilities
├── utils/              # Text processing and chunking logic
├── vector_store/       # FAISS index management (save/search)
├── main.py             # Application entry point
└── requirements.txt    # Project dependencies
```

---

## Setup Instructions

### 1. Prerequisites
- Python **3.9+**
- Google AI Studio API Key (Gemini)

---

### 2. Installation
```bash
git clone https://github.com/ayushb1331/rag-qa-system.git
cd rag-qa-system

python -m venv venv
source venv/bin/activate   # Linux / Mac
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

---

### 3. Environment Configuration
Create a `.env` file in the project root:

```plaintext
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

## Running the API
```bash
uvicorn main:app --reload
```

- API URL: `http://127.0.0.1:8000`
- Swagger Docs: `http://127.0.0.1:8000/docs`

---

## API Endpoints

### POST `/api/upload`
Uploads a document for ingestion.

**Response**
```json
{
  "message": "File 'doc.pdf' uploaded. Processing in background."
}
```

---

### POST `/api/ask`
Ask a question based on uploaded documents.

**Request Body**
```json
{
  "question": "What is the company's refund policy?"
}
```

**Response**
```json
{
  "question": "What is the company's refund policy?",
  "answer": "The refund policy states...",
  "metrics": {
    "top_k_distances": [0.65, 0.82, 0.95],
    "average_distance": 0.806
  },
  "sources": [
    "chunk 1 text...",
    "chunk 2 text..."
  ]
}
```

---

## Rate Limiting
The `/api/ask` endpoint is limited to **5 requests per minute per IP**.  
Exceeding this limit returns **429 Too Many Requests**.
