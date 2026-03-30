from groq import Groq

client = Groq()


def transcribe(audio_bytes: bytes) -> str:
    transcription = client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",
        file=("audio.wav", audio_bytes),
    )
    return transcription.text
