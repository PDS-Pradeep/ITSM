# core/llm.py
import os
import json
from openai import AzureOpenAI
from config import deployment

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-15-preview" 
)

def call_llm(system_prompt: str, user_prompt: str, temperature=0):
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)