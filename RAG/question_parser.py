class QuestionPaser:
    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == '1':
                sql = self.sql_transfer(question_type, entity_dict.get('character'))

            elif question_type == '2':
                sql = self.sql_transfer(question_type, entity_dict.get('weapon'))
            elif question_type == '3':
                sql = self.sql_transfer(question_type, entity_dict.get('character'))
            elif question_type == '4':
                sql = self.sql_transfer(question_type, entity_dict.get('material'))
            elif question_type=='5':
                sql = self.sql_transfer(question_type, entity_dict.get('character'))
            # elif question_type=='6':
            #     sql = self.sql_transfer(question_type, entity_dict.get('weapon'))
            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []
        print(entities)
        # 查询语句
        sql = []
        if question_type == '1':
            sql = ["MATCH (ch:Character )-[rel:需求]->(m:Material) where ch.name = '{0}' return ch.name,m.name".format(i) for i in entities]
        elif question_type == '2':
            sql =["MATCH (w:Weapon)-[rel:需求]->(m:Material) where w.name = '{0}' return w.name,m.name".format(i) for i in entities]
        
        elif question_type == '3':
            entities = list(zip(entities, entities))
            sql=["MATCH (ch1:Character)-[rel:关联]->(ch2:Character) where ch1.name = '{0} and ch2.name = '{1}' return ch1.name, ch2.name ,rel.name".format(ch1_name, ch2_name) for ch1_name, ch2_name in entities]
        elif question_type == '4':
            sql=["MATCH (m1:Material)-[rel:相似素材]->(m2:Material) where m1.name = '{0} and m2.name = '{1}' return m1.name,m2.name,rel.name".format(ch1_name, ch2_name) for ch1_name, ch2_name in entities]
        elif question_type == '5':
            sql=["""MATCH (ch:Character ) where ch.name='{0}' 
                return ch.name AS name, 
                ch.intro AS intro""".format(i) for i in entities]
        # elif question_type == '6':
        #     sql=["""MATCH (w:Weapon) where w.name='{0}' 
        #         return w.name AS name, w.range as range,w.typeName as typeName""".format(i) for i in entities]
        return sql
# ch.title AS title, ch.gender AS gender, ch.rarity AS rarity, ch.pool AS pool, 
                # ch.constellation AS constellation, ch.specialCuisine AS specialCuisine, 
                # ch.equipDate AS equipDate, 
                # ch.tag AS tag, 


if __name__ == '__main__':
    handler = QuestionPaser()