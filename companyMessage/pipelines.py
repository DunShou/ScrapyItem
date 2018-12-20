# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pandas as pd
from companyMessage.items import CompanymessageItem
from companyMessage.items import DetailedInformation
from scrapy.exporters import CsvItemExporter

class BytesEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,bytes):
            return str(obj,encoding='utf-8')
        return json.JSONEncoder.default(self,obj)

class CompanymessagePipeline(object):
    def __init__(self):
#        python
#        self.f = open('../../files/pythonSystem/python_job_message.json','w')
        self.f = open('../../files/baiyunqu/job_message.json','w')
#        self.detailf = open('../../files/pythonSystem/python_job_company_message.json','w')
        self.detailf = open('../../files/baiyunqu/job_company_message.json','w')
        
        #csv文件的位置,无需事先创建
        #打开(创建)文件
#        self.file = open('../../files/pythonSystem/python_job.csv','wb')
        self.file = open('../../files/baiyunqu/job.csv','wb')
#        对应detailf
#        self.company_file = open('../../files/pythonSystem/python_company_message.csv','wb')
        self.company_file = open('../../files/baiyunqu/company_message.csv','wb')
        #csv写法
        self.exporter = CsvItemExporter(self.file)
        self.company_exporter = CsvItemExporter(self.company_file)
        
        self.exporter.start_exporting()
        self.company_exporter.start_exporting()
    
    def process_item(self, item, spider):
        
        if isinstance(item, CompanymessageItem):
            item = dict(item)
            content = json.dumps(item,cls=BytesEncoder,ensure_ascii = False)+',\n'
            
            self.f.write(content)
            
            self.exporter.export_item(item)
            
            return item
        elif isinstance(item, DetailedInformation):
            
            item = dict(item)
            content = json.dumps(item,cls=BytesEncoder,ensure_ascii = False)+',\n'
            self.detailf.write(content)
            
            self.company_exporter.export_item(item)
            
            return item
    
    def close_spider(self,spider):
        self.f.close()
        self.detailf.close()
        
        self.exporter.finish_exporting()
        self.company_exporter.finish_exporting()
        self.file.close()


















































