# Vmware Velo  Python script

This repo contains a Python script to get data, potentially push to Velocloud's - VCO -  developed by Peter Mraz, at&t SDWAN EE. 
Tested on macOS Catalyna and ubuntu 20.10.
All outputs (pre-deffined) or you will build - can be saved to csv/txt/json (depends on format).[TBD]



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

### CUSTOMER ONBOARDING

```
In folder authentication, create file (do copy of cust1_vco_config.yaml to lab_vco_config.yaml)
Edit lab_vco_config.yaml, fill at least Token, Tenant ID, if you run it from lab set proxy to False, if you do it behind proxy keep there True

```

### VERIFICATION OF THE CODE
```
python3 velocloud.p --customer cust1 show-vco-info
```

### SECURE-CRT

```
It is recommended to have Character Code in Secure CRT set to UTF-8
Session Options -> Terminal -> Appearance -> Character Encoding - > Set to UTF-8
Otherwise some outputs may be printed well
```
