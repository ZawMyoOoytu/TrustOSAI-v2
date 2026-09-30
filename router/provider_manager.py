from adapters.local_adapter import LocalModelAdapter
from adapters.openai_adapter import OpenAIAdapter
from adapters.claude_adapter import ClaudeAdapter



class ProviderManager:



    def __init__(self):


        self.adapters={


            "local":
            LocalModelAdapter(),


            "openai":
            OpenAIAdapter(),


            "anthropic":
            ClaudeAdapter()

        }



    def execute(
        self,
        provider,
        model,
        prompt
    ):


        adapter = (
            self.adapters[provider]
        )


        return adapter.execute(

            prompt,

            model

        )