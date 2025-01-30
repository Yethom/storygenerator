import openai
import requests
from pathlib import Path
from openaikey import openai_api_key

if not openai_api_key:
    raise ValueError("Error, no openAI API key found.")

client = openai.Client(api_key=openai_api_key)

def get_completions(prompt, system_prompt="", messages= []):
    if system_prompt != "" and len(messages) == 0:
        messages.append({"role": "assistant", "content": system_prompt})

    messages.append({"role": "user", "content": prompt})

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=messages
        )
        res = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": res})
        return res
    except Exception as e:
        return f"OpenAI exception : {str(e)}"


def generate_img(prompt, filename=""):
    resp = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = resp.data[0].url

    if filename:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        except Exception as e:
            print(f"Ean error occurred while downloading the image : {e}")

    return image_url

def text_to_speech(prompt, filename):
    if filename:
        try:
            speech_file_path = Path(__file__).parent / filename
            response = client.audio.speech.create(
                model="tts-1",
                voice="sage",
                input=prompt,
            )
            response.write_to_file(speech_file_path)
            return speech_file_path
        except Exception as e:
            print(f"Error : {e}")
