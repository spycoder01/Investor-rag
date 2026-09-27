# Investor Intelligence RAG

A Streamlit-based **Retrieval-Augmented Generation (RAG)** application for analyzing financial and annual reports. The system processes uploaded PDFs locally, generates semantic embeddings, retrieves relevant document sections using FAISS, and supports **both local and cloud-based LLM inference**.

Users can choose between:

* **Local inference:** Qwen3:4B running through Ollama
* **Cloud inference:** Google Gemini through the Gemini API

The document processing, embedding generation, and FAISS-based retrieval remain local in both modes.

## Key Features

* Upload financial and annual report PDFs through a Streamlit interface
* Extract text from PDF pages using PyMuPDF
* Split documents into smaller chunks for retrieval
* Generate embeddings using `all-MiniLM-L6-v2`
* Store and retrieve document embeddings using FAISS
* Retrieve the most relevant document chunks for each question
* Display page-level sources for retrieved information
* Choose between local Qwen3:4B and cloud-based Gemini
* Support an offline inference mode using Ollama
* Keep PDF processing, embeddings, and vector retrieval local

## Architecture

```text
                         PDF Upload
                              │
                              ▼
                      PyMuPDF Extraction
                              │
                              ▼
                         Text Chunking
                              │
                              ▼
                    all-MiniLM-L6-v2
                         Embeddings
                              │
                              ▼
                            FAISS
                              │
                              ▼
                       Similarity Search
                              │
                              ▼
                      Retrieved Chunks
                              │
                       ┌──────┴──────┐
                       │             │
                       ▼             ▼
                  Qwen3:4B       Gemini API
                   Ollama         Cloud LLM
                  (Local)        (Online)
                       │             │
                       └──────┬──────┘
                              ▼
                           Answer
                              │
                              ▼
                        Source Pages
```

## Tech Stack

| Component      | Technology         |
| -------------- | ------------------ |
| Interface      | Streamlit          |
| PDF Processing | PyMuPDF            |
| Text Splitting | LangChain          |
| Embeddings     | `all-MiniLM-L6-v2` |
| Vector Search  | FAISS              |
| Local LLM      | Qwen3:4B + Ollama  |
| Cloud LLM      | Google Gemini API  |
| Language       | Python             |

## Local vs Cloud LLM

The application provides two inference modes while keeping document processing and retrieval local.

### Local Mode

```text
PDF
 ↓
Local Embeddings
 ↓
FAISS
 ↓
Retrieved Chunks
 ↓
Qwen3:4B
 ↓
Answer
```

Qwen3:4B runs locally through Ollama. The retrieved document context is not sent to a cloud LLM.

### Cloud Mode

```text
PDF
 ↓
Local Embeddings
 ↓
FAISS
 ↓
Retrieved Chunks
 ↓
Gemini API
 ↓
Answer
```

In this mode, the retrieved context and user question are sent to Gemini for answer generation.

## Project Structure

```text
Investor-rag/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── pdf_processor.py
│   ├── vectorstore.py
│   ├── rag_pipeline.py
│   │
│   └── llm/
│       ├── __init__.py
│       ├── ollama_llm.py
│       └── gemini_llm.py
│
└── data/
    └── uploads/
```

## V1 Retrieval Configuration

| Parameter        | V1 Configuration   |
| ---------------- | ------------------ |
| Embedding Model  | `all-MiniLM-L6-v2` |
| Vector Store     | FAISS              |
| Retrieved Chunks | Top 4              |
| Chunk Size       | 1000 characters    |
| Chunk Overlap    | 100 characters     |

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/spycoder01/Investor-rag.git
cd Investor-rag
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Local LLM Setup

Install Ollama and download Qwen3:4B:

```bash
ollama pull qwen3:4b
```

Verify the model:

```bash
ollama list
```

Test it with:

```bash
ollama run qwen3:4b
```

## Gemini Setup

For cloud-based inference, create a `.env` file in the project root:

```text
GOOGLE_API_KEY=your_gemini_api_key
```

Never commit `.env` or expose your API key publicly.

## Run the Application

```bash
streamlit run app.py
```

The Streamlit interface will open in your browser.

## How It Works

1. Upload a financial or annual report PDF.
2. Select **Qwen3:4B (Local)** or **Gemini (Cloud)**.
3. Process the document.
4. Extract and chunk the PDF text.
5. Generate embeddings using `all-MiniLM-L6-v2`.
6. Store the embeddings in FAISS.
7. Convert the user question into an embedding.
8. Retrieve the top 4 relevant document chunks.
9. Pass the retrieved context to the selected LLM.
10. Display the generated answer and source pages.

## Example Questions

```text
What was the company's revenue in 2025?

What was the EBIT margin of the automotive segment?

What were the major financial highlights?

What guidance was provided for the next financial year?
```

## V1 Limitations

The current version uses FAISS semantic similarity for retrieval.

Not yet implemented:

* BM25 keyword retrieval
* Hybrid retrieval
* Cross-encoder reranking
* Dynamic retrieval parameter tuning
* Automated RAG evaluation
* OCR for scanned PDFs
* Financial KPI extraction

## Future Improvements

### V2 — Hybrid Retrieval

Combine FAISS semantic search with BM25 keyword retrieval.

### V3 — Reranking

Add a cross-encoder to rerank retrieved chunks based on query relevance.

### V4 — Dynamic RAG Controls

Allow users to tune parameters such as chunk size, chunk overlap, and retrieval Top-K.

### V5 — RAG Evaluation

Add retrieval and generation evaluation using metrics such as Recall@K, MRR, context precision, answer relevance, and faithfulness.

### V6 — Investor Intelligence

Add financial KPI extraction, revenue/profit summaries, segment analysis, and year-over-year comparisons.

## Security

* Store API keys in `.env`.
* Never commit `.env` to GitHub.
* Keep uploaded documents outside version control.
* Local mode uses Ollama for on-device LLM inference.

## Version

**V1.0 — Dual-Mode PDF RAG**

The first version establishes a working document RAG pipeline with local PDF processing, semantic embeddings, FAISS retrieval, source-page display, and support for both **local Qwen3:4B and cloud-based Gemini inference**.

## Author

**Abhisek Gupta**

GitHub: [@spycoder01](https://github.com/spycoder01)
