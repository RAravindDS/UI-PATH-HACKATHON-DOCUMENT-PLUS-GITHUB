


############################################ TASK 0 extract images from the pdf ##########################################################
from pdf2html import *

#INPUTS 
pdf_path = "give your pdf path"
saving_path = "give your pdf saving path (give the folder path)" 

out = get_images_from_pdf(pdf_path, saving_path)
print(out)


############################################ TASK 1 convert text 2 graph and query ########################################################
from text2graph_main import * 

#INPUTS
pdf_path = "give your pdf path"
query = "ask your question"


graph = create_graph_database(pdf_path)
output = query_graph_database(graph, query)
print(output)



################################################## TASK 2 graph chat ######################################################################
from graph_chat import * 

model, processor = load_model()

## INPUTS 
query = "What is this graph is talking about?"
path = "1.jpg"

data_table = generate_table(path, model, processor)
out = process_query(data_table, query)
print(out)

############################################### TASK 3 table query (yet to come) ###########################################################
from table_query import * 

pdf_path = "1.jpg"
query = "which model has the highest score"

tables = AzureReadModule(give_byte_arr(pdf_path))
output = query(tables[0],query)
print(output)