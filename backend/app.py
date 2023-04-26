import os
import logging
import tempfile

import flask
from flask import request, jsonify, send_from_directory
from flask_cors import CORS

from text_speech import generate
from speech_text import transcribe
from openai_util import call_open_api
from utils import get_uuid
from bark import preload_models

app = flask.Flask(__name__)
CORS(app)

app.config["AUDIO_FILES_DIR"] = "audio-files"


@app.route("/audio-files/<path:filename>")
def serve_file(filename: str) -> str:
    root = "."
    folder_path = os.path.join(root, app.config["AUDIO_FILES_DIR"])
    return send_from_directory(folder_path, filename)


@app.route("/chat", methods=["POST"])
def speech_to_text() -> dict:
    logging.info("Speech To Text")
    try:
    # Create Temp file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            save_path = f.name
            wav_file = request.files["audio_data"]
            wav_file.save(save_path)
            
            logging.debug("Temp Audio Saved")

            response_text = transcribe(save_path)
            res = call_open_api(response_text)
            
            logging.debug("Response Test")
            logging.debug(response_text)

            # Conver Text To Speech
            if not os.path.isdir(app.config["AUDIO_FILES_DIR"]):
                os.makedirs(app.config["AUDIO_FILES_DIR"])

            file_name = f"{get_uuid()}.wav"
            file_path = os.path.join(app.config["AUDIO_FILES_DIR"], file_name)
            generate(res, file_path)

            return {
                "text": res,
                "audio": f"http://localhost:5001{flask.url_for('serve_file', filename=file_name, _external=False)}",
            }
    except:
        print("Something else went wrong")


@app.route("/text-speech", methods=["POST"])
def text_to_speech() -> dict:
    data = request.get_json()
    text = data["text"]

    logging.info("Logging Text")
    logging.debug(text)

    if not os.path.isdir(app.config["AUDIO_FILES_DIR"]):
        os.makedirs(app.config["AUDIO_FILES_DIR"])

    file_name = f"{get_uuid()}.wav"
    file_path = os.path.join(app.config["AUDIO_FILES_DIR"], file_name)
    generate(text, file_path)
    logging.info("Audio generated")

    return {
        "audio": flask.url_for("serve_file", filename=file_name, _external=True),
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    preload_models()
    logging.info("Starting App")
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
