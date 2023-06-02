import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from src.containers.tasks_container import TaskContainer


def main(task_container: TaskContainer):
    ...

if __name__ == "__main__":
    main(TaskContainer)