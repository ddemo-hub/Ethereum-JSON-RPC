from .base_task import BaseTask

import pandas

class Task1(BaseTask):
    def __init__(self, config_service, data_service):
        super().__init__(config_service, data_service)
                   
    def run(self):
        df_block_data = self.data_service.get_blocks()        
        
        pass