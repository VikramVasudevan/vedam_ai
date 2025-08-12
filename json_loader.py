import json
import chromadb
from embeddings import get_embedding

# ===== SETTINGS =====
JSON_FILE = "./output/chathusloki/chathusloki_detailed.json"  # your JSON file path
COLLECTION_NAME = "chathusloki"

# Load the JSON data
with open(JSON_FILE, "r", encoding="utf-8") as f:
    slokas = json.load(f)

# Start Chroma DB client (can persist to disk or run in-memory)
client = chromadb.PersistentClient(path="./chromadb-store")  # persistent
# OR: client = chromadb.Client()  # in-memory only

# Get or create the collection
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# Prepare and insert each sloka
ids = []
documents = []
embeddings = []
metadatas = []

for sloka in slokas:
    sloka_num = sloka["verse"]

    # Combine fields into one searchable text blob
    text_blob = (
        f"Sloka {sloka_num}\n\n"
        f"Devanagari:\n{sloka['sloka_devanagari']}\n\n"
        f"Transliteration:\n{sloka['sloka_english_transliteration']}\n\n"
        f"Meaning:\n{sloka['meaning']}\n\n"
        f"Commentary:\n{sloka['commentary']}"
    )

    ids.append(f"sloka-{sloka_num}")
    documents.append(text_blob)
    embeddings.append(get_embedding(text=text_blob))
    metadatas.append(
        {
            "sloka_number": sloka_num,
            "meaning_short": sloka["meaning"][:200],  # snippet
        }
    )

# Add to Chroma collection
collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

print(f"Inserted {len(documents)} slokas into collection '{COLLECTION_NAME}'.")
