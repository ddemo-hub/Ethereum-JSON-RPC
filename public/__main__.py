import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from src.utils.globals import Globals
from src.utils import logger 
logger.set_logger_path(Globals.artifacts_path.joinpath("logs.txt"))

from tasks import *
from src.containers.tasks_container import TaskContainer

from apscheduler.schedulers.blocking import BlockingScheduler

def run_tasks(tasks: TaskContainer):
    logger.info("[TASK 1] Starts")
    tasks.task1.run()
    logger.info("[TASK 1] Ends\n")
    
    logger.info("[TASK 2] Starts")
    tasks.task2.run()
    logger.info("[TASK 2] Ends\n")
    
    logger.info("[TASK 3] Starts")
    tasks.task3.run()
    logger.info("[TASK 3] Ends\n")

def main(tasks: TaskContainer):
    run_tasks(tasks)
    
    scheduler = BlockingScheduler()
    scheduler.add_job(Task2.anomaly_detector, args=[tasks.task2], trigger="cron", hour="*")
    scheduler.start()

if __name__ == "__main__":
    tasks = TaskContainer()
    main(tasks=tasks)