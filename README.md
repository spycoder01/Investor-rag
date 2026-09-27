# Investor Intelligence RAG

A document-based Retrieval-Augmented Generation (RAG) application for querying financial and annual reports using **local document processing, FAISS retrieval, and Qwen3:4B through Ollama**.

The application allows users to upload a PDF, retrieve relevant sections for a question, and generate an answer grounded in the retrieved document context.

## Key Features

* Upload financial and annual report PDFs through a Streamlit interface
* Extract and chunk PDF text using PyMuPDF
* Generate embeddings with `all-MiniLM-L6-v2`
* Store document vectors in FAISS
* Retrieve the top 4 relevant chunks for each query
* Display page-level sources for retrieved content
* Generate answers using **Qwen3:4B locally through Ollama**
* Optional Gemini API mode for online inference

## Architecture

```text
                    PDF Document
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
                  Similarity Search
                         │
                         ▼
                 Relevant Chunks
                         │
                  ┌──────┴──────┐
                  ▼             ▼
             Qwen3:4B       Gemini API
              Ollama         (Optional)
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
| Online LLM     | Google Gemini API  |
| Language       | Python             |

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

## Retrieval Configuration

The current V1 pipeline uses:

```text
Embedding Model    : all-MiniLM-L6-v2
Vector Store       : FAISS
Retrieved Chunks   : Top 4
Chunk Size         : 1000 characters
Chunk Overlap      : 100 characters
```

These parameters provide the baseline retrieval configuration for V1.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/spycoder01/Investor-rag.git
cd Investor-rag
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Ollama

Install Ollama and download Qwen3:4B:

```bash
ollama pull qwen3:4b
```

Verify the model:

```bash
ollama list
```

You can also test it directly:

```bash
ollama run qwen3:4b
```

### 5. Download the embedding model

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Download it once and store it locally if you want the embedding stage to work without internet access.

### 6. Run the application

```bash
streamlit run app.py
```

The Streamlit interface will open in your browser.

## How It Works

1. Upload a financial or annual report PDF.
2. The application extracts text from the document.
3. The extracted text is divided into chunks.
4. Each chunk is converted into an embedding using `all-MiniLM-L6-v2`.
5. Embeddings are indexed in FAISS.
6. The user's question is converted into an embedding.
7. FAISS retrieves the most relevant document chunks.
8. The retrieved context is passed to the selected LLM.
9. The generated answer is displayed along with the relevant source pages.

## Example Questions

```text
What was the company's revenue in 2025?

What was the EBIT margin of the automotive segment?

What were the major financial highlights?

What guidance was provided for the next financial year?
```

## V1 Limitations

The current version uses **semantic similarity retrieval with FAISS** as the retrieval method.

The following are not yet implemented:

* BM25 keyword retrieval
* Hybrid retrieval
* Cross-encoder reranking
* Dynamic retrieval parameter tuning
* Automated RAG evaluation
* OCR for scanned PDFs
* Financial KPI extraction

## Roadmap

### V2 — Hybrid Retrieval

Combine FAISS semantic retrieval with BM25 keyword search.

### V3 — Reranking

Add a cross-encoder to rerank retrieved chunks based on query relevance.

### V4 — Dynamic RAG Controls

Allow users to configure retrieval parameters such as chunk size, overlap, and Top-K directly from the interface.

### V5 — RAG Evaluation

Evaluate retrieval and generation using metrics such as:

* Recall@K
* MRR
* Context precision
* Answer relevance
* Faithfulness / unsupported-claim rate

### V6 — Investor Intelligence

Add structured financial analysis features such as:

* Financial KPI extraction
* Revenue and profit summaries
* Segment-wise analysis
* Year-over-year comparisons

## Security

* API keys should be stored in `.env`.
* `.env` must not be committed to GitHub.
* Uploaded PDFs are excluded from version control.
* Local inference through Ollama keeps the LLM generation stage on the user's machine.

## Version

**V1.0 — Dual-Mode PDF RAG**

The first version establishes the complete document RAG pipeline with PDF processing, local embeddings, FAISS retrieval, source-page display, and both local and online LLM inference.

## Author

**Abhisek Gupta**

GitHub: [@spycoder01](https://github.com/spycoder01)
