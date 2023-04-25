from bark import SAMPLE_RATE, generate_audio
from IPython.display import Audio
from scipy.io.wavfile import write as write_wav
import numpy as np
import nltk


def generate(text_prompt,filename):

    history_prompt = "en_speaker_3"
    
    sentences = nltk.sent_tokenize(text_prompt)
    chunks = ['']
    token_counter = 0
    for sentence in sentences:
        current_tokens = len(nltk.Text(sentence))
        if token_counter + current_tokens <= 250:
            token_counter = token_counter + current_tokens
            chunks[-1] = chunks[-1] + " " + sentence
        else:
            chunks.append(sentence)
            token_counter = current_tokens
    
    # Generate audio for each prompt
    audio_arrays = []
    for prompt in chunks:
        audio_array = generate_audio(prompt, history_prompt=history_prompt)
        audio_arrays.append(audio_array)

    # Combine the audio files
    combined_audio = np.concatenate(audio_arrays)
    
    write_wav(filename, SAMPLE_RATE, combined_audio)
    return True
