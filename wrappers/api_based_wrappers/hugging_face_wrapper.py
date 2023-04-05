# import requests
# import os

# def query(payload, model_id, api_token):
# 	headers = {"Authorization": f"Bearer {api_token}"}
# 	API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()



# model_id = "distilbert-base-uncased"
# api_token = os.getenv("HUGGING_FACE_API_TOKEN") # get yours at hf.co/settings/tokens
# data = query("The goal of life is [MASK].", model_id, api_token)

# print(data)




from typing import Literal, TypeVar, TypedDict, Dict, Any
import json
import requests
from dataclasses import dataclass
from .base_api_wrapper import RestAPIWrapper, BaseConfiguration

COMPLETIONS_API_URL = "https://api-inference.huggingface.co/models"
dalleModel = TypeVar('dalleModel')

class GPTWrapperException(Exception):
    pass

@dataclass
class HuggingFaceConfiguration(BaseConfiguration):
    model_id: str

class CompletionsRequestBody(TypedDict):
    prompt: str
    n: int
    size: str


class HuggingFaceWrapper(RestAPIWrapper):
    def __init__(self, prompt: str, configuration: HuggingFaceConfiguration) -> None:
        super().__init__(prompt, configuration)
        self.api_url = COMPLETIONS_API_URL
    
    def _get_body(self) -> CompletionsRequestBody:
        return json.dumps({
            "inputs": self.prompt,
        })

    def _get_api_url(self) -> str:
        return self.api_url + '/' + self.config.model_id

    def _parse_response(self, response: Dict[str, Any]) -> str:
        print (response)
        return response