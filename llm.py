from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_reply(system_prompt, messages, retrieved_context):
    catalog_text = "\n".join([
        f"{item['name']} - {item['url']}"
        for item in retrieved_context
    ])

    final_messages = [
        {
            "role": "system",
            "content": system_prompt + "\n\nCatalog:\n" + catalog_text
        }
    ]

    final_messages.extend(messages)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=final_messages,
        temperature=0.2
    )

    return response.choices[0].message.content
