class GPTConfiguration:
    api_key: str
    model: str


class GPTWrapper:
    def __init__(self, prompt: str, configuration: GPTConfiguration) -> None:
        self.prompt = prompt
        self.config = configuration

    def __call__(self) -> str:
        pass