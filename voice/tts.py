import os
import base64
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")


def synthesize(text: str) -> str:
    audio_generator = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=text,
        model_id="eleven_turbo_v2",
    )
    audio_bytes = b"".join(audio_generator)
    return base64.b64encode(audio_bytes).decode()