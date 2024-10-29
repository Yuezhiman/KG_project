# coding: utf-8
"""将json转化为csv格式的关系知识图谱"""
import json
import csv
import pandas as pd

def getEntityID(entity, query):
    global results
    for e in results[entity]:
        if e['名称'][0] == query:
            if entity == 'features':
                return e['id']
            elif entity == 'skills':
                return e['ID']
            elif entity == 'pokemons':
                return e['ID']['全国']
    return None

entities = ['character', 'country', 'material', 'weapon', 'element', 'weapontype']
results = dict()
for entity in entities:
    file = open(f"D:\Git\KG_project\crawl\my_data\{entity}.json", encoding='utf-8')
    result = {}
    count = 0
    for line in file:
        line = line.strip()  # 去掉首尾空白字符
        if line:
            try:
                item_dict = json.loads(line)
                result[count]=item_dict
                count+=1
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e} - Line: {line}")
    results[entity]=result


# for entity in entities:
#     file = open(entity+'.json', encoding='utf-8')
#     result = {}
#     count = 0
#     for line in file:
#         item_dict = json.loads(line)
#         result[count]=item_dict
#         count+=1
#     results[entity]=result

'''
"""角色与国家"""
headers = ['END_ID', 'type', 'START_ID']
with open('D:\Git\KG_project\crawl\my_data\character2country.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    for chId in results['character'].keys():
        startId = '#'+str(chId)
        cname = results['character'][chId]['所在国家']
        for cId in results['country'].keys():
            if results['country'][cId]['国家名称'] == cname:
                data = [['c'+str(cId), '来自', startId]]
                #print(data)
                csv_writer.writerows(data)
print('character2country finish!')


"""角色与武器类型"""
headers = ['END_ID', 'type', 'START_ID']
with open('D:\Git\KG_project\crawl\my_data\character2weapontype.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    for chId in results['character'].keys():
        startId = '#'+str(chId)
        wtname = results['character'][chId]['武器类型']
        for endId in results['weapontype'].keys():
            if results['weapontype'][endId]['名称'] in wtname:
                data = [['wt'+str(endId), '使用', startId]]
                #print(data)
                csv_writer.writerows(data)
print('character2weapontype finish!')


"""武器与武器类型"""
headers = ['END_ID', 'type', 'START_ID']
with open('D:\Git\KG_project\crawl\my_data\weapon2weapontype.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    for wId in results['weapon'].keys():
        startId = 'w'+str(wId)
        wtname = results['weapon'][wId]['武器类型']
        for endId in results['weapontype'].keys():
            if results['weapontype'][endId]['名称'] == wtname:
                data = [['wt'+str(endId), '属于', startId]]
                #print(data)
                csv_writer.writerows(data)
print('weapon2weapontype finish!')


"""角色与元素"""
headers = ['END_ID', 'type', 'START_ID']
with open('D:\Git\KG_project\crawl\my_data\character2element.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    for chId in results['character'].keys():
        startId = '#'+str(chId)
        try:
            ename = results['character'][chId]['神之眼']
        except KeyError:
            ename = '无'
        # print(chId)
        for endId in results['element'].keys():
            if results['element'][endId]['名称'] in ename:
                data = [['e'+str(endId), '神之眼', startId]]
                #print(data)
                csv_writer.writerows(data)
print('character2element finish!')

"""元素与元素"""
headers = ['END_ID', 'type', 'START_ID']
with open('D:\Git\KG_project\crawl\my_data\element2element.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    for eId in results['element'].keys():
        startId = 'e'+str(eId)
        ename = results['element'][eId]['名称']
        for endId in results['element'].keys():
            item = json.loads(results['element'][endId]['反应元素'])
            if ename in item.keys():
                data = [['e'+str(endId), item[ename], startId]]
                #print(data)
                csv_writer.writerows(data)
print('element2element.csv finish!')


"""角色与素材"""
headers = ['END_ID', 'type', 'START_ID']
with open('D:\Git\KG_project\crawl\my_data\character2material.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    for chId in results['character'].keys():
        startId = '#'+str(chId)
        chname = results['character'][chId]['全名/本名']
        for endId in results['material'].keys():
            item = results['material'][endId]['相关角色']
            if chname in item:
                data = [['m'+str(endId), '需求', startId]]
                #print(data)
                csv_writer.writerows(data)
print('character2material.csv finish!')

"""武器与素材"""
headers = ['END_ID', 'type', 'START_ID']
with open('D:\Git\KG_project\crawl\my_data\weapon2material.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    for wId in results['weapon'].keys():
        startId = 'w'+str(wId)
        wname = results['weapon'][wId]['武器名称']
        for endId in results['material'].keys():
            item = results['material'][endId]['相关武器']
            if wname in item:
                data = [['m'+str(endId), '需求', startId]]
                #print(data)
                csv_writer.writerows(data)
print('weapon2material.csv finish!')
'''
"""素材与素材"""
headers = ['END_ID', 'type', 'START_ID']
with open('D:\Git\KG_project\crawl\my_data\material2material.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    for mId in results['material'].keys():
        startId = 'm'+str(mId)
        mname = results['material'][mId]['材料名称']
        for endId in results['material'].keys():
            item = results['material'][endId]['同类素材']
            data = []
            if mname in item:
                data = [[startId, '同类素材', 'm'+str(endId)]]
                #print(data)
            if '系列素材' in results['material'][endId].keys():
                if mname in results['material'][endId]['系列素材']:
                    data.append(['m'+str(endId), '系列素材', startId])
            if len(data)>0:
                csv_writer.writerows(data)
print('material2material.csv finish!')

