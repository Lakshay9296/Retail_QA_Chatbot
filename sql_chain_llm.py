import os
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from few_shots import few_shots, mysql_prompt
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import FewShotPromptTemplate


def few_shots_chain():
    api_key = os.getenv("groq_api_key")
    llm = ChatGroq(
    model="llama3-groq-70b-8192-tool-use-preview",
    temperature=0.1,
    groq_api_key=api_key
    )
    
    db_user = "root"
    db_password = "root"
    db_host = "localhost"
    db_name = "tshirts"

    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}", sample_rows_in_table_info=3)

    to_vectorize  =[" ".join(example.values()) for example in few_shots]
    
    encoder = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    
    vector_store = FAISS.from_texts(to_vectorize, embedding=encoder, metadatas=few_shots)
    
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore= vector_store,
        k=3
    )
    
    example_prompt = PromptTemplate(
        input_variables=["Question","SQLQuery","SQLResult","Answer"],
        template = "\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )
    
    few_shot_prompt = FewShotPromptTemplate(
        input_variables=["input", "table_info", "top_k"],
        example_prompt = example_prompt,
        example_selector = example_selector,
        prefix = mysql_prompt,
        suffix = PROMPT_SUFFIX,
    )
            
    chain = SQLDatabaseChain.from_llm(llm,db,verbose= True, prompt=few_shot_prompt)
    
    return chain

if __name__ == "__main__":
    chain = few_shots_chain()

    
    