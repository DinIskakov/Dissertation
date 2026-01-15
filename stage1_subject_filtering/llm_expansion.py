import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()  # loads .env into environment

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Synonyms(BaseModel):
    synonyms: list[str]

def get_synonyms(word: str) -> list[str]:
    response = client.responses.parse(
        model="gpt-4o-2024-08-06",
        input=[
            {"role": "system", "content": "Return a concise list of synonyms."},
            {"role": "user", "content": f"Give synonyms for: {word}"},
        ],
        text_format=Synonyms,
    )
    return response.output_parsed.synonyms
