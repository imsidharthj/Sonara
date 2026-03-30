from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()

from voice.stt import transcribe
from voice.tts import synthesize
from agent.graph import run_agent

app = FastAPI(title="Sonara", description="Voice AI E-Commerce Support Assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/voice")
async def voice(audio: UploadFile = File(...), session_id: str = Form(default=None)):
    audio_bytes = await audio.read()
    transcript = transcribe(audio_bytes)
    reply_text, session_id = await run_agent(transcript, session_id)
    audio_base64 = synthesize(reply_text)
    return {
        "transcript": transcript,
        "reply_text": reply_text,
        "audio_base64": audio_base64,
        "session_id": session_id,
    }
