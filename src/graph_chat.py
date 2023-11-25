#
# This files contains the code for graph chat, you can import everything and start running the code 
#  

"""
How to use this? 
from graph_chat import * 

model, processor = load_model()
data_table = generate_table(path, model, processor)

query = "What is this graph is talking about?"
path = "1.jpg"

out = process_query(data_table, query)
print(out)
"""

import openai, os, torch  
import streamlit as st
from dotenv import load_dotenv
from transformers import Pix2StructForConditionalGeneration, Pix2StructProcessor
from PIL import Image
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

load_dotenv()
device = 'cuda' if torch.cuda.is_available() else 'cpu' 
llm = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo")
prompt = PromptTemplate(
    input_variables=["question", "elements"],
    template="""You are a helpful assistant that can answer question related to a graph image. You have the ability to see the graph image and answer questions about it. 
    I will give you a question and a the associated data table of the grah and you will answer the question.
        \n\n
        #Question: {question}
        #Elements: {elements}
        \n\n
        Your structured response:""",
    )

def load_model():
    model = Pix2StructForConditionalGeneration.from_pretrained('google/deplot').to(device)
    processor = Pix2StructProcessor.from_pretrained('google/deplot')

    return model, processor

def process_query(data_table, query):
    prompt = PromptTemplate(
    input_variables=["question", "elements"],
    template="""You are a helpful assistant capable of answering questions related to graph images.
     You possess the ability to view the graph image and respond to inquiries about it. 
     I will provide you with a question and the associated data table of the graph, and you will answer the question
        \n\n
        #Question: {question}
        #Elements: {elements}
        \n\n
        Your structured response:""",
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(question=query, elements=data_table)

    return response

def generate_table(uploaded_file, model, processor):
    image = Image.open(uploaded_file)
    # model, processor = load_model()
    inputs = processor(images=image, text="Generate underlying data table of the figure below:", return_tensors="pt").to(device)
    predictions = model.generate(**inputs, max_new_tokens=512)

    return processor.decode(predictions[0], skip_special_tokens=True)




# model, processor = load_model()



 

### AFTER this in separate file, before this everything should be in same file 

# data_table = generate_table(path, model, processor)
# query = "What is this graph is talking about?"
# path = "1.jpg"
# out = process_query(data_table, query)
