
from sentence_transformers import SentenceTransformer

# Step 1: Load SentenceTransformer model
# model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def get_embedding(text: str) -> list:
    return model.encode(text).tolist()
