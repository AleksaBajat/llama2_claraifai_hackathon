import streamlit as st
from computation import get_data_from_clarify
from streamlit.runtime.uploaded_file_manager import UploadedFile

st.title("IndieMeta Story Generator")

description: str = st.text_area('Area for textual entry')

image: UploadedFile = st.file_uploader("Choose a file", type=["jpeg", "jpg", "png"])
if image is not None:
    bytes_data: bytes = image.getvalue()

st.write(get_data_from_clarify(description, image))
