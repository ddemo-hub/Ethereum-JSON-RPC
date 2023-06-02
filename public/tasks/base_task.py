from src.utils.globals import Globals
from src.utils import logger

from src.services.config_service import ConfigService
from src.services.data_service import DataService

from abc import ABC, abstractmethod

import pandas

class BaseTask(ABC):
    def __init__(self, config_service: ConfigService, data_service: DataService):
        self.config_service = config_service
        self.data_service = data_service

        self.globals = Globals
        self.logger = logger

    def cache_block_data(self, block_data: pandas.DataFrame):
        self.globals.block_data_cache = block_data.copy()
        self.globals.use_cache = True
        
    def read_cached_block(self):
        cached_data = self.globals.block_data_cache.copy()
        return cached_data

    def free_cache(self):
        self.globals.use_cache = False
        self.globals.block_data_cache = None
        

    @abstractmethod
    def run(self):
        pass