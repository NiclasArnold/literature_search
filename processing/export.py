import os
import re
import requests
import pandas as pd
from datetime import datetime

def generate_key(paper):
    authors = paper.get("authors", "")
    first_author = authors.split(",")[0].split()[-1] if authors else "unknown"
    
    year = str(paper.get("year", "0000"))
    
    title = paper.get("title", "")
    stopwords = {"a", "an", "the", "of", "in", "on", "for", "and", "with", "to"}
    words = [w for w in title.lower().split() if w not in stopwords]
    first_word = words[0] if words else "unknown"
    
    key = f"{first_author}{year}{first_word}"
    key = re.sub(r"[^a-zA-Z0-9]", "", key)
    
    return key.lower()


def make_unique_keys(papers):
    seen = {}
    for paper in papers:
        key = generate_key(paper)
        if key in seen:
            seen[key] += 1
            key = f"{key}{seen[key]}"
        else:
            seen[key] = 0
        paper["key"] = key
    return papers


def save_csv(papers, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(output_dir, f"search_{today}.csv")

    df = pd.DataFrame(papers)
    df.to_csv(path, index=False, encoding="utf-8")


def save_bibtex(papers, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "papers.bib")

    with open(path, "w", encoding="utf-8") as f:
        for p in papers:
            authors = p.get("authors", "").replace(", ", " and ")
            f.write(f"@article{{{p['key']},\n")
            f.write(f"  title   = {{{p.get('title', '')}}},\n")
            f.write(f"  author  = {{{authors}}},\n")
            f.write(f"  year    = {{{p.get('year', '')}}},\n")
            f.write(f"  doi     = {{{p.get('doi', '')}}},\n")
            f.write(f"  abstract= {{{p.get('abstract', '')}}},\n")
            f.write(f"}}\n\n")


def download_pdfs(papers, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    downloaded = 0

    for paper in papers:
        pdf_url = paper.get("pdf_url", "")
        if not pdf_url or not pdf_url.startswith("https://"):
            continue

        filename = f"{paper['key']}.pdf"
        pdf_dir = os.path.join(output_dir, "pdf")
        filepath = os.path.join(pdf_dir, filename)

        if os.path.exists(filepath):
            continue  # schon heruntergeladen

        try:
            response = requests.get(pdf_url, timeout=2)
            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)
                downloaded += 1
        except Exception as e:
            print(e)

    print(f"\n{downloaded} PDFs heruntergeladen")