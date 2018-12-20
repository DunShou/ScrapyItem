# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 12:43:46 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 23:00:02 2018

@author: Administrator

查询出各阶段工资  大于4K小于8K
还要判断公司规模？以及工作经验
"""
import json
import re
import csv

class BytesEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,bytes):
            return str(obj,encoding='utf-8')
        return json.JSONEncoder.default(self,obj)

# python
#filename = './files/pythonSystem/python_job_message.json'
filename = './files/baiyunqu/job_message.json'

#company_f = './files/pythonSystem/python_job_company_message.json'
company_f = './files/baiyunqu/job_company_message.json'

with open(filename,'r') as f:
    json_data = json.load(f)
#print(json_data)
with open(company_f,'r') as f:
    company_json_data = json.load(f)


find_salary = []
find_company = []

company_name_lists = []
company_name_list_final = []

job_url = []

for data in json_data:
    if data['work_place'] == '广州-白云区':
        company_name_lists.append(data['company_name'])
    elif data['work_place'] == '异地招聘':
        continue
    else:
        salary_list = re.findall('[\d+\.\d]*', data['salary'])
    #    print(salary_list[0],'最大',salary_list[2])
        if salary_list[0] and float(salary_list[0]) >= 4:
            if salary_list[2] and float(salary_list[2]) <=8:
                company_name_lists.append(data['company_name'])
#                find_salary.append(data)
    #            print(salary_list[0],'测试',salary_list[2])

for data in company_json_data:
    if data['company_name'] in company_name_lists:
        hands_on_list = re.findall('[\d+\.\d]*', data['hands_on_background'])
#        print('测试经验分割：', hands_on_list)
        if (hands_on_list[0] and float(hands_on_list[0]) < 2) or ( not hands_on_list[0]):
            if data['academic_requirement'] == '大专' or data['academic_requirement'] == '本科':
                company_name_list_final.append(data['company_name'])
                
                find_company.append(data)

for data in json_data:
    if data['company_name'] in company_name_list_final:
        job_url.append({'company_name': data['company_name'], 'job_url': data['job_url']})
        find_salary.append(data)

#find_file = './files/pythonSystem/find/job4_8K.json'
find_file = './files/baiyunqu/find/job4_8K.json'

#find_company_file = './files/pythonSystem/find/find_job_company.json'
find_company_file = './files/baiyunqu/find/find_job_company.json'

file = open(find_file, 'w')
file_company = open(find_company_file, 'w')
#find_salary = dict(find_salary)
for find_one in find_salary:
    content = json.dumps(find_one,cls=BytesEncoder,ensure_ascii = False)+',\n'
    file.write(content)

for find_one in find_company:
    content = json.dumps(find_one,cls=BytesEncoder,ensure_ascii = False)+',\n'
    file_company.write(content)

file.close()
file_company.close()


# 转化为CSV格式
for data in find_company:
    for data_one in job_url:
        if data_one['company_name'] == data['company_name']:
            data['job_url'] = data_one['job_url']
            break
#print('测试find_company：', find_company)
headers = list(find_company[0].keys())
#print('测试', headers)
#print('测试：', find_company)
#to_csv_file = './files/pythonSystem/find/find_python_job.csv'
to_csv_file = './files/baiyunqu/find/find_job.csv'

with open(to_csv_file, 'w', newline='') as f:
    
    writer = csv.DictWriter(f, headers, extrasaction='ignore')
    writer.writeheader()
    
    for row in find_company:
        writer.writerow(row)


































