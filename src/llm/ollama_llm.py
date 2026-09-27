import streamlit as st
from langchain_ollama import OllamaLLM


@st.cache_resource
def get_local_llm():

    return OllamaLLM(
        model="qwen3:4b",
        temperature=0,
        num_ctx=4096,
        num_predict=512
    )