from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import io
from PIL import Image
import replicate
from dotenv import load_dotenv
import pypdfium2 as pdfium
import os

load_dotenv()

replicate = replicate.Client(api_token= os.environ['REPLICATE']) #replace with environment variable
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

def convert_inches_to_pix(bbox, pdf_size,img_size):
   x1, y1, x2, y2 = bbox
   x1_, x2_ = x1 * img_size[0] /pdf_size[0] , x2 * img_size[0] /pdf_size[0]
   y1_, y2_ = y1 * img_size[0] /pdf_size[0] , y2 * img_size[0] /pdf_size[0]
   bbox_new = map(round , [x1_,y1_,x2_,y2_])
   return list(bbox_new)


def AzureReadModule(filename):
    endpoint = "https://quixyocr.cognitiveservices.azure.com/"
    key = "03462e450efa4e338d200900d30d8c7b"
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    ocr_module = "prebuilt-layout"
    poller = document_analysis_client.begin_analyze_document(
            ocr_module, filename) #, locale="en-US")
    
    pdf = pdfium.PdfDocument(filename)

    final = {}
    for table_idx, table in enumerate(poller.result().tables):
        table_dict = table.to_dict()
        page_number = table_dict['bounding_regions'][0]['page_number']
        height = poller.result().pages[page_number-1].height
        width = poller.result().pages[page_number-1].width
        page = pdf.get_page(page_number-1)
        pil_image = page.render(scale = 300/72).to_pil()
        img_size = pil_image.size
        pdf_size = (width,height)
        polygon = table_dict['bounding_regions'][0]['polygon']
        x1 , y1 = polygon[0]['x'], polygon[0]['y']
        x2 , y2 = polygon[2]['x'], polygon[2]['y']
        box = x1, y1, x2,y2
        
        crop_coordinates = convert_inches_to_pix(box, pdf_size,img_size)
        cropped_img = pil_image.crop(crop_coordinates)
        cropped_img.show()
        cropped_img.save(f'table_output/table{table_idx}.png')
        for idx in range(len(table_dict['cells'])):
            del table_dict['cells'][idx]['bounding_regions']
        final[table_idx] = table_dict

    return final, poller

def query_llm(table,query):
    prompt = f"""<|system|>\n You are an analyst who mainly deals with structured data. \
                Analyze the table according to the user query and give a correct, easy-to-understand, concise output.
                You will be given a table json and a user query, you should answer complex queries also by finding patterns in the rows and columns. \
                Be consice and confident while giving answers.</s>
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