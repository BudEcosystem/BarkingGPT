import os
import tempfile
import flask
from flask import request, jsonify, send_from_directory
from flask_cors import CORS

from text_speech import generate
from speech_text import transcribe
from openai_util import call_open_api

from utils import upload_file_to_s3, get_uuid, delete_file_if_exists
import config
from bark import preload_models  # Bark
import logging


app = flask.Flask(__name__)
CORS(app)

app.config["AUDIO_FILES_DIR"] = "audio-files"


@app.route("/audio-files/<path:filename>")
def serve_file(filename):
    from pathlib import Path

    root = Path(".")
    folder_path = root / app.config["AUDIO_FILES_DIR"]
    return send_from_directory(folder_path, filename)

    # return send_from_directory(app.config["AUDIO_FILES_DIR"], filename)


@app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    logging.info("Speech To Text")
    # Create Temp file
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = get_uuid() + ".wav"
        save_path = os.path.join(temp_dir, file_name)

        # Save Wav File
        wav_file = request.files["audio_data"]
        wav_file.save(save_path)

        response_text = transcribe(save_path)

        logging.debug(response_text)

        # Use the response text to call the api
        res = call_open_api(response_text)

        # text = res["choices"][0]["message"]["content"]

        logging.debug(res)

        # Conver Text To Speech
        # Folder
        if not os.path.isdir(app.config["AUDIO_FILES_DIR"]):
            os.makedirs(app.config["AUDIO_FILES_DIR"])

        file_name = get_uuid() + ".wav"
        file_path = os.path.join(app.config["AUDIO_FILES_DIR"], file_name)
        generate(res, file_path)
        logging.info("Audio generated")
        logging.info(file_path)

    # return {"text": response_text}
    return {
        "text": res,
        "audio": "http://localhost:5001"
        + flask.url_for("serve_file", filename=file_name, _external=False),
    }


@app.route("/text-speech", methods=["POST"])
def text_to_speech():
    data = request.get_json()
    text = data["text"]

    # Debug
    logging.info("Logging Text")
    logging.debug(text)

    # Folder
    if not os.path.isdir(app.config["AUDIO_FILES_DIR"]):
        os.makedirs(app.config["AUDIO_FILES_DIR"])

    file_name = get_uuid() + ".wav"
    file_path = os.path.join(app.config["AUDIO_FILES_DIR"], file_name)
    generate(text, file_path)
    logging.info("Audio generated")

    return {
        "text": text,
        "audio": flask.url_for("serve_file", filename=file_name, _external=True),
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    preload_models()  # Bark
    logging.info("Starting App")
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
