from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import io
from PIL import Image
import replicate
from dotenv import load_dotenv


load_dotenv()

replicate = replicate.Client(api_token='r8_3Bap3zElUszqMy6QwIVRIF1zkWg6LUZ47Qbka') #replace with environment variable
def AzureReadModule(filename):
    endpoint = "https://quixyocr.cognitiveservices.azure.com/"
    key = "03462e450efa4e338d200900d30d8c7b"
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    ocr_module = "prebuilt-layout"
    poller = document_analysis_client.begin_analyze_document(
            ocr_module, filename) #, locale="en-US")
    
    
    final = {}
    for table_idx, table in enumerate(poller.result().tables):
        table_dict = table.to_dict()
        for idx in range(len(table_dict['cells'])):
            del table_dict['cells'][idx]['bounding_regions']
        final[table_idx] = table_dict
    return final

def give_byte_arr(image_link:str):
    try:
        img = Image.open(image_link).convert('RGB')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PDF')
        img_byte_arr = img_byte_arr.getvalue()
    except:
        with open(image_link, 'rb') as file:
            img_byte_arr = file.read()
    return img_byte_arr

def query_llm(table,query):
    prompt = f"""<|system|>\n You are an analyst who mainly deals with structured data. \
                Analyze the table according to the user query and give a correct, easy-to-understand, concise output.
                You will be given a table json and a user query, you should answer complex queries also by finding patterns in the rows and columns.</s>
                <|user|>
                {table} \

                Below is the query from the above table: \n 
                {query}</s>

                <|assistant|>
                """
    output = replicate.run(
            "tomasmcm/zephyr-7b-beta:961cd6665b811d0c43c0b9488b6dfa85ff5c7bfb875e93b4533e4c7f96c7c526",
            input={
                "top_k": 30,
                "top_p": 0.5,
                "prompt": prompt,
                "temperature": 0.1,
                "max_new_tokens": 200,
                "presence_penalty": 1
            })   
    return output