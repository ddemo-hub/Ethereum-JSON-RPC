from src.utils.singleton import Singleton
from src.utils import logger

from .config_service import ConfigService

import asyncio
import aiohttp
import pandas
import time

import os
if os.name == "nt": # If running on Windows:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())     # Windows has a problem with the EventLoopPolicy, using this line to bypass it

class DataService(metaclass=Singleton):
    def __init__(self, config_service: ConfigService):
        self.config_service = config_service
        
    async def _request_block_data(self, payload, session) -> dict:
        response = await session.request('POST', url=self.config_service.json_rpc_endpoint, json=payload)
        if response.status != 200:
            raise Exception(f"payload: {payload}... status Code: {response.status}")
        
        json_response = await response.json()
        return json_response["result"]
        
    async def _pool(self, payloads) -> list:
        # Asynchronously request the data of each block. More performant than requesting blocks sequentially 
        async with aiohttp.ClientSession() as session:
            queue = [
                self._request_block_data(payload=payload, session=session)
                for payload in payloads
            ]
                
            block_data = await asyncio.gather(*queue, return_exceptions=False)
        
        return block_data

    def get_blocks(self) -> pandas.DataFrame:
        # Prepare the payloads for all requests
        payloads = [
            {
                "jsonrpc": "2.0",
                "method": "eth_getBlockByNumber",
                "params": [block_number, self.config_service.txn_details],  
                "id": 1
            }
            for block_number in range(self.config_service.start_block, self.config_service.end_block+1)    
        ]
        # Split the payloads into chuncks in order to avoid exceeding the rate limit
        chunks = [payloads[x:x+self.config_service.limit_per_second] for x in range(0, len(payloads), self.config_service.limit_per_second)]
        
        list_block_data = []
        for chunk in chunks:
            try:
                list_block_data += asyncio.run(self._pool(chunk))
                logger.info(f"[DATA SERVICE] Collecting data => {int(len(list_block_data) / (self.config_service.end_block - self.config_service.start_block+1) * 100)}%")
            except Exception as ex:
                logger.error(f"[DATA SERVICE] Error while requesting the chunk {chunk}\n{ex}\nTrying again in {self.config_service.sleep_on_error} seconds")
                time.sleep(self.config_service.sleep_on_error)   # Sleep for some time and try again
                list_block_data += asyncio.run(self._pool(chunk))   # Program terminates if another exception is raised once again
                
            time.sleep(1)   # After requesting a chunk, sleep for 1 second to avoid exceeding the rate limit per second

        list_block_data = list(filter(lambda x: x is not None, list_block_data)) # remove None values in case of an error
        df_block_data = pandas.DataFrame(list_block_data)
        
        return df_block_data
