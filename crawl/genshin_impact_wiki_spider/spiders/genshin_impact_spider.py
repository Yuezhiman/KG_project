from collections.abc import Iterable

import bs4
from bs4 import BeautifulSoup

import json
import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor

import logging
from collections import defaultdict
def get_text_dict(d):
    for k, v in d.items():
        if isinstance(v, dict):
            v = get_text_dict(v)
        elif isinstance(v, str):
            continue
        elif isinstance(v, Iterable):
            v = [d.text().strip() for d in v]
            if len(v) == 1:
                v = v[0]
        elif isinstance(v, bs4.element.Tag):
            v = v.text().strip()
        d[k] = v
    return d


class GenshinImpactSpider(Spider):
    name = 'genshin_impact_spider'
    allowed_domains = ['wiki.biligame.com']
    # start_urls = ['http://wiki.biligame.com/ys/']
    # start_urls = ['https://wiki.biligame.com/ys/%E6%9D%90%E6%96%99%E5%9B%BE%E9%89%B4']#材料
    start_urls = ['http://wiki.biligame.com/ys/%E8%A7%92%E8%89%B2%E8%AF%AD%E9%9F%B3']#语音
    def parse(self, response, **kwargs):
        # 人物语音
        linkextractor = LinkExtractor(restrict_xpaths = '//div[@class="home-box-tag-1"]//a')
        for link in linkextractor.extract_links(response):
            logging.info(f"从 {response.url} 提取链接: {link.url}")
            yield Request(link.url, callback = self.parse_relation ,errback=self.handle_error)
        
        '''人物,武器
        linkextractors = [
            # (LinkExtractor(restrict_xpaths = '//a[@title="角色图鉴"]'), 'parse_character'),
            # (LinkExtractor(restrict_xpaths = '//a[@title="武器图鉴"]'), 'parse_weapon'),
        ]
        # link=start_urls
        # callback='parse_material'
        # for lx, callback in linkextractors:
        #     for link in lx.extract_links(response):
        #         logging.info(f"正在跟随链接: {link.url}")#
        #         yield Request(link.url, callback = self.parse_url, cb_kwargs = {'cb': callback},errback=self.handle_error)
        '''
        '''材料
        specific_link = response.xpath('//a[@title="材料一览"]/@href').get()
        if specific_link:
            # 访问特定链接
            yield response.follow(specific_link, callback=self.parse_next_page) 
        '''
    def parse_next_page(self, response):
        linkextractors = [
            (LinkExtractor(restrict_xpaths = '//a[@title="材料图鉴"]'), 'parse_material'),
        ]
        for lx, callback in linkextractors:
            for link in lx.extract_links(response):
                logging.info(f"正在跟随链接: {link.url}")#
                yield Request(link.url, callback = self.parse_url, cb_kwargs = {'cb': callback},errback=self.handle_error)
    def parse_relation(self, response):
        def parse_general_table(general_table, character):
            for child in [c for c in general_table.children if not isinstance(c, bs4.element.NavigableString)]:
                relation['语音'].append(child.div.text.strip())
        print('--------')
        relation = {}
        relation['语音']=[]
        soup = BeautifulSoup(response.text, 'lxml')
        element = response.xpath('//*[@id="firstHeading"]/text()').get()
        relation['character']=element.strip()
        if(element=='旅行者语音'):
            return None
        # print(relation['character'])
        tables = soup.findAll('div', class_ = 'resp-tab-content')
        parse_general_table(tables[0], relation)
        if 'character' in relation:
            return {'type': 'relation', 'data': relation}
        else:
            return None

    def parse_url(self, response, cb, **kwargs):
        # 材料
        linkextractor = LinkExtractor(restrict_xpaths = '//div[@class="ys-iconLarge"]/a')
        for link in linkextractor.extract_links(response):
            logging.info(f"从 {response.url} 提取链接: {link.url}")
            yield Request(link.url, callback = getattr(self, cb),errback=self.handle_error)
        '''
        #人物
        # linkextractor = LinkExtractor(restrict_xpaths = '//table[@id="CardSelectTr"]') 
        # for link in linkextractor.extract_links(response):
            # yield Request(link.url, callback = self.__getattribute__(cb))
            # logging.info(f"从 {response.url} 提取链接: {link.url}")
            # yield Request(link.url, callback = getattr(self, cb),errback=self.handle_error)
        '''
        
        '''武器
        linkextractor = LinkExtractor(restrict_xpaths = '//table[@id="CardSelectTr"]/tbody//tr/td[1]/div/a')# 武器
        for link in linkextractor.extract_links(response):
            logging.info(f"从 {response.url} 提取链接: {link.url}")
            yield Request(link.url, callback = getattr(self, cb),errback=self.handle_error)
        # pass
        '''
    def handle_error(self, failure):
        logging.error(f"请求失败: {failure}")

# 解析xpath
    
    def parse_character(self, response, **kwargs):
        def parse_general_table(general_table, character):
            for child in [c for c in general_table.tbody.children if not isinstance(c, bs4.element.NavigableString)]:
                if child.th.text.strip() == '稀有度':
                    character[child.th.text.strip()] = child.td.img['alt'].split('.')[0]
                else:
                    character[child.th.text.strip()] = child.td.text.strip()

        character = {}
        soup = BeautifulSoup(response.text, 'lxml')
        tables = soup.findAll('table', class_ = 'wikitable')
        parse_general_table(tables[0], character)

        if '称号' in character:
            return {'type': 'character', 'data': character}
        else:
            return None

    def parse_weapon(self, response, **kwargs):
        def parse_general_table(general_table, weapon):
            children = [c for c in general_table.div.children if not isinstance(c, bs4.element.NavigableString)]
            weapon['武器名称'] = children[0].text.strip()
            weapon['稀有度']=children[1].text.strip()
        weapon = {}
        soup = BeautifulSoup(response.text, 'lxml')
        tables = soup.findAll('div', class_ = 'YS-WeaponBrief')
        # print(tables[0])
        parse_general_table(tables[0], weapon)
        tables = soup.findAll('div', class_ = 'YS-WeaponBrief')
        a=soup.findAll('div', class_ = 'card-title2')
        weapon['基础属性']=a[0].text.strip()
        weapon['技能名称']=a[1].text.strip()
        b=soup.findAll('div', class_ = 'card-title3')
        d=soup.findAll('div', class_ = 'card-content3')
        count=0
        for th, td in zip(b, d):
            if count<5:
                weapon[th.text.strip()] = td.text.strip()
                count+=1
        if '武器名称' in weapon:
            return {'type': 'weapon', 'data': weapon}
        else:
            return None
    def parse_material(self, response, **kwargs):
        def parse_general_table(general_table, material):
            children = [c for c in general_table.tbody.children if not isinstance(c, bs4.element.NavigableString)]
            material['材料名称'] = children[0].th.text.strip()
            print(material['材料名称'])
            # "合成": 
            for child in children[2:]:
                if child.th.text.strip() == '稀有度':
                    material[child.th.text.strip()] = child.td.img['alt'].split('.')[0]
                elif child.th.text.strip() == '图鉴描述':
                    continue
                elif child.th.text.strip() == '合成':
                    continue
                else:
                    material[child.th.text.strip()] = child.td.text.strip()

        material = {}
        soup = BeautifulSoup(response.text, 'lxml')
        tables = soup.findAll('table', class_ = 'wikitable')
        # print(tables[0])
        parse_general_table(tables[0], material)

        fliter = ['角色培养', '天赋', '武器突破', '特产']

        if '类型' in material and any([f in material['类型'] for f in fliter]):
            return {'type': 'material', 'data': material}
        else:
            return None
