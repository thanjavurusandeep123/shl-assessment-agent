import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("faiss_index")

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def search_catalog(query: str, top_k: int = 5):
    embedding = model.encode([query])
    embedding = np.array(embedding).astype("float32")

    distances, indices = index.search(embedding, top_k)

    results = []

    for idx in indices[0]:
        item = catalog[idx]

        results.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": item.get("test_type", "Unknown")
        })

    return results
