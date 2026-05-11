import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

texts = []

for item in catalog:
    combined = f"""
    Name: {item['name']}
    Description: {item.get('description', '')}
    Type: {item.get('test_type', '')}
    """
    texts.append(combined)

embeddings = model.encode(texts)
embeddings = np.array(embeddings).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "faiss_index")

print("FAISS index built successfully")
