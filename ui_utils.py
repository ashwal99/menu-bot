import streamlit as st


def render_Info(msg, refined_query):
    st.sidebar.subheader(msg)
    st.sidebar.write(refined_query)
