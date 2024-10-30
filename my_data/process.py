import json
import csv
import pandas as pd
file = open("D:\\Git\\KG_project\\crawl\\my_data\\relation.json", encoding='utf-8')
data=[]
for line in file:
    result={}
    line=json.loads(line)
    filtered_data = []
    for sen in line["语音"]:
        if '关于' in sen:
            filtered_data.append(sen)
            print('------')
            print(line['character'])
    # line["语音"]=filtered_data
    result["语音"]=filtered_data
    result["全名/本名"]=line['character']
    data.append(result)
with open('D:\\Git\\KG_project\\crawl\\my_data\\relation_mod.json', 'w', encoding='utf-8') as f:
    # json.dump(data, f, ensure_ascii=False, indent=4)
    for item in data:
        json.dump(item, f, ensure_ascii=False)
        f.write("\n")  # 每个字典后添加换行
    # for i, item in enumerate(data):
    # # json.dump(item, file, ensure_ascii=False, indent=4)
    #     if i < len(data) - 1:  # 如果不是最后一个字典，添加换行
    #         f.write(",\n\n")  # 添加逗号和两个换行
    #     else:
    #         f.write("\n")  # 最后一个字典后面只加一个换行