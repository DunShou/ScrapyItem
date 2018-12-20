# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanymessageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
     #工作名称
    job_name = scrapy.Field()
    
    job_url = scrapy.Field()
    #公司名
    company_name = scrapy.Field()
    #工作地点
    work_place = scrapy.Field()
    #薪资
    salary = scrapy.Field()
    #发布时间
    publish_time = scrapy.Field()
    #招聘要求
#    jobrequire = scrapy.Field()
    #职位信息
#    job_information = scrapy.Field()
    #上班地点
    #workinglocation = scrapy.Field()

class DetailedInformation(scrapy.Item):
    job_name = scrapy.Field()
    #公司名
    company_name = scrapy.Field()
    #公司URL
    company_url = scrapy.Field()
#    公司人数
    num_of_companies = scrapy.Field()
#    工作经验
    hands_on_background = scrapy.Field()
#    地区
    region = scrapy.Field()
#    学历要求
    academic_requirement = scrapy.Field()
#    招多少人
    how_many = scrapy.Field()
#    额外要求
    extra_requirement = scrapy.Field()
#    职能类别
    functional_categories = scrapy.Field()
#    上班地点
    work_place = scrapy.Field()
#    职位信息
    job_information = scrapy.Field()






































