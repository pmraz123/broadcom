# Vmware Velo  Python script

This repo contains a Python script to get data, potentially push to Velocloud's - VCO -  developed by Peter Mraz, at&t SDWAN EE.

Tested on macOS Catalyna and ubuntu 20.10.

All outputs (pre-deffined) or you will build - can be saved to csv/txt/json (depends on format).[TBD]



## Requirements
* Python 3.6+

## Installation
(prepare your git username/pasword, as it is not well open repo, you need access and authentication will be required)

This is server: https://dev.azure.com/ACC-Azure-05/NGNSD%20Team/

```
git clone https://dev.azure.com/ACC-Azure-05/NGNSD%20Team/_git/velo_sdwan_scripts
```

You will be asked for username and password, once clone is completed execute:

```
cd velo_sdwan_scripts
```
### Creating Python virtual environment - venv
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
In folder authentication, create customer specific file. (do copy of cust1_vco_config.yaml to lab_vco_config.yaml)

cust1, cust2 or lab in front of "_vco_config.yaml" will be later used in the script, name it to identify your customer easily. 
#############################################
Edit lab_vco_config.yaml and fill:
#############################################
VCO_HOST: VCO_DNS
VCO_PORT: 443
CUSTOMER_NAME: "CUSTOMER_NAME"
# this keep "yaml"
VCO_AUTHENTICATION: "yaml"


##########################################################################################
#               HOW to get and set VCO_TENANT_ID
##########################################################################################
# https://vco206-fra1.velocloud.net/ui/msp/customers/5/sd-wan/monitor/edges/7/overview
# above is VCO_TENANT_ID: 5(required), edge id is 7(not required in yaml file)
VCO_TENANT_ID:  5


##########################################################################################
#               HOW to get and set VCO_TOKEN
##########################################################################################
# get it from GUI VCO,  generate TOKEN (EE or LE sme can help you with that or look to this HOW to page:
https://docs.vmware.com/en/VMware-Cloud-services/services/Using-VMware-Cloud-Services/GUID-E2A3B1C1-E9AD-4B00-A6B6-88D31FCDDF7C.html

# this is how to set it:
VCO_TOKEN: 'generated_vco_token_sure_this_is_example_and_not_valid_token'


##########################################################################################
#               HOW to set PROXY_STATE
##########################################################################################
# PROXY_STATE: True  ====> it should be used in case script is running from company network network
# PROXY_STATE: False ====> it should be used in case script is running from LAB or home where is not proxy
# If PROXY_STATE: False, it should be used outside of at&t network (LAB for example)
PROXY_STATE: True
PROXY_SERVER: "http://sub.proxy.att.com:8080"
```



### VERIFICATION OF THE CODE
```
Execute the command:
python3 velocloud.p --customer cust1 show-vco-info

In this case I had balab_vco_config.yaml in authentication folder and I called it: 
Sure you can have many different custx_vco_config.yaml in that folder and run scripts against that specific customer. 

------------------------------------------------------------------------------------------------------------------------
Command executed: python3 velocloud.py --customer balab show-vco-info
------------------------------------------------------------------------------------------------------------------------
Collecting info via API calls:
APIs 2/2: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:03<00:00,  1.78s/API call]
Login to VCO https://vco206-fra1.velocloud.net:443 was success.
------------------------------------------------------------------------------------------------------------------------
Customer details:
------------------------------------------------------------------------------------------------------------------------
Tenant name: Bratislava MSDE POC Lab
Tenant id: 5
LogicalId(API2): 0fc2d206-83ea-4258-93ec-00df6644834c
Tenant created: 2018-09-07T11:20:43.000Z
Tenant accountNumber: BRA-LAB-ABL
Tenant contactName: Peter Mraz
Tenant contactEmail: pm7625@att.com
Tenant streetAddress: Tomasikova 64/A
Tenant city: Bratislava
Tenant country: Slovak Republic
------------------------------------------------------------------------------------------------------------------------
Customer is part of MSP:
------------------------------------------------------------------------------------------------------------------------
MSP type: MSP
MSP name: AT&T Test
MSP domain: ATTTest
------------------------------------------------------------------------------------------------------------------------
Tenant details:
Edges:       Total: 12 ,Activated: 12 ,Connected 8 ,Degraded 0 ,Down 4 ,UpToDate 12
Hubs:        Total: 5 ,Activated: 5 ,Connected 5 ,Degraded 0 ,Down 0
Links:       Total: 22 ,Stable: 22 ,Unstable 0 ,Down 0
HubLinks:    Total: 10 ,Stable: 10 ,Unstable 0 ,Down 0
HA:          Total: 2 ,Pending: 0 ,Ready 2 ,Failed 0
VNFs:        Total: 0 ,On: 0 ,Off 0 ,Error 0
------------------------------------------------------------------------------------------------------------------------

Api Calls: 2
Api Calls per second: 0.67
Time of processing: 3.6
```

### SECURE-CRT

```
It is recommended to have Character Code in Secure CRT set to UTF-8
Session Options -> Terminal -> Appearance -> Character Encoding - > Set to UTF-8
Otherwise some outputs may be printed well
```


### SCRIPT BACKGROUND

```
look to:
base/api_class.py where are functions and there is API definition
cbase/lick_main_functions.py is where you have you show-vco-info commands and many more can be added. 
```

### SCRIPT - HELP (click)

```
python3 velocloud.py --customer balab --help
(venv) pm7625@SKLSPMAC007 git_velo_sdwan % python3 velocloud.py --customer balab --help
Usage: velocloud.py [OPTIONS] COMMAND [ARGS]...

  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  Tool built by Peter Mraz - SDNEE, at&t. Version 1.0.0
  It helps to gather details from vco, configure vco, get config/CSVs and any API in nice table format from vco.
  All can be exported to CSV or txt file. For more details use help of specific command.
  
  Each command also has option for --help:
  python3 velocloud.py --customer cust1 --help  
  or
  python3 velocloud.py --help

  Find what other options/sub-commands are within main command, also with help command: 
  Example:                                                             
  python3 velocloud.py --customer customer1 aar --help                                    
  python3 velocloud.py --customer customer1 alarm --help                            
  
  Most of main commands also got sub-commands. Those are usually self-explenationary, if not reach owner Peter Mraz. 
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Options:
  --customer TEXT  cust1, cust2 (cust1_vco_config.yaml or
                   cust2_vco_config.yaml)
  --help           Show this message and exit.

Commands:
  show-vco-info  ...
```

or more specific

```
(venv) pm7625@SKLSPMAC007 git_velo_sdwan % python3 velocloud.py --customer balab show-vco-info --help
Usage: velocloud.py show-vco-info [OPTIONS]

  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  SHOW-vco-INFO - This command is showing details about vco, version, account. 

  ----------------------------------------------------------------------------   
  Example:
  ----------------------------------------------------------------------------
  python3 velocloud.py --customer customer1 show-vco-info
  
  ----------------------------------------------------------------------------   
  Output:
  ----------------------------------------------------------------------------
  Outpu is just on the screen. 
  
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Options:
  --help  Show this message and exit.
  
```


more to come, stay tuned ....
