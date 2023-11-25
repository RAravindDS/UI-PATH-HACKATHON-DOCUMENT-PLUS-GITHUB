#
# This notebook help to get the images that present in the pdf 
# 
# Tested working 💚

"""How to use? 

from task_0_pdf2html import * 

pdf_path = "give your pdf path (give the pdf path)"
saving_path = "give your pdf saving path (give the folder path)" 

out = get_images_from_pdf(pdf_path, saving_path)
print(out)
"""

import fitz, io 
from PIL import Image 
from ensure import ensure_annotations


@ensure_annotations 
def get_images_from_pdf(pdf_path:str, saving_path:str) -> str: 
    pdf_file = fitz.open(pdf_path)
     
    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]

        for image_index, img in enumerate(page.get_images(), start=1):
            xref = img[0]
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))
            image.save(open(f"{saving_path}/image{page_index+1}_{image_index}.{image_ext}", "wb"))

    return "Done bro"
    


