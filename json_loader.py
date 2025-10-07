import json
import chromadb
from tqdm import tqdm
from embeddings import get_embedding

# ===== SETTINGS =====
JSON_FILE = "./output/sri_stavam/sri_stavam_detailed.json"  # your JSON file path
COLLECTION_NAME = "sri_stavam"

# Load the JSON data
with open(JSON_FILE, "r", encoding="utf-8") as f:
    slokas = json.load(f)

# Start Chroma DB client (can persist to disk or run in-memory)
client = chromadb.PersistentClient(path="./chromadb-store")  # persistent
# OR: client = chromadb.Client()  # in-memory only

# Get or create the collection
try:
    client.delete_collection(name=COLLECTION_NAME)
except:
    pass
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# Prepare and insert each sloka
ids = []
documents = []
embeddings = []
metadatas = []
for id, sloka in tqdm(enumerate(slokas)):
    sloka_num = sloka.get("verse", 0)

    # Combine fields into one searchable text blob
    text_blob = (
        f"Sloka {sloka_num}\n\n"
        f"Translation:\n{sloka['translation']}\n\n"
        f"Commentary:\n{sloka['commentary']}\n\n"
    )

    ids.append(f"sloka-{id}")
    documents.append(text_blob)
    embeddings.append(get_embedding(text=text_blob))
    metadatas.append(
        {
            "_global_index": id + 1,
            "sloka_number": sloka_num,
            "meaning_short": sloka["translation"],
            "chapter": sloka["chapter"],
            "sanskrit": sloka["sanskrit"],
            "transliteration": sloka["transliteration"],
            "commentary": sloka["commentary"],
        }
    )

# Add to Chroma collection
collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

print(f"Inserted {len(documents)} slokas into collection '{COLLECTION_NAME}'.")
