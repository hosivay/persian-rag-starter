import os

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "200"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    sentences = [s.strip() for s in text.replace("،", ".").split(".") if s.strip()]
    chunks: list[str] = []
    current = ""

    for sentence in sentences:
        piece = sentence + "."
        if len(current) + len(piece) <= chunk_size:
            current += piece
            continue

        if current:
            chunks.append(current.strip())
            if overlap > 0:
                current = current[-overlap:] if len(current) > overlap else current
            else:
                current = ""

        if len(piece) > chunk_size:
            if current:
                chunks.append(current.strip())
                current = ""
            chunks.append(piece.strip())
            continue

        current += piece

    if current:
        chunks.append(current.strip())

    return chunks


def chunk_file(file_path: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    with open(file_path, encoding="utf-8") as f:
        text = f.read()
    return chunk_text(text, chunk_size=chunk_size)
