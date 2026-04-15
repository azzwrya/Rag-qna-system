## RAG System Design Notes

### 1. Chunking Strategy
- **Size:** 700 characters. 
- **Reasoning:** This allows for roughly 100-150 words per chunk. It's large enough to contain a complete thought but small enough to keep the LLM focused on specific facts.

### 2. Known Retrieval Failure Case
- **Case:** "Anaphora Resolution" (e.g., asking "What did he do next?" when the name is in a previous chunk).
- **Observation:** If the name "Steve Jobs" is in Chunk A, and Chunk B says "He started NeXT," the retriever might only pull Chunk B, leaving Gemini with no idea who "He" is.

### 3. Metric: Similarity Score
- **Tracked:** Euclidean distance (L2) from FAISS.
- **Interpretation:** A distance closer to 0 means a high match. If the top-1 distance is > 1.5, the answer is likely to be a hallucination because the context is irrelevant.