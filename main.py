from clarifai import Generate
import streamlit as st
from computation import get_data_from_clarify
from streamlit.runtime.uploaded_file_manager import UploadedFile

st.title("IndieMeta Story Generator")

st.write("What is going on??")


description: str = st.text_area('Area for textual entry')

image: UploadedFile = st.file_uploader("Choose a file", type=["jpeg", "jpg", "png"])
if image is not None:
    bytes_data: bytes = image.getvalue()

st.write(get_data_from_clarify(description, image))

# results = Generate()

# out = results.outputs
# outResult = out[-1]

# st.write(outResult.data.text.raw)