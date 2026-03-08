import base64
import io
import json
import os
from typing import Any, Optional

from dotenv import load_dotenv

load_dotenv()

# Provider: "groq" or "gemini" (default groq for better free-tier limits)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").strip().lower()


class _Response:
    """Minimal response object with .text for compatibility with agents."""

    def __init__(self, text: str):
        self.text = text


def _groq_text(prompt: str) -> str:
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=4096,
    )
    return (completion.choices[0].message.content or "").strip()


def _groq_vision(prompt: str, image_data: bytes, image_mime: str) -> str:
    from groq import Groq

    b64 = base64.b64encode(image_data).decode("utf-8")
    url = f"data:{image_mime or 'image/jpeg'};base64,{b64}"
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": url}},
                ],
            }
        ],
        temperature=0.2,
        max_tokens=4096,
    )
    return (completion.choices[0].message.content or "").strip()


def _mime_to_audio_ext(mime: Optional[str]) -> str:
    if not mime:
        return "wav"
    m = (mime or "").lower()
    if "mp3" in m or "mpeg" in m:
        return "mp3"
    if "m4a" in m or "mp4" in m:
        return "m4a"
    if "ogg" in m:
        return "ogg"
    if "webm" in m:
        return "webm"
    if "flac" in m:
        return "flac"
    return "wav"


def _groq_whisper(audio_data: bytes, audio_mime: Optional[str]) -> str:
    """Transcribe audio via Groq Whisper; returns JSON string { \"text\": \"...\", \"confidence\": 0.85 }."""
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    ext = _mime_to_audio_ext(audio_mime)
    buf = io.BytesIO(audio_data)
    buf.seek(0)
    transcription = client.audio.transcriptions.create(
        file=(f"audio.{ext}", buf),
        model="whisper-large-v3-turbo",
        response_format="text",
        language="en",
        temperature=0.0,
        prompt="Math problem: use 'square root of', 'raised to', 'over' for fractions. Transcribe clearly.",
    )
    transcript_text = transcription if isinstance(transcription, str) else getattr(transcription, "text", "") or ""
    return json.dumps({"text": (transcript_text or "").strip(), "confidence": 0.85})


def _gemini_text(prompt: str) -> str:
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    m = genai.GenerativeModel("gemini-2.0-flash")
    r = m.generate_content(prompt)
    return (r.text or "").strip()


def _gemini_multimodal(prompt: str, image_data: Optional[bytes] = None, image_mime: Optional[str] = None,
                       audio_data: Optional[bytes] = None, audio_mime: Optional[str] = None) -> str:
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    m = genai.GenerativeModel("gemini-2.0-flash")
    parts = [prompt]
    if image_data is not None:
        parts.append({"mime_type": image_mime or "image/jpeg", "data": image_data})
    if audio_data is not None:
        parts.append({"mime_type": audio_mime or "audio/wav", "data": audio_data})
    r = m.generate_content(parts)
    return (r.text or "").strip()


class LLMWrapper:
    """
    Single interface for text and multimodal generation.
    Use model.generate_content(prompt) for agents; use image_data/audio_data for app OCR/ASR.
    """

    def generate_content(
        self,
        prompt: Any,
        image_data: Optional[bytes] = None,
        image_mime: Optional[str] = None,
        audio_data: Optional[bytes] = None,
        audio_mime: Optional[str] = None,
    ):
        # Support legacy Gemini-style list input: [prompt, {"mime_type":..., "data":...}]
        if isinstance(prompt, list):
            text_part = None
            img_data, img_mime = None, None
            aud_data, aud_mime = None, None
            for part in prompt:
                if isinstance(part, str):
                    text_part = part
                elif isinstance(part, dict):
                    mt = part.get("mime_type", "")
                    data = part.get("data")
                    if data and ("image" in mt or mt in ("image/jpeg", "image/png")):
                        img_data, img_mime = data, mt
                    elif data and "audio" in mt:
                        aud_data, aud_mime = data, mt
            prompt = text_part or ""
            image_data = img_data
            image_mime = img_mime
            audio_data = aud_data
            audio_mime = aud_mime

        if LLM_PROVIDER == "groq":
            if audio_data:
                # Use Groq Whisper for speech-to-text (no Gemini needed)
                text = _groq_whisper(audio_data, audio_mime)
            elif image_data is not None:
                text = _groq_vision(prompt, image_data, image_mime or "image/jpeg")
            else:
                text = _groq_text(prompt)
        else:
            if image_data or audio_data:
                text = _gemini_multimodal(prompt, image_data=image_data, image_mime=image_mime,
                                          audio_data=audio_data, audio_mime=audio_mime)
            else:
                text = _gemini_text(prompt)
        return _Response(text)


model = LLMWrapper()
