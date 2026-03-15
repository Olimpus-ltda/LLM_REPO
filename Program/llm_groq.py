from dotenv import load_dotenv
from groq import Groq
import os
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API"),  # This is the default and can be omitted
)


def consult_groq(prompt,tetx): 
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"{prompt}\n\nTexto: {tetx}",
        }
    ],
    model="openai/gpt-oss-120b",
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content