def deduplicate(papers):
    seen_dois = set()
    seen_titles = set()
    unique = []

    for paper in papers:
        doi = paper.get("doi", "").strip().lower()
        title = paper.get("title", "").strip().lower()

        if doi:
            if doi in seen_dois:
                continue
            seen_dois.add(doi)

        else:
            if title in seen_titles:
                continue
            seen_titles.add(title)

        unique.append(paper)

    return unique