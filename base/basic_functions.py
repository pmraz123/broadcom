from .py_modules import *

from tabulate import *
from datetime import datetime, timedelta, date
# import hashlib, binascii, os
# from re import A
# import time
# import datetime
# from datetime import datetime, timedelta, date
# import logging, traceback, sys
# from termcolor import colored
# import pandas
# from tabulate import tabulate



#! /usr/bin/env python
# --------------------------------------------------------------------------------------------------
#              other small functions, not API related
# --------------------------------------------------------------------------------------------------
def countdown(t, string):
    orig = t
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        if string == "push":
            print(colored("Waiting to push configuration : ", 'red'), colored(orig, 'red'), colored("seconds ...[", 'red'),colored(timer, 'red'),colored("]", 'red'),end="\r")
        else: 
            print(colored("Waiting   ", 'red'), colored(orig, 'red'), colored("seconds ...[", 'red'),colored(timer, 'red'),colored("]", 'red'),end="\r")
        #print(timer, end="\r")
        time.sleep(1)
        t -= 1

def get_json_from_response(response):
  """Gets the JSON from a VeloCloud API response.

  Args:
    response: The VeloCloud API response.

  Returns:
    The JSON from the VeloCloud API response.
  """

  return json.loads(response.content)


def replace_null_values_with_empty_string(json_object):
  """Replaces all null values in a JSON object with the empty string.

  Args:
    json_object: The JSON object.

  Returns:
    A JSON object with all null values replaced with the empty string.
  """

  if isinstance(json_object, dict):
    for key, value in json_object.items():
      if value is None:
        json_object[key] = "none"
      elif isinstance(value, dict):
        replace_null_values_with_empty_string(value)
      elif isinstance(value, list):
        for item in value:
          replace_null_values_with_empty_string(item)
  elif isinstance(json_object, list):
    for item in json_object:
      replace_null_values_with_empty_string(item)

  return json_object
    
def save_dict_to_csv_question(df, default_file_name, path):
    yes_or_no_output = yes_or_no("Would you like to save output?")
    df = convert_unix_timestamp(df)
    if yes_or_no_output == True:
        os.chdir(path)
        try:
            print("-" * 120)
            print("Enter filename, if not defined, this will be used:", default_file_name, ")")
            print("-" * 120)
            filename = input("file name:")
            is_empty = isNotBlank(filename)
            if is_empty == False:
                print("Writing to", default_file_name)
                df.to_csv(default_file_name, index=False, sep = ';')
                # default_file_name.close()
            else:
                today = date.today()
                todaystr = today.isoformat()
                todaystr = todaystr.replace('-', '_')
                filename = today + "_" + filename
                print("Output Writing to file ", filename)
                df.to_csv(filename, index=False, sep = ';')
                # filename.close()
        except ValueError:
            print("Incorrect file name.(probably empty string)")
            exit(0)
    else:
        exit(0)

def validate_integer(value):
  """Validates that the given value is an integer.

  Args:
    value: The value to validate.

  Returns:
    True if the value is an integer, False otherwise.
  """

  try:
    int(value)
    return True
  except ValueError:
    return False

def validate_boolean(value):
  """Validates that the given value is False or True.

  Args:
    value: The value to validate.

  Returns:
    True if the value is False or True, False otherwise.
  """

  return value in [True, False]



def save_dict_to_csv(df, file_name, path):
    now = datetime.now()
    now_n = now.strftime("%Hh_%Mm") 
    os.chdir(path)
    today = date.today()
    todaystr = today.isoformat()
    todaystr = todaystr.replace('-', '_')
    filename = todaystr + "_" + now_n + "_" + file_name + ".csv"
    df = convert_unix_timestamp(df)
    length = len(df)
    df_print = df.head(20)
    if length > 0:
        print(colored("\n****** Only short output is written also on the screen( max 20 lines), all is in CSV ******", 'green'))
        print(tabulate(df_print, headers='keys', tablefmt='psql', showindex=False))
        print(colored("Output Writing to file: ", 'green'), path + filename)
    df.to_csv(filename, index=False, sep = ';')        

def save_dict_to_csv_json_insert_time(json, file_name, path):
    now = datetime.now()
    now_n = now.strftime("%Hh_%Mm") 
    os.chdir(path)
    today = date.today()
    todaystr = today.isoformat()
    todaystr = todaystr.replace('-', '_')
    filename = todaystr + "_" + now_n + "_" + file_name + ".csv"
    # original: 
    #data = json["data"]
    data = json['data']
    df = pandas.DataFrame(data)
    df_index = df.keys()
    df = convert_unix_timestamp(df)
    date_time_api1 = now.strftime("%Y-%m-%d %H:%M")
    df.insert(0, 'Date[UTC]', date_time_api1)
    df.to_csv(filename, index=False, sep = ';')   
    



    print(colored("Output Writing to file: ", 'green'), path + filename)

    

def save_dict_to_csv_no_date(df, file_name, path):
    os.chdir(path)
    filename = file_name + ".csv"
    df = convert_unix_timestamp(df)
    df.to_csv(filename, index=False, sep = ';')        
    df = convert_unix_timestamp(df)
    length = len(df)
    df_print = df.head(20)
    if length > 0:
        print(colored("\n****** Only short output is written also on the screen( max 20 lines), all is in CSV ******", 'green'))
        print(tabulate(df_print, headers='keys', tablefmt='psql', showindex=False))
        print(colored("Output Writing to file: ", 'green'), path + filename)
        
        

def validate_time(date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S UTC')
            return True
        except ValueError:
            raise ValueError("Incorrect data format, should be  \"2022-05-26T13:00:00 UTC\"")
            return False
        
def save_dict_to_csv_no_print(df, file_name, path):
    now = datetime.now()
    now_n = now.strftime("%Hh_%Mm") 
    os.chdir(path)
    today = date.today()
    todaystr = today.isoformat()
    todaystr = todaystr.replace('-', '_')
    filename = todaystr + "_" + now_n + "_" + file_name + ".csv"
    df = convert_unix_timestamp(df)
    df.to_csv(filename, index=False, sep = ';')     
    
    print(colored("Output Writing to file: ", 'green'), path + filename)

def save_dict_to_csv_no_print_no_time(df, file_name, path):
    os.chdir(path)
    df = convert_unix_timestamp(df)
    df.to_csv(file_name + ".csv", index=False, sep = ';')        
    print(colored("Output Writing to file: ", 'green'),  file_name)
    
def loop_callibration(start_time, mins, sleep, loop_check_number):
    later = time.time()
    delta = int(later - start_time)
    delta_1_loop = (later - start_time)/loop_check_number
    new_loop = (60 * mins)/delta_1_loop
    return (int(new_loop), delta) 
    

def inputNumber(integer, parameter):
  while True:
    try:
       integer = int(integer)       
    except ValueError:
       print(colored(parameter, 'red'), " is not integer. Program will be closed")
       continue
    else:
       return integer 
       break 

def convert_unix_timestamp(df):
    try:
        df['createTimeStamp'] = pandas.to_datetime(df['createTimeStamp'].astype(int), unit='ms')
    except Exception as e:
        pass
    try:
        df['lastupdated'] = pandas.to_datetime(df['lastupdated'].astype(int), unit='ms')
    except Exception as e:
        pass
    try:
        df['entry_time'] = pandas.to_datetime(df['entry_time'].astype(int), unit='ms')
    except Exception as e:
        pass
    try:
        df['statcycletime'] = pandas.to_datetime(df['statcycletime'].astype(int), unit='ms')
    except Exception as e:
        pass
    try:
        df['receive_time'] = pandas.to_datetime(df['receive_time'].astype(int), unit='ms')
    except Exception as e:
        pass  
    try:
        df['last-conn-time-date'] = pandas.to_datetime(df['last-conn-time-date'].astype(int), unit='ms')
    except Exception as e:
        pass                
    try:
        df['downtime-date'] = pandas.to_datetime(df['downtime-date'].astype(int), unit='ms')
    except Exception as e:
        pass 
    try:
        df['lastUpdatedOn'] = pandas.to_datetime(df['lastUpdatedOn'].astype(int), unit='ms')
    except Exception as e:
        pass 
    try:
        df['uptime-date'] = pandas.to_datetime(df['uptime-date'].astype(int), unit='ms')
    except Exception as e:
        pass   
    try:
        df['time-date'] = pandas.to_datetime(df['time-date'].astype(int), unit='ms')
    except Exception as e:
        pass       
    try:
        df['time'] = pandas.to_datetime(df['time'].astype(int), unit='ms')
    except Exception as e:
        pass  
    try:
        df['up-time-date'] = pandas.to_datetime(df['up-time-date'].astype(int), unit='ms')
    except Exception as e:
        pass      
    return df
# omp-peers to check
def raise_except(e):
    print("\n\n")
    print(colored("~" * 120, 'red'))
    print(colored("Something went wrong. Exiting the script....", 'red'))
    print(colored("~" * 120, 'red'))
    print(colored("\nREASON OF FAILING: \n", 'red'))
    ex_type, ex_value, ex_traceback = sys.exc_info()      
    trace_back = traceback.extract_tb(ex_traceback)
    # Format stacktrace
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))  
            
    print("Exception type : %s " % colored(ex_type.__name__, 'red'))
    print("Exception message : %s" %colored(ex_value, 'red'))
    print("Stack trace : %s" %colored(stack_trace[0], 'red'))
    raise SystemExit

    


def hash_string(string):
    """Hash a password for storing."""
    #print(string)
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', string.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_hash(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return (pwdhash, stored_password)

def create_folders(customer, basic_path):
    new_path = basic_path + "/Customers_OUTPUTs"
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    
    customer = customer.replace('-', '_')
    customer = customer.replace(' ', '_')
    
    customer_path = new_path + "/" + customer
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        
    new_path = customer_path +  "/RUN_CONFIG"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        
    new_path = customer_path + "/LOCAL_CONFIG"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        
    new_path = customer_path + "/CSV_FILES"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        
    new_path = customer_path + "/AAR"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    
    new_path = customer_path + "/ALARMS"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    
    new_path = customer_path + "/ALARMS/"  + "ALARMS"
    if not os.path.exists(new_path):
        os.makedirs(new_path)  

    new_path = customer_path + "/ALARMS/"  + "AUDITLOGS"
    if not os.path.exists(new_path):
        os.makedirs(new_path)  
        

    new_path = customer_path + "/ALARMS/"  + "EVENTS"
    if not os.path.exists(new_path):
        os.makedirs(new_path)  

    new_path = customer_path + "/ALARMS/"  + "ALARMS_5MINS"
    if not os.path.exists(new_path):
        os.makedirs(new_path)  
        

    new_path = customer_path + "/RADIO_STATUS"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    new_path = customer_path + "/JASON_OUTPUTS"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        
    new_path = customer_path + "/LOGS"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    new_path = customer_path + "/CRONJOB_LOGS"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    new_path = customer_path + "/OTHER_OUTPUTS"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    new_path = customer_path + "/TSHOOT"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        
    new_path = customer_path + "/CSV_PER_TEMPLATE"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    new_path = customer_path + "/BULK_APIS"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        
    new_path = customer_path + "/ONE_TRANSPORT_DOWN"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    new_path = customer_path + "/VMANAGE_API_CSV"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    new_path = customer_path + "/DEVICE_API_CSV"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    new_path = customer_path + "/DEVICES_API_CSV"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        
    new_path = customer_path + "/PUSH_CHANGE"     
    if not os.path.exists(new_path):
        os.makedirs(new_path) 
        
    new_path = customer_path + "/POST_APIS"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    new_path = customer_path + "/VMBS_STATS"     
    if not os.path.exists(new_path):
        os.makedirs(new_path)
                   
    return customer_path

def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    try:
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False
        else:
            return yes_or_no("Please (y/n) only.")
    except:
        return yes_or_no("Please (y/n) only.")


def isNotBlank(myString):
    if myString and myString.strip():
        # myString is not None AND myString is not empty or blank
        return True
    # myString is None OR myString is empty or blank
    return False


def input_integer(RANGE):
    while True:
        try:
            print("Select group you wish to collect data (0 - ", RANGE, "):")
            number = int(input(""))
            if number < 0 or number > RANGE:
                raise ValueError  # this will send it to the print message and back to the input option
            return number
            break
        except ValueError:
            print("Invalid integer. The number must be in the range of 0 -", RANGE)

def retrieve_template_list():
    
    url = base_url + "/template/device"
    template_list = {}

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get list of templates")
        exit()

    for item in items:
        template_list.update({item['templateName']:{'templateName':item['templateName'],'templateId':item['templateId'],'configType':item['configType'],'devicesAttached':item['devicesAttached']}})
    return(template_list)

##########################################

def devices_per_template(template_id):

    url = base_url + "/template/device/config/attached/{0}".format(template_id)

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get template details")
        exit()

    devices = list()

    for item in items:
        devices.append(item['uuid'])

    return(devices)


#######################################

def save_csv_per_template(template_name,template_id,device_list,newdir_path):


    url = base_url + 'dataservice/template/device/config/input'

    payload = {
   "templateId":template_id,
   "deviceIds":device_list,
   "isEdited":"false",
   "isMasterEdited":"false"
    }

    response = requests.post(url=url, data=json.dumps(payload), headers=header, verify=False)
       
    if response.status_code == 200:
        items = response.json()
    else:
        print("Failed to get template details")
        exit()

    csv_header = list()
    csv_data = list()

    for i in range(len(items['header']['columns'])):
        csv_header.append(items['header']['columns'][i]['property'])

    csv_header.pop(0)

    time = datetime.now().strftime('on-%Y-%m-%d-@-%H-%M-%S') 
    
    outfile_name = newdir_path +'\\' + template_name + '_' + time + '.csv'
    print(outfile_name)
    
    with open (outfile_name, mode='a',newline='') as outfile:
        writer = csv.writer(outfile)     
        writer.writerow(csv_header) 
        for i in range(len(items['data'])):
            csv_data = []
            for x in items['data'][i]:
                csv_data.append(items['data'][i][x])
            csv_data.pop(0)
            writer.writerow(csv_data)     

###################################################################

def backup_csv(customer, outputs_path):
   
    path = outputs_path + "/LOGS/" 
    os.chdir(path)
    
    now = datetime.now()
    newdir_name = now.strftime("%Y-%m-%d-%H-%M-%S")
    newdir_path = os.path.join(parent_dir,newdir_name)
    os.mkdir(newdir_path)

    templates = retrieve_template_list()

    used_template_ids = {}    

    for template in templates:
        if templates[template]['devicesAttached'] > 0:
            used_template_ids.update({templates[template]['templateName']:{'templateName':templates[template]['templateName'], 'templateId':templates[template]['templateId']}})

    devices_per_template_dict = {}

    for used_template in used_template_ids:
        device_list = devices_per_template(used_template_ids[used_template]['templateId'])    
        devices_per_template_dict.update({used_template_ids[used_template]['templateName']:{'devices':device_list,'templateId':used_template_ids[used_template]['templateId']}})  

    for template in devices_per_template_dict:
        save_csv_per_template(template, devices_per_template_dict[template]["templateId"], devices_per_template_dict[template]["devices"], newdir_path)

