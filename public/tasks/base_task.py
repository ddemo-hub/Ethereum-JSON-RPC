from src.services.config_service import ConfigService
from src.services.data_service import DataService

from abc import ABC, abstractmethod

class BaseTask(ABC):
    def __init__(self, config_service: ConfigService, data_service: DataService):
        self.config_service = config_service
        self.data_service = data_service


    @abstractmethod
    def run(self):
        pass