from .base_task import BaseTask

from src.utils.globals import Globals
from src.utils import logger

import pandas
import pandasql

class Task2(BaseTask):
    def __init__(self, config_service, data_service):
        super().__init__(config_service, data_service)
        
    def get_transactions_df(self, block_data: pandas.DataFrame) -> pandas.DataFrame:
        list_transactions = [
            transaction for block in block_data.itertuples() 
            for transaction in block.transactions
        ]
        df_transactions = pandas.DataFrame(list_transactions)
        
        return df_transactions
    
    def run(self):
        # Get the data
        df_block_data = self.data_service.get_blocks()        

        # Create the transactions table
        df_transactions = self.get_transactions_df(df_block_data)
        
        # Drop error prone columns
        df_transactions.drop(columns="accessList", inplace=True)                # List type is not supported by sql
        
        # Convert necessary columns from hex string to hex integer
        hex_to_dec_cols = ["blockNumber", "gasPrice", "value"]
        df_hex_to_dec = df_transactions[hex_to_dec_cols].copy()
        df_hex_to_dec = df_hex_to_dec.apply(lambda row: pandas.Series([int(r, base=16) for r in row]), axis=1)        
        
        df_transactions[hex_to_dec_cols] = df_hex_to_dec
        df_transactions["value"] = df_transactions["value"] / 10                # In order to avoid integer overflow
    
        # Top 10 Ethereum addresses by the total Ether received
        query1 = f"""
        SELECT [to]
        FROM df_transactions
        WHERE [to] IS NOT NULL 
        AND blockNumber BETWEEN {self.config_service.start_block} AND {self.config_service.end_block}
        GROUP BY [to]
        ORDER BY SUM(value) DESC
        LIMIT 10;
        """
        top_receivers = pandasql.sqldf(query1, locals())
        
        logger.info(f"[TASK 2] Top 10 Ethereum addresses that received the most Ether can be listed as:\n{top_receivers}")
        
        # Top 5 Smart Contracts by the total number of transactions
        query2 = f"""
        WITH 
        sender_nonce AS (
            SELECT [from] as contract, SUM(nonce) as count
            FROM df_transactions
            WHERE [to] IS NOT NULL 
            AND blockNumber BETWEEN {self.config_service.start_block} AND {self.config_service.end_block}
            GROUP BY [from]
        ),
        sender_count AS (
            SELECT [from] as contract, COUNT(*) as count
            FROM df_transactions
            WHERE [to] IS NOT NULL 
            AND blockNumber BETWEEN {self.config_service.start_block} AND {self.config_service.end_block}
            GROUP BY [from]            
        ),
        receiver_count AS (
            SELECT [to] as contract, COUNT(*) as count
            FROM df_transactions
            WHERE [to] IS NOT NULL 
            AND blockNumber BETWEEN {self.config_service.start_block} AND {self.config_service.end_block}
            GROUP BY [from]                        
        )
        SELECT sender_nonce.contract
        FROM sender_nonce JOIN sender_count JOIN receiver_count
        ORDER BY sender_nonce.count + sender_count.count + receiver_count.count DESC
        LIMIT 5;
        """
        top_transactors = pandasql.sqldf(query2, locals())
        
        logger.info(f"[TASK 2] Top 5 Smart Contracts by the total number of transactions can be listed as:\n{top_receivers}")

    def anomaly_detector(self):
        df_block_data = self.data_service.get_blocks()        

        df_transactions = self.get_transactions_df(df_block_data)
        
        gas_prices = df_transactions[["transactionIndex", "gasPrice"]]
        gas_prices["gasPrice"] = gas_prices["gasPrice"].apply(lambda x: int(x, base=16))
        
        gas_prices["zscore"] = (gas_prices["gasPrice"] - gas_prices["gasPrice"].mean()) / gas_prices["gasPrice"].std(ddof=0)
        
        anomalies = gas_prices.loc[(gas_prices["zscore"] >= self.config_service.anomaly_threshold) | (gas_prices["zscore"] <= -self.config_service.anomaly_threshold)]
        
        logger.info(f"[TASK 2] Following transactions have anormal gas prices:\n {anomalies}")
