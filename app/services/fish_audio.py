from __future__ import annotations

from pathlib import Path

import requests


FISH_TTS_URL = "https://api.fish.audio/v1/tts"
FISH_FREE_MODEL = "s2.1-pro-free"


def tts(
    *,
    api_key: str,
    text: str,
    reference_id: str,
    output_file: str,
    model: str = FISH_FREE_MODEL,
    fmt: str = "mp3",
    timeout: int = 120,
) -> None:
    clean_api_key = (api_key or "").strip()
    clean_text = (text or "").strip()
    clean_reference_id = (reference_id or "").strip()

    if not clean_api_key:
        raise ValueError("FISH_AUDIO_API_KEY nao configurada.")

    if not clean_text:
        raise ValueError("Texto vazio.")

    if not clean_reference_id:
        raise ValueError("reference_id da voz Fish nao informado.")

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.post(
        FISH_TTS_URL,
        headers={
            "Authorization": f"Bearer {clean_api_key}",
            "Content-Type": "application/json",
            "model": model,
        },
        json={
            "text": clean_text,
            "reference_id": clean_reference_id,
            "format": fmt,
        },
        timeout=timeout,
    )

    if response.status_code != 200:
        message = response.text or ""
        if len(message) > 1200:
            message = message[:1200] + "..."
        raise RuntimeError(f"Fish Audio falhou: HTTP {response.status_code} - {message}")

    output_path.write_bytes(response.content)

    if not output_path.exists() or output_path.stat().st_size <= 0:
        raise RuntimeError("Fish Audio respondeu, mas o arquivo de audio ficou vazio.")
