from openai_api import *
import json
from jinja2 import Template

system_prompt = ("You are a story creator for kids, you will create simple stories, these stories will be funny and"
                 "captivating and also interactive. Each times you will propose short paragraphs of the story and it"
                 "has to lead to multiple choice for the user to choose from. The user will have to choose between 3 "
                 "choices, a, b or c. At the very beginning, ask the user to choose from 3 types of stories. Please "
                 "propose an option (x) to stop the story everytime")
messages = []

def get_story_text():
    return get_completions("rewrite the whole story without the choices and this is the story, and "
                           "format the text in paragraphs", "", messages)

# ----
def get_story_info(text):
    json_prompt = ("Generate a response in JSON format, it should be like this : "
                   "{ 'title' : < story tile >, 'image' : < prompt to generate an image for the cover of the story"
                   "without any text >} Make sure to only give the json object so I can user json.loads right away. "
                   "Here's the whole story : " + text)
    json_response = get_completions(json_prompt)
    try:
        data = json.loads(json_response)
        return data["title"], data["image"]
    except Exception as ex:
        print(f"Error while deserializing JSON : {ex}")
        return "", "A cover for a kids story"

# ----

def generate_html_page(title, txt):
    template_code = ""
    with open("story_template.html", "r", encoding="utf-8") as file:
        template_code = file.read()

    template = Template(template_code)

    context = {
        "title": title,
        "text": txt
    }

    html = template.render(context)
    with open("story.html", "w", encoding="utf-8") as file:
        file.write(html)

# ---
response = get_completions("", system_prompt, messages)
print(response)
while True:
    prompt = input("You : ")
    if prompt == "x":
        break
    print()
    res = get_completions(prompt, system_prompt, messages)
    print(res)

# --- file saving
print("Saving story file text...")
story_text = get_story_text()
title, img_prompt = get_story_info(story_text)
with open("story.txt", "w") as f:
    f.write(f"Title : {title}\n")
    f.write(story_text)
print("Story saved.")

# --- image generation
print("Generating image...")
try:
    generate_img(img_prompt, "story.png")
    print("Image generated.")
except Exception as e:
    print(f"Error : {e}")

# --- text to speech
try:
    print("Generating audio...")
    text_to_speech(story_text, "story.mp3")
    print("Audio generated.")
except Exception as e:
    print(f"Error : {e}")

print("Generating HTML file...")
generate_html_page(title, story_text)
print("HTML file generated.")
