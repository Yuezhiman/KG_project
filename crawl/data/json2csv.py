#json2csv.py
import os
import json
import csv
import pandas as pd

entities = ['character', 'country', 'material', 'weapon', 'element', 'weapontype']
results = dict()

def get_key_counts(entity):
    keys = {}
    file = open(entity+'.json', encoding='utf-8')
    for line in file:
        item = json.loads(line)
        key = list(item.keys())
        for k in key:
            if k not in keys.keys():
                keys[k]=1
            else:
                keys[k]+=1
    return keys
    
for entity in entities:
    file = open(entity+'.json', encoding='utf-8')
    result = {}
    count = 0
    for line in file:
        item_dict = json.loads(line)
        result[count]=item_dict
        count+=1
    results[entity]=result

#处理character.json
#剩余 元素属性\武器类型\所属
character_attr = ['name','title','gender','rarity','pool','constellation','specialCuisine','equipDate','tag','intro']
character_attr_ = ['全名/本名','称号','性别','稀有度','常驻/限定','命之座','特殊料理','实装日期','TAG','介绍']
begin = "CharacterID"
end = "LABEL"
with open('characters.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow([begin]+character_attr+[end])
    for chId in results['character'].keys():
        item = results['character'][chId]
        data = []
        data.append('#'+str(chId))
        for col in character_attr_:
            value = item[col]
            if value == '' or '无' in value:
                value = 'N/A'
            data.append(value)
        last = "Character"
        data.append(last)
        #print(data)
        csv_writer.writerow(data)
print('Character Finish!')


#处理country.json
#剩余 
country_attr = ['name', 'eng_name', 'army', 'desc', 'background']
country_attr_ = ['国家名称', '英文', '军队', '描述', '地区背景']
begin = "CountryID"
end = "LABEL"
with open('countries.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow([begin]+country_attr+[end])
    for cId in results['country'].keys():
        item = results['country'][cId]
        data = []
        data.append('c'+str(cId))
        for col in country_attr_:
            value = item[col]
            if value == '' or '无' in value:
                value = 'N/A'
            data.append(value)
        last = "Country"
        data.append(last)
        # print(data)
        csv_writer.writerow(data)
print('Country Finish!')

#处理weapon.json
#剩余 类型
weapon_attr = ['name', 'rarity', 'baseProperty1', 'baseProperty2', 'intro', 'skillname', 'skillDesc', 'obtain', 'tag']
weapon_attr_ = ['武器名称', '稀有度', '基础属性1', '基础属性2', '介绍', '技能名称', '效果介绍', '获取途径', 'TAG']
begin = "WeaponID"
end = "LABEL"
with open('weapons.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow([begin]+weapon_attr+[end])
    for wId in results['weapon'].keys():
        item = results['weapon'][wId]
        data = []
        data.append('w'+str(wId))
        for col in weapon_attr_:
            value = item[col]
            if value == '' or '无' in value:
                value = 'N/A'
            data.append(value)
        last = "Weapon"
        data.append(last)
        # print(data)
        csv_writer.writerow(data)
print('Weapon Finish!')

#处理weapontype.json
#剩余 类型
weapontype_attr = ['typeName', 'range', 'frequency', 'accumulate']
weapontype_attr_ = ['名称', '类型', '速度', '蓄力']
begin = "WeapontypeID"
end = "LABEL"
with open('weapontypes.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow([begin]+weapontype_attr+[end])
    for wId in results['weapontype'].keys():
        item = results['weapontype'][wId]
        data = []
        data.append('wt'+str(wId))
        for col in weapontype_attr_:
            value = item[col]
            if value == '' or '无' in value:
                value = 'N/A'
            data.append(value)
        last = "WeaponType"
        data.append(last)
        # print(data)
        csv_writer.writerow(data)
print('WeaponType Finish!')

#处理element.json
#剩余 反应元素
element_attr = ['name', 'reaction', 'resonance']
element_attr_ = ['名称', '元素反应', '元素共鸣']
begin = "ElementID"
end = "LABEL"
with open('element.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow([begin]+element_attr+[end])
    for eId in results['element'].keys():
        item = results['element'][eId]
        data = []
        data.append('e'+str(eId))
        for col in element_attr_:
            value = item[col]
            if value == '' or '无' in value:
                value = 'N/A'
            data.append(value)
        last = "Element"
        data.append(last)
        # print(data)
        csv_writer.writerow(data)
print('Element Finish!')


#处理material.json
#剩余 用处\相关角色\相关武器\同类素材\系列素材
material_attr = ['name', 'rarity', 'type', 'source', 'intro', 'relatedFurnish', 'relatedFood']
material_attr_ = ['材料名称', '稀有度', '类型', '来源', '介绍', '相关摆设', '相关食物']
begin = "MaterialID"
end = "LABEL"
with open('materials.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow([begin]+material_attr+[end])
    for mId in results['material'].keys():
        item = results['material'][mId]
        data = []
        data.append('m'+str(mId))
        for col in material_attr_:
            value = item[col]
            if value == '' or '无' in value:
                value = 'N/A'
            data.append(value)
        last = "Material"
        data.append(last)
        # print(data)
        csv_writer.writerow(data)
print('Material Finish!')