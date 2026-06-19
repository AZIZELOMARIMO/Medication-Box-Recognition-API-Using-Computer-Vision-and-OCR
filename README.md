# Medication-Box-Recognition-API-Using-Computer-Vision-and-OCR
Recognizing a medication from an image of its box or packaging can be highly useful in digital healthcare  applications. Such recognition is challenging because it may involve visual similarity between products, varying  image quality, and multilingual text appearing on packaging, especially in Arabic and French.

# 1. Importation des bibliothèques
from fastapi import FastAPI, File, UploadFile.

import easyocr

import pandas as pd

import re

import numpy as np

from PIL import Image

import io

from rapidfuzz import fuzz


# 2. Création de l'API
app = FastAPI()

+ Cette ligne crée l'application FastAPI.
+ Toutes les requêtes des utilisateurs passeront par cette application.

# 3. Configuration CORS

app.add_middleware(
    CORSMiddleware,
    
    allow_origins=["*"],
    
    allow_credentials=True,
    
    allow_methods=["*"],
    
    allow_headers=["*"],
)

+ Cette partie autorise n'importe quel site web à communiquer avec notre API.
+ Sans cette configuration, un navigateur peut bloquer les requêtes.

# 4. Chargement du modèle OCR

reader = easyocr.Reader(['fr', 'en'])

+ Ici on crée un objet Reader ensuite charge le modèle d'intelligence artificielle d'EasyOCR.
+ Il est capable de reconnaître : Francais/Arabe/Anglais


# 5. Chargement de la base de données

meds = pd.read_excel("medications.xlsx", usecols="B:F")

meds.columns = meds.columns.str.strip().str.upper()

Explication:
+ Cette ligne ouvre le fichier Excel contenant les médicaments.
+ Enlève les espaces inutiles
+ Transforme tous les noms de colonnes en majuscules

# 6. Fonction OCR

def extract_text(image_bytes):  #Cette fonction extrait le texte contenu dans une image

image = Image.open(io.BytesIO(image_bytes))  #Le fichier reçu par l'API est constitué de bytes ce dernier transforme en image

image = np.array(image) #EasyOCR travaille avec des tableaux NumPy Donc on convertit l'image.

result = reader.readtext(image) #EasyOCR détecte toutes les zones de texte.

texts = [item[1] for item in result] #Cette ligne récupère uniquement le texte.

full_text = " ".join(texts).lower() #Tous les mots sont réunis dans une seule phrase.

ocr_numbers = set(re.findall(r'\d+', full_text)) #Cette ligne extrait uniquement les nombres.

return full_text, ocr_numbers

# 7. Filtre NOM

def filter_nom(full_text): #Cette fonction cherche les médicaments dont le nom commercial ressemble au texte détecté.

for _, row in meds.iterrows(): #On parcourt chaque ligne de la base.

nom = row["NOM"] # On récupère nom

similarity_nom = fuzz.partial_ratio(full_text, nom) #RapidFuzz calcule la ressemblance.

similarity_nom >=50 # Si cette condition est vérifier le médicament est conservé Sinon il est rejeté.

# 8. Filtre DCI

filter_dci() # Maintenant on compare le principe actif.RapidFuzz calcule encore la similarité,si elle est suffisante, le médicament reste dans la liste.

# 9. Scoring

def scoring() # Cette fonction ajoute des points.

score = 0

DOSAGE1 # On récupère dosage

re.findall() # extrait le nombre

score +=2 # Si ce nombre existe aussi dans l'image OCR,Le médicament gagne deux points.

# 10. Endpoint API

@app.post("/predict") # C'est la route principale lorsque l'utilisateur envoie une image,cette fonction est exécutée.

image_bytes = await file.read() # On lit l'image.

extract_text() # OCR

filter_nom() # Recherche du NOM

filter_dci() # Recherche du DCI

scoring() # Calcul du score

best = max(...) # Choix du meilleur médicament ayant le score le plus élevé

# 11. Résultat envoyé

Si un médicament est trouvé

return {
    "status":"found",     
    
    ...
} 

L'API renvoie par exemple :

{
 "status":"found",
 
 "medicine":{
 
   "NOM":"Doliprane",
   
   "DCI":"Paracétamol",

   "DOSAGE1":"1000",
   
   "UNITE_DOSAGE1":"mg",
   
   "FORME":"Comprimé"
 }
}




