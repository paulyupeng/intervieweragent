"""
Voice Pipeline - Speech-to-Text and Text-to-Speech integration
"""
import asyncio
import json
from typing import AsyncIterator, Optional, Callable
from abc import ABC, abstractmethod

from app.core.config import settings


class STTProvider(ABC):
    """Abstract base class for Speech-to-Text providers"""

    @abstractmethod
    async def transcribe(self, audio_data: bytes) -> str:
        """Transcribe audio data to text"""
        pass

    @abstractmethod
    async def transcribe_stream(self) -> AsyncIterator[tuple[str, bool]]:
        """Stream transcription - yields (text, is_final) tuples"""
        pass


class DeepgramSTT(STTProvider):
    """Deepgram Speech-to-Text implementation"""

    def __init__(self):
        self.api_key = settings.DEEPGRAM_API_KEY
        self.base_url = "https://api.deepgram.com/v1/listen"
        self._stream_queue = asyncio.Queue()
        self._ws = None

    async def transcribe(self, audio_data: bytes) -> str:
        """Transcribe audio using Deepgram REST API"""
        import httpx

        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "audio/webm"
        }

        params = {
            "model": "nova-2",
            "language": "en",
            "punctuate": "true",
            "smart_format": "true"
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                params=params,
                content=audio_data
            )

            if response.status_code != 200:
                raise Exception(f"Deepgram API error: {response.text}")

            result = response.json()
            transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
            return transcript

    async def transcribe_stream(self) -> AsyncIterator[tuple[str, bool]]:
        """Stream transcription using WebSocket"""
        import websockets

        ws_url = "wss://api.deepgram.com/v1/listen"
        params = {
            "model": "nova-2",
            "language": "en",
            "punctuate": "true",
            "smart_format": "true",
            "vad_events": "true",
            "endpointing": "300"
        }

        headers = {
            "Authorization": f"Token {self.api_key}"
        }

        async with websockets.connect(
            f"{ws_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}",
            extra_headers=headers
        ) as ws:
            self._ws = ws

            # Start listener task
            async def listen():
                try:
                    async for message in ws:
                        data = json.loads(message)
                        if "channel" in data and "alternatives" in data["channel"]:
                            transcript = data["channel"]["alternatives"][0]["transcript"]
                            is_final = data.get("is_final", False)
                            if transcript:
                                await self._stream_queue.put((transcript, is_final))
                        if data.get("type") == "SpeechStarted":
                            await self._stream_queue.put(("__speech_started__", False))
                except Exception as e:
                    print(f"Deepgram listener error: {e}")

            listener_task = asyncio.create_task(listen())

            try:
                while True:
                    result = await self._stream_queue.get()
                    yield result
            finally:
                listener_task.cancel()

    async def send_audio(self, audio_data: bytes):
        """Send audio data to the streaming connection"""
        if self._ws:
            await self._ws.send(audio_data)

    async def close(self):
        """Close the streaming connection"""
        if self._ws:
            await self._ws.close()


class TTSProvider(ABC):
    """Abstract base class for Text-to-Speech providers"""

    @abstractmethod
    async def synthesize(self, text: str) -> bytes:
        """Synthesize speech from text, returns audio data"""
        pass


class ElevenLabsTTS(TTSProvider):
    """ElevenLabs Text-to-Speech implementation"""

    def __init__(self, voice_id: Optional[str] = None):
        self.api_key = settings.ELEVENLABS_API_KEY
        # Default to Rachel voice - professional and clear
        self.voice_id = voice_id or "21m00Tcm4TlvDq8ikWAM"
        self.base_url = "https://api.elevenlabs.io/v1"

    async def synthesize(self, text: str) -> bytes:
        """Synthesize speech using ElevenLabs API"""
        import httpx

        url = f"{self.base_url}/text-to-speech/{self.voice_id}"

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                json=data,
                headers={
                    "xi-api-key": self.api_key,
                    "Content-Type": "application/json"
                }
            )

            if response.status_code != 200:
                raise Exception(f"ElevenLabs API error: {response.text}")

            return response.content

    async def synthesize_streaming(self, text: str) -> AsyncIterator[bytes]:
        """Synthesize speech with streaming response"""
        import httpx

        url = f"{self.base_url}/text-to-speech/{self.voice_id}/stream"

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST",
                url,
                json=data,
                headers={
                    "xi-api-key": self.api_key,
                    "Content-Type": "application/json"
                }
            ) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk


class VoicePipeline:
    """
    Combines STT and TTS for full voice interaction
    Manages the conversation flow for interviews
    """

    def __init__(
        self,
        stt_provider: Optional[STTProvider] = None,
        tts_provider: Optional[TTSProvider] = None
    ):
        self.stt = stt_provider or DeepgramSTT()
        self.tts = tts_provider or ElevenLabsTTS()
        self._is_speaking = False
        self._is_listening = False

    @property
    def is_speaking(self) -> bool:
        return self._is_speaking

    @property
    def is_listening(self) -> bool:
        return self._is_listening

    async def speak(self, text: str, audio_callback: Callable[[bytes], None]):
        """Synthesize speech and send to audio output"""
        self._is_speaking = True
        try:
            audio_data = await self.tts.synthesize(text)
            audio_callback(audio_data)
        finally:
            self._is_speaking = False

    async def listen(self, audio_data: bytes) -> str:
        """Transcribe audio data"""
        self._is_listening = True
        try:
            return await self.stt.transcribe(audio_data)
        finally:
            self._is_listening = False

    async def process_conversation_turn(
        self,
        agent_text: str,
        user_audio_callback: Callable[[], asyncio.Future[bytes]]
    ) -> str:
        """
        Process a full conversation turn:
        1. Agent speaks (TTS)
        2. User responds (STT)
        3. Return user's transcribed response
        """
        # Agent speaks
        agent_audio = await self.tts.synthesize(agent_text)
        # In a real implementation, this would play the audio
        # For now, we just return it
        self._is_speaking = False

        # Listen for user response
        user_audio = await user_audio_callback()
        user_transcript = await self.stt.transcribe(user_audio)

        return user_transcript

    def get_voice_config(self) -> dict:
        """Get voice configuration for frontend"""
        return {
            "stt_provider": "deepgram",
            "tts_provider": "elevenlabs",
            "voice_id": self.tts.voice_id if hasattr(self.tts, 'voice_id') else None
        }
