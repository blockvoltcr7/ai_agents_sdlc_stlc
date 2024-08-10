from .gemini import GeminiLLM
from .llama import LlamaLLM
from .anthropic import AnthropicLLM
from .openai import OpenAILLM

class LLMFactory:
    """
    Factory class for creating LLM instances.
    """

    @staticmethod
    def create_llm(llm_type: str, api_key: str):
        """
        Create and return an instance of the specified LLM.
        """
        if llm_type == "gemini":
            return GeminiLLM(api_key)
        elif llm_type == "llama":
            return LlamaLLM(api_key)
        elif llm_type == "anthropic":
            return AnthropicLLM(api_key)
        elif llm_type == "openai":
            return OpenAILLM(api_key)
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")
