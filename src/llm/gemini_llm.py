import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


@st.cache_resource
def get_gemini_llm():

    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0,
        max_output_tokens=512,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )