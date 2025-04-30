from fastapi import FastAPI, UploadFile, File
import whisper
import requests
import tempfile
app = FastAPI()
model = whisper.load_model("base") # Or use 'small' for better quality

def call_ollama(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()

@app.post("/process/")
async def process_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    # Explicitly set fp16=False to avoid the warning when running on CPU
    transcript = model.transcribe(tmp_path, fp16=False)["text"]
    summary_prompt = f"Summarize the following meeting transcript:\n\n{transcript}"
    tasks_prompt = f"List the key action items from this meeting:\n\n{transcript}"
    summary = call_ollama(summary_prompt)
    action_items = call_ollama(tasks_prompt)
    return {
        "transcript": transcript.strip(),
        "summary": summary,
        "action_items": action_items
    }