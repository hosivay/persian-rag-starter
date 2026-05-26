from core.chunker import chunk_text, chunk_file
from core.embedder import Embedder


def test_chunk_text_persian():
    text = "شیراز پایتخت استان فارس است. ارگ کریم‌خان در مرکز شیراز قرار دارد."
    chunks = chunk_text(text)
    assert len(chunks) > 0
    assert isinstance(chunks[0], str)


def test_chunk_text_small():
    text = "یک جمله کوتاه."
    chunks = chunk_text(text)
    assert len(chunks) == 1


def test_embedder_persian():
    embedder = Embedder()
    result = embedder.embed_one("شیراز پایتخت استان فارس است")
    assert len(result) == 384


def test_embedder_english():
    embedder = Embedder()
    result = embedder.embed_one("Shiraz is a city in Iran")
    assert len(result) == 384


def test_embedder_returns_list():
    embedder = Embedder()
    results = embedder.embed(["متن اول", "متن دوم"])
    assert len(results) == 2
