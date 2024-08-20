import os
import google.generativeai as genai
import anthropic
from openai import OpenAI
from together import Together
from groq import Groq
from utils.logger import setup_logger

logger = setup_logger()

def get_llm_client(api_choice):
    if api_choice == "Gemini":
        return genai.GenerativeModel
    elif api_choice == "OpenAI":
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    elif api_choice == "Claude":
        return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    elif api_choice == "Meta-Llama":
        return Together(api_key=os.getenv('TOGETHER_API_KEY'))
    elif api_choice == "Groq":
        return Groq(api_key=os.getenv("GROQ_API_KEY"))
    else:
        logger.error(f"Unsupported API choice: {api_choice}")
        return None

def process_text(content, prompt, api_choice, model, temperature=None, top_p=None, max_tokens=None):
    if api_choice == "Gemini":
        return process_text_gemini(content, prompt, model, temperature, top_p, max_tokens)
    elif api_choice == "OpenAI":
        return process_text_openai(content, prompt, model, temperature, max_tokens)
    elif api_choice == "Claude":
        return process_text_claude(content, prompt, model, max_tokens)
    elif api_choice == "Meta-Llama":
        return process_text_meta_llama(content, prompt, model, temperature, top_p, max_tokens)
    elif api_choice == "Groq":
        return process_text_groq(content, prompt, model, temperature, max_tokens)
    else:
        logger.error(f"Unsupported API choice: {api_choice}")
        return None

def process_text_gemini(content, prompt, model, temperature, top_p, max_tokens):
    try:
        logger.info(f"Starting text processing with Gemini. Model: {model}, Temperature: {temperature}, Top P: {top_p}, Max Tokens: {max_tokens}")
        gemini_model = genai.GenerativeModel(model_name=model)
        full_prompt = f"{content}\n\n{prompt}"
        response = gemini_model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_tokens,
            )
        )
        logger.info("Content generated successfully by Gemini model")
        return response.text if response and response.parts else None
    except Exception as e:
        logger.error(f"An error occurred while processing the text with Gemini: {str(e)}")
        return None



# Include the process_text_* functions from the provided code
# (process_text_meta_llama, process_text_gemini, process_text_openai, process_text_claude)

def process_text_meta_llama(content, prompt, model, temperature, top_p, max_tokens):
    try:
        logger.info(f"Starting text processing with Meta-Llama. Model: {model}, Temperature: {temperature}, Top P: {top_p}, Max Tokens: {max_tokens}")
        client = Together(api_key=os.getenv('TOGETHER_API_KEY'))
        full_prompt = f"{content}\n\n{prompt}"
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": full_prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=50,
            repetition_penalty=1,
            stop=["<|eot_id|>"],
            stream=False
        )
        
        logger.info("Content generated successfully by Meta-Llama model")
        return response.choices[0].message.content if response.choices else None
    except Exception as e:
        logger.error(f"An error occurred while processing the text with Meta-Llama: {str(e)}")
        return None

# def process_text_gemini(content, prompt, model, temperature, top_p, max_tokens):
#     try:
#         logger.info(f"Starting text processing with Gemini. Model: {model}, Temperature: {temperature}, Top P: {top_p}, Max Tokens: {max_tokens}")
#         gemini_model = genai.GenerativeModel(model_name=model)
#         full_prompt = f"{content}\n\n{prompt}"
#         response = gemini_model.generate_content(
#             full_prompt,
#             generation_config=genai.types.GenerationConfig(
#                 temperature=temperature,
#                 top_p=top_p,
#                 max_output_tokens=max_tokens,
#             )
#         )
#         logger.info("Content generated successfully by Gemini model")
#         return response.text if response and response.parts else None
#     except Exception as e:
#         logger.error(f"An error occurred while processing the text with Gemini: {str(e)}")
#         return None




def process_text_openai(content, prompt, model, temperature, max_tokens):
    try:
        logger.info(f"Starting text processing with OpenAI. Model: {model}, Temperature: {temperature}, Max Tokens: {max_tokens}")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable is not set")
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        client = OpenAI(api_key=api_key)
        full_prompt = f"{content}\n\n{prompt}"
        
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        logger.info("Content generated successfully by OpenAI model")
        return completion.choices[0].message.content if completion.choices else None
    except Exception as e:
        logger.error(f"An error occurred while processing the text with OpenAI: {str(e)}")
        return None

def process_text_claude(content, prompt, model, max_tokens):
    try:
        logger.info(f"Starting text processing with Claude. Model: {model}, Max Tokens: {max_tokens}")
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            logger.error("ANTHROPIC_API_KEY environment variable is not set")
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

        client = anthropic.Anthropic(api_key=api_key)
        full_prompt = f"{content}\n\n{prompt}"

        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": full_prompt
                }
            ]
        )

        logger.info("Content generated successfully by Claude model")
        return message.content[0].text if message.content else None
    except Exception as e:
        logger.error(f"An error occurred while processing the text with Claude: {str(e)}")
        return None
def process_text_groq(content, prompt, model, temperature, max_tokens):
    try:
        logger.info(f"Starting text processing with Groq. Model: {model}, Temperature: {temperature}, Max Tokens: {max_tokens}")
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        full_prompt = f"{content}\n\n{prompt}"
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": full_prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        logger.info("Content generated successfully by Groq model")
        return response.choices[0].message.content if response.choices else None
    except Exception as e:
        logger.error(f"An error occurred while processing the text with Groq: {str(e)}")
        return None