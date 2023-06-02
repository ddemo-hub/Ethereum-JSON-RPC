from src.utils.singleton import Singleton
from src.utils import logger

from .config_service import ConfigService

import asyncio
import aiohttp
import pandas
import time

class DataService(metaclass=Singleton):
    def __init__(self, config_service: ConfigService):
        self.config_service = config_service
        
    async def _request_block_data(self, payload, session) -> dict:
        response = await session.request('POST', url=self.config_service.json_rpc_endpoint, json=payload)
        json_response = await response.json()

        return json_response["result"]
        
    async def _pool(self, payloads) -> list:
        async with aiohttp.ClientSession() as session:
            queue = [
                self._request_block_data(payload=payload, session=session)
                for payload in payloads
            ]
                
            block_data = await asyncio.gather(*queue, return_exceptions=True)
        
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
            except Exception as ex:
                logger.error(f"Error while requesting the chunk {chunk}\n{ex}")
                time.sleep(5)   # Sleep for some time and try again
                list_block_data += asyncio.run(self._pool(chunk))
                
            time.sleep(1)   # After requesting a chunk, sleep for 1 second to avoid exceeding the rate limit per second

        df_block_data = pandas.DataFrame(list_block_data)
        
        return df_block_data
