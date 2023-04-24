import os
import tempfile
import flask
from flask import request, jsonify, send_from_directory

from flask_cors import CORS
import json

from text_speech import generate
from speech_text import transcribe

from utils import upload_file_to_s3, get_uuid, delete_file_if_exists
import config
from bark import preload_models  # Bark
import logging


app = flask.Flask(__name__)
CORS(app)


# static file
@app.route("/audio-files/<path:filename>")
def serve_file(filename):
    return send_from_directory("audio-files", filename)


@app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    logging.info("Speech To Text")
    # Create Temp file
    temp_dir = tempfile.mkdtemp()
    file_name = get_uuid() + ".wav"
    save_path: str = os.path.join(temp_dir, file_name)

    # Save Wav File
    wav_file = request.files["audio_data"]
    wav_file.save(save_path)

    response_text = transcribe(save_path)

    return {"text": response_text}


@app.route("/text-speech", methods=["POST"])
def text_to_speech():
    data = request.get_json()
    text = data["text"]

    # Debug
    logging.debug(text)

    # Folder
    dir_name = "audio-files"
    file_name = get_uuid() + ".wav"
    file_path = os.path.join(dir_name, file_name)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    generate(text, file_path)
    print("Audio generated")

    return {"text": text, "audio": "http://localhost:5001" + "/" + file_path}

if __name__ == "__main__":
    
    print("Starting App")
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
