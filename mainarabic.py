import pandas as pd
import easyocr
import arabic_reshaper
from bidi.algorithm import get_display
import cv2

# Read database
meds = pd.read_csv("medicaments_arabe.csv")
meds.columns = meds.columns.str.lower()



# OCR للعربية والإنجليزية
reader_ar = easyocr.Reader(['ar', 'en'])

def extract_text(image_path):


    #result_fr = reader_fr.readtext(image_path)
    result_ar = reader_ar.readtext(image_path)


    text_ar = " ".join([r[1] for r in result_ar])

    final_text = text_ar

    return final_text.lower()

# search
def search_med(final_text):
    for index, row in meds.iterrows():
        if row["nom_ar"] in final_text:
            return row["nom_ar"]
    return "Not found"

# TEST Complet
image = "ar.jpeg"


text = extract_text(image)

reshaped_text = arabic_reshaper.reshape(text)
display_text = get_display(reshaped_text)



print("OCR Text:")
print(display_text)
result = search_med(text)


reshaped_result = arabic_reshaper.reshape(result)
display_result = get_display(reshaped_result)

print("Detected Medication:", display_result)