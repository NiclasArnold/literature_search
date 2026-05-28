import streamlit as st
import os
import json
import pandas as pd

def show_review():
    st.title("Paper sichten")
    
    project_path = st.session_state.projekt["path"]
    
    # Alle CSVs finden
    csvs = [f for f in os.listdir(project_path) if f.startswith("search") and f.endswith(".csv")]
    
    if not csvs:
        st.info("Noch keine Suche gelaufen – zuerst eine Suche starten!")
        return
    
    aktive_csv = st.selectbox("Welche Suche sichten?", csvs)
    csv_pfad = os.path.join(project_path, aktive_csv)

    # Reset wenn CSV gewechselt
    if "aktive_csv" not in st.session_state or st.session_state.aktive_csv != aktive_csv:
        st.session_state.aktive_csv = aktive_csv
        st.session_state.current_index = 0
        st.session_state.entscheidungen = {}
    
    df = pd.read_csv(csv_pfad)
    st.success(f"{len(df)} Paper geladen")

    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    if "entscheidungen" not in st.session_state:
        st.session_state.entscheidungen = {}

    # Aktuelles Paper
    i = st.session_state.current_index

    if i < len(df):
        # erst prüfen, dann zugreifen
        paper = df.iloc[i]

        st.subheader(f"Paper {i+1} von {len(df)}")
        st.markdown(f"### {paper['title']}")
        st.write(f"**Jahr:** {paper['year']}  |  **Zitationen:** {paper['cited_by_count']}")
        st.write(f"**Autoren:** {paper['authors']}")
        st.divider()
        st.write(paper['abstract'])

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Relevant"):
                st.session_state.entscheidungen[i] = "relevant"
                st.session_state.current_index += 1
                
                st.rerun()
        with col2:
            if st.button("Nicht relevant"):
                st.session_state.entscheidungen[i] = "nicht relevant"
                st.session_state.current_index += 1
                
                st.rerun()

    else:
        st.success("Alle Paper gesichtet!")
        
        relevante = [idx for idx, e in st.session_state.entscheidungen.items() if e == "relevant"]
        df_relevant = df.iloc[relevante]
        
        st.write(f"**{len(df_relevant)} relevante Paper**")
        
        if st.button("Relevante Paper speichern"):
            output = os.path.join(project_path, aktive_csv.replace("search_", "relevant_"))
            df_relevant.to_csv(output, index=False)
            st.success(f"Gespeichert: {output}")