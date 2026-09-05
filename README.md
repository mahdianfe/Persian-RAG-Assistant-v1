
# Persian RAG Assistant

A Persian Retrieval-Augmented Generation (RAG) system designed for extracting, processing, embedding, retrieving, and answering questions from Persian documents.

The project focuses on reliable Persian PDF processing, especially mixed RTL/LTR text reconstruction, Persian normalization, and semantic retrieval.

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
- REST API for document management
- Database migrations with Alembic
- Automated test suite

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
                LLM
                  |
                  v
          Generated Answer
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
- Prompt generation

### Testing

- Pytest
- Unit tests
- Integration tests

---

## Persian PDF Processing

One of the main challenges in Persian RAG systems is preserving the correct text order.

PDF extraction often returns Persian text in visual order instead of logical reading order.

This project implements:

- Character-level geometry analysis
- RTL ordering correction
- LTR token preservation
- Mixed Persian-English sentence reconstruction

Example:

Original PDF:
این سند برای آزمایش سیستم RAG ساخته شده است.



Extracted correctly as:
این سند برای آزمایش سیستم RAG ساخته شده است


---

## Project Structure
```text

app/  
├── api/  
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

```
uv sync
```

---

## Database Setup

Run services:

```
docker compose up -d
```

Apply migrations:

```
uv run alembic upgrade head
```

---

## Running Tests

Run complete test suite:

```
uv run pytest -v
```

Current status:

```
64 passed
```

---

## Running the Application

Start FastAPI:

```
uv run uvicorn app.main:app --reload
```

API documentation:

```
http://localhost:8000/docs
```

---

## Development Notes

The PDF reconstruction module was tested on Persian documents containing:

- Persian sentences
- English technical terms
- Mixed RTL/LTR content
- Presentation form characters

Examples:

```
Python
RAG
PDF
scikit-learn
```

are preserved correctly during extraction.

---

## Future Improvements

- Better multilingual embedding models
- Streaming LLM responses
- Advanced reranking
- Document metadata filtering
- OCR support for scanned PDFs
- Web-based user interface

---

## License

MIT License

---


## RAG Confidence Thresholds

This project uses two confidence checks before generating answers.

### RETRIEVAL_SIMILARITY_THRESHOLD

Controls which document chunks are allowed to enter the RAG context.

Low similarity chunks are removed before sending information to the LLM.

Example:
```

Question  
|  
Embedding Search  
|  
Similarity Filter  
|  
Relevant Context

```

Configured in `.env`:
```

RETRIEVAL_SIMILARITY_THRESHOLD=0.42

```

---

### RAG_MIN_ANSWER_SCORE

A second safety layer after retrieval.

The system checks the best retrieved chunk score before generating an answer.

If confidence is below this value, the system refuses to answer.

Configured in `.env`:
```

RAG_MIN_ANSWER_SCORE=0.40

```

This prevents hallucinated answers when the document does not contain relevant information.

