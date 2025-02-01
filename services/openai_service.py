import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
with open("prompt.txt", "r") as file:
    instruction_prompt = file.read().strip()


def get_openai_completion(description):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": instruction_prompt},
            {"role": "user", "content": description},
        ],
        model="gpt-3.5-turbo",
    )
    return json.loads(response.choices[0].message.content)
