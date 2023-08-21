from datetime import datetime
from dotenv import dotenv_values

import requests
from flask import Flask, render_template, request

import openai
import json

app = Flask(__name__)


config = dotenv_values(".env")
print(config["COLOR"])
openai.api_key = config["OPENAI_API_KEY"]
# print(__name__)

def get_post(msg):
    reply = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": "You are a helpful assistant that shorten user's message and generate a piece of text for user to post on social medias."},
          {"role": "user", "content": f'{msg}'}
        ],
        max_tokens=200
    )
    post_text = reply["choices"][0]["message"]["content"]
    return post_text

def get_image(msg):
    res = openai.Image.create (
        prompt=f"generate an image based on the situation:{msg}, with simple background and ready for social media style.",
        size='512x512',
        n=1
    )
    post_image = res["data"][0]["url"]
    return post_image



# print(get_post("I have a bad mood kind of suck and hate my boss he treated me like i have no use"))

@app.route("/")
def hello_world():
    current_year = datetime.now().year
    return render_template('index.html', year=current_year)


@app.route('/result', methods=['GET', 'POST'])
def result_route():
    if request.method == 'POST':
        # textarea name="message" id="message"
        query = request.form.get('message')  # Get the 'name' from the form
        if query:
            post_for_user = get_post(query)
            image_for_user = get_image(query)
            return render_template('index2.html', render_post=post_for_user, render_img=image_for_user)
        else:
            return "Failed to retrieve data."

    return render_template('index2.html')


if __name__ == "__main__":
    app.run(debug=True)


