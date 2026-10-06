import os
import re
import json
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

KB_DIR = os.path.join(os.path.dirname(__file__), 'knowledge_base')
INDEX_FILE = os.path.join(os.path.dirname(__file__), 'faiss_index.bin')
META_FILE = os.path.join(os.path.dirname(__file__), 'faiss_meta.json')
VECT_FILE = os.path.join(os.path.dirname(__file__), 'faiss_vectorizer.pkl')

def chunk_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    doc_name = os.path.basename(file_path)
    # Split by markdown headers
    sections = re.split(r'\n(?=#{1,3}\s+)', content)
    chunks = []
    for sec in sections:
        sec = sec.strip()
        if len(sec) > 40:
            header_match = re.match(r'^(#{1,3}\s+[^\n]+)', sec)
            title = header_match.group(1).replace('#', '').strip() if header_match else doc_name
            chunks.append({
                'source': doc_name,
                'title': title,
                'text': sec
            })
    return chunks

def build_index():
    print(f"Loading knowledge base documents from: {KB_DIR}")
    all_chunks = []
    for f in sorted(os.listdir(KB_DIR)):
        if f.endswith('.md'):
            f_path = os.path.join(KB_DIR, f)
            c = chunk_markdown(f_path)
            all_chunks.extend(c)
            print(f"  Parsed {f} -> {len(c)} chunks")

    corpus = [f"{c['title']} \n {c['text']}" for c in all_chunks]
    
    # Use word + char n-grams for robust matching of domain terms, codes, and names
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=4096,
        sublinear_tf=True
    )
    X = vectorizer.fit_transform(corpus).toarray().astype('float32')

    # Normalize vectors for cosine similarity via inner product
    faiss.normalize_L2(X)

    dimension = X.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(X)

    print(f"Built FAISS IndexFlatIP with {index.ntotal} vectors of dimension {dimension}.")

    # Persist index and metadata
    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, indent=2)
    with open(VECT_FILE, 'wb') as f:
        pickle.dump(vectorizer, f)

    print("Index and metadata saved successfully!")
    return index, all_chunks, vectorizer

def search_index(query, top_k=3):
    if not os.path.exists(INDEX_FILE) or not os.path.exists(META_FILE) or not os.path.exists(VECT_FILE):
        index, chunks, vectorizer = build_index()
    else:
        index = faiss.read_index(INDEX_FILE)
        with open(META_FILE, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        with open(VECT_FILE, 'rb') as f:
            vectorizer = pickle.load(f)

    q_vec = vectorizer.transform([query]).toarray().astype('float32')
    faiss.normalize_L2(q_vec)

    scores, indices = index.search(q_vec, top_k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx >= 0 and idx < len(chunks):
            results.append({
                'score': float(score),
                'source': chunks[idx]['source'],
                'title': chunks[idx]['title'],
                'text': chunks[idx]['text']
            })
    return results

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        print(f"\nSearching for: '{query}'")
        res = search_index(query, top_k=3)
        for i, r in enumerate(res, 1):
            print(f"\n[{i}] Score: {r['score']:.4f} | Source: {r['source']} | Title: {r['title']}")
            print("-" * 60)
            print(r['text'][:350] + ("..." if len(r['text']) > 350 else ""))
    else:
        build_index()
