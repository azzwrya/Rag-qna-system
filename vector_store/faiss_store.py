import faiss
import numpy as np
import pickle
import os

INDEX_PATH = "data/faiss_index.bin"
METADATA_PATH = "data/metadata.pkl"


def save_to_faiss(chunks: list[str]):
    from embeddings.embedding_utils import get_embeddings

    embeddings = np.array(get_embeddings(chunks)).astype("float32")
    dimension = embeddings.shape[1]

    # Initialize FAISS index
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Persist index
    faiss.write_index(index, INDEX_PATH)

    # Persist chunk metadata
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(chunks, f)


def search_index(query: str, k: int = 3):
    from embeddings.embedding_utils import get_embeddings

    if not os.path.exists(INDEX_PATH):
        return [], []

    # Load index
    index = faiss.read_index(INDEX_PATH)

    # Embed query
    query_vector = np.array(get_embeddings([query])).astype("float32")

    # D = distances (L2), I = indices
    D, I = index.search(query_vector, k)

    # Load stored chunks
    with open(METADATA_PATH, "rb") as f:
        all_chunks = pickle.load(f)

    # Collect results and scores
    results = []
    scores = []

    for idx, dist in zip(I[0], D[0]):
        if idx != -1:
            results.append(all_chunks[idx])
            scores.append(float(dist))

    return results, scores
