# Medication-Box-Recognition-API-Using-Computer-Vision-and-OCR
Recognizing a medication from an image of its box or packaging can be highly useful in digital healthcare  applications. Such recognition is challenging because it may involve visual similarity between products, varying  image quality, and multilingual text appearing on packaging, especially in Arabic and French.

# 1. Importation des bibliothèques
from fastapi import FastAPI, File, UploadFile
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

meds = pd.read_excel("medications.xlsx", usecols="B:F")                                                                                    meds.columns = meds.columns.str.strip().str.upper()

Explication:
+ Cette ligne ouvre le fichier Excel contenant les médicaments.
+ Enlève les espaces inutiles
+ Transforme tous les noms de colonnes en majuscules
