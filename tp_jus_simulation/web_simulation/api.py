
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Simulation de fabrication du jus de fruit",
    description="Bilan de matière et bilan thermique",
    version="1.0"
)


class Parametres(BaseModel):
    m0: float = 1000.0
    x0: float = 0.10
    residus: float = 20.0
    mR: float = 100.0
    xR: float = 0.40
    Cp: float = 3.8
    T2: float = 20.0
    T3: float = 80.0
    x4: float = 0.40
    lambda_v: float = 2300.0
    T4: float = 80.0
    T5: float = 25.0


@app.get("/")
def accueil():
    return {
        "message": "Bienvenue dans la simulation du jus de fruit",
        "documentation": "/docs"
    }


@app.post("/simuler")
def simuler(p: Parametres):

    # Validation des parametres
    if p.m0 <= 0 or p.mR < 0:
        raise HTTPException(400, "Débits incorrects")

    if p.residus < 0 or p.residus >= p.m0:
        raise HTTPException(400, "Résidus incorrects")

    if not (0 < p.x0 <= 1 and 0 <= p.xR <= 1):
        raise HTTPException(400, "Concentrations incorrectes")

    if not (0 < p.x4 <= 1):
        raise HTTPException(400, "Concentration finale incorrecte")

    if p.Cp <= 0 or p.lambda_v <= 0:
        raise HTTPException(400, "Propriétés thermiques incorrectes")

    if p.T3 < p.T2 or p.T4 < p.T5:
        raise HTTPException(400, "Températures incorrectes")

    # 1. FILTRATION
    m1 = p.m0 - p.residus
    x1 = (p.m0 * p.x0) / m1

    if x1 > 1:
        raise HTTPException(400, "Concentration après filtration invalide")

    # 2. MELANGE
    m2 = m1 + p.mR
    x2 = (m1 * x1 + p.mR * p.xR) / m2

    # 3. CHAUFFAGE
    Q3 = m2 * p.Cp * (p.T3 - p.T2) / 3600

    # 4. EVAPORATION
    if p.x4 < x2:
        raise HTTPException(
            400,
            "La concentration finale doit être supérieure à la concentration initiale"
        )

    m4 = (m2 * x2) / p.x4
    mv = m2 - m4

    Q4 = mv * p.lambda_v / 3600

    # 5. REFROIDISSEMENT
    Q5 = m4 * p.Cp * (p.T4 - p.T5) / 3600

    # 6. BILAN GLOBAL
    erreur = (p.m0 + p.mR) - (
        p.residus + mv + m4
    )

    # RESULTATS
    return {
        "Debit_filtre_kg_h": round(m1, 2),
        "Concentration_filtre_pourcent": round(x1 * 100, 2),
        "Debit_melange_kg_h": round(m2, 2),
        "Concentration_melange_pourcent": round(x2 * 100, 2),
        "Puissance_chauffage_kW": round(Q3, 2),
        "Eau_evaporee_kg_h": round(mv, 2),
        "Debit_concentre_kg_h": round(m4, 2),
        "Puissance_evaporation_kW": round(Q4, 2),
        "Puissance_refroidissement_kW": round(Q5, 2),
        "Erreur_bilan_kg_h": round(erreur, 4),
        "Statut": "Simulation reussie"
    }