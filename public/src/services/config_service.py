from src.utils.singleton import Singleton

import pathlib
import yaml 
import os

class ConfigService(metaclass=Singleton):
    def __init__(self, configs: pathlib.Path):
        self.config = {} 

        # Append the contents of every .yaml file in configs directory into self.config dictionary 
        for config_file in os.listdir(configs):
            config_name = config_file[:-5]  # Remove .yaml suffix
            config_path = configs.joinpath(config_file) 
            
            with open(config_path, "r") as cf:
                self.config[config_name] = yaml.safe_load(cf)

    @property
    def json_rpc_endpoint(self):
        return self.config["config"]["JSON_RPC_endpoint"]
    
    @property
    def start_block(self):
        return self.config["config"]["block_range"]["start"]
    
    @property
    def end_block(self):
        return self.config["config"]["block_range"]["end"]
    
    @property
    def txn_details(self):
        return self.config["config"]["block_range"]["txn_details"]
    
    @property
    def limit_per_second(self):
        return self.config["config"]["limit_per_second"]
    
    @property
    def sleep_on_error(self):
        return self.config["config"]["sleep_on_error"]    
    
    @property
    def anomaly_threshold(self):
        return self.config["config"]["anomaly_threshold"]