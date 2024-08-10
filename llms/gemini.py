from .base_llm import BaseLLM

class GeminiLLM(BaseLLM):
    """
    Gemini LLM implementation.
    """

    def __init__(self, api_key: str):
        """
        Initialize Gemini LLM with API key.
        """
        # TODO: Implement Gemini initialization

    def send_prompt(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the response.
        """
        # TODO: Implement Gemini prompt sending

    def process_response(self, response: str) -> str:
        """
        Process the raw response from Gemini.
        """
        # TODO: Implement Gemini response processing
