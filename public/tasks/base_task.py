from src.utils.globals import Globals

from src.services.config_service import ConfigService
from src.services.data_service import DataService

from abc import ABC, abstractmethod

import pandas

class BaseTask(ABC):
    def __init__(self, config_service: ConfigService, data_service: DataService):
        self.config_service = config_service
        self.data_service = data_service

    def cache_block_data(block_data: pandas.DataFrame):
        Globals.block_data_cache = block_data.copy()
        Globals.use_cache = True
        
    def read_cached_block():
        cached_data = Globals.block_data_cache.copy()
        return cached_data


    @abstractmethod
    def run(self):
        pass