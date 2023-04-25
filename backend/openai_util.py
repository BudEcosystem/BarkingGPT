import openai
import config


openai.api_key = config.OPENAI_API_KEY

def call_open_api(response_text):
    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": response_text+"Depending upon the context the response should contain non-speech sounds such as [laughter], [laughs],[sighs],[music],[gasps],[clears throat],— or ... for hesitations,♪ for song lyrics,capitalization for emphasis of a word,MAN/WOMAN: for bias towards speaker."},
        ]
    )
    
    return response['choices'][0]['message']['content']

    