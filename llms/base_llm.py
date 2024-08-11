from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """
    Abstract base class for LLM implementations.
    Defines the common interface that all LLM classes should implement.
    """

    @abstractmethod
    def __init__(self, api_key: str):
        """
        Initialize the LLM with the API key.
        """
        pass

    @abstractmethod
    def send_prompt(self, prompt: str) -> str:
        """
        Send a prompt to the LLM and return the response.
        """
        pass

    @abstractmethod
    def process_response(self, response: str) -> str:
        """
        Process the raw response from the LLM.
        """
        pass
