from .api_class import *
from .basic_functions import *
from .py_modules import *
import urllib.parse
from tabulate import *
from datetime import datetime, timedelta, date
import xlsxwriter
import asyncio
import ssl
from aiohttp import ClientSession
# TODO ak confi file je empty ...nie je to osetrene
# TODO ADD IOS based APIs: # if device_model in vco_class.deviceModelEdges:



# --------------------------------------------------------------------------------------------------
# This script was built by Peter Mraz (pm7625@intl.att.com), SDNEE
# its for gathering details from VCO, potentially make changes.
# Its prohibited to share it outside of at&t and outside of Robert Hutchinson organization.
#
# Author is not guarantee functionality and not taking responsobility If you make changes in the script
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
#              To use this script, some python packages must be installed
#              Once you install packages, you can start to use the script.
# --------------------------------------------------------------------------------------------------
@ click.group()
@ click.option('--customer', help="cust1, cust2 (cust1_vco_config.yaml or cust2_vco_config.yaml)")
def cli(customer):
    
    """
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Tool built by Peter Mraz - SDNEE, at&t. Version 1.0.0
    It helps to gather details from vco, configure vco, get config/CSVs and any API in nice table format from vco.
    All can be exported to CSV or txt file. For more details use help of specific command.
    \b
    Each command also has option for --help:
    python3 velocloud.py --customer cust1 --help  
    or
    python3 velocloud.py --help
    
    \b 
    Find what other options/sub-commands are within main command, also with help command: 
    Example:                                                             
    python3 velocloud.py --customer customer1 aar --help                                    
    python3 velocloud.py --customer customer1 alarm --help                            
    \b
    Most of main commands also got sub-commands. Those are usually self-explenationary, if not reach owner Peter Mraz. 
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    
    pass
    global CUSTOMER_FILE 
    global CUSTOMER_FILE_DATA
    global CUSTOMER_NAME
    global outputs_path
    global vco_config
    global CUSTOMERS
    global CUSTOMER
    CUSTOMERS = []
    vco_config_files = []
    path = os.getcwd() + "/authentication"
    path_data = os.getcwd() + "/data"
    if customer == None:

        for r, d, f in os.walk(path):
            for files in f:
                if files != '.DS_Store': 
                    vco_config_files.append(files)
        vco_config_files = sorted(vco_config_files)
        if (len(vco_config_files)) == 1:
            CUSTOMER_FILE = vco_config_files[0]
            
        else:
            print("-" * 120)
            print("More than one vco_config.yaml file exist in authentication folder. Please use --customer or pick one of these:")
            print("If file name is named cust1_vco_config.yaml, use command python velocloud.py --customer cust1 show-vco-info ")
            print("-" * 120)
            CUSTOMERS = []
            final_files = []
            for vco_config_file in vco_config_files:
                new_path = os.getcwd() + "/authentication/" + vco_config_file  
                if vco_config_file != '.DS_Store':    
                    if os.path.isfile(new_path):
                        try:
                            with open(new_path) as f:
                                config = yaml.safe_load(f.read())
                                CUSTOMER_NAME = config["CUSTOMER_NAME"] 
                                CUSTOMERS.append(CUSTOMER_NAME)
                                final_files.append(new_path)
                                
                        except Exception as e:
                            raise_except(e)                      
                            
            print("+" * 60)
            print(f"{'  ':<2}{'  '}{'Customer':<30}{'vco_config.yaml file':<70}")   
            print("+" * 60)   
            for count, customer in enumerate(CUSTOMERS):
                #print(count,":", customer, "[",vco_config_files[count],"]")
                print(f"{count:<2}{': '}{customer:<30}{vco_config_files[count]:<70}")
            exit_n = count + 1
            print(f"{exit_n:<2}{': '}{'Exit'}")
            

            
            
            
            try:
                customer_number = int(input("Choose customer from above (press 0-{}):".format(count)))	
            except ValueError:
                print("-" * 120)
                print("Not proper number. Exiting.") 
                print("-" * 120)
                exit(0)
            
            if customer_number == exit_n:
                print("Exiting...")
                exit(0)
                
            elif customer_number > count:
                print("-" * 120)
                print("Used number is not in range above. Exiting.") 
                print("-" * 120)
                exit(0)
                
            else:
                print("-" * 120)
                print("Onboarding customer:", CUSTOMERS[customer_number])
                print("-" * 120)

            CUSTOMER_FILE = vco_config_files[customer_number]
            outputs_path = create_folders(CUSTOMERS[customer_number], os.getcwd())
    else: 
        CUSTOMER_FILE = path + "/" + customer + "_vco_config.yaml"
        CUSTOMER_FILE_DATA = path_data + "/" + customer + "_data.yaml"
        CUSTOMER = customer
        try:
            with open(CUSTOMER_FILE) as f:
                config = yaml.safe_load(f.read())
            CUSTOMERS = config["CUSTOMER_NAME"] 
            CUSTOMER_FILE = customer + "_vco_config.yaml"
            outputs_path = create_folders(CUSTOMERS, os.getcwd())
            
        except Exception as e:
            raise_except(e)                 
    pass  

@click.command()
@click.option("--option", default="api-json-device", help="api-json-device(DEFAULT), api-json-vco")
@click.option("--filename", help="file name how json will be stored")
def get_api_json(option, filename):
    """ 
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    GET-API-JSON - This command is executing GET api calls and output is json.
    \b
    ----------------------------------------------------------------------------   
    Example:
    ----------------------------------------------------------------------------
    python3 velocloud.py --customer customer1  get-api-json
    --------------------------------------
    Argument parts:
    --------------------------------------
    --option 
        api-json-device         = API, device specific in format [dataservice/device/bfd/sessions?deviceId=] 
        api-json-vco        = API, vco specific in format [dataservice/device/hardwarehealth/detail]
    \b
    ----------------------------------------------------------------------------   
    Output:
    ----------------------------------------------------------------------------
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """ 
    try:
        startTime = time.time()
        vco_class = Api_calls(CUSTOMER_FILE)
        vco_class.show_vco_info_user() 
        api_calls = 3
        full_file_path = os.path.join(outputs_path + "/JASON_OUTPUTS/", filename)
        print("Command executed: python3 velocloud.py --customer", CUSTOMER, "get-api-keys")
        print(CUSTOMER_FILE)
        exit(0)
        
        
                    
        if option == "api-json-device":  
            hostname = input("Enter hostname based on vco:")
            is_empty = isNotBlank(hostname)
            api_to_be_processed = input("Enter api, device specific in format [dataservice/device/bfd/sessions?deviceId=] :")
            is_empty2 = isNotBlank(api_to_be_processed)


            if is_empty == True and is_empty2 == True:
                (system_ip, status, api_calls) = vco_class.get_system_ip(hostname, api_calls)

                if status == True:
                    api_to_be_processed = api_to_be_processed + system_ip
                    (api_to_be_processed_header, api_to_be_processed_header_str)  = vco_class.get_api_only_arg(api_to_be_processed)
                    api_calls
                    print(api_to_be_processed_header_str)
                else:
                    print(colored("Status is error, means the hostame was not found, the script is exiting...."), 'red')
                    exit(0)
                    
            else:
                print(colored("One of inputs is empty. ", 'red'))
            
        elif option == "api-json-vco":  
            api_to_be_processed = input("Enter api, vco specific in format [dataservice/system/device/vedges]:")
            is_empty = isNotBlank(api_to_be_processed)




            # (get_api_json, is_jason_status) = vco_class.get_api_only_arg(api + system_ips_reachable[i])
            # api_calls +=1     
            # if is_jason_status == False:
            #     print(colored("\n\n---------------------------------------------------------------------------------------------------------------", 'red'))
            #     print("The most likely API is wrong, as I got wrong output. Check If used API is OK for device type you defined in the file, issue with device:")
            #     print("Problematic hostname:", hostnames_reachable[i])
            #     print("Used API:", api)
            #     print("Device model:", device_model_reachable[i])
            #     print("Device class:", device_class_reachable[i])
            #     print("Please, fix API or look what is going on. Script is exiting.")
            #     print(colored("---------------------------------------------------------------------------------------------------------------", 'red'))
            #     exit(0)




            if is_empty == True:

                (get_api_json, is_jason_status)  = vco_class.get_api_only_arg(api_to_be_processed)
                api_calls +=1
                if is_jason_status != False:
                    #print(get_api_json)
                    
                    with open(full_file_path , "w") as json_file:
                        json.dump(get_api_json, json_file, indent=4)
                    print(f"JSON data has been saved to '{full_file_path}' in a nicely formatted way.")
                    
            else:
                print(colored("One of inputs is empty. ", 'red'))
         


        else:
            print("\nWrong argument.Check --help to verify arguments.....Exiting.\n") 
            exit(0)  


        time_seconds = time.time() - startTime
        time_seconds = int(time_seconds)
        if time_seconds == 0:
            time_seconds = 1
            
            
        print("\nApi Calls:", api_calls)
        print("Api Calls per second:", round(api_calls/time_seconds, 2))
        print("Time of processing:", round(time.time() - startTime, 2))
        
    except Exception as e:
        raise_except(e)
    finally:
        try:
            vco_class.logut()
        except Exception as e:
            pass
        raise SystemExit
    



@click.command()
@click.option("--option", default="api-keys-device", help="api-keys-device(DEFAULT), api-keys-vco")
def get_api_keys(option):
    """ 
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    GET-API-KEYS - This command is executing GET api calls and output are keys in string format which can be later use. [helping script only]
    \b
    ----------------------------------------------------------------------------   
    Example:
    ----------------------------------------------------------------------------
    python3 velocloud.py --customer customer1  get-api-keys
    --------------------------------------
    Argument parts:
    --------------------------------------
    --option 
        api-keys-device     = API, device specific in format [dataservice/device/bfd/sessions?deviceId=] 
        api-keys-vco        = API, vco specific in format [dataservice/device/hardwarehealth/detail]
    \b
    ----------------------------------------------------------------------------   
    Output:
    ----------------------------------------------------------------------------
    Output is string of keys what later can be used in the script, in case can be simplified or filtered. 
    ["src-ip", "dst-ip", "color", "vdevice-name", "src-port", "system-ip", "dst-port", "site-id", "transitions", "vdevice-host-name", "local-color", "uptime", "detect-multiplier", "vdevice-dataKey", "proto", "lastupdated", "state", "tx-interval", "uptime-date"]
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """ 
    try:


        startTime = time.time()
        vco_class = Api_calls(CUSTOMER_FILE)
        api_calls = 0


        print("-" *120)
        print("Command executed: python3 velocloud.py --customer", CUSTOMER, "get-api-keys")
            
        try:
            api_processed = vco_class.getEnterpriseEdges_API
            json_processed = vco_class.getEnterpriseEdges_JSON_BODY
            print("-" *120)
            print("api to be processed:", api_processed)
            print("-" *120)
            print("JSON body to be processed:", json.dumps(json_processed, indent=4))
            print("-" *120)
            (data, status, data_type) =  vco_class.post_api(api_processed, json_processed)
            api_calls += 1
            if status == True and data_type == "dict":

                print("Keys for dictionary:")

                keys = set()  # Create an empty set to store unique keys
                for item in data:
                    keys.update(item.keys())

                # Convert the set of keys to a list if needed
                key_list = list(keys)

                # Print the list of keys
                print(key_list)

            elif status == True and data_type == "pandas": 
                 print("Keys for dictionary:")
                 print(data.columns)
                                
            elif status == True and data_type == "no dict":            
                print(type(data))
            elif status == False:
                print(type(data))
            


        except TypeError:
            print("Error code: TypeError")
            raise SystemExit


        time_seconds = time.time() - startTime
        time_seconds = int(time_seconds)
        if time_seconds == 0:
            time_seconds = 1
            
            
        print("\nApi Calls:", api_calls)
        print("Api Calls per second:", round(api_calls/time_seconds, 2))
        print("Time of processing:", round(time.time() - startTime, 2))
        
    except Exception as e:
        raise_except(e)
    

@click.command()
@click.option("--option", default="vco", help="vco, device")    
def show_api_help(option):
    """ 
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    SHOW-API - This command is showing API calls which can be used for other functions. 
    Example: dataservice/device/hardwarehealth/detail
    \b
    ----------------------------------------------------------------------------
    Argument parts:
    ----------------------------------------------------------------------------
    --option                    
        vco                 = Show list of all vco APIs which later can be used for get-api-vco_csv function
        device-vedge            = Show list of all device APIs which later can be used for get-api-device-csv function
        device-cedge            = Show list of all device APIs which later can be used for get-api-device-csv function
    \b
    ----------------------------------------------------------------------------   
    Example:
    ----------------------------------------------------------------------------
    python3 velocloud.py --customer customer1  show-api --option vco
    \b
    ----------------------------------------------------------------------------   
    Output:
    ----------------------------------------------------------------------------
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """ 
    try:
        startTime = time.time()
        vco_class = Api_calls(CUSTOMER_FILE)
        vco_class.show_vco_info_user() 
        api_calls = 3
        print("Command executed: python3 velocloud.py --customer", CUSTOMER, "show-api --option", option)
        if option == "vco":
            print(colored("This is list of all vco specific API calls", 'green'))
            
        elif option == "device-vedge":
            print(colored("This is list of all device specific API calls", 'green'))
            
        elif option == "device-cedge":
            print(colored("This is list of all device specific API calls", 'green'))

        else:
            print(colored("Defined option is not correct, use vco or device. Exiting the script.", 'red')) 
            exit(0)

        time_seconds = time.time() - startTime
        time_seconds = int(time_seconds)
        if time_seconds == 0:
            time_seconds = 1
            
            
        print("\nApi Calls:", api_calls)
        print("Api Calls per second:", round(api_calls/time_seconds, 2))
        print("Time of processing:", round(time.time() - startTime, 2))
    


    except Exception as e:
        raise_except(e)
        

    
    finally:
        try:
            vco_class.logut()
        except Exception as e:
            pass
        raise SystemExit
    

    
# TODO :  more APIs - defined in the file 
@click.command()
@click.option("--api", help="use API in format \"dataservice/device/bfd/sessions?deviceId=\"")
@click.option("--csv_filename", help="bfd_sessions")
@click.option("--hostnames-filename", help="hostname od device (from vco), in txt file, separated by spaces, columns, or semicolons. Files are in folder USERS_INPUTS. ")
def get_api_devices_csv(api, csv_filename, hostnames_filename):
    """ 
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    GET-API-DEVICES-CSV - This command is executing GET api call for devices deffined in the file. There can be one or more devices - hostnames. 
    File must be in folder USERS_INPUTS.
    It must be device API not vco global specific API. 
    Script do not support mixed enviroment where in file are both vEdges and cEdges, script is able to recognize it and it will stop and share what are vedges and cedges. 
    Script is also checking if hostnames are valid, if devices are reachable or unreachable. 
    \b
    Example of API: "dataservice/device/bfd/sessions?deviceId=
    \b
    ----------------------------------------------------------------------------
    Argument parts:
    ----------------------------------------------------------------------------
    --api                        = API in format: dataservice/device/bfd/sessions?deviceId=  [you can find APIs in REAL-TIME section in the vco under device]
                                   API docs: https://developer.cisco.com/docs/sdwan/
    --csv_filename               = String, what will be added into CSV file name. example :  "bfd_sessions_customer1_auttid". Output will be in this case 2023_04_21_11h_57m_bfd_sessions_customer1_auttid.csv
    --hostname_filename          = Name of the file, inside are exact hostname from vco. Hostnames inside the file can be separated by space(s), column, semicolon or TAB.
                                   File MUST be im folder USERS_INPUTS.  
                                   Example of file bfd_sessions_hostnames_customer1_auttid.txt
                                   S0001,S0002,S0003,S0003
                                   or 
                                   S0001 S0002 S0003 S0003
                                   or 
                                   S0001;S0002;S0003;S0003
    ----------------------------------------------------------------------------   
    Example:
    ----------------------------------------------------------------------------
    python3 velocloud.py --customer customer1  get-api-devices-csv --api "dataservice/device/bfd/sessions?deviceId=" --csv_filename bfd_sessions_customer1_AUTTID --hostnames_filename customer1_bfd_test.txt
    \b
    ----------------------------------------------------------------------------   
    Output:
    ----------------------------------------------------------------------------
    As for any other script, output is xlsx/csv/txt file and path and file name is showed at the end of the script. 
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """ 
    try:
        startTime = time.time()
        vco_class = Api_calls(CUSTOMER_FILE)
        #vco_class.show_vco_info_user() 
        api_calls = 3
        print("Command executed: python3 velocloud.py --customer", CUSTOMER, "get-api-devices-csv --api", '"' + str(api) + '"', "--hostnames_filename", hostnames_filename, "--csv_filename", csv_filename)

        if hostnames_filename == None:
            print(colored("Exit the script, argument hostname_filename is not defined. Be sure it is in folder USERS_INPUTS and you desfine entire file name. Example: ", 'red'))
            exit(0)
        
        elif csv_filename == None:
            print(colored("Exit the script, argument csv_filename is not defined.", 'red'))
            exit(0)

        elif api == None:
            print(colored("Exit the script, argument api is not defined.", 'red'))
            exit(0)

        users_input = basic_path + "/USERS_INPUTS/" + hostnames_filename
        try:
            df_hostnames = pandas.read_csv(users_input, sep='\s*[:,;]\s*|\s+|\t+|\t+\s+|\s*[,;|\t]\s*', header=None, engine='python')
            df_hostnames = df_hostnames.drop_duplicates()
        except Exception as e:
            print(colored("------------------------------------------------------------------------------", 'red'))
            print(colored("File do not exist or file name defined is not right, correct it.", 'red'))
            print(colored("------------------------------------------------------------------------------", 'red'))
            exit(0)
        lst = df_hostnames.values.tolist()
        hostnames = []
        invalid_hostnames = []
        for sublist in lst:
                hostnames.extend(sublist)
            
        # remove nan from the list 
        hostnames = [x for x in hostnames if isinstance(x, str)]

        
        (device_info, mix_devices, api_calls) = vco_class.get_system_ips(hostnames, api_calls)   
        api_calls +=1     
        i = 0
        loop = len(device_info)
        
        # Go over results print them.         
        hostnames_unreachable = []
        system_ips_unreachable = []
        hostnames_reachable = []
        system_ips_reachable = []
        hostnames_not_exists = []
        hostnames_cedges = []
        hostnames_vedges = []
        list_err = []
        device_model_reachable = []
        device_class_reachable = []
        df_exists = 0
        

                        
        if mix_devices == 1:
            
            while i < loop:
                if device_info[i][4] == "cedge":
                    hostnames_cedges.append(device_info[i][0])
                elif device_info[i][4] == "vedge":
                    hostnames_vedges.append(device_info[i][0])
                i += 1
            print(colored("\n\n----------------------------------------------------------------------------------------------------------------------------------------------------------", 'red'))
            print(colored("Inside file is mix of vedges and cedges, a lot of time API is different for those. Script is existing, correct the file and ensure one type is there. ", 'red'))
            print("These devices are cedges:\n", colored( ', '.join(hostnames_cedges), 'red'))
            print("These devices are vedges:\n", colored(', '.join(hostnames_vedges), 'red'))
            print(colored("----------------------------------------------------------------------------------------------------------------------------------------------------------", 'red'))
            exit(0)  
            
            
        
        
        while i < loop:
            if device_info[i][2] == "unreachable":
                hostnames_unreachable.append(device_info[i][0])
                system_ips_unreachable.append(device_info[i][1])
            elif device_info[i][2] == "reachable":
                hostnames_reachable.append(device_info[i][0])
                system_ips_reachable.append(device_info[i][1])
                device_model_reachable.append(device_info[i][3])
                device_class_reachable.append(device_info[i][4])
                
            else:
                hostnames_not_exists.append(device_info[i][0])       
            i += 1
        
        if len(hostnames_unreachable) != 0 or len(hostnames_not_exists) != 0:
            print(colored("\n\n---------------------------------------------------------------------------------------------------------------", 'red'))
        if len(hostnames_unreachable) != 0:
            print("These devices are unreachable, but hostname was recognized in vco:\n", colored( ', '.join(hostnames_unreachable), 'red'))
        if len(hostnames_not_exists) != 0:
            print("These devices are not recognized by vco based on the hostname:\n", colored(', '.join(hostnames_not_exists), 'red'))
        if len(hostnames_unreachable) != 0 or len(hostnames_not_exists) != 0:
            print(colored("---------------------------------------------------------------------------------------------------------------", 'red'))
        if len(hostnames_reachable) != 0:
            print(colored("\n\n---------------------------------------------------------------------------------------------------------------", 'green'))
            print("These devices are recognized by vco based on the hostname, also are reachable now, API will be collected:\n", colored(','.join(hostnames_reachable), 'green'))
            print(colored("---------------------------------------------------------------------------------------------------------------", 'green'))
        else:
            print("There is not valid hostname in file. Please correct it. Script is exiting.")
            exit(0)
            
        
                
            
        i = 0
        loop = len(hostnames_reachable)

        while i < loop:
            (get_api_json, is_jason_status) = vco_class.get_api_only_arg(api + system_ips_reachable[i])
            api_calls +=1     
            if is_jason_status == False:
                print(colored("\n\n---------------------------------------------------------------------------------------------------------------", 'red'))
                print("The most likely API is wrong, as I got wrong output. Check If used API is OK for device type you defined in the file, issue with device:")
                print("Problematic hostname:", hostnames_reachable[i])
                print("Used API:", api)
                print("Device model:", device_model_reachable[i])
                print("Device class:", device_class_reachable[i])
                print("Please, fix API or look what is going on. Script is exiting.")
                print(colored("---------------------------------------------------------------------------------------------------------------", 'red'))
                exit(0)

            # TODO : in case not deffined or wrong API is used in 1st itteration, it fails in another itterations
            #df = pandas.concat([df, df_temp])

            if get_api_json["data"]:

                if get_api_json != False and is_jason_status != False:
                    print(i + 1, " of " , loop ,  "Device processed:", hostnames_reachable[i],", device model:", device_model_reachable[i],  ", api called:", api + system_ips_reachable[i] )
                    data = get_api_json["data"]
    
                    if i == 0:
                        df = pandas.DataFrame(data)
                        df = convert_unix_timestamp(df)
                    elif df_exists != 1:
                        df = pandas.DataFrame(data)
                        df = convert_unix_timestamp(df)
                        
                    else:
                        df_temp = pandas.DataFrame(data)
                        df_temp = convert_unix_timestamp(df_temp)
                        df = pandas.concat([df, df_temp])
                    df_exists = 1

            else: 
                #print("Probably API is wrong as data is empty for device:", system_ips_reachable[i])
                print(i + 1, " of " , loop ,  colored("Device NOT success(maybe wrong API for particular device):", 'red'), colored(hostnames_reachable[i],'red'),", device model:", device_model_reachable[i],  ", api called:", api + system_ips_reachable[i] )
                str_error = system_ips_reachable[i]  + ";" + " something went wrong"
                list_err.append(str_error)   
                 
            i += 1
        if df_exists == 1:
            now = datetime.now()
            date_time_api1 = now.strftime("%Y-%m-%d %H:%M")
            df.insert(0, 'Date[UTC]', date_time_api1)
            save_dict_to_csv(df, csv_filename, outputs_path + "/DEVICES_API_CSV/")
        else:
            print("The most probably API is wrong as non of loop was success, or potentially for short period of the time device lost connection to vco.")
    
    
        time_seconds = time.time() - startTime
        time_seconds = int(time_seconds)
        if time_seconds == 0:
            time_seconds = 1
            
            
        print("\nApi Calls:", api_calls)
        print("Api Calls per second:", round(api_calls/time_seconds, 2))
        print("Time of processing:", round(time.time() - startTime, 2))



    except Exception as e:
        raise_except(e)
    finally:
        try:
            vco_class.logut()
        except Exception as e:
            pass
        raise SystemExit
    


    
# TODO :  more APIs - defined in the file 
@click.command()
@click.option("--api", help="use API in format \"dataservice/device/bfd/sessions?deviceId=\"")
@click.option("--csv_filename", help="bfd_sessions")
@click.option("--device_type", default="cedge", help="cedge(default), vedge, vbond, vsmart, vco")
def get_api_devices_all_csv(api, csv_filename, device_type):
    """ 
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    GET-API-DEVICES-ALL-CSV - This command is executing GET api call for all devices deffined via device_type, all which are reachable at the time. Used --api must be api 
    which works with specific device_type. 
    It must be device API not vco global specific API. 
    \b
    #TODO add example here
    Example of API: "dataservice/device/bfd/sessions?deviceId=
    \b
    ----------------------------------------------------------------------------
    Argument parts:
    ----------------------------------------------------------------------------
    --api                        = API in format: dataservice/device/bfd/sessions?deviceId=  [you can find APIs in REAL-TIME section in the vco under device]
                                   API docs: https://developer.cisco.com/docs/sdwan/
    --csv_filename               = String, what will be added into CSV file name. example :  "bfd_sessions_customer1_auttid". Output will be in this case 2023_04_21_11h_57m_bfd_sessions_customer1_auttid.csv
    --device_type                = in case cedge is used, must be used cedge API and it will run on all cEdge in the network
                                   in case vedge is used, must be used vedge API and it will run on all cEdge in the network
                                   in case vco is used, must be used vbond API and it will run on all vcos in the network (like status of vco, memory of vco etc)
                                   in case vbond is used, must be used vbond API and it will run on all vBonds in the network  (like status of vco, memory of vco etc)
                                   in case vbond is used, must be used vsmart API and it will run on all vSmarts in the network  (like status of vSmart, memory of vSmart etc)
                                   
    ----------------------------------------------------------------------------   
    Example:
    ----------------------------------------------------------------------------
    python3 velocloud.py --customer customer1  get-api-devices-all-csv --api "dataservice/device/bfd/sessions?deviceId=" --csv_filename bfd_sessions_customer1_AUTTID --device_type cedge
    \b
    ----------------------------------------------------------------------------   
    Output:
    ----------------------------------------------------------------------------
    As for any other script, output is xlsx/csv/txt file and path and file name is showed at the end of the script. 
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """ 
    try:
        startTime = time.time()
        vco_class = Api_calls(CUSTOMER_FILE)
        vco_class.show_vco_info_user() 
        system_ips_reachable = []
        list_err = []
        df_exists = 0
        api_calls = 3
        print("Command executed: python3 velocloud.py --customer", CUSTOMER, "get-api-devices-all-csv --api", '"' + str(api) + '"', "--device_type", device_type, "--csv_filename", csv_filename)
        if device_type == "vedge" or device_type == "cedge" or device_type == "vbond" or device_type == "vco" or device_type == "vsmart":
            pass

        elif csv_filename == None:
            print(colored("Exit the script, argument csv_filename is not defined.", 'red'))
            exit(0)

        elif api == None:
            print(colored("Exit the script, argument api is not defined.", 'red'))
            exit(0)
        else:
            print(colored("Exit the script, argument device_type is not right. Must be vedge or cedge, vbond, vsmart or vco.", 'red'))
            exit(0)
        

        if device_type == "vedge" or device_type == "cedge":
            device_info = vco_class.get_devices_info(device_type, api_calls)     
            device_info = device_info.loc[device_info['device_class'] == device_type]
            device_info = device_info.reset_index(drop=True)

        elif device_type == "vbond" or device_type == "vsmart" or device_type == "vco":
            device_info = vco_class.get_controllers_info(device_type, api_calls)   
            device_info = device_info.loc[device_info['deviceType'] == device_type]
            device_info = device_info.reset_index(drop=True)
            

        if device_info.shape[0] == 0:
            print(colored("Exit the script, --device_type resulted into zero output. The most likely there are not reachable device with deffined --device_type", 'red'))
            exit(0)
        

        # TODO: this must be finished     (vsmart, vbond and vco portion)
        i = 0
        
        list_err = []

        if device_type == "vedge" or device_type == "cedge":
            device_info = device_info.loc[device_info['reachability'] == 'reachable']
            device_info = device_info.reset_index()
            
        loop = device_info.shape[0]
        
        #print(device_info)
        
        while i < loop:
            if device_type == "vedge" or device_type == "cedge":
                system_ip = device_info.loc[i, 'system-ip']
            elif device_type == "vbond" or device_type == "vsmart" or device_type == "vco":
                system_ip = device_info.loc[i, 'deviceIP']

            # hint
            if device_type == "vedge" or device_type == "cedge":
                (get_api_json, is_jason_status) = vco_class.get_api_only_arg(api + device_info.loc[i, 'system-ip'])
                if is_jason_status == False:
                    print(colored("\n\n---------------------------------------------------------------------------------------------------------------", 'red'))
                    print("The most likely API is wrong, as I got wrong output. Check If used API is OK for device type you defined in the file, issue with device:")
                    print("Problematic hostname:", device_info.loc[i, 'host-name'])
                    print("Used API:", api)
                    print("Please, fix API or look what is going on. Script is exiting.")
                    print(colored("---------------------------------------------------------------------------------------------------------------", 'red'))
          
                
            elif device_type == "vbond" or device_type == "vsmart" or device_type == "vco":
                (get_api_json, is_jason_status) = vco_class.get_api_only_arg(api + device_info.loc[i, 'deviceIP'])
                
                if is_jason_status == False:
                    print(colored("\n\n---------------------------------------------------------------------------------------------------------------", 'red'))
                    print("The most likely API is wrong, as I got wrong output. Check If used API is OK for device type you defined in the file, issue with device:")
                    print("Problematic hostname:", device_info.loc[i, 'deviceIP'])
                    print("Used API:", api)
                    print("Please, fix API or look what is going on. Script is exiting.")
                    print(colored("---------------------------------------------------------------------------------------------------------------", 'red'))
          
                
            api_calls += 1


            if get_api_json["data"]:
                
                if get_api_json != False and is_jason_status != False:
                    if device_type == "vedge" or device_type == "cedge":
                        print(i + 1, " of " , loop ,  "Device processed:", device_info.loc[i, 'host-name'],", device model:", device_info.loc[i, 'deviceModel'],  ", api called:", api + device_info.loc[i, 'system-ip'])
                    elif device_type == "vbond" or device_type == "vsmart" or device_type == "vco":
                        print(i + 1, " of " , loop ,  "Device processed:", device_info.loc[i, 'host-name'],", device type:", device_info.loc[i, 'deviceModel'],  ", api called:", api + device_info.loc[i, 'deviceIP'])
                    data = get_api_json["data"]
                    
                    if i == 0:
                        df = pandas.DataFrame(data)
                        df = convert_unix_timestamp(df)
                    elif df_exists != 1:
                        df = pandas.DataFrame(data)
                        df = convert_unix_timestamp(df)
                    else:
                        df_temp = pandas.DataFrame(data)
                        df_temp = convert_unix_timestamp(df_temp)
                        df = pandas.concat([df, df_temp])
                    df_exists = 1

            else: 
                #print("Probably API is wrong as data is empty for device:", system_ips_reachable[i])
                if device_type == "vedge" or device_type == "cedge":
                    print(i + 1, " of " , loop ,  colored("Device NOT success(maybe wrong API for particular device):", 'red'), colored(device_info.loc[i, 'host-name'],'red'),", device model:", device_info.loc[i, 'deviceModel'],  ", api called:", api + device_info.loc[i, 'system-ip'])
                    str_error = device_info.loc[i, 'host-name'] + ";"  +  device_info.loc[i, 'system-ip']    + ";" + " something went wrong"
                elif device_type == "vbond" or device_type == "vsmart" or device_type == "vco":
                    print(i + 1, " of " , loop ,  colored("Device NOT success(maybe wrong API for particular device):", 'red'), colored(device_info.loc[i, 'host-name'],'red'),", device model:", device_info.loc[i, 'deviceModel'],  ", api called:", api + device_info.loc[i, 'deviceIP'])
                    str_error = device_info.loc[i, 'host-name'] + ";"  +  device_info.loc[i, 'deviceIP']    + ";" + " something went wrong"
                        
                list_err.append(str_error)   
                 
            i += 1
        if df_exists == 1:
            now = datetime.now()
            date_time_api1 = now.strftime("%Y-%m-%d %H:%M")
            df.insert(0, 'Date[UTC]', date_time_api1)
            save_dict_to_csv(df, csv_filename, outputs_path + "/DEVICES_API_CSV/")
        else:
            print("The most probably API is wrong as non of loop was success, or potentially for short period of the time device lost connection to vco.")

        time_seconds = time.time() - startTime
        time_seconds = int(time_seconds)
        if time_seconds == 0:
            time_seconds = 1
            
            
        print("\nApi Calls:", api_calls)
        print("Api Calls per second:", round(api_calls/time_seconds, 2))
        print("Time of processing:", round(time.time() - startTime, 2))
        

    except Exception as e:
        raise_except(e)
    finally:
        try:
            vco_class.logut()
        except Exception as e:
            pass
        raise SystemExit
    
      
    


@click.command()
# @click.option("--api", help="use API in format \"dataservice/device/hardwarehealth/detail\"")
def get_api_body():
    """ 
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    GET-API-vco-CSV - This command is executing GET api call defined by input against vco and export into CSV. It must be vco API not device specific API. 
    Example: dataservice/device/hardwarehealth/detail
    \b
    ----------------------------------------------------------------------------
    Argument parts:
    ----------------------------------------------------------------------------
    --api                       = API in format: dataservice/device/hardwarehealth/detail, it must be global vco API, not device specific. 
                                  API docs: https://developer.cisco.com/docs/sdwan/
    --csv_filename                  = File name, example "hardwarehealth", output will be in reality : 

    \b
    ----------------------------------------------------------------------------   
    Example:
    ----------------------------------------------------------------------------
    python3 velocloud.py --customer customer1  get-api-vco-csv --api "dataservice/device/hardwarehealth/detail" --csv_filename hardwarehealth

    \b
    ----------------------------------------------------------------------------   
    Output:
    ----------------------------------------------------------------------------
    As for any other script, output is xlsx/csv/txt file and path and file name is showed at the end of the script. 
    \b
    Output Writing to file:  /Customers_OUTPUTs/Customer1/vco_API_CSV/2023_04_21_11h_57m_hardwarehealth.csv
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """ 
    try:
        startTime = time.time()
        vco_class = Api_calls(CUSTOMER_FILE)
        vco_class.show_vco_info_user() 
        api_calls = 3
        print("Command executed: python3 velocloud.py --customer", CUSTOMER, "get-api-body")
        # api = "dataservice/statistics/system/aggregation"
        # BODY_JSON = {
        # "query": {
        #     "condition": "AND",
        #     "rules": [
        #     {
        #         "value": [
        #         "48"
        #         ],
        #         "field": "entry_time",
        #         "type": "date",
        #         "operator": "last_n_hours"
        #     },
        #     {
        #         "value": [
        #         "10.255.1.203"
        #         ],
        #         "field": "vdevice_name",
        #         "type": "string",
        #         "operator": "in"
        #     }
        #     ]
        # },
        # "aggregation": {
        #     "metrics": [
        #     {
        #         "property": "mem_util",
        #         "type": "avg"
        #     }
        #     ],
        #     "histogram": {
        #     "property": "entry_time",
        #     "type": "hour",
        #     "interval": 1,
        #     "order": "asc"
        #     }
        # }
        # }
        
        api = "dataservice/statistics/system"
        BODY_JSON = {
        "query": {
            "condition": "AND",
            "rules": [
            {
                "value": [
                "24"
                ],
                "field": "entry_time",
                "type": "date",
                "operator": "last_n_hours"
            },
            {
                "value": [
                "10.255.1.203"
                ],
                "field": "vdevice_name",
                "type": "string",
                "operator": "in"
            }
            ]
        },
        "fields": [
            "entry_time",
            "count",
            "cpu_user_new",
            "cpu_system"
        ],
        "sort": [
            {
            "field": "entry_time",
            "type": "date",
            "order": "asc"
            }
        ]
        }

        #BODY_JSON = json.load(BODY_JSON)
        #get_api_only_arg_body(self, API, BODY_JSON):
        (get_api_json, is_jason_status) = vco_class.post_device(api, BODY_JSON)
        api_calls +=1
        print(get_api_json)
        # if is_jason_status == True:
        #     save_dict_to_csv_json_insert_time(get_api_json, csv_filename, outputs_path + "/vco_API_CSV/")
        # else: 
        #     print(colored("Provided IP is not right, please correct it. ", 'red'))

        api_calls += 1
    
        time_seconds = time.time() - startTime
        time_seconds = int(time_seconds)
        if time_seconds == 0:
            time_seconds = 1
            
            
        print("\nApi Calls:", api_calls)
        print("Api Calls per second:", round(api_calls/time_seconds, 2))
        print("Time of processing:", round(time.time() - startTime, 2))
        
    except Exception as e:
        raise_except(e)
    finally:
        try:
            vco_class.logut()
        except Exception as e:
            pass
        raise SystemExit
    



@click.command()
@click.option("--api", help="use API in format \"dataservice/device/hardwarehealth/detail\"")
@click.option("--csv_filename", help="file name, there will be always date in front of the file \"hardwarehealth\"")
def get_api_vco_csv(api, csv_filename):
    """ 
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    GET-API-vco-CSV - This command is executing GET api call defined by input against vco and export into CSV. It must be vco API not device specific API. 
    Example: dataservice/device/hardwarehealth/detail
    \b
    ----------------------------------------------------------------------------
    Argument parts:
    ----------------------------------------------------------------------------
    --api                       = API in format: dataservice/device/hardwarehealth/detail, it must be global vco API, not device specific. 
                                  API docs: https://developer.cisco.com/docs/sdwan/
    --csv_filename                  = File name, example "hardwarehealth", output will be in reality : 

    \b
    ----------------------------------------------------------------------------   
    Example:
    ----------------------------------------------------------------------------
    python3 velocloud.py --customer customer1  get-api-vco-csv --api "dataservice/device/hardwarehealth/detail" --csv_filename hardwarehealth

    \b
    ----------------------------------------------------------------------------   
    Output:
    ----------------------------------------------------------------------------
    As for any other script, output is xlsx/csv/txt file and path and file name is showed at the end of the script. 
    \b
    Output Writing to file:  /Customers_OUTPUTs/Customer1/vco_API_CSV/2023_04_21_11h_57m_hardwarehealth.csv
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """ 
    try:
        if csv_filename == None:
                print(colored("Exit the script, argument csv_filename is not defined.", 'red'))
                exit(0)
        
        elif api == None:
                print(colored("Exit the script, argument api is not defined.", 'red'))
                exit(0)
            
        startTime = time.time()
        vco_class = Api_calls(CUSTOMER_FILE)
        vco_class.show_vco_info_user() 
        api_calls = 3
        print("Command executed: python3 velocloud.py --customer", CUSTOMER, "get-api-vco-csv --api", '"' + str(api) + '"', "--csv_filename", csv_filename)
            
        (get_api_json, is_jason_status) = vco_class.get_api_only_arg(api)
        api_calls +=1
        if is_jason_status == True:
            save_dict_to_csv_json_insert_time(get_api_json, csv_filename, outputs_path + "/vco_API_CSV/")
        else: 
            print(colored("Provided IP is not right, please correct it. ", 'red'))

        api_calls += 1
    
        time_seconds = time.time() - startTime
        time_seconds = int(time_seconds)
        if time_seconds == 0:
            time_seconds = 1
            
            
        print("\nApi Calls:", api_calls)
        print("Api Calls per second:", round(api_calls/time_seconds, 2))
        print("Time of processing:", round(time.time() - startTime, 2))
        
    except Exception as e:
        raise_except(e)
    finally:
        try:
            vco_class.logut()
        except Exception as e:
            pass
        raise SystemExit
    
    
@ click.command()
def show_vco_info():
    """ 
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    SHOW-vco-INFO - This command is showing details about vco, version, account. 

    \b
    ----------------------------------------------------------------------------   
    Example:
    ----------------------------------------------------------------------------
    python3 velocloud.py --customer customer1 show-vco-info
    \b
    ----------------------------------------------------------------------------   
    Output:
    ----------------------------------------------------------------------------
    Outpu is just on the screen. 
    \b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """ 
    try:
         
        startTime = time.time()
        vco_class = Api_calls(CUSTOMER_FILE)
        api_calls = 0
        call_number = 0
        num_api_calls = 2
        
        print("-" * 120)
        print("Command executed: python3 velocloud.py --customer", CUSTOMER, "show-vco-info")
        # hint - progress bar
        print("-" * 120)              
        print(colored("Collecting info via API calls:", 'green'))
        progress_bar = tqdm(total=num_api_calls, unit="API call")
        (data, status, data_type) =  vco_class.post_api(vco_class.getEnterprise_API, vco_class.getEnterprise_JSON_BODY)
        call_number = 1
        progress_bar.update(1)  # Update the progress bar
        progress_bar.set_description(f"APIs {call_number}/{num_api_calls}")

        (data2, status2, data_type2) =  vco_class.post_api(vco_class.getNetworkOverviewInfo_API, vco_class.getNetworkOverviewInfo_JSON_BODY)
        call_number = 2
        progress_bar.update(1)  # Update the progress bar
        progress_bar.set_description(f"APIs {call_number}/{num_api_calls}")

        progress_bar.close()
        progress_bar.clear()
        api_calls += 2
        # print relevant data from post API calls
        
        
        if status == True and data_type == "dict":   
            #print(type(data))
            print("Login to VCO",colored(vco_class.base_url, 'green'), "was success." )
            print("-" * 120)
            print("Customer details:")
            print("-" * 120)
            print("Tenant name:", colored(data["result"]["name"], 'green'))
            print("Tenant id:", colored(data["result"]["id"], 'green'))
            print("LogicalId(API2):", colored(data["result"]["logicalId"], 'green'))
            print("Tenant created:", colored(data["result"]["created"], 'green'))
            print("Tenant accountNumber:", colored(data["result"]["accountNumber"], 'green'))
            print("Tenant contactName:", colored(data["result"]["contactName"], 'green'))                        
            print("Tenant contactEmail:", colored(data["result"]["contactEmail"], 'green'))            
            print("Tenant streetAddress:", colored(data["result"]["streetAddress"], 'green'))            
            print("Tenant city:", colored(data["result"]["city"], 'green'))
            print("Tenant country:", colored(data["result"]["country"], 'green'))
            
            print("-" * 120)            
            print("Customer is part of MSP:")
            print("-" * 120)            
            print("MSP type:", colored(data["result"]["enterpriseProxy"]["proxyType"], 'green'))
            print("MSP name:", colored(data["result"]["enterpriseProxy"]["name"], 'green'))
            print("MSP domain:", colored(data["result"]["enterpriseProxy"]["domain"], 'green'))
            print("-" * 120)
            
        elif status == False:
            print("Something wrong. Here are details of collected data")
            print(data)
            print(type(data))

        if status2 == True and data_type2 == "dict":
            print("Tenant details:")
            print(colored("Edges:    ", 'blue'), "  Total:", colored(data2["result"]["edges"]["total"], 'green'), ",Activated:",colored(data2["result"]["edges"]["activated"], 'green'), ",Connected", colored(data2["result"]["edges"]["connected"], 'green'), ",Degraded", colored(data2["result"]["edges"]["degraded"], 'green'), ",Down", colored(data2["result"]["edges"]["down"], 'green'), ",UpToDate", colored(data2["result"]["edges"]["upToDate"], 'green'))
            print(colored("Hubs:     ", 'blue'), "  Total:", colored(data2["result"]["hubs"]["total"], 'green'), ",Activated:",colored(data2["result"]["hubs"]["activated"], 'green'), ",Connected", colored(data2["result"]["hubs"]["connected"], 'green'), ",Degraded", colored(data2["result"]["hubs"]["degraded"], 'green'), ",Down", colored(data2["result"]["hubs"]["down"], 'green'))
            print(colored("Links:    ", 'blue'), "  Total:", colored(data2["result"]["links"]["total"], 'green'), ",Stable:",colored(data2["result"]["links"]["stable"], 'green'), ",Unstable", colored(data2["result"]["links"]["unstable"], 'green'),  ",Down", colored(data2["result"]["links"]["down"], 'green'))
            print(colored("HubLinks: ", 'blue'), "  Total:", colored(data2["result"]["hubLinks"]["total"], 'green'), ",Stable:",colored(data2["result"]["hubLinks"]["stable"], 'green'), ",Unstable", colored(data2["result"]["hubLinks"]["unstable"], 'green'),  ",Down", colored(data2["result"]["hubLinks"]["down"], 'green'))
            print(colored("HA:       ", 'blue'), "  Total:", colored(data2["result"]["ha"]["total"], 'green'), ",Pending:",colored(data2["result"]["ha"]["pending"], 'green'), ",Ready", colored(data2["result"]["ha"]["ready"], 'green'),  ",Failed", colored(data2["result"]["ha"]["failed"], 'green'))
            print(colored("VNFs:     ", 'blue'), "  Total:", colored(data2["result"]["vnfs"]["total"], 'green'), ",On:",colored(data2["result"]["vnfs"]["on"], 'green'), ",Off", colored(data2["result"]["vnfs"]["off"], 'green'),  ",Error", colored(data2["result"]["vnfs"]["error"], 'green'))
            
            print("-" * 120)

        elif status2 == False:
            print("Something wrong. Here are details of collected data2")
            print(data2)
            print(type(data2))
            
            
        time_seconds = time.time() - startTime
        time_seconds = int(time_seconds)
        if time_seconds == 0:
            time_seconds = 1
        print("\nApi Calls:", api_calls)
        print("Api Calls per second:", round(api_calls/time_seconds, 2))
        print("Time of processing:", round(time.time() - startTime, 2))

    except TypeError:
        print("Error code: TypeError")
        raise SystemExit

# Allowed commands
cli.add_command(get_api_keys)
cli.add_command(get_api_vco_csv)
cli.add_command(get_api_json)
cli.add_command(get_api_devices_csv)
cli.add_command(get_api_devices_all_csv)
cli.add_command(get_api_body)
cli.add_command(show_vco_info)
