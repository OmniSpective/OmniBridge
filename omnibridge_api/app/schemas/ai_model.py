from pydantic import BaseModel


class AIModel(BaseModel):
    id: int
    name: str
    type: str
    description: str
    input_dtype: str
    output_dtype: str

class TextualModelPromptRequest(BaseModel):
    model_name: str
    prompt: str

class TextualModelPromptResponse(BaseModel):
    response: str