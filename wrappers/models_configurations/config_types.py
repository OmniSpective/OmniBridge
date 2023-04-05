from enum import Enum

class ConfigTypes(str, Enum):
    BASE = 'BASE'
    CHATGPT = 'CHATGPT'
    DALLE = 'DALLE'
    HUGGINGFACE = 'HUGGINGFACE'
