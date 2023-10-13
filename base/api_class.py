#! /usr/bin/env python
from .basic_functions import *
from .py_modules import *
import logging

from tabulate import *
from datetime import datetime, timedelta, date




# --------------------------------------------------------------------------------------------------
#              other small functions, not API related
# --------------------------------------------------------------------------------------------------

API_CALL_LIMIT = 5
API_CALL_PERIOD = 1
API_MAX_TRIES = 3

basic_path = os.getcwd()


#onboarding, read file, set some tuff. Only YAML format is allowed. 

class Api_calls:
    def __init__(self, customer):
        path = basic_path + "/authentication/" + customer #+  "_vco_config.yaml"
        try:
            with open(path) as f:

                config = yaml.safe_load(f.read())
                VCO_HOST = config["VCO_HOST"]
                VCO_PORT = config["VCO_PORT"]
                VCO_TENANT_ID = config["VCO_TENANT_ID"]
                
                # Validate the value.
                if not validate_integer(VCO_TENANT_ID):
                    print("The value of the VCO_TENANT_ID must be an integer.Correct yaml file. Exiting...")
                    exit(1)
                # to do - tenant ID must be integer, and PROXY State must be True or False, nothing else. 
                VCO_AUTHENTICATION = config["VCO_AUTHENTICATION"]
                PROXY_STATE = config["PROXY_STATE"]
                # Validate the value.
                if not validate_boolean(PROXY_STATE):
                    print("The value of the PROXY_STATE must be False or True..Correct yaml file. Exiting...")
                    exit(1)
                    
    
                PROXY_SERVER = config["PROXY_SERVER"]                
                VCO_AUTHENTICATION = config["VCO_AUTHENTICATION"]
                VCO_TOKEN = config["VCO_TOKEN"]
                VCO_SUFIX = "/portal/"
                if VCO_AUTHENTICATION == "yaml":
                    VCO_TOKEN = config["VCO_TOKEN"]

          
                else:    
                    print(colored("VCO_AUTHENTICATAION in yaml file is not in right format. Only options is for now yaml. Script is exiting....", 'red'))
                    print("maybe in the future username/password and mechID will be added. ")
                    exit(0)

        except IOError:
            print("-" * 120)
            print("Not correct customer/VCO_config.yaml file.") 
            print("-" * 120)
            exit(0)
            

        if VCO_TENANT_ID is None or VCO_HOST is None or PROXY_STATE is None or PROXY_SERVER is None or VCO_PORT is None or VCO_TOKEN is None:
            print("YAML file must be properly filled, otherwise scripts ends. Details are inside cust1_vco_config.yaml. Required: VCO_TENANT_ID,  VCO_HOST, PROXY_STATE, PROXY_SERVER, VCO_PORT, VCO_TOKEN")
            exit(0)

        # API for authentication, construct base_url of VCO
# --------------------------------------------------------------------------------------------------
# REST variables
# --------------------------------------------------------------------------------------------------

        self.VCO_HOST = VCO_HOST
        self.VCO_PORT = VCO_PORT
        self.VCO_TOKEN = VCO_TOKEN
        self.PROXY_STATE = PROXY_STATE
        self.PROXY_SERVER = PROXY_SERVER
        self.VCO_SUFIX = VCO_SUFIX
        self.VCO_TENANT_ID = VCO_TENANT_ID
        self.yaml_login_file = config
        self.API_CALL_LIMIT = 3
        self.API_CALL_PERIOD = 1
        self.API_MAX_TRIES = 3

        self.base_url = "https://%s:%s"%(self.VCO_HOST, self.VCO_PORT)
        

        
        # TODO - > complete this function.
        

        #---------------------------------------------------------------------------------------------------------------------
        # description of API:API will get list of Edges for specific tenant 
        self.getEnterpriseEdges_API = "/portal/rest/enterprise/getEnterpriseEdges"
        self.getEnterpriseEdges_JSON_BODY = {
                            "enterpriseId": int(self.VCO_TENANT_ID),
                            "with": ["site", "links", "configuration",
                                    "cloudServices", "wan",
                                    "nvsFromEdge", "certificates", "licenses"]
                    }
        self.getEnterpriseEdges_header = ['id']
        self.getEnterpriseEdges_header_readable = ['id']
        # keys:
        # Index(['id', 'created', 'enterpriseId', 'enterpriseLogicalId', 'siteId',
        #     'activationKey', 'activationKeyExpires', 'activationState',
        #     'activationTime', 'softwareVersion', 'buildNumber',
        #     'factorySoftwareVersion', 'factoryBuildNumber',
        #     'platformFirmwareVersion', 'platformBuildNumber',
        #     'modemFirmwareVersion', 'modemBuildNumber', 'softwareUpdated',
        #     'selfMacAddress', 'deviceId', 'logicalId', 'serialNumber',
        #     'modelNumber', 'deviceFamily', 'lteRegion', 'name', 'dnsName',
        #     'description', 'alertsEnabled', 'operatorAlertsEnabled', 'edgeState',
        #     'edgeStateTime', 'isLive', 'systemUpSince', 'serviceUpSince',
        #     'lastContact', 'serviceState', 'endpointPkiMode', 'haState',
        #     'haPreviousState', 'haLastContact', 'haSerialNumber', 'bastionState',
        #     'modified', 'customInfo', 'haMode', 'standbySystemUpSince',
        #     'standbyServiceUpSince', 'standbySoftwareVersion',
        #     'standbyFactorySoftwareVersion', 'standbyFactoryBuildNumber',
        #     'standbyBuildNumber', 'standbyModelNumber', 'standbyDeviceId', 'isHub',
        #     'site', 'links', 'cloudServices', 'certificates', 'licenses',
        #     'configuration', 'nvsFromEdge'],
        #     dtype='object')
        #---------------------------------------------------------------------------------------------------------------------
        # description of API:API will get list of Edges for specific tenant 
#         keys=["name", "id", "modelNumber", "softwareVersion", "dnsName",  "description", "serviceState", "haMode", "isHub", "customInfo", 'description']
    
        self.getEnterprise_API = "/portal/"        
        self.getEnterprise_JSON_BODY =  {
        "id": self.VCO_TENANT_ID,
        "jsonrpc": "2.0",
        "method": "enterprise/getEnterprise",
        "params": {
            "id": self.VCO_TENANT_ID,
            "with": [
            "enterpriseProxy"
            ]
        }
        }
        self.getEnterprise_header = ['id','networkId','name',]
        self.getEnterprise_header_readable = ['id','networkId','name',]
        # keys:
        # Index(['id', 'created', 'networkId', 'gatewayPoolId', 'alertsEnabled',
        #    'operatorAlertsEnabled', 'endpointPkiMode', 'name', 'domain', 'prefix',
        #    'logicalId', 'accountNumber', 'description', 'contactName',
        #    'contactPhone', 'contactMobile', 'contactEmail', 'streetAddress',
        #    'streetAddress2', 'city', 'state', 'postalCode', 'country', 'lat',
        #    'lon', 'timezone', 'locale', 'bastionState', 'modified',
        #    'enterpriseProxy'],
        #   dtype='object')

        #---------------------------------------------------------------------------------------------------------------------
        self.getNetworkOverviewInfo_API = "/portal/"  
        # id is the most likely what type of API call, hard to say :)    
        self.getNetworkOverviewInfo_JSON_BODY =  {
          "id": 7,
          "jsonrpc": "2.0",
          "method": "enterprise/getNetworkOverviewInfo",
          "params": {
            "enterpriseId": self.VCO_TENANT_ID
          }
        }
        # response 
        # {
        #   "jsonrpc": "2.0",
        #   "result": {
        #     "edges": {
        #       "total": 15,
        #       "activated": 12,
        #       "connected": 8,
        #       "degraded": 0,
        #       "down": 4,
        #       "upToDate": 12
        #     },
        #     "hubs": {
        #       "total": 5,
        #       "activated": 5,
        #       "connected": 5,
        #       "degraded": 0,
        #       "down": 0
        #     },
        #     "links": {
        #       "total": 23,
        #       "stable": 22,
        #       "unstable": 0,
        #       "down": 1
        #     },
        #     "hubLinks": {
        #       "total": 11,
        #       "stable": 10,
        #       "unstable": 0,
        #       "down": 1
        #     },
        #     "vnfs": {
        #       "total": 0,
        #       "on": 0,
        #       "off": 0,
        #       "error": 0
        #     },
        #     "ha": {
        #       "total": 3,
        #       "pending": 1,
        #       "ready": 2,
        #       "failed": 0
        #     }
        #   },
        #   "id": 7
        # }
        #---------------------------------------------------------------------------------------------------------------------
        
         
                
##################################
# VCO API:
##################################

                    
# --------------------------------------------------------------------------------------------------
# post API - Velocloud VCO, INPUST is JSON, TOKEN. 
# --------------------------------------------------------------------------------------------------

# used 
    @sleep_and_retry
    @on_exception(expo, ConnectionError, max_tries=API_MAX_TRIES)
    @limits(calls=API_CALL_LIMIT, period=API_CALL_PERIOD)
    def post_api(self, API, data):
        
        # PROXIES and VCO_TOKEN is taken from yaml file. 
        PROXIES = {
            "http": self.PROXY_SERVER,
            "https": self.PROXY_SERVER
        }
        token_error = 0
        headers = {'Authorization': 'Token '+self.VCO_TOKEN}  
        warnings.simplefilter('ignore', InsecureRequestWarning)
        
        # this is used If we are testing it from at&t 
        if self.PROXY_STATE == True:
            response = requests.post(f"{self.base_url}" + API , verify=False, json=data, proxies=PROXIES, headers=headers, timeout=600)
            
            
        # this is used If we are testing it from at&t 
        elif self.PROXY_STATE == False:
            response = requests.post(f"{self.base_url}" + API , verify=False, json=data, headers=headers, timeout=600)

        
        else:
            print("PROXY_STATE in YAML file must be True or False. Exiting...")

        if response.status_code != 200:
            print("Response is wrong, maybe wrong API or content of API")
            return (response, False, "no dict")
        
        
        
        else:
            try:
                #b'{"id":5,"jsonrpc":"2.0","error":{"code":-32000,"message":"tokenError [credential for authentication missing]"}}'
                #print(response.content)
                response_content = response.content
                decoded_json_data = json.loads(response_content.decode())                                
                error = decoded_json_data["error"]["message"]
                if error == "tokenError [credential for authentication missing]":
                    print(colored("Token wrong, exiting the script, error:", 'red'), response_content)
                    #token_error = 1
                    return (False, False, False)
                    exit(0)

            except:
                #print("try with \"result\" failed")
                pass                
            try:
                try:
                    response_content = response.content
                    decoded_json_data = json.loads(response_content.decode())
                    decoded_json_data = replace_null_values_with_empty_string(decoded_json_data)
                    #print("try with \"result\" OK")                  
                    return (decoded_json_data, True, "dict")
                
                except:
                    #print("try with \"result\" failed")
                    pass
        
                try:
                    json_data = response.content
                    data_list = json.loads(json_data)
                    data_list = replace_null_values_with_empty_string(data_list)
                    df = pandas.DataFrame(data_list)
                    df = df.fillna("")
                    return (df, True, "pandas")
                except:
                    #print("try without \"result\" failed")
                    pass
                return (df, True, "no dict")
            except:
                return (response, True, "other")
        

    
# used       
    @sleep_and_retry
    @on_exception(expo, ConnectionError, max_tries=API_MAX_TRIES)
    @limits(calls=API_CALL_LIMIT, period=API_CALL_PERIOD)
    def show_vco_info_user(self):
        (df, is_jason_status)= self.get_api_only_arg(self.api_client_server_info)
        VCO_name = df['data']['server']
        tenancyMode = df['data']['tenancyMode']
        user = df['data']['user']
        description = df['data']['description']
        roles = df['data']['roles']
        platformVersion = df['data']['platformVersion']
        print("\nVCO:",colored(VCO_name,'green'),  " Tenancy Mode",  colored(tenancyMode,'green'), ", Username:",  colored(user,'green'), ", User:", colored(description,'green'),", Role:", colored(roles,'green'), ", vMange version:", colored(platformVersion,'green')) 
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(colored("Date and time:",'red'), dt_string, "CET\n\n")	    
        print(colored("I'm running the script, hold on and be patient please. It may take few seconds.\n\n", 'blue'))
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'magenta'))
        print(colored("~~~~~~  All configuration related details are in configuration customer specific yaml file in authentication folder (example cust1_vco_config.yaml  ~~~~~~~~", 'magenta'))
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'magenta'))
        



# used          
    @sleep_and_retry
    @on_exception(expo, ConnectionError, max_tries=API_MAX_TRIES)
    @limits(calls=API_CALL_LIMIT, period=API_CALL_PERIOD)
    def get_api_keys(self, API):
        sess = self.sess
        get_api_url = self.base_url + API

        warnings.simplefilter('ignore', InsecureRequestWarning)
        staging_get_url_json = sess.get(url=get_api_url, verify=False)
        if staging_get_url_json.status_code != 200:
            print('-' * 120)
            print("API you provided is wrong, code is:", staging_get_url_json.status_code)
            print('-' * 120)
            exit(0)
        (get_api_json, is_jason_status) = self.is_json(staging_get_url_json.content)
        if get_api_json != False and is_jason_status != False:
            data = get_api_json['data']
            df = pandas.DataFrame(data)
            df_index = df.keys()
            keys_list = df_index.tolist()
            keys_str = str(keys_list)
            keys_str = keys_str.replace('\'', '\"')   
            #print(key_list_str)
            return  (keys_list, keys_str)  
        else: 
            print("something went wrong, maybe API or something else")  


# --------------------------------------------------------------------------------------------------
# get_api - get system_ip based on the hostname
# class Api_calls
# --------------------------------------------------------------------------------------------------
#used 
    @sleep_and_retry
    @on_exception(expo, ConnectionError, max_tries=API_MAX_TRIES)
    @limits(calls=API_CALL_LIMIT, period=API_CALL_PERIOD)
    def get_devices_info(self, device_type, api_calls):

        (get_api_json_models, is_jason_status_models) = self.get_api_only_arg(self.device_models)
        api_calls = api_calls + 1
        (get_api_json, is_jason_status) = self.get_api_only_arg(self.api_device_list_staging)
        api_calls = api_calls + 1
        (get_api_json2, is_jason_status2) = self.get_api_only_arg(self.api_devices)
        api_calls = api_calls + 1
        data = get_api_json
        data2 = get_api_json2
        data3 = get_api_json_models

        devices = []
        devices = [{key: device.get(key, "N/A") for key in self.api_device_list_staging_header} for device in data["data"]]
        devices2 = []
        devices2 = [{key: device.get(key, "N/A") for key in self.api_devices_header} for device in data2["data"]]
        devices3 = []
        devices3 = [{key: device.get(key, "N/A") for key in self.device_models_header} for device in data3["data"]]


        df = pandas.DataFrame(devices)
        df2 = pandas.DataFrame(devices2)
        df_models = pandas.DataFrame(devices3)
        df_original = df

        df_original = pandas.merge(df_original, df2, how="left", on=["system-ip"])
        df_original = df_original.sort_values(by='host-name', ascending=True)
        df_original = df_original.loc[df_original['reachability'] == 'reachable']
        df_original = df_original.reset_index(drop=True)

        
        loop = df_original.shape[0]
        device_info_row = []
        device_info = []
        vedge_inside = 0
        cedge_inside = 0
        mix_devices = 0
                
        df_new = df_original
        df_new['device_class'] = ''
        i = 0
        while i < loop:
            current_device_model = df_original.loc[i, 'deviceModel']
            current_device_class = df_models[df_models['name']==str(current_device_model)]['templateClass'].item()  
            df_new.loc[i, 'device_class'] = current_device_class

            i += 1 # move to the next row

        return df_new   









# --------------------------------------------------------------------------------------------------
# get_api - with API defined in OS
# class Api_calls
# --------------------------------------------------------------------------------------------------

#used 
    @sleep_and_retry
    @on_exception(expo, ConnectionError, max_tries=API_MAX_TRIES)
    @limits(calls=API_CALL_LIMIT, period=API_CALL_PERIOD)
    def get_api_only_arg(self, API):
        get_api_json = {}
        is_jason_status = True
        get_api_url = self.base_url + API
        sess = self.sess
        warnings.simplefilter('ignore', InsecureRequestWarning)
        staging_get_url_json = sess.get(url=get_api_url, verify=False)
        if staging_get_url_json.status_code != 200:
            if staging_get_url_json.content == None:
                print("API you provided is wrong :", staging_get_url_json.status_code)
                return (staging_get_url_json.status_code, False, )
            else:
                return (staging_get_url_json.content, False)
 
        (get_api_json, is_jason_status) = self.is_json(staging_get_url_json.content)
        return (get_api_json, is_jason_status)

        
    @sleep_and_retry
    @on_exception(expo, ConnectionError, max_tries=API_MAX_TRIES)
    @limits(calls=API_CALL_LIMIT, period=API_CALL_PERIOD)
    def get_api_only_arg_body(self, API, BODY_JSON):
        get_api_url = self.base_url + API
        sess = self.sess
        warnings.simplefilter('ignore', InsecureRequestWarning)
        
        staging_get_url_json = sess.get(url=get_api_url, data=BODY_JSON , verify=False)
        
        if staging_get_url_json.status_code != 200:
            print('-' * 120)
            print("API you provided is wrong, code is:", staging_get_url_json.status_code)
            print('-' * 120)
            exit(0)
        (get_api_json, is_jason_status) = self.is_json(staging_get_url_json.content)
        if is_jason_status == True:
            return (get_api_json, is_jason_status)
        if is_jason_status == False:
            return (get_api_json, is_jason_status)

    


# --------------------------------------------------------------------------------------------------
# VCO info function
# class Api_calls
# --------------------------------------------------------------------------------------------------


    def vco_info_f(self):
        
        
        
        #sess = self.sess
        warnings.simplefilter('ignore', InsecureRequestWarning)
        
        (get_api_json, is_jason_status) = self.get_api_only_arg(self.api_organization)
        data_org = get_api_json
        devices = []
        devices = [{key: device.get(key, "N/A") for key in self.api_organization_header}
                   for device in data_org["data"]]
        df_org = pandas.DataFrame(devices)
        warnings.simplefilter('ignore', InsecureRequestWarning)
        (get_api_json, is_jason_status) = self.get_api_only_arg(self.api_smartaccount)
        data = get_api_json
        devices = []
        devices = [{key: device.get(key, "N/A") for key in self.api_smartaccount_header}
                   for device in data["data"]]
        df_sa_va = pandas.DataFrame(devices)
        return (df_org, self.api_organization_header, df_sa_va, self.api_smartaccount_header)



# --------------------------------------------------------------------------------------------------
# is it json ? function
# class Api_calls
# --------------------------------------------------------------------------------------------------


    def is_json(self, myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            return myjson, False
        return json_object, True





    # @sleep_and_retry
    # @on_exception(expo, ConnectionError, max_tries=API_MAX_TRIES)
    # @limits(calls=API_CALL_LIMIT, period=API_CALL_PERIOD)
    # def post_device(self, API, data):
    #     sess = self.sess
    #     i = 0
    #     url = self.base_url + API
    #     warnings.simplefilter('ignore', InsecureRequestWarning)
    #     # print(url)
    #     # print(data)
    #     response = sess.post(url, headers=sess.headers, json=data, verify=False)
    #     if response.status_code != 200:
    #         i = 10
        
    #     (response, is_jason_status) = self.is_json(response.content)
    #     if is_jason_status == True:
    #         return (response, is_jason_status)
    #     if is_jason_status == False:
    #         return (response, is_jason_status)

    @sleep_and_retry
    @on_exception(expo, ConnectionError, max_tries=API_MAX_TRIES)
    @limits(calls=API_CALL_LIMIT, period=API_CALL_PERIOD)
    def post_device_d(self, API, data):
        sess = self.sess
        url = self.base_url + API
        warnings.simplefilter('ignore', InsecureRequestWarning)
        #sess = self.get_token()
        response = sess.post(url, headers=sess.headers, data=data, verify=False)
        if response.status_code != 200:
            print('-' * 120)
            print("API you provided is wrong, or device not connected to VCO, code is:", response.status_code)
            print(response.content)
            print('-' * 120)

        (response, is_jason_status) = self.is_json(response.content)
        if is_jason_status == True:
            return (response, is_jason_status)
        if is_jason_status == False:
            return (response, is_jason_status)


