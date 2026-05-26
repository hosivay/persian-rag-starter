from sentence_transformers import SentenceTransformer
from langdetect import detect

MODELS = {
    "fa": "paraphrase-multilingual-MiniLM-L12-v2",
    "default": "all-MiniLM-L6-v2",
}

class Embedder:
    def __init__(self):
        self._models = {}

    def _get_model(self, lang: str) -> SentenceTransformer:
        model_name = MODELS.get(lang, MODELS["default"])
        if model_name not in self._models:
            self._models[model_name] = SentenceTransformer(model_name)
        return self._models[model_name]

    def embed(self, texts: list[str]) -> list:
        lang = detect(texts[0])
        model = self._get_model(lang)
        return model.encode(texts).tolist()

    def embed_one(self, text: str) -> list:
        return self.embed([text])[0]