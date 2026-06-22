# Medication-Box-Recognition-API-Using-Computer-Vision-and-OCR
Recognizing a medication from an image of its box or packaging can be highly useful in digital healthcare  applications. Such recognition is challenging because it may involve visual similarity between products, varying  image quality, and multilingual text appearing on packaging, especially in Arabic and French.

# FastAPI Medication Recognition API

## 1. Importation des bibliothèques

Le projet utilise plusieurs bibliothèques Python :

- **FastAPI** : création de l'API REST.
- **EasyOCR** : extraction du texte depuis une image.
- **Pandas** : lecture et manipulation de la base de données des médicaments.
- **Regular Expressions (re)** : extraction des nombres présents dans le texte OCR.
- **NumPy** : conversion des images en tableaux compatibles avec EasyOCR.
- **Pillow (PIL)** : ouverture des images reçues par l'API.
- **io** : lecture des fichiers envoyés par l'utilisateur.
- **RapidFuzz** : calcul de la similarité entre le texte OCR et les médicaments de la base.

---

## 2. Création de l'API

```python
app = FastAPI()
```

Cette ligne crée l'application **FastAPI**.

Toutes les requêtes envoyées par les utilisateurs passent par cette application.

---

## 3. Configuration CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Cette configuration autorise les applications web à communiquer avec l'API.

Elle évite les erreurs de type **Cross-Origin Resource Sharing (CORS)** lors des appels depuis un navigateur.

---

## 4. Chargement du modèle OCR

```python
reader = easyocr.Reader(['fr', 'en'])
```

Le modèle EasyOCR est chargé une seule fois au démarrage de l'application.

Il permet de reconnaître le texte présent dans les images.

**Langues supportées :**

- Français
- Anglais

---

## 5. Chargement de la base de données

```python
meds = pd.read_excel("medications.xlsx", usecols="B:F")
meds.columns = meds.columns.str.strip().str.upper()
```

La base de données est chargée depuis un fichier Excel.

Les colonnes sont ensuite :

- nettoyées (suppression des espaces inutiles) ;
- converties en majuscules afin de faciliter les comparaisons.

---

## 6. Fonction OCR

```python
def extract_text(image_bytes):
```

Cette fonction extrait le texte contenu dans l'image.

### Étapes :

1. Conversion des données reçues (*bytes*) en image.
2. Conversion de l'image en tableau NumPy.
3. Détection du texte avec EasyOCR.
4. Fusion de tous les mots détectés.
5. Conversion du texte en minuscules.
6. Extraction des nombres présents dans le texte (dosages).

La fonction retourne :

- le texte complet détecté ;
- les nombres extraits.

---

## 7. Filtre par NOM

```python
def filter_nom(full_text):
```

Cette fonction recherche les médicaments dont le **nom commercial** ressemble au texte détecté.

Pour chaque médicament :

- récupération du nom (`NOM`) ;
- calcul du pourcentage de similarité avec **RapidFuzz** ;
- conservation des médicaments dont la similarité est supérieure ou égale à **50 %**.

---

## 8. Filtre par DCI

```python
def filter_dci(...)
```

Cette étape compare le **principe actif (DCI)** avec le texte extrait par OCR.

RapidFuzz calcule également la similarité.

Les médicaments ayant une correspondance suffisante sont conservés.

---

## 9. Calcul du score

```python
def scoring(...)
```

Chaque médicament reçoit un score en fonction des informations retrouvées dans l'image.

### Exemple :

- correspondance du dosage → **+2 points**
- correspondance du nom → points supplémentaires
- correspondance de la DCI → points supplémentaires

Le médicament ayant le score le plus élevé sera sélectionné.

---

## 10. Endpoint de l'API

```python
@app.post("/predict")
```

Cette route est appelée lorsqu'un utilisateur envoie une image.

Les étapes exécutées sont les suivantes :

1. Lecture de l'image.
2. Extraction du texte (OCR).
3. Recherche par NOM.
4. Recherche par DCI.
5. Calcul des scores.
6. Sélection du meilleur médicament.

---

## 11. Réponse de l'API

Si un médicament est identifié, l'API retourne une réponse au format JSON.

### Exemple

```json
{
  "status": "found",
  "medicine": {
    "NOM": "Doliprane",
    "DCI": "Paracétamol",
    "DOSAGE1": "1000",
    "UNITE_DOSAGE1": "mg"
  }
}
```

Si aucun médicament ne correspond, l'API renvoie :

```json
{
  "status": "not_found"
}
```

---




   # Arabic Medication Detection using OCR

##  Description

This project detects the name of a medication written in Arabic from an image using **EasyOCR**. The extracted text is compared with a CSV database containing Arabic medication names to identify the medication.

---

##  Features

- Extract Arabic and English text from images using EasyOCR.
- Read a medication database from a CSV file.
- Search for the detected medication name in the database.
- Display Arabic text correctly using `arabic_reshaper` and `python-bidi`.

---

##  Project Structure

```
project/
│── main.py
│── medicaments_arabe.csv
│── ar.jpeg
│── README.md
```

---

##  Requirements

Install the required Python packages:

```bash
pip install pandas easyocr arabic-reshaper python-bidi
```

---

##  Dataset

The project uses a CSV file named:

```
medicaments_arabe.csv
```

The CSV file should contain at least the following column:

| Column |
|---------|
| nom_ar |

Example:

| nom_ar |
|--------|
| باراسيتامول |
| أموكسيسيلين |

---

##  How It Works

1. Load the medication database.
2. Read the input image.
3. Extract Arabic text using EasyOCR.
4. Convert the extracted text to lowercase.
5. Search for the medication name in the CSV database.
6. Display the OCR result and the detected medication.

---

##  Usage

Replace the image path if needed:

```python
image = "ar.jpeg"
```

Run the program:

```bash
python mainarabic.py
```

Example output:

```
OCR Text:
باراسيتامول

Detected Medication:
باراسيتامول
```

---

##  Libraries Used

- pandas
- easyocr
- arabic-reshaper
- python-bidi

---

##  Notes

- The image should contain clear Arabic text for better OCR accuracy.
- The medication database must include Arabic medication names in the `nom_ar` column.
- OCR accuracy depends on the quality of the input image.

---

##  Author

Developed as a simple OCR-based Arabic medication recognition project using Python.
   
   "FORME":"Comprimé"
 }
}




