from langchain_core.prompts import PromptTemplate

from .llm.ollama_llm import get_local_llm
from .llm.gemini_llm import get_gemini_llm


PROMPT_TEMPLATE = """
You are an AI assistant that answers questions about uploaded
financial documents.

Answer the question ONLY using the provided context.

If the answer cannot be found in the context, say:

"I could not find this information in the uploaded document."

Do not use outside knowledge.

Context:
{context}

Question:
{question}

Answer:
"""


def generate_answer(vectorstore, question, llm_mode):

    # Retrieve relevant chunks
    retrieved_docs = vectorstore.similarity_search(
        question,
        k=4
    )

    # Build context
    context_parts = []

    for doc in retrieved_docs:

        page_number = doc.metadata.get(
            "page_number",
            "Unknown"
        )

        context_parts.append(
            f"[Page {page_number}]\n{doc.page_content}"
        )

    context = "\n\n".join(context_parts)

    # Create prompt
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    final_prompt = prompt.format(
        context=context,
        question=question
    )

    # Select LLM
    if llm_mode == "Offline - Qwen3:4B":
        llm = get_local_llm()
    else:
        llm = get_gemini_llm()

    # Generate answer
    response = llm.invoke(final_prompt)

    # Extract clean text
    if hasattr(response, "content"):

        content = response.content

        if isinstance(content, str):
            answer = content

        elif isinstance(content, list):
            answer = "\n".join(
                item.get("text", "")
                for item in content
                if isinstance(item, dict)
                and item.get("type") == "text"
            )

        else:
            answer = str(content)

    else:
        answer = str(response)

    # IMPORTANT: return both values
    return answer, retrieved_docs