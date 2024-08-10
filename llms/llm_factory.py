from .anthropic import AnthropicLLM
# ... other imports ...

class LLMFactory:
    @staticmethod
    def create_llm(llm_type: str, model: Optional[str] = None):
        """
        Create and return an instance of the specified LLM.

        :param llm_type: The type of LLM to create ("anthropic", "gemini", etc.)
        :param model: Optional model name to use. If not provided, uses the default for the LLM type.
        :return: An instance of the specified LLM.
        """
        if llm_type == "anthropic":
            return AnthropicLLM(model) if model else AnthropicLLM()
        # ... other LLM types ...
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")

    @staticmethod
    def get_available_llms():
        """
        Return a list of available LLM types.

        :return: A list of strings representing available LLM types.
        """
        return ["anthropic", "gemini", "llama", "openai"]