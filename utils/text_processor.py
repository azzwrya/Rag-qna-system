def split_text(text: str, chunk_size: int = 700, overlap: int = 70):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i : i + chunk_size])
    return chunks