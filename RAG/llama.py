from llama_index.graph_stores.neo4j import Neo4jGraphStore  
username = "neo4j"   
password = "yzm696969"         
url = "bolt://10.222.201.177:7687"
database = "neo4j"        
graph_store = Neo4jGraphStore(        
    username=username,         
    password=password,         
    url=url,        
    database=database,         
)
from llama_index.core import StorageContext,KnowledgeGraphIndex
from transformers import GPT2LMHeadModel, GPT2Tokenizer
model_path ="/home/zhimanyue/sftpFolder/KG_project/RAG/internlm2_5-7b"
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained(model_path)

# Settings.embed_model = OllamaEmbedding(model_name="znbang/bge:large-zh-v1.5-f32")
# llm=
Settings.llm=model
storage_context = StorageContext.from_defaults(graph_store=graph_store)
index = KnowledgeGraphIndex.from_documents([], storage_context=storage_context)
query_engine = index.as_query_engine(    
    include_text=False,      
    response_mode="tree_summarize",       
    embedding_mode="hybrid",       
    similarity_top_k=5,       
    verbose=True,       
)         
response = query_engine.query("琴和芭芭拉的关系？")       
print(f"Response: {response}")
"""
from neo4j import GraphDatabase
from llama_index import Document

def get_documents_from_neo4j(graph_store):
    # 获取数据库连接
    driver = GraphDatabase.driver(graph_store.url, auth=(graph_store.username, graph_store.password))
    session = driver.session(database=graph_store.database)
    
    # 执行查询以获取节点和关系
    query = '
    MATCH (p:Person)-[r:KNOWS]->(other:Person)
    RETURN p.name AS person_name, other.name AS acquaintance_name, r.since AS since
    '
    
    result = session.run(query)
    
    # 转换为文档格式
    documents = []
    for record in result:
        # 每条记录都是一个节点和关系的实例
        doc_text = f"{record['person_name']} knows {record['acquaintance_name']} since {record['since']}"
        documents.append(Document(doc_text))
    
    session.close()
    return documents
documents = get_documents_from_neo4j(graph_store)
"""