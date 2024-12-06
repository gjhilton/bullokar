from pydantic import BaseModel
from openai import OpenAI
from text import get_text
import os
import json

ROLE = "You are a natural language processor which finds adjectives and the nouns they describe."  

PROMPT = "Find all the adjectives in the following text and the nouns which they describe. Discard all qantitative adjectives. Discard all possessive adjectives. Discard all nous with zero adjectives. Organise your results so that only unique nouse are returned, plus a kist of all the adjectives which descibe them. The text is: "

class Result(BaseModel):
    noun: str
    adjectives: list[str]
    
class Resultset(BaseModel):
    found: list[Result]

def get_adjectives(text):
    client = OpenAI(api_key=os.environ['OPENAI_KEY'])
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": ROLE},
            {"role": "user", "content": PROMPT + text},
        ],
        response_format=Resultset
    )
    return(completion.choices[0].message.content)
    

def process(filename, including):
    text = get_text(filename, including)
    return get_adjectives(text)


if __name__ == "__main__":
    filename = "./src/PROB 11_609_123.txt"
    including = [
        (
            "the vicarage at Bexley",
            "to be equally parted between her and my Nephew Mr Thomas Knipe",
        ),
        ("I give her my six", "Gold shoes"),
    ]
    json_obj = (process(filename, including))
    parsed = json.loads(json_obj)
    print(json.dumps(parsed, indent=4))

# returns...
#
# {
#     "found": [
#         {
#             "noun": "smocks",
#             "adjectives": [
#                 "new"
#             ]
#         },
#         {
#             "noun": "handkercheifs",
#             "adjectives": [
#                 "Cambrick"
#             ]
#         },
#         {
#             "noun": "hood",
#             "adjectives": [
#                 "new",
#                 "black",
#                 "white"
#             ]
#         },
#         {
#             "noun": "gloves",
#             "adjectives": [
#                 "white"
#             ]
#         },
#         {
#             "noun": "Mantua",
#             "adjectives": [
#                 "black",
#                 "striped"
#             ]
#         },
#         {
#             "noun": "petticoat",
#             "adjectives": [
#                 "black",
#                 "striped"
#             ]
#         },
#         {
#             "noun": "coate",
#             "adjectives": [
#                 "white",
#                 "quilted"
#             ]
#         },
#         {
#             "noun": "Aprons",
#             "adjectives": [
#                 "finest"
#             ]
#         },
#         {
#             "noun": "shoes",
#             "adjectives": [
#                 "Cloath of Gold"
#             ]
#         }
#     ]
# }