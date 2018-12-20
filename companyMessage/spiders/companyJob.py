# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 00:39:31 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
import scrapy
import json
from companyMessage.items import CompanymessageItem, DetailedInformation
import re

class CompanyjobSpider(scrapy.Spider):
    name = 'companyJob'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/030200,030205,0000,00,9,99,python,2,1.html?'
                  'lang=c&stype=1&postchannel=0000&workyear=01%2C02&cotype=99&degreefrom=03%2C04&jobterm=99&'
                  'companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=17&dibiaoid=0&address=&'
                  'line=&specialarea=00&from=&welfare=']
    
    place = {'天河区':0,
             '白云区':0,
             '广州':0,
             '越秀区':0,
             '海珠区':0,
             '番禺区':0,
             '荔湾区':0,
             '黄埔区':0,
             '花都区':0,
             '南沙区':0,
             '增城区':0,
             '从化区':0,
             '异地招聘':0,}
    pages = 0
    name_lists = []
    

    def parse(self, response):
        node_list = response.xpath("//div[@class='dw_table']/div[@class='el']")
        for node in node_list:
#            item = CompanymessageItem()
            job_item = {'job_name': '', 'company_name': '', 'job_url': '', 'work_place': '', 'salary': '', 'publish_time': ''}
            job_item['job_name'] = node.xpath('normalize-space(./p/span/a/text())').extract()[0].encode("utf-8")
            
#            jobURL
            job_url = node.xpath("./p/span/a/@href").extract()[0]
            
#            #item['jobname'] = response.xpath("//div[@class='el']/p/span/a/text()").extrace()[0].encode('utf-8')
            job_item['company_name'] = node.xpath("normalize-space(./span[@class='t2']/a/text())").extract()[0].encode('utf-8')
            job_item['job_url'] = job_url
            
            
            if job_item['company_name'] in self.name_lists:
                continue
            else:
                self.name_lists.append(job_item['company_name'])
            
            job_item['work_place'] = node.xpath("normalize-space(./span[@class='t3']/text())").extract()[0].encode('utf-8')
            job_item['salary'] = node.xpath("normalize-space(./span[@class='t4']/text())").extract()[0].encode('utf-8')
            job_item['publish_time'] = node.xpath("normalize-space(./span[@class='t5']/text())").extract()[0].encode('utf-8')
            
            yield scrapy.Request(url=job_url, meta={'job_item':job_item}, callback=self.jobparse)
        self.pages += 1
#        print('第几页：', self.pages)
        if self.pages < 10:
            if self.pages == 1:
                next_url = response.xpath("//div[@class='p_in']/ul/li[@class='bk']/a/@href").extract()[0]
            else:
                next_url = response.xpath("//div[@class='p_in']/ul/li[@class='bk']/a/@href").extract()[1]
#            print('下一页：', next_url)
            request = scrapy.Request(next_url, callback=self.parse)
            yield request
            
        
    def jobparse(self, response):
        
        job_item = DetailedInformation()
        company_message_item = CompanymessageItem()
        company_message_item['job_name'] = response.meta['job_item']['job_name'].decode('utf-8')
        company_message_item['company_name'] = response.meta['job_item']['company_name'].decode('utf-8')
        company_message_item['job_url'] = response.meta['job_item']['job_url']
        company_message_item['work_place'] = response.meta['job_item']['work_place'].decode('utf-8')
        company_message_item['salary'] = response.meta['job_item']['salary'].decode('utf-8')
        if '年' in company_message_item['salary']:
            return
        elif '月' in company_message_item['salary']:
#            print('月')
            if '万' in company_message_item['salary']:
                salary_list = re.findall('[\d+\.\d]*', company_message_item['salary'])
                
                replace_min_num = float(salary_list[0])*10
                replace_max_num = float(salary_list[2])*10
#                print('测试数值：', salary_list,replace_min_num,replace_max_num)
                company_message_item['salary'] = str(replace_min_num)+'-'+str(replace_max_num)+'千/月'
#                print('测试万化千：', company_message_item['salary'])
        company_message_item['publish_time'] = response.meta['job_item']['publish_time'].decode('utf-8')
        
        job_item['job_name'] = response.meta['job_item']['job_name'].decode('utf-8')
        job_item['company_name'] = response.meta['job_item']['company_name'].decode('utf-8')
#        简介
        hands_on_background_lists = response.xpath("//p[@class='msg ltype']").extract()[0]
        hands_tmp = hands_on_background_lists.split('"')[-1].split(' ')
#        删除字母
        hands_tmp = re.sub('[A-Za-z]','', str(hands_tmp)).replace('<>','').replace('</>','').replace('\\0','').replace('\\','').replace('[\>'','').replace('']','').split('|')
#        
#        地区
        job_item['region'] = hands_tmp[0].replace('[\'>', '')
#        工作经验
        job_item['hands_on_background'] = hands_tmp[1]
#        学历要求
        job_item['academic_requirement'] = hands_tmp[2]
#        招多少人
        job_item['how_many'] = hands_tmp[3]
        if len(hands_tmp) > 5:
#            额外要求
            job_item['extra_requirement'] = hands_tmp[5]
        
#        职能类别 //p[@class='fp']/a, 分解一下
        functional_categories = response.xpath("//p[@class='fp']/a").extract()[0]
        functional_categories = re.sub('[A-Za-z0-9\\t\\\<\>\=\r\n\"\/\.\:\-]','',functional_categories)
        job_item['functional_categories'] = functional_categories
#        工作地点 //div[@class='bmsg inbox']/p[@class='fp']
        work_place = response.xpath("//div[@class='bmsg inbox']/p[@class='fp']").extract()[0]
        work_place = re.sub('[a-z\\t\\\<\>\=\r\n\"\/]','',work_place)
        job_item['work_place'] = work_place
#        职位信息
        job_information_lists = response.xpath("//div[@class='bmsg job_msg inbox']/p").extract()
        job_information = []
        for i in range(len(job_information_lists)):
            job_information.append(job_information_lists[i].replace('<p>','').replace('</p>','').replace('<span>','').replace('</span>','').replace('<br>','').replace('<u>','').replace('</u>',''))
        
        job_item['job_information'] = job_information
        
        company_job_url = response.xpath("//p[@class='cname']/a/@href").extract()[0]
#        job_item['company_url'] = response.xpath("//p[@class='cname']/a/@href").extract()[0]
        yield scrapy.Request(company_job_url,meta={'job_item': job_item, 'company_message_item': company_message_item}, callback=self.companyparse)
        
    
    def companyparse(self, response):
#        判断是否有官网，若是没有，则排除
#        print('测试传递的item类型：', type(response.meta['job_item']), response.meta['job_item'])
        job_item = response.meta['job_item']
        company_message_item = response.meta['company_message_item']
        company_url = response.xpath("//p[@class='fp tmsg']/a[@href]").extract()
        if company_url:
            company_url = company_url[0].split('>')[1]
            company_url = company_url.replace('</a', '')
#            print('测试公司官网', company_url)
            job_item['company_url'] = company_url
            num_of_companies = response.xpath("//p[@class='ltype'][@title]").extract()[0]
            num_of_companies = num_of_companies.split('"')[3].split(' ')[0].split('|')[1].replace('\xa0','')
            job_item['num_of_companies'] = num_of_companies
            
            job_information = []
            for i in range(len(job_item['job_information'])):
#                print('测试工作信息：', job_item['job_information'][i])
                job_information.append(job_item['job_information'][i].replace('\xa0',''))
            job_item['job_information'] = job_information
#            ops = str(company_message_item['work_place'],"utf-8")
            ops = company_message_item['work_place']
            if ops == '广州-天河区':
                self.place['天河区'] +=1
            elif ops == '广州-白云区':
                self.place['白云区'] +=1
            elif ops == '广州':
                self.place['广州'] +=1
            elif ops == '广州-越秀区':
                self.place['越秀区'] +=1
            elif ops == '广州-海珠区':
                self.place['海珠区'] +=1
            elif ops == '广州-番禺区':
                self.place['番禺区'] +=1
            elif ops == '广州-荔湾区':
               self. place['荔湾区'] +=1
            elif ops == '广州-黄埔区':
                self.place['黄埔区'] +=1
            elif ops == '广州-花都区':
                self.place['花都区'] +=1
            elif ops == '广州-南沙区':
                self.place['南沙区'] +=1
            elif ops == '广州-增城区':
                self.place['增城区'] +=1
            elif ops == '广州-从化区':
                self.place['从化区'] +=1
            else:
                self.place['异地招聘'] +=1
            
            self.f = open('../../files/baiyunqu/regin_company_Message.json','w')
            cont = json.dumps(self.place,ensure_ascii=False)
            self.f.write(repr(cont))
            self.f.close()
            
            yield job_item
            yield company_message_item
        else:
            return
        







































































