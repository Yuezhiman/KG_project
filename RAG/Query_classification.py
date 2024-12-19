from neo4j import GraphDatabase
from langchain_neo4j import Neo4jGraph
username = "neo4j"   
password = "yzm696969"         
url = "bolt://10.222.145.115:7687"
database = "neo4j" 
class Neo4jQueryHandler:
    def __init__(self, url, user, password):
        self.kg = Neo4jGraph(url=url, username=user, password=password, database='neo4j')

    @staticmethod
    def build_query(category, text):
        # 这里根据不同的类别构建不同的Cypher查询语句
        # 仅作为示例，实际情况需要根据你的数据模型调整
        # 询问原神人物
        if category == "1":
            # a=text
            return """
            MATCH (ch:Character {name: $a})
            RETURN ch.name AS name, 
                   ch.title AS title, 
                   ch.gender AS gender, 
                   ch.rarity AS rarity, 
                   ch.pool AS pool, 
                   ch.constellation AS constellation, 
                   ch.specialCuisine AS specialCuisine, 
                   ch.equipDate AS equipDate, 
                   ch.tag AS tag, 
                   ch.intro AS intro;
            """
        # # 询问原神材料
        # elif category == "2":
        #     island = text
        #     return """
        #     MATCH (ch:Material {name: $a})
        #     RETURN ch.name AS name, 
        #            ch.title AS title, 
        #            ch.gender AS gender, 
        #            ch.rarity AS rarity, 
        #            ch.pool AS pool, 
        #            ch.constellation AS constellation, 
        #            ch.specialCuisine AS specialCuisine, 
        #            ch.equipDate AS equipDate, 
        #            ch.tag AS tag, 
        #            ch.intro AS intro;
        #     """
        else:
            raise ValueError("抱歉，暂未提供此类型查询功能！")

    def query_and_return(self,category, text):
        if category=='1':
            answer = '人物的信息：'
        # elif category=='2':
        #     answer=f'{text}用到材料的人有:'
        else:
            answer=''
        query = self.build_query(category, text)
        parameters = {"a": text}  # 提供参数
        results = self.kg.query(query,parameters)
        # formatted_strings=results[0]
        formatted_strings = ['({}, {})'.format(key, value) for key, value in results[0].items()]
        answers =answer+ ';'.join(formatted_strings)
        return answers
# 使用示例
if __name__ == "__main__":
    neo4j_handler = Neo4jQueryHandler(url, "neo4j", password)
    # 假设我们要查询类别为"person"，名字为"John Doe"的记录
    results = neo4j_handler.query_and_return("1",'埃洛伊（Aloy）' )
    print(results)

