from .singleton import Singleton

from datetime import datetime
import pathlib
import os

class Logger(metaclass=Singleton):
    def __init__(self):
        self.logger_path: pathlib.Path
    
    def set_logger_path(self, path: pathlib.Path) -> None:
        log_time = datetime.now().strftime("%Y/%m/%d %H.%M.%S")
        try:
            with open(path, "w") as log_file:
                log_file.write(f"[{log_time}][INFO] Logger created at -> {path}\n")
        except FileNotFoundError:
            directory_path = path.parent
            os.makedirs(directory_path)
            
            with open(path, "w") as log_file:
                log_file.write(f"[{log_time}][INFO] Logger created at -> {path}\n")
        
        print(f"[{log_time}][INFO] Logger created at -> {path}")
        self.logger_path = path
    
    def info(self, message):
        log_time = datetime.now().strftime("%Y/%m/%d %H.%M.%S")
        with open(self.logger_path, "a") as log_file:
            log_file.write(f"[{log_time}][INFO] {message}\n")
        print(f"[{log_time}][INFO] {message}")

    def warn(self, message):
        log_time = datetime.now().strftime("%Y/%m/%d %H.%M.%S")
        with open(self.logger_path, "a") as log_file:
            log_file.write(f"[{log_time}][WARN] {message}\n")    
        print(f"[{log_time}][WARN] {message}")

    def error(self, message):
        log_time = datetime.now().strftime("%Y/%m/%d %H.%M.%S")
        with open(self.logger_path, "a") as log_file:
            log_file.write(f"[{log_time}][ERROR] {message}\n")   
        print(f"[{log_time}][ERROR] {message}")

    def print(self, message):
        log_time = datetime.now().strftime("%Y/%m/%d %H.%M.%S")
        print(f"[{log_time}] {message}")
