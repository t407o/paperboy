from openai import OpenAI
import os

client = OpenAI(api_key =  os.getenv("OPENAI_API_KEY"))

def one_shot(content: str, prompt: str, model="gpt-3.5-turbo-16k"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "assistant", "content": content},
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.choices[0].message.content
