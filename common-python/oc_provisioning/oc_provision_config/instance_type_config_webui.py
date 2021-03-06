# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Michael Shanley (A-Team Cloud Solution Architects)"
__copyright__ = "Copyright (c) 2016  Oracle and/or its affiliates. All rights reserved."
__version__ = "1.0.0.0"
__module__ = "instance_type_config_webui"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import json 

# mapping of instance type to the dependencies required for that install. The tuple is the JSON keys required
instance_dependencies = {'atg': ['ATG_install', 'ATGPATCH_install', 'JAVA_install', 'copy_ssh_keys', 'advanced_storage'],
                         'weblogic': ['WEBLOGIC_common', 'WEBLOGIC_domain_setup', 'WEBLOGIC_managed_servers', 'WEBLOGIC_datasources', 'JAVA_install', 'copy_ssh_keys', 'advanced_storage'],
                         'weblogicManagedServer': ['WEBLOGIC_common', 'WEBLOGIC_managed_server', 'JAVA_install', 'copy_ssh_keys', 'advanced_storage'],
                         'otd': ['OTD_install', 'copy_ssh_keys', 'advanced_storage'],
                         'otdconfig': ['OTD_config', 'copy_ssh_keys', 'advanced_storage'],
                         'endeca': ['ENDECA_install', 'copy_ssh_keys', 'advanced_storage'],
                         'dgraph': ['ENDECA_install', 'copy_ssh_keys', 'advanced_storage'],
                         'db': ['ORACLE_RDBMS_install', 'copy_ssh_keys', 'advanced_storage']}

# entry point for collecting required data based on instance types selected
def instance_type_config(instance_types):
    
    # collected user data to return
    user_data = {}
    # hold a list of our required JSON keys based on dependency mappings
    json_deps = []
    for instance_type in instance_types:
        for deps in instance_dependencies[instance_type]:
            json_deps.append(deps)
    
    # there can be overlap in dependencies. Make a unique list so we only ask for info once
    unique_deps = set(json_deps)

    for dependency in unique_deps:
        user_data.update(_get_user_data(dependency))
         
    return user_data
            
# entry point for web GUI for collecting required data based on instance types selected
def instance_type_config_web(instance_types):
    
    # collected user data to return
    user_data = {}
    # hold a list of our required JSON keys based on dependency mappings
    json_deps = []
    for instance_type in instance_types:
        for deps in instance_dependencies[instance_type]:
            json_deps.append(deps)
    
    # there can be overlap in dependencies. Make a unique list so we only ask for info once
    unique_deps = set(json_deps)

    for dependency in unique_deps:
        # user_data.update(_get_required_fields(dependency))
        user_data[dependency] = (_get_required_fields_silent(dependency))
         
    return user_data

def _get_user_data(json_key):
    json_data = _get_required_fields(json_key)
    user_data = {}
    if isinstance(json_data, list):
        user_data[json_key] = _get_json_data_list(json_data)
    else:
        user_data[json_key] = _get_json_data(json_data)      
    return user_data

# used with the web version - no output
def _get_required_fields_silent(instance_key):
    """
    Read json data from a file on the filesystem
    """        
    data_file = 'orch_templates/json.template'
    key = "commerceSetup"
    with open(data_file) as data_file:    
        data = json.load(data_file)
        if key not in data:
            raise ValueError ("Root " + key + " item missing") 
        return data[key][instance_key] 
        
def _get_required_fields(instance_key):
    """
    Read json data from a file on the filesystem
    """        
    print "Configure install data for " + instance_key + "\n"
    data_file = 'orch_templates/json.template'
    key = "commerceSetup"
    with open(data_file) as data_file:    
        data = json.load(data_file)
        if key not in data:
            raise ValueError ("Root " + key + " item missing") 
        return data[key][instance_key] 

def _get_json_data_list(json_data):
    print "JSON element is a list - you can add multiple values. \n"
    cloned_zero_elem = json_data[0]
    return_list = []
    user_data = {}
    choice = ''
    while choice != 'd':
        for key, value in cloned_zero_elem.items():
            if isinstance(value, dict):
                user_data[key] = _get_json_data(value)            
            else:
                field_desc = value[0]
                field_default = value[1]
                print "Enter value for field  " + key + "   Description: " + field_desc
                print "Press enter for default value of [" + field_default + "]" 
                choice = raw_input(" >>  ")
                if choice == '':
                    user_data[key] = field_default
                else:
                    user_data[key] = choice
                # Lock servers and the BCC require ports different from other instance types. Get them here
                if key == "atgServerType":
                    print "check atg server type"
                    if choice == "lock":
                        print "Enter ServerLockManager Port:"
                        lockPortChoice = raw_input(" >>  ")
                        user_data["atgLockManPort"] = lockPortChoice                        
                    elif choice == "bcc":
                        print "Enter fileSychronizationDeploymentPort:"
                        syncPortChoice = raw_input(" >>  ")
                        user_data["bccFileSyncPort"] = syncPortChoice
                        print "Enter bccLockManagerPort:"
                        syncPortChoice = raw_input(" >>  ")
                        user_data["bccLockPort"] = syncPortChoice                         
                        
        return_list.append(user_data)
        print "\n List item configured."
        print "[d] - Done adding to list"
        print "[a] - add another value to the list"
        while (choice != 'd') and (choice != 'a'): 
               choice = raw_input(" >>  ")
    
    return return_list        

def _get_json_data(json_data):

    if isinstance(json_data, list):
        print "list"
    user_data = {}
    for key, value in json_data.items():
        if isinstance(value, dict):
            user_data[key] = _get_json_data(value)            
        else:
            field_desc = value[0]
            field_default = value[1]
            print "Enter value for field  " + key + "   Description: " + field_desc
            print "Press enter for default value of [" + field_default + "]" 
            choice = raw_input(" >>  ")
            if choice == '':
                user_data[key] = field_default
            else:
                user_data[key] = choice

    return user_data    

def _pause():
    raw_input("Press Enter to continue...")   
