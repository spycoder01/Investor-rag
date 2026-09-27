from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def create_chunks(pages):
    """
    Split extracted PDF pages into smaller chunks
    while preserving page metadata.
    """

    documents = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    for page in pages:

        chunks = splitter.split_text(page["text"])

        for chunk in chunks:

            documents.append({
                "text": chunk,
                "page_number": page["page_number"]
            })

    return documents


def create_vectorstore(chunks):

    texts = [chunk["text"] for chunk in chunks]

    metadatas = [
        {
            "page_number": chunk["page_number"]
        }
        for chunk in chunks
    ]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    return vectorstore