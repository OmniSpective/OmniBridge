from enum import Enum

class SupportedModels(str, Enum):
    CHATGPT = 'chatgpt'
    DALLE = 'dalle'
    HUGGINGFACE = 'huggingface'