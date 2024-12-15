from llama_index.graph_stores.neo4j import Neo4jGraphStore  
username = "neo4j"   
password = "yzm696969"         
url = "bolt://10.230.34.43:7687"
database = "neo4j"        
graph_store = Neo4jGraphStore(        
    username=username,         
    password=password,         
    url=url,        
    database=database,         
)
from llama_index.core import StorageContext,KnowledgeGraphIndex,Settings
from transformers import AutoTokenizer, AutoModelForCausalLM
# from transformers import AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained("internlm2_5-7b")
import torch
model_path ="/home/zhimanyue/sftpFolder/KG_project/RAG/internlm2_5-1_8b"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
# Set `torch_dtype=torch.float16` to load model in float16, otherwise it will be loaded as float32 and might cause OOM Error.
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16, trust_remote_code=True).cuda()
from llama_index.llms.huggingface import HuggingFaceLLM
# Wrap the Hugging Face model and tokenizer in HuggingFaceLLM
hf_llm = HuggingFaceLLM(
    model=model,
    tokenizer=tokenizer,
)
from sentence_transformers import SentenceTransformer,models
model="/home/zhimanyue/sftpFolder/KG_project/RAG/tao-8k"
transformer = models.Transformer(model_name_or_path=model , max_seq_length=128)
pooling = models.Pooling(transformer.get_word_embedding_dimension())
storage_context = StorageContext.from_defaults(graph_store=graph_store)
Settings.llm=hf_llm
embed_model = SentenceTransformer(modules=[transformer, pooling])
# Settings.embed_model = SentenceTransformer(modules=[transformer, pooling])
# Load a local embedding model
# model = model.eval()
# Settings.llm=model
# storage_context = StorageContext.from_defaults(graph_store=graph_store)
# service_context = ServiceContext.from_defaults(llm=model, chunk_size=512)

index = KnowledgeGraphIndex.from_documents([], storage_context=storage_context,embed_model=embed_model)
query_engine = index.as_query_engine(    
    include_text=True,      
    response_mode="tree_summarize",          
    similarity_top_k=5,     
    embedding_mode=embed_model,  
    verbose=True,       
)         
response = query_engine.query("芭芭拉的培养材料是什么")       
print(f"Response: {response}")
"""
inputs = tokenizer(["琴和芭芭拉的关系"], return_tensors="pt")
for k,v in inputs.items():
    inputs[k] = v.cuda()
gen_kwargs = {"max_length": 128, "top_p": 0.8, "temperature": 0.8, "do_sample": True, "repetition_penalty": 1.0}
output = model.generate(**inputs, **gen_kwargs)
output = tokenizer.decode(output[0].tolist(), skip_special_tokens=True)
print(output)
"""
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