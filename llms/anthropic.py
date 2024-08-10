import os
from typing import Optional, Generator
from anthropic import Anthropic, AsyncAnthropic
from dotenv import load_dotenv
from .base_llm import BaseLLM

class AnthropicLLM(BaseLLM):
    def __init__(self, model: str = "claude-3-opus-20240229"):
        load_dotenv()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model

    def send_prompt(self, prompt: str) -> str:
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            raise Exception(f"Error in sending prompt to Anthropic: {str(e)}")

    def process_response(self, response: str) -> str:
        return response.strip()

    async def stream_prompt(self, prompt: str) -> Generator[str, None, None]:
        try:
            async_client = AsyncAnthropic(api_key=self.api_key)
            stream = await async_client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )
            async for chunk in stream:
                if chunk.content:
                    yield chunk.content[0].text
        except Exception as e:
            raise Exception(f"Error in streaming prompt to Anthropic: {str(e)}")

    def count_tokens(self, text: str) -> int:
        return len(text.split())