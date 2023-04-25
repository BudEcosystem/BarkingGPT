from bark import SAMPLE_RATE, generate_audio
from IPython.display import Audio
from scipy.io.wavfile import write as write_wav
import numpy as np
import nltk


def generate(text_prompt,filename):


    # words = text_prompt.split()
    # # Initialize an empty list to store the 10-word strings
    # text_prompts = []
    
    # # Loop through the list of words and add every 10 words to a new string
    # for sentence in words:
    #     # Append the sentence to the text_prompts list if it's not empty
    #     if sentence:
    #         text_prompts.append(sentence + ".")
        
    # Set up history prompt
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
    # text_prompt = """
    #      Hello, my name is Suno. And, uh — and I like pizza. [laughs]
    #      But I also have other interests such as playing tic tac toe.
    # """
    #audio_array = generate_audio(text=text_prompt,history_prompt="en_speaker_1")
    #audio_obj = Audio(audio_array, rate=SAMPLE_RATE)
    # print(audio_obj)
    write_wav(filename, SAMPLE_RATE, combined_audio)
    return True


# if __name__ == "__main__":
#     generate("hello how are you","test.wav")