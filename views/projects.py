import streamlit as st
import os
import json
from datetime import date

TOOL_DIR = os.path.expanduser("~/literature_search")
os.makedirs(TOOL_DIR, exist_ok=True)

def show_project():
    st.title("Projects")

    st.subheader("Load project")
    
    projects = [p for p in os.listdir(TOOL_DIR) if os.path.isdir(os.path.join(TOOL_DIR, p))]
    
    if projects:
        for project_name in projects:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{project_name}")
            with col2:
                if st.button("Load", key=f"load_{project_name}"):
                    project_path = os.path.join(TOOL_DIR, project_name)
                    json_pfad = os.path.join(project_path, "project.json")
                    with open(json_pfad, "r") as f:
                        st.session_state.projekt = json.load(f)

                    st.session_state.current_index = 0
                    st.session_state.entscheidungen = {}

                    st.rerun()
    else:
        st.info("Noch keine Projekte vorhanden")

    st.divider()

    # Neues Projekt erstellen
    st.subheader("Create new project")
    
    new_name = st.text_input("Project name", placeholder="Image Classification")
    
    if st.button("Erstellen"):
        if new_name:
            project_path = os.path.join(TOOL_DIR, new_name)
            os.makedirs(os.path.join(project_path, "pdf"), exist_ok=True)
            
            projekt = {
                "name": new_name,
                "path": project_path,
                "created": str(date.today()),
            }
            
            with open(os.path.join(project_path, "project.json"), "w") as f:
                json.dump(projekt, f, indent=4)
            
            st.session_state.projekt = projekt
            st.rerun()
        else:
            st.error("Enter a project name")