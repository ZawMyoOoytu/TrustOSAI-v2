from abc import ABC, abstractmethod


class BaseModelAdapter(ABC):


    @abstractmethod
    def execute(
        self,
        prompt: str,
        model: str,
        **kwargs
    ):

        pass