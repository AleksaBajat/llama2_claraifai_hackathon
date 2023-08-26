import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


@st.cache_data
def get_data_from_clarify(text:str, image:UploadedFile) -> str:
    return "woah"