from .base_task import BaseTask

from src.utils.globals import Globals
from src.utils import logger

class Task1(BaseTask):
    def __init__(self, config_service, data_service):
        super().__init__(config_service, data_service)
                   
    def run(self):
        # Get the data
        df_block_data = self.data_service.get_blocks()  
        
        # Cache the data
        self.cache_block_data(df_block_data)    
        
        # Save the data in .json format
        save_json_path = Globals.artifacts_path.joinpath("block_data.json")
        df_block_data.to_json(save_json_path)        
        logger.info(f"[TASK 1] The block data is saved to '{save_json_path}' in .json format")
        
        # Calculate the Average Gas Price of the Transactions
        total_gasPrice = 0
        num_txn = 0
        for block in df_block_data.itertuples():                    # In this situation, itertuples is faster than other iteration methods including the apply method
            txn = block.transactions                                # Plus, itertuples is more readable
            list_gasPrices = list(
                map (
                    lambda x: int(x["gasPrice"], base=16),  # Get the gasPrice and convert it to decimal
                    txn                                     # For every transaction in txn
                )
            )
            
            total_gasPrice += sum(list_gasPrices) 
            num_txn += 1
        
        avg_gasPrice = total_gasPrice / num_txn        
        logger.info(
            f"[TASK 1] The average gas price of the transactions within the blocks in range " + \
            f"{self.config_service.start_block}-{self.config_service.end_block} is: {avg_gasPrice} Wei"
        )
        
        # Calculate the total amount of Ether transferred
        ether_transferred = 0
        for block in df_block_data.itertuples():
            txn = block.transactions
            list_ether_transferred = list(
                map (
                    lambda x: int(x["value"], base=16) * 1e-18,     # Get the Wei value and convert it to decimal, then convert it to ether
                    txn                                             # For every transaction in txn
                )
            )
            ether_transferred += sum(list_ether_transferred)

        logger.info(
            f"[TASK 1] The total amount of Ether transferred by the transactions within the blocks " + \
            f"{self.config_service.start_block}-{self.config_service.end_block} is: {ether_transferred} Ether"
        )   
