import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import OpenAI

from backend.backend import Project, User, db, init_app

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

app = Flask(__name__)
init_app(app)


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
                "content": "Give me an inspirational quote of the day",
            }
        ],
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content.strip()


@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()

    if not data.get("role") or not data.get("name") or not data.get("email"):
        return jsonify({"error": "Missing required fields"}), 400

    new_user = User(role=data["role"], name=data["name"], email=data["email"])

    db.session.add(new_user)
    db.session.commit()

    return (
        jsonify({"message": "User added successfully!", "user": new_user.to_dict}),
        201,
    )


@app.route("/add_porject", methods=["POST"])
def add_project():
    data = request.get_json()

    required_fields = [
        "description",
        "returned_x_value",
        "returned_y_value",
        "x_value_justification",
        "y_value_justification",
        "type",
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_project = Project(
        description=data["description"],
        returned_x_value=data["returned_x_value"],
        returned_y_value=data["returned_y_value"],
        x_value_justification=data["x_value_justification"],
        y_value_justification=data["y_value_justification"],
        type=data["type"],
    )

    db.session.add(new_project)
    db.session.commit()
    return (
        jsonify(
            {"message": "Project added successfully!", "project": new_project.to_dict()}
        ),
        201,
    )


if __name__ == "__main__":
    app.run(debug=True)
