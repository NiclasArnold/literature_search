def filter_papers(papers, conditions):
    filtered = []
    for paper in papers:
        if all(condition(paper) for condition in conditions):
            filtered.append(paper)
    
    print(f"Filter angewendet. {len(papers)} auf {len(filtered)}")
    return filtered