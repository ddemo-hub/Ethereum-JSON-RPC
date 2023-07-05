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

    def free_cache(self):
        self.globals.use_cache = False
        self.globals.block_data_cache = None
        
    def read_block_data(self):
        if self.globals.use_cache == True:
            df_block_data = self.globals.block_data_cache.copy()
        else:
            df_block_data = self.data_service.get_blocks()        
            
            # The data is cached for future use to avoid requesting the same data over and over 
            self.globals.block_data_cache = df_block_data.copy()
            self.globals.use_cache = True

        return df_block_data

    @abstractmethod
    def run(self):
        pass