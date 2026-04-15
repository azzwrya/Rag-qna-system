from pathlib import Path
from pypdf import PdfReader

from utils.text_processor import split_text
from vector_store.faiss_store import save_to_faiss

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def process_document(file_path: str):
    content = ""

    # ---- Handle PDF files ----
    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                content += page_text + "\n"

    # ---- Handle TXT files ----
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

    # ---- Safety check ----
    if not content.strip():
        print(f"[WARN] No text extracted from {file_path}")
        return []

    # ---- Chunk + Store ----
    chunks = split_text(content)
    save_to_faiss(chunks)

    print(f"[INFO] Processed {len(chunks)} chunks from {file_path}")
    return chunks
