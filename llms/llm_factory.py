from typing import Optional
from .anthropic import AnthropicLLM

class LLMFactory:
    @staticmethod
    def create_llm(llm_type: str, model: Optional[str] = None):
        if llm_type == "anthropic":
            if model not in ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]:
                model = "claude-3-opus-20240229"  # Default to opus if not specified or invalid
            return AnthropicLLM(model)
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")

    @staticmethod
    def get_available_llms():
        return ["anthropic"]  # Add other LLM types as you implement them

    @staticmethod
    def get_available_models(llm_type: str):
        if llm_type == "anthropic":
            return ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")