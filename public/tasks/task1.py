from .base_task import BaseTask

from src.utils.globals import Globals
from src.utils import logger

import pandas

class Task1(BaseTask):
    def __init__(self, config_service, data_service):
        super().__init__(config_service, data_service)
                   
    def run(self):
        # Get the data
        df_block_data = self.data_service.get_blocks()        
        
        # Save the data in .json format
        save_json_path = Globals.artifacts_path.joinpath("block_data.json")
        df_block_data.to_json(save_json_path)        
        logger.info(f"[TASK 1] The block data is saved to '{save_json_path}' in .json format")
        
        
        pass