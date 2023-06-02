from src.utils.singleton import Singleton
from src.utils.globals import Globals

from src.services.config_service import ConfigService
from src.services.data_service import DataService

from public.tasks import *

class TaskContainer(metaclass=Singleton):
    config_service = ConfigService(
        configs=Globals.project_path.joinpath("src", "configs")
    )
    data_service = DataService(config_service=config_service)

    task1 = Task1(config_service, data_service)
    task2 = Task2(config_service, data_service)
    task3 = Task3(config_service, data_service)
