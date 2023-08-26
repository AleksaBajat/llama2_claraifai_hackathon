from clarifai import clarify_text_to_audio, get_data_from_clarify
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from io import BytesIO
from PIL import Image
import numpy as np

st.title("IndieMeta Story Generator")

description: str = st.text_area('Make sure that it contains:')

image: UploadedFile = st.file_uploader("Choose a file", type=["jpeg", "jpg", "png"])
bytes_data: bytes | None = None
if image is not None:
    bytes_data: bytes = image.getvalue()

if bytes_data is not None:
    img = Image.open(BytesIO(bytes_data))
    img_array = np.array(img)

    left_co, cent_co, last_co = st.columns(3)
    with cent_co:
        st.image(img_array, width=300)

    story, tags = get_data_from_clarify(description, bytes_data)
    

    print(story)
    if story is None:
        st.write("Mighty AI was not inspired to write a story for this image with the particular parameters. Maybe try something else?")
    elif story.strip() == "":
        st.write("Mighty AI was not inspired to write a story for this image with the particular parameters. Maybe try something else?")

    st.write(story)

    st.write('Relevant Hashtags:')

    tags_text = ''
    for i in tags:
        tags_text = tags_text + '#' + i.replace(' ', '_') + ' '

    tags_text = tags_text[:-1]
    st.write(tags_text)

    sentences = story.split('.')
    audio_sentences = []
    counter = 0
    for i in sentences:
        counter += 1
        st.write(counter)

        temp = clarify_text_to_audio(i)
        audio_sentences.append(temp)
        st.audio(temp, format="audio/wav", start_time=0)

    concatenated_bytes = b"".join(audio_sentences)

    #st.audio(audio_sentences, format="audio/wav", start_time=0)
