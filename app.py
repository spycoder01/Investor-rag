import streamlit as st

from src.pdf_processor import extract_text_from_pdf
from src.vectorstore import create_chunks, create_vectorstore
from src.rag_pipeline import generate_answer


st.set_page_config(
    page_title="Investor Intelligence RAG",
    page_icon="📄",
    layout="wide"
)


st.title("Offline Investor Intelligence RAG")
st.caption("PDF Question Answering using Qwen3:4B + Ollama")


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("Document")

    uploaded_file = st.file_uploader(
        "Upload an annual report",
        type=["pdf"]
    )

    llm_mode = st.selectbox(
        "LLM Mode",
        [
            "Offline - Qwen3:4B",
            "Online - Gemini"
        ]
    )

    process_button = st.button(
        "Process Document",
        use_container_width=True
    )


# --------------------------------------------------
# Process PDF
# --------------------------------------------------

if uploaded_file is not None and process_button:

    with st.spinner("Processing PDF..."):

        pdf_bytes = uploaded_file.read()

        # Extract text
        pages = extract_text_from_pdf(pdf_bytes)

        if not pages:
            st.error(
                "Could not extract text from this PDF."
            )
            st.stop()

        # Create chunks
        chunks = create_chunks(pages)

        # Create FAISS vector store
        vectorstore = create_vectorstore(chunks)

        # Store in session
        st.session_state.vectorstore = vectorstore
        st.session_state.file_name = uploaded_file.name

    st.success("Document processed successfully!")

    st.write(f"**Pages extracted:** {len(pages)}")
    st.write(f"**Chunks created:** {len(chunks)}")


# --------------------------------------------------
# Question Answering
# --------------------------------------------------

if st.session_state.vectorstore is not None:

    st.divider()

    st.subheader("Ask a question")

    question = st.chat_input(
        "Ask something about the uploaded report..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("Searching document and generating answer..."):
                
                answer, retrieved_docs = generate_answer(
                st.session_state.vectorstore,
                question,
                llm_mode
            )

            st.write(answer)

            # Sources
            st.markdown("### Sources")

            shown_pages = set()

            for doc in retrieved_docs:

                page_number = doc.metadata.get(
                    "page_number",
                    "Unknown"
                )

                if page_number not in shown_pages:

                    st.write(
                        f"**{st.session_state.file_name} — "
                        f"Page {page_number}**"
                    )

                    shown_pages.add(page_number)


else:

    st.info(
        "Upload an annual report from the sidebar "
        "and click 'Process Document' to begin."
    )