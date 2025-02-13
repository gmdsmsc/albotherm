import streamlit as st

user = st.secrets["DB_USERNAME"]
                         
st.title(f"{user}")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
