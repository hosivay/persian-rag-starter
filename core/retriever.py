import os
import chromadb
from core.embedder import Embedder

DB_PATH = os.getenv("DB_PATH", "./db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "default")


class Retriever:
    def __init__(self, collection_name: str = COLLECTION_NAME, db_path: str = DB_PATH):
        self.embedder = Embedder()
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add(self, texts: list[str], ids: list[str] = None):
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(texts))]
        embeddings = self.embedder.embed(texts)
        self.collection.add(documents=texts, embeddings=embeddings, ids=ids)

    def search(self, query: str, n: int = 3) -> list[str]:
        if self.collection.count() == 0:
            return []
        query_emb = self.embedder.embed_one(query)
        results = self.collection.query(query_embeddings=[query_emb], n_results=n)
        return results["documents"][0] or []
