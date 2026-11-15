
import streamlit as st
import requests
import pandas as pd

# Configuration
st.set_page_config(
    page_title="Simulation Jus de Fruit",
    page_icon="🍊",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/simuler"

# Style
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
h1 {
    color: #e87516;
    text-align: center;
}
h2, h3 {
    color: #285943;
}
</style>
""", unsafe_allow_html=True)

# En-tete
st.title("🍊 SIMULATION DE FABRICATION DU JUS DE FRUIT")
st.markdown(
    "<h3 style='text-align:center'>"
    "Bilan de matière et bilan thermique"
    "</h3>",
    unsafe_allow_html=True
)

st.divider()

st.info(
    "Bienvenue dans notre application de simulation "
    "du procédé de fabrication du jus de fruit."
)

# Parametres
st.header("⚙️ Paramètres de fonctionnement")

with st.form("simulation_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("1. Filtration")
        m0 = st.number_input(
            "Débit initial (kg/h)", min_value=0.1,
            value=1000.0
        )
        x0 = st.number_input(
            "Concentration initiale",
            min_value=0.001, max_value=1.0,
            value=0.10
        )
        residus = st.number_input(
            "Résidus (kg/h)", min_value=0.0,
            value=20.0
        )

    with col2:
        st.subheader("2. Mélange")
        mR = st.number_input(
            "Débit de retour (kg/h)",
            min_value=0.0, value=100.0
        )
        xR = st.number_input(
            "Concentration du retour",
            min_value=0.0, max_value=1.0,
            value=0.40
        )
        Cp = st.number_input(
            "Chaleur spécifique (kJ/kg°C)",
            min_value=0.01, value=3.8
        )

    with col3:
        st.subheader("3. Chauffage")
        T2 = st.number_input(
            "Température initiale (°C)",
            value=20.0
        )
        T3 = st.number_input(
            "Température de chauffage (°C)",
            value=80.0
        )
        st.write("")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.subheader("4. Évaporation")
        x4 = st.number_input(
            "Concentration finale",
            min_value=0.001, max_value=1.0,
            value=0.40
        )
        lambda_v = st.number_input(
            "Chaleur latente (kJ/kg)",
            min_value=0.01, value=2300.0
        )

    with col5:
        st.subheader("5. Refroidissement")
        T4 = st.number_input(
            "Température avant refroidissement (°C)",
            value=80.0
        )
        T5 = st.number_input(
            "Température finale (°C)",
            value=25.0
        )

    with col6:
        st.subheader("Simulation")
        st.write("Vérifiez les paramètres avant de lancer le calcul.")
        lancer = st.form_submit_button(
            "🚀 LANCER LA SIMULATION",
            use_container_width=True
        )

# Execution
if lancer:

    donnees = {
        "m0": m0,
        "x0": x0,
        "residus": residus,
        "mR": mR,
        "xR": xR,
        "Cp": Cp,
        "T2": T2,
        "T3": T3,
        "x4": x4,
        "lambda_v": lambda_v,
        "T4": T4,
        "T5": T5
    }

    try:
        with st.spinner("Calcul de la simulation en cours..."):

            response = requests.post(
                API_URL,
                json=donnees,
                timeout=10
            )

            response.raise_for_status()
            resultats = response.json()

        if "erreur" in resultats:
            st.error(resultats["erreur"])

        else:
            st.success("Simulation réalisée avec succès !")

            st.divider()

            # Resultats
            st.header("📊 Résultats de la simulation")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Débit filtré",
                f"{resultats['Debit_filtre_kg_h']} kg/h"
            )

            c2.metric(
                "Débit mélangé",
                f"{resultats['Debit_melange_kg_h']} kg/h"
            )

            c3.metric(
                "Concentration du mélange",
                f"{resultats['Concentration_melange_pourcent']} %"
            )

            c4, c5, c6 = st.columns(3)

            c4.metric(
                "Eau évaporée",
                f"{resultats['Eau_evaporee_kg_h']} kg/h"
            )

            c5.metric(
                "Débit concentré",
                f"{resultats['Debit_concentre_kg_h']} kg/h"
            )

            c6.metric(
                "Erreur du bilan",
                f"{resultats['Erreur_bilan_kg_h']} kg/h"
            )

            st.divider()

            # Bilan thermique
            st.header("🔥 Bilan thermique")

            t1, t2, t3 = st.columns(3)

            t1.metric(
                "Puissance de chauffage",
                f"{resultats['Puissance_chauffage_kW']} kW"
            )

            t2.metric(
                "Puissance d'évaporation",
                f"{resultats['Puissance_evaporation_kW']} kW"
            )

            t3.metric(
                "Puissance de refroidissement",
                f"{resultats['Puissance_refroidissement_kW']} kW"
            )

            st.divider()

            # Tableau
            st.header("📋 Tableau récapitulatif")

            tableau = pd.DataFrame({
                "Paramètre": [
                    "Débit filtré",
                    "Débit mélangé",
                    "Concentration du mélange",
                    "Eau évaporée",
                    "Débit concentré",
                    "Puissance chauffage",
                    "Puissance évaporation",
                    "Puissance refroidissement"
                ],
                "Valeur": [
                    resultats["Debit_filtre_kg_h"],
                    resultats["Debit_melange_kg_h"],
                    resultats["Concentration_melange_pourcent"],
                    resultats["Eau_evaporee_kg_h"],
                    resultats["Debit_concentre_kg_h"],
                    resultats["Puissance_chauffage_kW"],
                    resultats["Puissance_evaporation_kW"],
                    resultats["Puissance_refroidissement_kW"]
                ]
            })

            st.dataframe(
                tableau,
                use_container_width=True,
                hide_index=True
            )

            # Graphique
            st.header("📈 Graphique des puissances thermiques")

            graphique = pd.DataFrame({
                "Puissance (kW)": [
                    resultats["Puissance_chauffage_kW"],
                    resultats["Puissance_evaporation_kW"],
                    resultats["Puissance_refroidissement_kW"]
                ]
            }, index=[
                "Chauffage",
                "Évaporation",
                "Refroidissement"
            ])

            st.bar_chart(graphique)

            # Telechargement
            st.divider()

            st.download_button(
                label="📥 Télécharger les résultats CSV",
                data=tableau.to_csv(index=False).encode("utf-8-sig"),
                file_name="resultats_simulation.csv",
                mime="text/csv"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "Impossible de contacter l'API. "
            "Veuillez démarrer le serveur FastAPI."
        )

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de communication : {e}")

st.divider()

st.markdown(
    "<p style='text-align:center;color:gray'>"
    "Simulation de fabrication du jus de fruit | Projet académique"
    "</p>",
    unsafe_allow_html=True
)
