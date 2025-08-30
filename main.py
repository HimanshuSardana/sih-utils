from google import genai
import time
import json
from pydantic import BaseModel, Field
import csv

client = genai.Client()

# read csv file
with open('ps.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    data = [
        {k: v for k, v in row.items() if not k.startswith("idk")}
        for row in csv_reader
    ]

# print(data)

class Content(BaseModel):
    problem_statement: str = Field(..., description="A brief description of the problem statement. (No more than 50 words)")
    idea: str = Field(..., description="The main idea or topic for the PPT slide deck. (No more than 50 words)")
    problem_resolution: str = Field(..., description="A concise explanation of how the idea addresses the problem statement. (No more than 50 words)")

    how_it_works: str = Field(..., description="A brief explanation of how the idea works. List all the technologies involved and how they work, no word limit")
    
    feasibility_points: list[str] = Field(..., description="A list of 3 points explaining the feasibility of the idea. Each point should be no more than 30 words.")
    viability_points : list[str] = Field(..., description="A list of 3 points explaining the viability of the idea. Each point should be no more than 30 words.")

    impact_points: list[str] = Field(..., description="A list of 2 points explaining the impact of the idea. Each point should be no more than 30 words.")
    beneficiaries: list[str] = Field(..., description="A list of 2 points explaining who will benefit from the idea. Each point should be no more than 30 words.")

SYSTEM_PROMPT = """
You are a PPT Maker for a hackathon, given a problem statement, 
you need to create content that can be used in a PPT slide deck. 
"""

for item in data:
    user_prompt = f"""
    Problem Statement: {item['problem_statement']}
    
    Create content for a PPT slide deck based on the above problem statement.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents='\n'.join([SYSTEM_PROMPT, user_prompt]),
        config={
            "response_mime_type": "application/json",
            "response_schema": Content.model_json_schema(),
        },
    )

    json_resp = response.parsed
    json_resp["category"] = item["category"]
    # print(json.dumps(response.parsed, indent=2))
    with open(f"ideas/output_{item['sno']}.json", "w") as f:
        json.dump(json_resp, f, indent=2)
    print(f"Output written to output_{item['sno']}.json")
