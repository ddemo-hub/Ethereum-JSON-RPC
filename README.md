# Ethereum Case Study

## Project Description
* Collect and analyze block & transaction data from the Ethereum Network using Ethereum's JSON-RPC API.
* Data Service contains a script to asynchronously request data from Ethereum's JSON-RPC API. Request limit (per second) of the API provider can be specified so that the algorithm can avoid exceeding the limit.    

## Installation
### Dependencies
Python 3 \
Python packages used can be found in requirements.txt \
Using the exact versions of the dependencies is recommended to avoid bugs & errors 
### Setup
* __On Linux:__
  - Run "make install" if Python 3 is not installed
  - Run "make init" to initialize a virtual environment with dependencies installed
  - You may use "make run" in order to run the main file
