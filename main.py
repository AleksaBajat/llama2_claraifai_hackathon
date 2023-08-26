from clarifai import Generate
import streamlit as st


st.write("What is going on??")


results = Generate()

out = results.outputs
outResult = out[-1]

st.write(outResult.data.text.raw)
