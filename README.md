# Cisco Viptela vManage Python script

This repo contains a Python script for Cisco Velocloud vManaVCOge developed by Peter Mraz, at&t SDWAN EE. 
Tested on macOS Catalyna and ubuntu 20.10.
Python module requirements will be built and defined later. So far - you can use manual module installation.
All outputs (pre-deffined) or you will build - can be saved to csv/txt/json (depends on format).



## Requirements
* Python 3.6+

## Installation


```
git clone https://dev.azure.com/ACC-Azure-05/NGNSD%20Team/_git/velo_sdwan_scripts
cd velo_sdwan_scripts
```
### Creating Python virtual environment - test
```
python3 -m venv venv
source venv/bin/activate
```
### Install packages: 
```
pip3 install -r requirements.txt 
```

TEST:
python3 velocloud.p --customer cust1 show-vco-info