import json
import csv
import pandas as pd
file = open("D:\\Git\\KG_project\\crawl\\my_data\\relation.json", encoding='utf-8')
result=[]
for line in file:
    line=json.loads(line)
    filtered_data = []
    for sen in line["语音"]:
        if '关于' in sen:
            filtered_data.append(sen)
    line["语音"]=filtered_data
    result.append(line)
with open('D:\\Git\\KG_project\\crawl\\my_data\\relation_mod.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False, indent=4)