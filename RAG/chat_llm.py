# ccoding = utf-8
import os
from question_classifier import *
from question_parser import *
import re
# from langchain_neo4j import Neo4jGraph
from py2neo import Graph,Node
from transformers import AutoTokenizer, AutoModelForCausalLM
entity_parser = QuestionClassifier()
username = "neo4j"   
password = "yzm696969"         
url = "bolt://10.222.145.115:7687"
database = "neo4j" 
# kg = Graph(url=url, username=username, password=password, database='neo4j')
kg = Graph(host="10.222.145.115",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            # http_port=7687,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="yzm696969")
# kg.query(query,parameters)
# model = ModelAPI(MODEL_URL="http://你的IP:3001/generate")
model_path ="/home/zhimanyue/sftpFolder/KG_project/RAG/internlm2_5-1_8b-chat"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, device_map='cuda:0')
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True,torch_dtype=torch.bfloat16, device_map='cuda:0')
entity_parser = QuestionClassifier()
class KGRAG():
    def __init__(self):
        self.cn_dict = {
                "name":"名称",
                'gender':"性别",
                "Character":"人物",
            "Weapon":"武器",
            "Country":"国家",
            "Weapontypes":"武器类型",
            "Element":"元素",
            "Material":"材料",
            'constellation':"命之座",
            'intro':"人物介绍",
            'specialCuisine':"特殊料理",
            'pool':"卡池",
            'tag':"技能",
            'ID':"编号",
            'equipDate':"日期",
            'title':"称号",
            'rarity':"稀有度",
            'desc':"描述",
            'eng_name':"英文名称",
            'background':"背景",
            'accumulate':"积累",
            'frequency':"频率",
            'range':"范围",
            'typeName':"类型名称",
            "reaction":"反应",
            "resonance":'原理',
            'relatedFood':"相关食物",
            'source':"材料来源",
            'type':"材料类型"
        }
        self.entity_rel_dict = {
            "character":["name", 'gender','constellation','intro','specialCuisine','pool','tag','ID','equipDate','title','rarity','desc'],
            "weapon":["name",'accumulate','frequency','range','typeName'],
            "country":[ "name",'desc','background','eng_name'],
            "weapontypes":["name"],
            "element":["name","reaction","resonance"],
            "material":["name",'relatedFood','source','type','rarity']
        }
        return

    def entity_linking(self, query):
        return entity_parser.check(query)

    def link_entity_rel(self, query, entity, entity_type):
        cate = [self.cn_dict.get(i) for i in self.entity_rel_dict.get(entity_type)]
        prompt = "请判定问题：{query}所提及的是{entity}的哪几个信息，请从{cate}中进行选择，并以列表形式返回。".format(query=query, entity=entity, cate=cate)
        answer, history = model.chat(query=prompt, history=[],tokenizer=tokenizer)
        cls_rel = set([i for i in re.split(r"[\[。、, ;'\]]", answer) if i.strip()]).intersection(set(cate))
        print([prompt, answer, cls_rel])
        return cls_rel

    def recall_facts(self, cls_rel, entity_type, entity_name, depth=1):
        entity_dict = {
            "character":"Character",
            "weapon":"Weapon",
            "country":"Country",
            "weapontypes":"Weapontypes",
            "element":"Element",
            "material":"Material"
        }
        # "MATCH p=(m:Disease)-[r*..2]-(n) where m.name = '耳聋' return p "
        # 遍历所有depth=1的相关节点，得到三元组集合
        sql = "MATCH p=(m:{entity_type})-[r*..{depth}]-(n) where m.name = '{entity_name}' return p".format(depth=depth, entity_type=entity_dict.get(entity_type), entity_name=entity_name)
        print(sql)
        ress = kg.query(sql).data()
        triples = set()
        for res in ress:
            p_data = res["p"]
            nodes = p_data.nodes
            rels = p_data.relationships
            for node in nodes:
                node_name = node["name"]
                for k,v in node.items():
                    
                    if v == node_name:
                        print(v)
                        continue
                    if self.cn_dict[k] not in cls_rel:
                        continue
                    triples.add("<" + ','.join([str(node_name), str(self.cn_dict[k]), str(v)]) + ">")
            for rel in rels:
                if rel.start_node["name"] == rel.end_node["name"]:
                    continue
                # print(rel["name"])
                if rel["name"] not in cls_rel:
                    continue
                triples.add("<" + ','.join([str(rel.start_node["name"]), str(rel["name"]), str(rel.end_node["name"])]) + ">")
        print(len(triples), list(triples)[:3])
        return list(triples)


    def format_prompt(self, query, context):
        prompt = "这是一个关于名叫原神的开放世界游戏领域的问题。给定以下知识三元组集合，三元组形式为<subject, relation, object>，表示subject和object之间存在relation关系" \
                    "请先从这些三元组集合中找到能够支撑问题的部分，在这里叫做证据，并基于此回答问题。如果没有找到，那么直接回答没有找到证据，回答不知道，如果找到了，请先回答证据的内容，然后在给出最终答案" \
                    "知识三元组集合为：" + str(context) + "\n问题是：" + query + "\n请回答："
        return prompt

    def chat(self, query):
        print("step1: linking entity.....")
        entity_dict = self.entity_linking(query)
        # entity_dict={'迪卢克·莱艮芬德（Diluc Ragnvindr）': ['character']}
        depth = 1
        facts = list()
        answer = ""
        default = "抱歉，我在知识库中没有找到对应的实体，无法回答。"
        if not entity_dict:
            print("no entity founded...finished...")
            return default
        print("step2：recall kg facts....")
        for entity_name, types in entity_dict.items():
            for entity_type in types:
                rels = self.link_entity_rel(query, entity_name, entity_type)
                entity_triples = self.recall_facts(rels, entity_type, entity_name, depth)
                facts += entity_triples
        fact_prompt = self.format_prompt(query, facts)
        print("step3：generate answer...")
        answer = model.chat(query=fact_prompt, history=[],tokenizer=tokenizer)
        return answer

if __name__ == "__main__":
    chatbot = KGRAG()
    query = input("USER:").strip()
    answer = chatbot.chat(query)
    print("KGRAG_BOT:", answer)