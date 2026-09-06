# Persian RAG Assistant

A Persian Retrieval-Augmented Generation (RAG) system designed for extracting, processing, embedding, retrieving, and answering questions from Persian documents.

The project focuses on reliable Persian PDF processing, especially mixed RTL/LTR text reconstruction, Persian normalization, semantic retrieval, and grounded question answering.

---

## Features

- Persian PDF text extraction
- RTL/LTR mixed-direction text reconstruction
- Persian Unicode normalization
- Persian and English token preservation
- Document chunking
- Vector-based retrieval
- Embedding pipeline
- LLM-based answer generation
- Grounded RAG responses
- RAG query REST API
- Document management REST API
- Confidence-based answer rejection
- Database migrations with Alembic
- Automated unit and integration tests

---

## Architecture

```text
             PDF Document
                  |
                  v
          PDF Parser (PyMuPDF)
                  |
                  v
    RTL/LTR Text Reconstruction
                  |
                  v
      Persian Text Normalization
                  |
                  v
            Text Chunking
                  |
                  v
             Embeddings
                  |
                  v
          Vector Retrieval
                  |
                  v
          Context Builder
                  |
                  v
        Extraction / LLM
                  |
                  v
         Answer Validation
                  |
                  v
            REST API
```

---

## Tech Stack

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL

### Document Processing

- PyMuPDF
- Persian Unicode normalization
- Custom RTL/LTR reconstruction engine

### RAG Pipeline

- Text segmentation
- Chunk management
- Embedding service
- Vector similarity retrieval
- Context building
- Grounded prompt generation
- Answer validation

### LLM and Embeddings

- Ollama
- Configurable embedding model
- Configurable LLM model

### Testing

- Pytest
- Unit tests
- Integration tests
- API tests

---

## Persian PDF Processing

One of the main challenges in Persian RAG systems is preserving the correct text order.

PDF extraction may return Persian and English text in visual or mixed content-stream order. This project implements custom reconstruction logic for Persian documents containing both RTL and LTR content.

The PDF pipeline includes:

- Character-level geometry analysis
- RTL ordering correction
- LTR token preservation
- Mixed Persian-English sentence reconstruction
- Persian presentation-form normalization
- Word-spacing reconstruction

Example:

```text
این سند برای آزمایش سیستم RAG ساخته شده است.
```

Mixed English terms such as the following are preserved:

```text
Python
RAG
PDF
scikit-learn
k-means
```

---

## Project Structure

```text
app/
├── api/
│   └── routes/
├── core/
├── db/
├── embedding/
├── llm/
├── models/
├── schemas/
└── services/

alembic/
└── versions/

scripts/
└── utility scripts

tests/
├── unit/
└── integration/
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/mahdianfe/Persian-RAG-Assistant-v1.git
cd Persian-RAG-Assistant-v1
```

Install dependencies:

```bash
uv sync
```

---

## Database Setup

Run the required services:

```bash
docker compose up -d
```

Apply database migrations:

```bash
uv run alembic upgrade head
```

---

## Running Tests

Run the complete test suite:

```bash
uv run pytest -v
```

Latest verified full-suite status:

```text
68 passed
```

A dedicated RAG API test has also been added and passes independently.

---

## Running the Application

Start FastAPI:

```bash
uv run uvicorn app.main:app --reload
```

API documentation is available at:

```text
http://localhost:8000/docs
```

---

## RAG Query API

The RAG endpoint allows clients to ask questions about the indexed Persian documents.

### Endpoint

```http
POST /rag/query
```

### Example Request

```bash
curl -X POST "http://127.0.0.1:8000/rag/query" \
-H "Content-Type: application/json" \
-d '{"question":"چه الگوریتم‌هایی در متن نام برده شده‌اند؟"}'
```

### Example Response

```json
{
  "answer": "Regression\nClassification\nk-means\nClustering"
}
```

For a question whose answer is not supported by the retrieved documents:

```bash
curl -X POST "http://127.0.0.1:8000/rag/query" \
-H "Content-Type: application/json" \
-d '{"question":"پایتخت فرانسه چیست؟"}'
```

Example response:

```json
{
  "answer": "پاسخ این سؤال در اسناد موجود پیدا نشد."
}
```

---

## Document API

The application also provides REST endpoints for document management and PDF upload.

Main document endpoints include:

```text
POST   /documents
POST   /documents/upload
GET    /documents
GET    /documents/{document_id}
PATCH  /documents/{document_id}
DELETE /documents/{document_id}
```

Uploaded PDFs are extracted, cleaned, chunked, and stored for later retrieval.

---

## RAG Confidence Thresholds

The project uses confidence checks before generating an answer.

### RETRIEVAL_SIMILARITY_THRESHOLD

Controls which retrieved chunks are allowed to enter the RAG context.

Low-similarity chunks are discarded before context construction.

Configured through the application settings:

```text
RETRIEVAL_SIMILARITY_THRESHOLD=0.42
```

Conceptually:

```text
Question
   |
   v
Embedding Search
   |
   v
Similarity Filter
   |
   v
Relevant Context
```

### RAG_MIN_ANSWER_SCORE

A second confidence check evaluates the best retrieved chunk before answer generation.

If the score is below the configured threshold, the system refuses to answer.

```text
RAG_MIN_ANSWER_SCORE=0.40
```

This reduces unsupported answers when relevant document context cannot be retrieved.

---

## Development Notes

The PDF reconstruction pipeline has been tested on documents containing:

- Persian sentences
- English technical terms
- Mixed RTL/LTR content
- Arabic/Persian presentation-form characters
- Numbers
- Hyphenated English tokens
- Geometric word spacing

The RAG pipeline has also been tested for:

- Semantic retrieval
- Similarity thresholds
- Document filtering
- Context construction
- Grounded prompts
- Out-of-document questions
- Term extraction
- REST API queries

---

## Future Improvements

- Generalize structured term extraction beyond fixed test vocabulary
- Advanced reranking
- Better document and chunk metadata
- Page-level citation support
- OCR support for scanned PDFs
- Streaming LLM responses
- Web-based user interface
- Retrieval evaluation on a larger Persian benchmark

---

## License

MIT License
