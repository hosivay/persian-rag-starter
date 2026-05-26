import httpx
import json
import os

from dotenv import load_dotenv

from api.cache import get_cached, set_cached
from api.deps import retriever

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")


def _build_prompt(query: str, docs: list[str]) -> str:
    top_docs = "\n".join(docs)
    return f"""تو یک دستیار هوشمند فارسی هستی.
فقط بر اساس اطلاعات زیر جواب بده:

{top_docs}

سوال: {query}

اگر جواب در اطلاعات نبود بگو: نمی‌دانم."""


async def ask(query: str):
    docs = retriever.search(query)
    prompt = _build_prompt(query, docs)

    cached = get_cached(prompt)
    if cached is not None:
        async def generate_cached():
            yield cached

        return generate_cached

    async def generate():
        parts: list[str] = []
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                async with client.stream(
                    "POST",
                    f"{OLLAMA_URL}/api/generate",
                    json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": True},
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        data = json.loads(line)
                        if "response" in data:
                            parts.append(data["response"])
                            yield data["response"]
        except httpx.ConnectError:
            yield "خطا: Ollama در دسترس نیست"
            return
        except httpx.HTTPStatusError:
            yield "خطا: پاسخ نامعتبر از Ollama"
            return

        if parts:
            set_cached(prompt, "".join(parts))

    return generate
