import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from openai import OpenAI

load_dotenv()


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quote")
def quote_page():
    return render_template("quote.html")


@app.route("/quote/data", methods=["GET"])
def quote_of_the_day():
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content.strip()


if __name__ == "__main__":
    app.run(debug=True)
