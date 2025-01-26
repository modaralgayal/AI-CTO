import os
import json

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import OpenAI

from backend.backend import Project, User, db, init_app
from bokeh_visualization import create_scatter_plot

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
with open("prompt.txt", "r") as file:
    instruction_prompt = file.read().strip()
app = Flask(__name__)
init_app(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_project", methods=["POST"])
def process_project():
    try:
        description = request.form.get("description")  
        if not description:
            return jsonify({"error": "Missing required fields"}), 400
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": instruction_prompt,
                },
                {
                    "role": "user",
                    "content": description,
                },

            ],
            #model="chatgpt-4o-latest",
            model = "gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
        )
        
        response_data = response.choices[0].message.content
        response_json = json.loads(response_data)

        # Extract data from the response JSON
        project_name = response_json["project_name"]
        business_novelty = int(response_json["business_novelty"])
        customer_novelty = int(response_json["customer_novelty"])
        impact = int(response_json["impact"])
        business_rationale = response_json["rationale_behind_business_novelty"]
        customer_rationale = response_json["rationale_behind_customer_novelty"]
        impact_rationale = response_json["rationale_behind_impact"]

        return render_template("index.html", project_name=project_name, business_novelty=business_novelty, customer_novelty=customer_novelty, impact=impact, business_rationale=business_rationale, customer_rationale=customer_rationale, impact_rationale=impact_rationale)
    
    except Exception as e:
        return jsonify({"error": "An error occurred while processing the project.", "details": str(e)}), 500
           
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
        model="chatgpt-4o-latest",
    )

    return jsonify({"quote": chat_completion.choices[0].message.content.strip()})


@app.route("/add_user", methods=["POST"])
def add_user():
    try:
        data = request.get_json()

        if not data.get("role") or not data.get("name") or not data.get("email"):
            return jsonify({"error": "Missing required fields"}), 400

        new_user = User(role=data["role"], name=data["name"], email=data["email"])

        db.session.add(new_user)
        db.session.commit()

        return (
            jsonify(
                {"message": "User added successfully!", "user": new_user.to_dict()}
            ),
            201,
        )
    except Exception as e:
        return (
            jsonify(
                {"error": "An error occurred while adding the user.", "details": str(e)}
            ),
            500,
        )


@app.route("/add_project", methods=["POST"])
def add_project():
    try:
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
                {
                    "message": "Project added successfully!",
                    "project": new_project.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An error occurred while adding the project.",
                    "details": str(e),
                }
            ),
            500,
        )


@app.route("/get_projects", methods=["GET"])
def get_projects():
    try:
        projects = Project.query.all()
        projects_list = [project.to_dict() for project in projects]
        return jsonify({"projects": projects_list}), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An error occurred while fetching projects.",
                    "details": str(e),
                }
            ),
            500,
        )


@app.route("/visualize")
def visualize():
    script, div = create_scatter_plot()
    return render_template("visualization.html", script=script, div=div)

@app.route("/previous_projects")
def previous_projects():
    return render_template("previous_projects.html")


if __name__ == "__main__":
    app.run(debug=True)
