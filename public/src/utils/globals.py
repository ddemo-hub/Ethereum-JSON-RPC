from .singleton import Singleton

from datetime import datetime 
import pathlib
import pandas

class Globals(metaclass=Singleton):
    DATETIME_NOW = datetime.now().strftime("%Y_%B/Day_%d/%H:%M:%S")
    
    # Paths
    project_path = pathlib.Path(__file__).parent.parent.parent
    
    artifacts_path = project_path.parent.joinpath("artifacts", DATETIME_NOW)

    use_cache = False
    block_data_cache: pandas.DataFrame