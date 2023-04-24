from bark import SAMPLE_RATE, generate_audio
from IPython.display import Audio
from scipy.io.wavfile import write as write_wav



def generate(text_prompt,filename):


    # text_prompt = """
    #      Hello, my name is Suno. And, uh — and I like pizza. [laughs]
    #      But I also have other interests such as playing tic tac toe.
    # """
    audio_array = generate_audio(text_prompt)
    audio_obj = Audio(audio_array, rate=SAMPLE_RATE)
    # print(audio_obj)
    write_wav(filename, SAMPLE_RATE, audio_array)
    return True


# if __name__ == "__main__":
#     generate("hello how are you","test.wav")