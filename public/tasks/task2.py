from .base_task import BaseTask

class Task2(BaseTask):
    def __init__(self, config_service):
        super().__init__(config_service)
        
    def run(self):
        ...