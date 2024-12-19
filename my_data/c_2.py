import os
import json
import csv
import pandas as pd
import re
file = open('D:\Git\KG_project\my_data\character.json', encoding='utf-8')
result = {}
count=0
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
for line in file:
    # item_dict=[]
    line = line.strip()  # 去掉首尾空白字符
    if line:
        try:
            item_dict = json.loads(line)
            result[count]=item_dict
            count+=1
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e} - Line: {line}")
character_attr = ['name','title','gender','rarity','pool','constellation','specialCuisine','equipDate','tag','intro']
character_attr_ = ['全名/本名','称号','性别','稀有度','常驻/限定','命之座','特殊料理','实装日期','TAG','介绍']
begin = "CharacterID"
end = "LABEL"
with open('D:\Git\KG_project\graph\characters.csv', 'w', encoding='utf-8-sig', newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow([begin]+character_attr+[end])
    for chId in result.keys():
        item = result[chId]
        data = []
        data.append('#'+str(chId))
        for col in character_attr_:
            value = item[col]
            if value == '' or '无' in value:
                value = 'N/A'
            if col =='全名/本名':
                ch = re.sub(r'（.*?）', '', value)
                value=ch
            data.append(value)
        last = "Character"
        data.append(last)
        print(data)
        csv_writer.writerow(data)
print('Character Finish!')
