import streamlit as st
import os

st.title("📚 Literatur Recherche")

# Schritt 1: Projektordner
projekt_pfad = st.text_input("Projektordner", placeholder="/Users/niclas/Desktop/literature_search")

if st.button("Create folder"):
    if projekt_pfad:
        os.makedirs(os.path.join(projekt_pfad, "pdf"), exist_ok=True)
        st.success(f"Folder created.")
        st.code(f"""
{projekt_pfad}/
├── papers.csv
├── papers.bib
└── pdf/
        """)
    else:
        st.error("Bitte einen Pfad eingeben!")


st.header("Suchbegriffe")

# Session State damit die Liste gespeichert bleibt
if "queries" not in st.session_state:
    st.session_state.queries = ["image classification"]

# Neuen Begriff hinzufügen
new_search = st.text_input("Add search query")
if st.button("Hinzufügen"):
    if new_search and new_search not in st.session_state.queries:
        st.session_state.queries.append(new_search)

# Aktuelle Liste anzeigen mit Löschen-Button
for i, query in enumerate(st.session_state.queries):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"🔹 {query}")
    with col2:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.queries.pop(i)
            st.rerun()

st.header("Filter")

max_results = st.slider("Maximale Paper pro Suchbegriff", 100, 1000, 500)
min_zitationen = st.slider("Mindestanzahl Zitationen", 0, 100, 20)
nur_mit_abstract = st.checkbox("Nur Paper mit Abstract", value=True)
nur_mit_doi = st.checkbox("Nur Paper mit DOI", value=True)

st.header("Recherche starten")

if st.button("Recherche starten"):
    if not projekt_pfad:
        st.error("Bitte erst einen Projektordner angeben!")
    elif not st.session_state.queries:
        st.error("Bitte mindestens einen Suchbegriff eingeben!")
    else:
        with st.spinner("Suche läuft..."):
            # Filter zusammenbauen
            conditions = []
            if nur_mit_abstract:
                conditions.append(lambda p: p.get("abstract", "") != "")
            if nur_mit_doi:
                conditions.append(lambda p: p.get("doi", "") != "")
            conditions.append(lambda p: (p.get("cited_by_count") or 0) >= min_zitationen)

            # Recherche durchführen
            from sources.openalex import search_openalex
            from processing.deduplication import deduplicate
            from processing.filter import filter_papers
            from processing.export import make_unique_keys, save_csv, download_pdfs, save_bibtex

            papers = search_openalex(st.session_state.queries, max_results)
            st.info(f"{len(papers)} Paper gefunden")

            papers = deduplicate(papers)
            st.info(f"{len(papers)} nach Deduplizierung")

            papers = filter_papers(papers, conditions)
            st.info(f"{len(papers)} nach Filterung")

            make_unique_keys(papers)
            download_pdfs(papers, projekt_pfad)
            save_csv(papers, projekt_pfad)
            save_bibtex(papers, projekt_pfad)

            st.success("Fertig!")