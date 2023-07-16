import streamlit as st


def render_refined_query_Info(refined_query):
    st.sidebar.subheader("Refined Query")
    st.sidebar.write(refined_query)
