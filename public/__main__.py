import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from src.containers.tasks_container import TaskContainer

from src.utils.globals import Globals
from src.utils.logger import Logger 
Logger.set_logger_path(Globals.artifacts_path.joinpath("logs.txt"))


def main(tasks: TaskContainer):
    tasks.task1.run()
    tasks.task2.run()
    tasks.task3.run()

if __name__ == "__main__":
    main(TaskContainer)