from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="10.222.145.115",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            # http_port=7687,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="yzm696969")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == '1':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['ch.name']
            final_answer = '{0}需要的培养材料包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == '2':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['w.name']
            final_answer = '{0}需要的培养材料包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == '3':
            ch1=answers[0]['ch1.name']
            ch2=answers[0]['ch2.name']
            subject = answers[0]['rel.name']
            final_answer = '{0}和{1}的关系是{2}'.format(ch1,ch2,subject)

        elif question_type == '4':
            ch1=answers[0]['m1.name']
            ch2=answers[0]['m2.name']
            subject = answers[0]['rel.name']
            final_answer = '{0}和{1}的关系是{2}'.format(ch1,ch2,subject)
        elif question_type == '5':
            desc = answers[0]['intro']
            subject = answers[0]['name']
            final_answer = '{0}的相关信息是：{1}'.format(subject, desc)

        # elif question_type == '6':
        #     desc = [';'.join(i['m.cure_way']) for i in answers]
        #     subject = answers[0]['name']
        #     final_answer = '{0}的相关信息是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

       
        # elif question_type == 'disease_acompany':
        #     desc1 = [i['n.name'] for i in answers]
        #     desc2 = [i['m.name'] for i in answers]
        #     subject = answers[0]['m.name']
        #     desc = [i for i in desc1 + desc2 if i != subject]
        #     final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        

        # elif question_type == 'disease_do_food':
        #     do_desc = [i['n.name'] for i in answers if i['r.name'] == '宜吃']
        #     recommand_desc = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]), ';'.join(list(set(recommand_desc))[:self.num_limit]))

        return final_answer

if __name__ == '__main__':
    searcher = AnswerSearcher()