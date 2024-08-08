import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_groq_client():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable not set")
    return Groq(api_key=GROQ_API_KEY)

def get_groq_response(client, messages, model="llama3-70b-8192", max_tokens=2000, temperature=0.7):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while getting a response from Groq: {str(e)}"