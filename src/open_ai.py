from pydantic import BaseModel
from openai import OpenAI
from text_utils import get_text
import os
import json

# Constants
ROLE = "You are a natural language processor which finds adjectives and the nouns they describe."
PROMPT = "Find all the adjectives in the following text and the nouns which they describe. Discard all quantitative adjectives. Discard all possessive adjectives. Discard all nouns with zero adjectives. Organise your results so that only unique nouns are returned, plus a list of all the adjectives which describe them. The text is: "

class Result(BaseModel):
    """Single result"""
    noun: str
    adjectives: list[str]

class Resultset(BaseModel):
    """Collection of results"""
    found: list[Result]

def get_adjectives(text: str) -> str:
    """Query OpenAI API for adjectives"""
    client = OpenAI(api_key=os.environ['OPENAI_KEY'])
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": ROLE},
            {"role": "user", "content": PROMPT + text},
        ],
        response_format=Resultset
    )
    return completion.choices[0].message.content

def process_file(filename: str, markers: list[tuple[str, str]]) -> dict:
    """Process file and extract adjectives"""
    text = get_text(filename, markers)
    response = get_adjectives(text)
    return json.loads(response)

if __name__ == "__main__":
    filename = "./src/PROB 11_609_123.txt"
    markers = [
        ("the vicarage at Bexley", "to be equally parted between her and my Nephew Mr Thomas Knipe"),
        ("I give her my six", "Gold shoes"),
    ]
    results = process_file(filename, markers)
    print(json.dumps(results, indent=4))