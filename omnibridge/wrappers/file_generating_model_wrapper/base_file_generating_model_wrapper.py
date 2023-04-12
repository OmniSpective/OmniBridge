from abc import ABC, abstractmethod


class FileGeneratingModelWrapper(ABC):
    @abstractmethod
    def generate_files(self):
        pass
