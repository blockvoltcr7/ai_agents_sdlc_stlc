import os
from typing import Optional, Generator
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from dotenv import load_dotenv
from .base_llm import BaseLLM

class AnthropicLLM(BaseLLM):
    """
    Anthropic LLM implementation.
    """

    def __init__(self, model: str = "claude-3-opus-20240229"):
        """
        Initialize Anthropic LLM.

        :param model: The Anthropic model to use. Defaults to "claude-3-opus-20240229".
        """
        load_dotenv()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = Anthropic(api_key=self.api_key)
        self.model = model

    def send_prompt(self, prompt: str) -> str:
        """
        Send a prompt to Anthropic and return the response.

        :param prompt: The prompt to send to the model.
        :return: The model's response as a string.
        """
        try:
            response = self.client.completions.create(
                model=self.model,
                prompt=f"{HUMAN_PROMPT} {prompt}{AI_PROMPT}",
                max_tokens_to_sample=1000
            )
            return response.completion
        except Exception as e:
            raise Exception(f"Error in sending prompt to Anthropic: {str(e)}")

    def process_response(self, response: str) -> str:
        """
        Process the raw response from Anthropic.

        :param response: The raw response from the model.
        :return: The processed response as a string.
        """
        # For Anthropic, we might not need to do any additional processing
        # but we'll keep this method for consistency with the BaseLLM interface
        return response.strip()
    
    def stream_prompt(self, prompt: str) -> Generator[str, None, None]:
        """
        Send a prompt to Anthropic and stream the response.

        :param prompt: The prompt to send to the model.
        :yield: Chunks of the model's response as they are generated.
        """
        try:
            stream = self.client.completions.create(
                model=self.model,
                prompt=f"{HUMAN_PROMPT} {prompt}{AI_PROMPT}",
                max_tokens_to_sample=1000,
                stream=True
            )
            for completion in stream:
                yield completion.completion
        except Exception as e:
            raise Exception(f"Error in streaming prompt to Anthropic: {str(e)}")
