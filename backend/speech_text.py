
from faster_whisper import WhisperModel

model_size = "large-v2"
model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")

def transcribe(save_path):
    segments, info = model.transcribe(save_path, language="en", beam_size=5, vad_filter=True)
    response_text = ""
    for segment in segments:
        response_text += segment.text
        
    # return response
    return response_text
