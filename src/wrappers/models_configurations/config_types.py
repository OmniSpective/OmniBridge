from enum import Enum

class ConfigTypes(str, Enum):
    CHATGPT = 'CHATGPT'
    DALLE = 'DALLE'
    HUGGINGFACE = 'HUGGING_FACE'
