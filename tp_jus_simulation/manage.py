# api.py
from fastapi import FastAPI
from pydantic import BaseModel

api_app = FastAPI(title="API Simulation Jus de fruit")

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

@api_app.post("/simuler")
def calculer_bilan(p: Parametres):
    # 1. Filtration
    m1 = p.m0 - p.residus
    x1 = p.m0 * p.x0 / m1
    
    # 2. Melange
    m2 = m1 + p.mR
    x2 = (m1 * x1 + p.mR * p.xR) / m2
    
    # 3. Chauffage
    Q3 = m2 * p.Cp * (p.T3 - p.T2) / 3600
    
    # 4. Evaporation
    m4 = m2 * x2 / p.x4
    mv = m2 - m4
    Q4 = mv * p.lambda_v / 3600
    
    # 5. Refroidissement
    Q5 = m4 * p.Cp * (p.T4 - p.T5) / 3600
    
    # Erreur Bilan global
    erreur = (p.m0 + p.mR) - (p.residus + mv + m4)

    return {
        "Debit_filtre": round(m1, 2),
        "Debit_melange": round(m2, 2),
        "Concentration_melange": round(x2 * 100, 2),
        "Puissance_chauffage": round(Q3, 2),
        "Eau_evaporee": round(mv, 2),
        "Debit_concentre": round(m4, 2),
        "Puissance_evaporation": round(Q4, 2),
        "Puissance_refroidissement": round(Q5, 2),
        "Erreur_bilan": round(erreur, 4)
    }