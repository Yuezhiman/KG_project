#!/usr/bin/env python3
# coding: utf-8
# File: question_classifier.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

import os
# import jieba
import ahocorasick
import re
# from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer,models
import torch
class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.character_path = os.path.join(cur_dir, 'dict/character.txt')
        self.element_path = os.path.join(cur_dir, 'dict/element.txt')
        self.weapon_path = os.path.join(cur_dir, 'dict/weapon.txt')
        self.weapontypes_path = os.path.join(cur_dir, 'dict/weapontypes.txt')
        self.material_path = os.path.join(cur_dir, 'dict/material.txt')
        self.country_path = os.path.join(cur_dir, 'dict/country.txt')
        # 加载特征词
        self.character_wds= [i.strip() for i in open(self.character_path) if i.strip()]
        self.element_wds= [i.strip() for i in open(self.element_path) if i.strip()]
        self.weapon_wds= [i.strip() for i in open(self.weapon_path) if i.strip()]
        self.weapontypes_wds= [i.strip() for i in open(self.weapontypes_path) if i.strip()]
        self.material_wds= [i.strip() for i in open(self.material_path) if i.strip()]
        self.country_wds= [i.strip() for i in open(self.country_path) if i.strip()]
        self.region_words = set(self.character_wds + self.element_wds + self.weapon_wds + self.weapontypes_wds + self.material_wds + self.country_wds)
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()

        # 问句疑问词
        self.grow_qwds = ['培养', '升级']
        self.relation_qwds = ['关系','联系','类型']
        # print(self.region_words)
        print('model init finished ......')
        return
    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree
    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if any(wd in s for s in self.character_wds):
                wd_dict[wd].append('character')
            if wd in self.element_wds:
                wd_dict[wd].append('element')
            if wd in self.weapon_wds:
                wd_dict[wd].append('weapon')
            if wd in self.weapontypes_wds:
                wd_dict[wd].append('weapontypes')
            if wd in self.material_wds:
                wd_dict[wd].append('material')
            if wd in self.country_wds:
                wd_dict[wd].append('country')
        return wd_dict
    # def check(self, question):
    #     region_wds = []
    #     pattern = r'\b(' + '|'.join(map(re.escape, list(self.region_words))) + r')\b'
    #     # 使用正则表达式匹配句子
    #     region_wds = re.findall(pattern, question, re.IGNORECASE)
    #     # if re.search(pattern, question, re.IGNORECASE):
    #     #     for i in self.region_tree(question):
    #     #         wd = i[1][1]
    #     #         # if any(wd in word for word in wordlist):
    #     #         region_wds.append(wd)
    #     print(region_wds)
    #     stop_wds = []
    #     for wd1 in region_wds:
    #         for wd2 in region_wds:
    #             if wd1 in wd2 and wd1 != wd2:
    #                 stop_wds.append(wd1)
    #     final_wds = [i for i in region_wds if i not in stop_wds]
    #     final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}
    #     return final_dict
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
            # pattern = re.compile(f"({wd})|({sent})", re.IGNORECASE)
            # return bool(pattern.search(wd) or pattern.search(sent))
        return False
    '''分类主函数'''
    def classify(self, question):
        data = {}
        dict = self.check(question)
        if not dict:
            return {}
        data['args'] = dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 培养
        if self.check_words(self.grow_qwds, question) and ('character' in types):
            question_type = '1'
            question_types.append(question_type)

        if self.check_words(self.grow_qwds, question) and ('weapon' in types):
            question_type = '2'
            question_types.append(question_type)

        # 人物关系
        if self.check_words(self.relation_qwds, question) and ('character' in types):
            question_type = '3'
            question_types.append(question_type)
        # 材料关系
        if self.check_words(self.relation_qwds, question) and ('material' in types):
            question_type = '4'
            question_types.append(question_type)
        if question_types == [] and 'character' in types:
            question_types = ['5']
        # if question_types == [] and 'weapon' in types:
        #     question_types = ['6']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        print(data)
        return data

    # def get_embedding(word):
    #     # 对词进行分词
    #     inputs = self.tokenizer(word, return_tensors='pt')
    #     # 获取词向量
    #     outputs = self.model(**inputs)
    #     # 取第一个 token 的向量（[CLS] token）
    #     embedding = outputs.last_hidden_state[:, 0, :].squeeze()
    #     return embedding
    
    def has_overlap_bert(self,word1, word2):
        # 获取词向量
        model_2="/home/zhimanyue/sftpFolder/KG_project/RAG/tao-8k"
        transformer = models.Transformer(model_name_or_path=model_2 , max_seq_length=128)
        pooling = models.Pooling(transformer.get_word_embedding_dimension()).cuda()
        model = SentenceTransformer(modules=[transformer, pooling]).cuda()
        # model = SentenceTransformer(model_2)
        embeddings_1 = model.encode(word1, normalize_embeddings=True)
        embeddings_2 = model.encode(word2, normalize_embeddings=True)
        similarity = embeddings_1 @ embeddings_2.T
        # print(similarity)

        # 设置相似度阈值
        threshold = 0.55
        if similarity>0.55:
            print(similarity)
            print(similarity.item())
        return similarity.item() > threshold
    def check(self, question):
        region_wds = []
        # self.region_words
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            print(wd)
            region_wds.append(wd)
        # for i in self.region_words:
            # print(self.region_words)
            # print(question)
            # if self.has_overlap_bert(question,i):
                # region_wds.append(i)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}
        return final_dict
if __name__ == '__main__':
    handler = QuestionClassifier()
    question = input('input an question:')
    data = handler.classify(question)
    print(data)