from src.utils.singleton import Singleton
from src.utils.globals import Globals

from src.services.config_service import ConfigService

from public.tasks import *

from dataclasses import dataclass

@dataclass
class TaskContainer(metaclass=Singleton):
    config_service = ConfigService(
        configs=Globals.project_path.joinpath("src", "configs")
    )

    task1 = Task1(config_service)
    task2 = Task1(config_service)
    task3 = Task1(config_service)