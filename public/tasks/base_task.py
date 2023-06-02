from src.services.config_service import ConfigService

from abc import ABC, abstractmethod

class BaseTask(ABC):
    def __init__(self, config_service: ConfigService):
        self.config_service = config_service
    
    @abstractmethod
    def run(self):
        pass