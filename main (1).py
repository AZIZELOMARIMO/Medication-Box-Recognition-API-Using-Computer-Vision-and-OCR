from fastapi import FastAPI, File, UploadFile
import easyocr
import pandas as pd
import re
import numpy as np
from PIL import Image
import io
from rapidfuzz import fuzz

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# =========================
# OCR (load once)
# =========================
reader = easyocr.Reader(['fr', 'en'])

# =========================
# Excel (load once)
# =========================
meds = pd.read_excel("medications.xlsx", usecols="B:F")
meds.columns = meds.columns.str.strip().str.upper()


# =========================
# OCR FUNCTION
# =========================
def extract_text(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = np.array(image)

    result = reader.readtext(image)
    texts = [item[1] for item in result]

    full_text = " ".join(texts).lower()

    ocr_numbers = set(re.findall(r'\d+', full_text))

    return full_text, ocr_numbers


# =========================
# FILTER NOM
# =========================
def filter_nom(full_text):
    candidates = []

    for _, row in meds.iterrows():
        nom = str(row.get("NOM", "")).lower().strip()

        if not nom:
            continue

        similarity_nom = fuzz.partial_ratio(full_text, nom)

        if similarity_nom >= 80:
            candidates.append({
                "row": row,
                "similarity_nom": similarity_nom
            })

    return candidates


# =========================
# FILTER DCI
# =========================
def filter_dci(candidates, full_text):
    results = []

    for c in candidates:
        row = c["row"]

        dci1 = str(row.get("DCI1", "")).lower().strip()

        if not dci1:
            continue

        similarity_dci = fuzz.partial_ratio(full_text, dci1)

        if similarity_dci >= 80:
            results.append({
                "row": row,
                "similarity_nom": c["similarity_nom"],
                "similarity_dci": similarity_dci
            })

    return results


# =========================
# SCORING
# =========================
def scoring(candidates, ocr_numbers):
    results = []

    for c in candidates:
        row = c["row"]

        score = 0

        dosage = str(row.get("DOSAGE1", "")).strip()

        if dosage:
            dosage_number = re.findall(r'\d+', dosage)

            if dosage_number and dosage_number[0] in ocr_numbers:
                score += 2

        results.append({
            "row": row,
            "score": score,
            "similarity_nom": c["similarity_nom"],
            "similarity_dci": c["similarity_dci"]
        })

    return results


# =========================
# API ENDPOINT
# =========================
@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    image_bytes = await file.read()

    # OCR
    full_text, ocr_numbers = extract_text(image_bytes)

    # NOM FILTER
    candidates_nom = filter_nom(full_text)

    if len(candidates_nom) < 1:
        return {"status": "not_found", "step": "nom","ocr_text": full_text}

    # DCI FILTER
    candidates_dci = filter_dci(candidates_nom, full_text)

    if len(candidates_dci) < 1:
        return {"status": "not_found", "step": "dci","ocr_text": full_text}

    # SCORING
    results = scoring(candidates_dci, ocr_numbers)

    if len(results) == 0:
        return {"status": "not_found", "step": "score","ocr_text": full_text}

    # BEST MATCH
    best = max(
        results,
        key=lambda x: (
            x["score"],
            x["similarity_nom"],
            x["similarity_dci"]
        )
    )

    row = best["row"]

    return {
        "status": "found",
        "ocr_text": full_text,
        "similarity_nom": best["similarity_nom"],
        "similarity_dci": best["similarity_dci"],
        "medicine": {
            "NOM": row.get("NOM"),
            "DCI": row.get("DCI1"),
            "DOSAGE1": row.get("DOSAGE1"),
            "UNITE_DOSAGE1": row.get("UNITE_DOSAGE1"),
            "FORME": row.get("FORME"),
        }
    }