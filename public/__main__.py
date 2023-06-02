import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from src.utils.globals import Globals
from src.utils import logger 
logger.set_logger_path(Globals.artifacts_path.joinpath("logs.txt"))

from src.containers.tasks_container import TaskContainer

def main(tasks: TaskContainer):
    logger.info("[TASK 1] Starts")
    tasks.task1.run()
    logger.info("[TASK 1] Ends")
    
    logger.info("[TASK 2] Starts")
    tasks.task2.run()
    logger.info("[TASK 2] Ends")
    
    logger.info("[TASK 3] Starts")
    tasks.task3.run()
    logger.info("[TASK 3] Ends")


if __name__ == "__main__":
    tasks = TaskContainer()
    main(tasks=tasks)