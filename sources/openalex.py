import requests
import time

BASE_URL = "https://api.openalex.org/works"

def search_openalex(queries=None, max_results=100):
    all_papers = []

    for query in queries:
        fetched = 0
        cursor = "*"

        while fetched < max_results:
            params = {
                "search": query,
                "per-page": 100,
                "cursor": cursor,
                "select": "title,authorships,publication_year,abstract_inverted_index,doi,open_access,cited_by_count",
            }

            response = requests.get(BASE_URL, params=params)

            if response.status_code != 200:
                break

            data = response.json()
            papers = data.get("results", [])

            if not papers:
                break

            for p in papers:
                all_papers.append({
                    "title":    p.get("title", ""),
                    "year":     p.get("publication_year", ""),
                    "abstract": decode_abstract(p.get("abstract_inverted_index")),
                    "cited_by_count": p.get("cited_by_count", 0),
                    "authors":  extract_authors(p.get("authorships", [])),
                    "doi":      p.get("doi", "").replace("https://doi.org/", "") if p.get("doi") else "",
                    "pdf_url":  p.get("open_access", {}).get("oa_url", "") or "",
                    "source":   "openalex",
                })

            fetched += len(papers)
            print(f"{fetched} Paper geholt")

            # Cursor für nächste Seite
            cursor = data.get("meta", {}).get("next_cursor")
            if not cursor:
                break

            time.sleep(0.5)

    return all_papers


def decode_abstract(inverted_index):
    if not inverted_index:
        return ""
    
    # Invertierter Index: {"word": [position1, position2], ...}
    positions = {}
    for word, indices in inverted_index.items():
        for i in indices:
            positions[i] = word
    
    return " ".join(positions[i] for i in sorted(positions))


def extract_authors(authorships):
    authors = []
    for a in authorships:
        name = a.get("author", {}).get("display_name", "")
        if name:
            authors.append(name)
    return ", ".join(authors)