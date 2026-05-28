import streamlit as st
import os
from views.projects import show_project
from views.search import show_search
from views.review import show_review

# Session State initialisieren
if "projekt" not in st.session_state:
    st.session_state.projekt = None

st.sidebar.title("Literatur search")

if st.session_state.projekt:
    st.sidebar.success(f"{st.session_state.projekt['name']}")
    seite = st.sidebar.radio("Navigation", [
        "Projects",
        "Search",
        "Review",
    ])
else:
    seite = "Projects"
    st.sidebar.info("Bitte zuerst ein Projekt laden")

if seite == "Projects":
    show_project()
elif seite == "Search":
    show_search()
elif seite == "Review":
    show_review()