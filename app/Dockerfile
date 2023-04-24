FROM python:3.8-slim

COPY . /srv/flask_app

WORKDIR /srv/flask_app

RUN apt-get clean && apt-get -y update && apt-get -y install git


RUN pip install -r requirements.txt --src /usr/local/src
RUN pip install git+https://github.com/suno-ai/bark.git
RUN pip install --force-reinstall "faster-whisper @ https://github.com/guillaumekln/faster-whisper/archive/refs/heads/master.tar.gz"


CMD ["python", "app.py"]