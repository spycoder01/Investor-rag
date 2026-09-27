Investor Intelligence RAG

A Streamlit-based PDF Question Answering system for analyzing financial
and annual reports using Retrieval-Augmented Generation (RAG).

The project processes the uploaded PDF locally, creates semantic
embeddings, stores them in FAISS, retrieves relevant document sections,
and generates answers using either a local Qwen3:4B model through Ollama
or Gemini through the Gemini API.

V1 Features

Upload financial or annual report PDFs through a Streamlit
interface.

Extract text from PDF pages using PyMuPDF.

Split extracted text into smaller chunks for retrieval.

Generate embeddings using all-MiniLM-L6-v2.

Store and search document embeddings using FAISS.

Retrieve the most relevant document chunks for each question.

Display page-level sources for retrieved information.

Support two LLM modes:

Offline - Qwen3:4B using Ollama

Online - Gemini using the Gemini API

Keep PDF processing, embeddings, and FAISS retrieval local in both
modes.

Architecture

                    PDF Upload
                        |
                        v
                PyMuPDF Extraction
                        |
                        v
                     Chunking
                        |
                        v
              MiniLM Embeddings
                        |
                        v
                      FAISS
                        |
                  User Question
                        |
                        v
               Similarity Search
                        |
                        v
                Retrieved Chunks
                        |
                +-------+-------+
                |               |
                v               v
          Qwen3:4B          Gemini API
           Ollama            (Online)
          (Offline)
                |               |
                +-------+-------+
                        |
                        v
                     Answer
                        |
                        v
                  Page Sources

Tech Stack

Python

Streamlit

PyMuPDF

LangChain

Hugging Face Sentence Transformers

FAISS

Ollama

Qwen3:4B

Google Gemini API

Project Structure

investor-rag/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
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

Installation

1. Clone the repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd investor-rag

2. Create a virtual environment

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

Ollama Setup

Install Ollama and download Qwen3:4B:

ollama pull qwen3:4b

Check that the model is available:

ollama list

You can test it with:

ollama run qwen3:4b

The offline mode uses this local model to generate answers without
sending the retrieved context to a cloud LLM.

Gemini API Setup

Create a .env file in the project root:

GOOGLE_API_KEY=your_gemini_api_key

The API key is loaded through an environment variable.

Do not commit .env to GitHub.

Make sure .gitignore contains:

.env
venv/
__pycache__/
*.pyc
data/uploads/

Run the Application

Start Streamlit:

streamlit run app.py

The application will open in your browser.

How to Use

Upload an annual report or financial PDF.

Select an LLM mode:

Offline - Qwen3:4B

Online - Gemini

Click Process Document.

Enter a question about the uploaded document.

The system retrieves relevant chunks from the PDF.

The selected LLM generates an answer using the retrieved context.

The application displays the source pages used for retrieval.

Example Questions

What was the EBIT margin in the Automotive Segment?

What was the company's revenue in 2025?

What are the key financial highlights mentioned in the report?

What guidance was provided for the next financial year?

V1 Retrieval Configuration

The current V1 uses:

Embedding model: sentence-transformers/all-MiniLM-L6-v2

Vector database: FAISS

Similarity search: Top 4 chunks

Chunk size: 1000 characters

Chunk overlap: 100 characters

These parameters can be improved in later versions.

Online vs Offline Mode

Offline Mode

PDF → Local Embeddings → FAISS → Retrieved Chunks → Qwen3:4B

Qwen3:4B runs locally through Ollama.

Online Mode

PDF → Local Embeddings → FAISS → Retrieved Chunks → Gemini API

The PDF is processed and searched locally. In online mode, the retrieved
context and question are sent to Gemini to generate the answer.

Limitations of V1

Retrieval currently uses FAISS semantic similarity only.

No BM25 keyword retrieval yet.

No cross-encoder reranking.

RAG parameters are not dynamically configurable from the UI.

No automated retrieval or answer evaluation.

Financial KPI extraction is not yet implemented.

OCR is not included for scanned/image-only PDFs.

Future Improvements

Planned improvements include:

V2 --- Hybrid Retrieval

Combine:

FAISS semantic search

BM25 keyword search

to improve retrieval for both conceptual questions and exact financial
terms.

V3 --- Reranking

Add a cross-encoder reranker to reorder retrieved chunks based on query
relevance.

V4 --- Dynamic RAG Controls

Add Streamlit controls for:

Chunk size

Chunk overlap

Retrieval Top-K

Final Top-K

Retrieval method

Reranking

V5 --- RAG Evaluation

Add metrics such as:

Recall@K

MRR

Context precision

Answer relevance

Faithfulness / unsupported-claim rate

V6 --- Investor Intelligence Features

Add:

Financial KPI extraction

Revenue and profit summaries

Segment-wise analysis

Year-over-year comparisons

Investor-focused dashboard

Security

API keys should be stored in .env.

.env should never be committed to GitHub.

Uploaded documents should not be committed to the repository.

Offline mode uses local inference through Ollama.

Version

V1.0 --- Dual-Mode PDF RAG

Current version focuses on building a working document RAG pipeline with
local retrieval and both offline and online LLM inference.