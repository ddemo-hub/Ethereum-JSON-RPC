from .base_task import BaseTask

import pandas
import pandasql

pandas.options.mode.chained_assignment = None   # Disable SettingWithCopyWarning

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
        if self.globals.use_cache == True:
            df_block_data = self.read_cached_block()
        else:
            df_block_data = self.data_service.get_blocks()        

        # Create the transactions table
        df_transactions = self.get_transactions_df(df_block_data)
        
        # Drop error prone columns
        df_transactions.drop(columns="accessList", inplace=True)                # List type is not supported by sql
        
        # Convert necessary columns from hex string to hex integer
        hex_to_dec_cols = ["blockNumber", "gasPrice", "value", "nonce"]
        df_hex_to_dec = df_transactions[hex_to_dec_cols].copy()
        df_hex_to_dec = df_hex_to_dec.apply(lambda row: pandas.Series([int(r, base=16) for r in row]), axis=1)        
        
        df_transactions[hex_to_dec_cols] = df_hex_to_dec
        df_transactions["value"] = df_transactions["value"].astype(float)       # In order to avoid integer overflow
    
        # Top 10 Ethereum addresses by the total Ether received
        query1 = f"""
        SELECT [to] as address, SUM(value) as ether_received 
        FROM df_transactions
        WHERE [to] IS NOT NULL                                     /* Transactions in which 'to' is NULL is eliminated since they are smart contract deployments */
        AND blockNumber BETWEEN {self.config_service.start_block} AND {self.config_service.end_block}
        GROUP BY [to]
        ORDER BY SUM(value) DESC
        LIMIT 10;
        """
        top_receivers = pandasql.sqldf(query1, locals())
        
        self.logger.info(f"\n[TASK 2] Top 10 Ethereum addresses that received the most Ether can be listed as:\n{top_receivers}\n")
        
        # Top 5 Smart Contracts by the total number of transactions
        query2 = f"""
        WITH 
        nonce AS (
            SELECT [from] as contract, MAX(nonce) as count          /* Only the highest nonce count is taken into account as nonce is incremented sequentially */
            FROM df_transactions
            WHERE [to] IS NOT NULL 
            AND blockNumber BETWEEN {self.config_service.start_block} AND {self.config_service.end_block}
            GROUP BY [from]
        ),
        receiver_count AS (
            SELECT [to] as contract, COUNT(*) as count              /* 'count' is the number of times an address received a transaction */
            FROM df_transactions
            WHERE [to] IS NOT NULL 
            AND blockNumber BETWEEN {self.config_service.start_block} AND {self.config_service.end_block}
            GROUP BY [to]                        
        )
        SELECT nonce.contract, (COALESCE(nonce.count,0) + COALESCE(receiver_count.count,0)) as total_transactions       /* COALESCE is needed since the rows can be NULL if the address is not present in both 'to' and 'from' columns */
        FROM nonce LEFT OUTER JOIN receiver_count on nonce.contract = receiver_count.contract                           /* FULL OUTER JOINS should be used by it is not supported by pandasql */     
        ORDER BY (COALESCE(nonce.count,0) + COALESCE(receiver_count.count,0)) DESC                                      /* Total number of transactions received and sent */  
        LIMIT 5;
        """
        top_transactors = pandasql.sqldf(query2, locals())
        
        self.logger.info(f"\n[TASK 2] Top 5 Smart Contracts by the total number of transactions can be listed as:\n{top_transactors}\n")

    def anomaly_detector(self):
        # Get block data
        df_block_data = self.data_service.get_blocks()        

        # Create the transactions table
        df_transactions = self.get_transactions_df(df_block_data)
         
        gas_prices = df_transactions[["blockNumber", "transactionIndex", "gasPrice"]]
        gas_prices["gasPrice"] = gas_prices["gasPrice"].apply(lambda x: int(x, base=16))    # Convert gas prices to decimal integers from hexadecimal strings
        
        # Calculate the zscore of each gas price
        gas_prices["zscore"] = (gas_prices["gasPrice"] - gas_prices["gasPrice"].mean()) / gas_prices["gasPrice"].std(ddof=0)
        
        # If the gas price is more than {self.config_service.anomaly_threshold} standard deviations away from the mean, mark it as an anomaly
        anomalies = gas_prices.loc[(gas_prices["zscore"] >= self.config_service.anomaly_threshold) | (gas_prices["zscore"] <= -self.config_service.anomaly_threshold)]
        
        self.logger.info(f"\n[TASK 2] Following transactions have anormal gas prices:\n {anomalies}")
