from sentence_transformers import SentenceTransformer

# This model is small (approx 100MB) and very fast
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(text_list: list[str]):
    """Converts a list of strings into a list of vectors."""
    embeddings = model.encode(text_list)
    return embeddings