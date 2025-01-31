import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()

class User(db.Model):
    """
    Represents a user in the system.
    Attributes:
        id (int): Primary key.
        role (str): The role of the user (e.g., admin, manager, viewer).
        name (str): The user's name.
        email (str): The user's email, which must be unique.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(
        db.String(120), unique=True, nullable=False
    )

    def __init__(self, role, name, email):
        self.role = role
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "name": self.name,
            "email": self.email,
        }


class Project(db.Model):
    """
    Represents a project with associated x and y values and their justifications.
    Attributes:
        id (int): Primary key.
        description (str): Description of the project.
        returned_x_value (float): The x-value returned by the project.
        returned_y_value (float): The y-value returned by the project.
        x_value_justification (str): Justification for the x-value.
        y_value_justification (str): Justification for the y-value.
        type (str): Either 'existing' or 'idea'.
    """

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    returned_x_value = db.Column(db.Float, nullable=False)
    returned_y_value = db.Column(db.Float, nullable=False)
    x_value_justification = db.Column(db.Text, nullable=False)
    y_value_justification = db.Column(db.Text, nullable=False)
    type = db.Column(
        db.Enum("existing", "idea", name="project_type_enum"), nullable=False
    )  # Either Existing or Idea

    def __init__(
        self,
        description,
        returned_x_value,
        returned_y_value,
        x_value_justification,
        y_value_justification,
        type,
    ):
        self.description = description
        self.returned_x_value = returned_x_value
        self.returned_y_value = returned_y_value
        self.x_value_justification = x_value_justification
        self.y_value_justification = y_value_justification
        self.type = type

    def to_dict(self):
        """Convert the project to a dictionary for JSON responses."""
        return {
            "id": self.id,
            "description": self.description,
            "returned_x_value": self.returned_x_value,
            "returned_y_value": self.returned_y_value,
            "x_value_justification": self.x_value_justification,
            "y_value_justification": self.y_value_justification,
            "type": self.type,
        }

