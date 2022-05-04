#!/usr/env/bin python
import re
import operator
import csv

errors_dict = {}
users_dict = {}
with open('syslog.log', 'r') as f:
    for line in f.readlines():
        result = re.search(r".* [A-Z]+ ([A-Za-z' ]*).*\(([a-z.]*)\)", line)
        if result[2] not in users_dict.keys():
            users_dict[result[2]] = {}
            users_dict[result[2]]['info'] = 0
            users_dict[result[2]]['errors'] = 0
            if "INFO" in line:
                users_dict[result[2]]['info'] = 1
            else:
                users_dict[result[2]]['errors'] = 1
        else:
            if "INFO" in line:
                users_dict[result[2]]['info'] += 1
            else:
                users_dict[result[2]]['errors'] += 1
        if "ERROR" in line:
            if result[1] in errors_dict.keys():
                errors_dict[result[1]] += 1
            else:
                errors_dict[result[1]] = 1
    sorted_errors = sorted(errors_dict.items(), key=operator.itemgetter(1), reverse=True)
f.close() 

users = []
for key, value in sorted(users_dict.items()):
    username = key
    info = value['info']
    errors = value['errors']  
    users_group = {}
    users_group['Username'] = username
    users_group['Info'] = info
    users_group['Error'] = errors
    users.append(users_group)

users_keys = ["Username", "Info", "Error"]
with open('users.csv', 'w') as users_details:
    writer = csv.DictWriter(users_details, fieldnames=users_keys)
    writer.writeheader()
    writer.writerows(users)
users_details.close()
error_list = []
for element in sorted_errors:
    error_item = element[0]
    count_item = element[1]
    error_count = {}
    error_count['Error'] = error_item
    error_count['Count'] = count_item
    error_list.append(error_count)

error_keys = ["Error", "Count"]
with open('errors.csv', 'w') as errors_details:
    writer = csv.DictWriter(errors_details, fieldnames=error_keys)
    writer.writeheader()
    writer.writerows(error_list)
errors_details.close()
    
    