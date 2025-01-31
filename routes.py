from flask import jsonify, render_template, request
from services.openai_service import get_openai_completion
from models import db, User, Project
from bokeh_visualization import create_scatter_plot


def setup_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/process_project", methods=["POST"])
    def process_project():
        try:
            description = request.form.get("description")
            if not description:
                return jsonify({"error": "Missing required fields"}), 400

            response_json = get_openai_completion(description)
            return render_template("index.html", **response_json)

        except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

    @app.route("/quote")
    def quote_page():
        return render_template("quote.html")

    @app.route("/quote/data", methods=["GET"])
    def quote_of_the_day():
        quote = get_openai_completion("Give me an inspirational quote of the day")
        return jsonify({"quote": quote})

    @app.route("/add_user", methods=["POST"])
    def add_user():
        try:
            data = request.get_json()
            new_user = User(**data)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User added!", "user": new_user.to_dict()}), 201
        except Exception as e:
            return jsonify({"error": "Failed to add user", "details": str(e)}), 500

    @app.route("/add_project", methods=["POST"])
    def add_project():
        try:
            data = request.get_json()
            new_project = Project(**data)
            db.session.add(new_project)
            db.session.commit()
            return jsonify({"message": "Project added!", "project": new_project.to_dict()}), 201
        except Exception as e:
            return jsonify({"error": "Failed to add project", "details": str(e)}), 500

    @app.route("/get_projects", methods=["GET"])
    def get_projects():
        try:
            projects = Project.query.all()
            return jsonify({"projects": [p.to_dict() for p in projects]}), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch projects", "details": str(e)}), 500

    @app.route("/delete_project/<int:project_id>", methods=["DELETE"])
    def delete_project(project_id):
        try:
            project = Project.query.get(project_id)
            if not project:
                return jsonify({"error": "Project not found"}), 404

            db.session.delete(project)
            db.session.commit()
            return jsonify({"message": "Project deleted!"}), 200
        except Exception as e:
            return jsonify({"error": "Failed to delete project", "details": str(e)}), 500

    @app.route("/visualize")
    def visualize():
        script, div = create_scatter_plot()
        return render_template("visualization.html", script=script, div=div)

    @app.route("/previous_projects")
    def previous_projects():
        return render_template("previous_projects.html")
