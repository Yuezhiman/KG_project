from bs4 import BeautifulSoup
import urllib.request
import codecs
#import pandas as pd
import requests
def remove_spaces(arr):
    return [x for x in arr if x != '\xa0']


character_yname = open("config", "r")
config_names = character_yname.read()
config_name = config_names.split("\n")
config_name = [x for x in config_name if x is not None and x != " " and x != ""]
print(config_name)

genshin_character_name=config_name
#genshin_character_name=['迪卢克','胡桃','阿贝多']

for ikey in genshin_character_name:
    ## 网页的URL
    url_patch = 'https://wiki.biligame.com/ys/'+ikey
    # 发送HTTP请求
    response = requests.get(url_patch)

    # 检查请求是否成功
    if response.status_code == 200:
        # 打开文件进行写入
        with open(ikey+'.html', 'w') as file:
            file.write(response.text)
        print('网页已保存到'+ikey+".html")

        url = "file:///root/test/rpm/"+ikey+'.html'
        print(url)
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all('tbody')
        tab = tables[0]
        sample_name = tab
        sample_tr = tab.find_all('tr')
        for tr in sample_tr:
            miRNA_family = tr.find_all('th')[0].get_text().split("\n")[0]
            count = "".join(remove_spaces(tr.find_all('td')[0].get_text().split("\n")[0]))
            print(miRNA_family)
            print(count)

            content = [[miRNA_family, count]]
            list_name = ['miRNA', 'count']

            data = pd.DataFrame(columns=list_name, data=content)
            print(data)
            data.to_csv("./maiev.csv", mode='a', header=False, encoding='utf-8')
    else:
        print('请求失败，状态码：', response.status_code)


#url_patch = 'https://wiki.biligame.com/ys/胡桃'












'''

url = 'file:///G:/爬虫/迪卢克.html'
html = urllib.request.urlopen(url).read()



soup = BeautifulSoup(html, "html.parser")

tables = soup.find_all('tbody')

#print(tables)
tab=tables[0]



sample_name=tab

sample_tr = tab.find_all('tr')
for tr in sample_tr:


    miRNA_family = tr.find_all('th')[0].get_text().split("\n")[0]
    count = "".join(remove_spaces(tr.find_all('td')[0].get_text().split("\n")[0]))
    print(miRNA_family)
    print(count)

    content = [[miRNA_family, count]]
    list_name = ['miRNA', 'count']

    data = pd.DataFrame(columns=list_name, data=content)
    print(data)
'''
   # data.to_csv("G:\\爬虫\maiev.csv", mode='a', header=False, encoding='utf-8')

