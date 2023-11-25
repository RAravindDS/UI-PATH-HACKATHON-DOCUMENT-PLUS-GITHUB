
# This file contains the main code for converting the pdf 2 neo4j and query the neo4j database
""" 
How to use? 
```python 
from text2graph_main import * 
graph = create_graph_database("2.pdf")

query = "ask your question"
output = query_graph_database(graph, query)

"""


from dotenv import load_dotenv
from text2graph_utils import * 
from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain

load_dotenv()


def create_graph_database(pdf_pth:str): 

    def open_ai_len(text): 
        enc = tiktoken.encoding_for_model("gpt-4")
        return len(enc.encode(text))


    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 200,
            chunk_overlap  = 20,
            length_function = open_ai_len,
            separators=['\n\n', '\n', ' ', ''],
        )
    
    loader = PyPDFLoader(pdf_pth)
    pages = loader.load_and_split()

    all_documents = []
    for i in range(len(pages)): 
        all_documents.extend( text_splitter.create_documents([pages[i].page_content]) )
    
    
    from tqdm import tqdm
    for i, d in tqdm(enumerate(all_documents), total=len(all_documents)):
        try: 
            extract_and_store_graph(d)
        except: pass

    return graph 


def query_graph_database(graph, query): 
    graph.refresh_schema()

    cypher_chain = GraphCypherQAChain.from_llm(
        graph=graph,
        cypher_llm=ChatOpenAI(temperature=0, model="gpt-4"),
        qa_llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
        validate_cypher=True, # Validate relationship directions
        verbose=True
    )

    return cypher_chain.run(query)



