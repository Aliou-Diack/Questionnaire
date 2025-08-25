import streamlit as st
import pandas as pd
import os
from datetime import date


st.set_page_config(page_title="Questionnaire Mortalité", layout="centered")

FICHIER = "reponses_questionnaire.xlsx"  # fichier où stocker les données

st.title("📝 Questionnaire - Mortalité Maternelle & Infantile")

with st.form("questionnaire", ):
    #-------------  Context et Menage  -------------------------
    st.header("**Section A: Ménage & Contexte**")
    identifiantMénage= st.number_input("Identifiant ménage", min_value=1, max_value=400, step = 1)
    lieu_residance= st.radio("Lieu de résidance", ["Rurale", "Urbain"])
    Region= st.radio("Region de résidance", ["Tamba", "Kolda"])
    Eau = st.radio("avez vous de l'Eau potable au domicile?", ["Oui", "Non"])
    SANIT = st.selectbox("Type d’assainissement principal", ["Aucun","lat brut", "lat amérioré", "WC raccordé"])
    Quin_Ric= st.selectbox("Quintile de richesse (score)", ["Q1 (pauvre)", "Q2", "Q3", "Q4", "Q5"])
    st.markdown("---")



    # -------- Bloc Maternité --------
    st.header("Section B: Caractéristiques maternelles")
    M_AGE = st.number_input("Âge de la mère (années)", min_value=10, max_value=60, step=1)

    M_EDU = st.selectbox("Niveau d’instruction", 
                        options={0:"Aucun",1:"Primaire",2:"Secondaire",3:"Supérieur"}.keys(),
                        format_func=lambda x: {0:"Aucun",1:"Primaire",2:"Secondaire",3:"Supérieur"}[x])

    M_MARIT = st.selectbox("Statut matrimonial", 
                        options={1:"Célibataire",2:"Mariée",3:"Union",4:"Div/Veuve"}.keys(),
                        format_func=lambda x: {1:"Célibataire",2:"Mariée",3:"Union",4:"Div/Veuve"}[x])

    M_BMI = st.number_input("IMC avant/1er trimestre (kg/m²)", min_value=10.0, max_value=50.0, step=0.1)

    M_ANEM = st.radio("Anémie pendant la grossesse ?", [0,1,9], 
                    format_func=lambda x: {1:"Oui",0:"Non",9:"Inconnu"}[x])

    M_HTN = st.radio("HTA/Prééclampsie/Éclampsie diagnostiquée ?", [0,1,9], 
                    format_func=lambda x: {1:"Oui",0:"Non",9:"Inconnu"}[x])

    M_HIV = st.radio("Statut VIH", [0,1,9], 
                    format_func=lambda x: {1:"Positif",0:"Négatif",9:"Inconnu/Non testé"}[x])

    M_MAL = st.selectbox("Épisodes de paludisme pendant la grossesse", 
                        options={0:"Non",1:"Oui, 1 fois",2:"Oui, ≥2 fois",9:"Inconnu"}.keys(),
                        format_func=lambda x: {0:"Non",1:"Oui, 1 fois",2:"Oui, ≥2 fois",9:"Inconnu"}[x])

    M_PNC = st.number_input("Nombre de consultations prénatales", min_value=0, max_value=20, step=1)

    M_ITN = st.radio("A dormi sous moustiquaire imprégnée (MII) la nuit passée ?", [0,1], 
                    format_func=lambda x: {1:"Oui",0:"Non"}[x])

    M_BIRTHINT = st.number_input("Intervalle avec grossesse précédente (mois) (888 si primipare)", min_value=0, max_value=888, step=1)

    M_PARITY = st.number_input("Parité (accouchements ≥28 SA)", min_value=0, max_value=20, step=1)

    M_ANC_BP = st.radio("TA contrôlée pendant la CPN ?", [0,1,9], 
                        format_func=lambda x: {1:"Oui",0:"Non",9:"Inconnu"}[x])
    st.markdown("---")
# ------------------------------------------------------------------------------

    st.markdown("### Section C. Accouchement & Système de santé")

    DELIV_PLACE = st.selectbox("Lieu d’accouchement", 
        options={1:"Domicile",2:"CS",3:"Hôpital",4:"Clinique"}.keys(),
        format_func=lambda x: {1:"Domicile",2:"CS",3:"Hôpital",4:"Clinique"}[x])

    DELIV_ATT = st.radio("Personnel qualifié présent ?", [1,0], 
        format_func=lambda x: {1:"Oui",0:"Non"}[x])

    DELIV_MODE = st.selectbox("Mode d’accouchement", 
        options={1:"Voie basse",2:"Césarienne",3:"Instrumental"}.keys(),
        format_func=lambda x: {1:"Voie basse",2:"Césarienne",3:"Instrumental"}[x])

    REF_TIME = st.number_input("Temps d’évacuation/référence (minutes)", min_value=0, max_value=720, step=5)

    BLOOD_AV = st.radio("Sang disponible pour transfusion ?", [1,0,9], 
        format_func=lambda x: {1:"Oui",0:"Non",9:"NA"}[x])

    PPH = st.radio("Hémorragie du post-partum ?", [1,0,9], 
        format_func=lambda x: {1:"Oui",0:"Non",9:"Inconnu"}[x])

    SEPSIS = st.radio("Infection/septicémie post-partum ?", [1,0,9], 
        format_func=lambda x: {1:"Oui",0:"Non",9:"Inconnu"}[x])


    st.markdown("### Section D. Nouveau-né & Soins postnataux")

    B_SEX = st.radio("Sexe du nouveau-né", [1,2], format_func=lambda x: {1:"Masculin",2:"Féminin"}[x])
    B_GA = st.number_input("Âge gestationnel (semaines) (99 si inconnu)", min_value=20, max_value=99, step=1)
    B_WT = st.number_input("Poids de naissance (g) (9999 si inconnu)", min_value=500, max_value=9999, step=10)
    APGAR5 = st.slider("Score d’Apgar à 5 minutes", 0, 10, 7)

    RESUS = st.radio("Réanimation nécessaire ?", [1,0,9], format_func=lambda x: {1:"Oui",0:"Non",9:"Inconnu"}[x])
    BF_INIT = st.radio("Allaitement initié <1h ?", [1,0,9], format_func=lambda x: {1:"Oui",0:"Non",9:"NA"}[x])
    EBF_6M = st.radio("Allaitement exclusif à 6 mois ?", [1,0,9], format_func=lambda x: {1:"Oui",0:"Non",9:"NA"}[x])
    IMMUN = st.radio("Statut vaccinal", [0,1,2], format_func=lambda x: {0:"Non",1:"Partiel",2:"Complet"}[x])
    NEO_INF = st.radio("Infection néonatale ?", [1,0,9], format_func=lambda x: {1:"Oui",0:"Non",9:"Inconnu"}[x])

    DIARR = st.number_input("Nb d’épisodes de diarrhée (0–11 mois)", min_value=0, max_value=20, step=1)
    ARI = st.number_input("Nb d’épisodes d’IRA (0–11 mois)", min_value=0, max_value=20, step=1)


    st.markdown("### Section E. Accès & Retards")

    PNC_POST = st.radio("Consultation postnatale mère <48h ?", [1,0], format_func=lambda x: {1:"Oui",0:"Non"}[x])
    PPC_NEWBORN = st.radio("Visite postnatale du nouveau-né <48h ?", [1,0], format_func=lambda x: {1:"Oui",0:"Non"}[x])
    DIST_FAC = st.number_input("Distance au centre de santé (km)", min_value=0, max_value=500, step=1)
    COST_CARE = st.number_input("Coût direct recours aux soins (FCFA)", min_value=0, max_value=1000000, step=1000)

    DELAY_1 = st.radio("Retard 1: Décision tardive ?", [1,0], format_func=lambda x: {1:"Oui",0:"Non"}[x])
    DELAY_2 = st.radio("Retard 2: Difficultés transport ?", [1,0], format_func=lambda x: {1:"Oui",0:"Non"}[x])
    DELAY_3 = st.radio("Retard 3: Problèmes accueil ?", [1,0], format_func=lambda x: {1:"Oui",0:"Non"}[x])


    st.markdown("### Section F. Issues (Outcomes)")

    MAT_DEATH = st.radio("Décès maternel ?", [1,0], format_func=lambda x: {1:"Oui",0:"Non"}[x])
    NND = st.radio("Décès néonatal (0–28j) ?", [1,0], format_func=lambda x: {1:"Oui",0:"Non"}[x])
    IMD = st.radio("Décès infantile (<1 an) ?", [1,0], format_func=lambda x: {1:"Oui",0:"Non"}[x])

    # Logique conditionnelle
    DOD, CAUSE = None, None
    if MAT_DEATH==1 or NND==1 or IMD==1:
        DOD = st.date_input("Date du décès (si applicable)", value=date.today())
        CAUSE = st.selectbox("Cause probable du décès",
            options={1:"Hémorragie",2:"HTA/éclampsie",3:"Infection",4:"Asphyxie",
                    5:"Prématurité",6:"Paludisme",7:"Autre"}.keys(),
            format_func=lambda x: {1:"Hémorragie",2:"HTA/éclampsie",3:"Infection",4:"Asphyxie",
                                5:"Prématurité",6:"Paludisme",7:"Autre"}[x])




    # -------- Bloc Enfant --------
    st.header("Section C: Accouchement & Système de santé")
    sexe_enfant = st.radio("Sexe de l’enfant", ["Masculin", "Féminin"])
    poids_naissance = st.number_input("Poids de naissance (en grammes)", min_value=500, max_value=6000, step=10)
    allaitement = st.radio("Allaitement exclusif ?", ["Oui", "Non"])
    vaccination = st.radio("Carnet de vaccination à jour ?", ["Oui", "Non"])
    mortalite_infantile = st.radio("Décès de l’enfant avant 1 an ?", ["Oui", "Non"])

    # -------- Bloc Mortalité maternelle --------
    mortalite_maternelle = st.radio("Décès de la mère lié à la grossesse ou accouchement ?", ["Oui", "Non"])

    # --- SUBMIT ---
    submitted = st.form_submit_button("✅ Enregistrer la réponse")

    if submitted:
        # Créer un dictionnaire
        nouvelle_reponse = {
            "Identifiant_ménage": identifiantMénage,
            "Lieu_résidance": lieu_residance,
            "Région": Region,
            "Eau_potable": Eau,
            "Assainissement": SANIT,
            "Quintile_richesse": Quin_Ric,

            "Âge_mère": M_AGE,
            "Niveau_instruction": M_EDU,
            "Statut_matrimonial": M_MARIT,
            "IMC": M_BMI,
            "Anémie": M_ANEM,
            "HTA": M_HTN,
            "VIH": M_HIV,
            "Paludisme": M_MAL,
            "Nb_CPN": M_PNC,
            "Moustiquaire": M_ITN,
            "Intervalle_grossesse": M_BIRTHINT,
            "Parité": M_PARITY,
            "TA_CPN": M_ANC_BP,

            "Lieu_accouchement": DELIV_PLACE,
            "Accouchement_assisté": DELIV_ATT,
            "Mode_accouchement": DELIV_MODE,
            "Temps_référence": REF_TIME,
            "Sang_disponible": BLOOD_AV,
            "Hémorragie": PPH,
            "Septicémie": SEPSIS,

            "Sexe_nouveau_né": B_SEX,
            "Âge_gestationnel": B_GA,
            "Poids_naissance": B_WT,
            "Apgar_5min": APGAR5,
            "Réanimation": RESUS,
            "Allaitement_<1h": BF_INIT,
            "Allaitement_6mois": EBF_6M,
            "Vaccination": IMMUN,
            "Infection_néonatale": NEO_INF,
            "Diarrhée": DIARR,
            "IRA": ARI,

            "Consult_postnatale_mère": PNC_POST,
            "Consult_postnatale_nouveau_né": PPC_NEWBORN,
            "Distance_santé": DIST_FAC,
            "Coût_soins": COST_CARE,
            "Retard_décision": DELAY_1,
            "Retard_transport": DELAY_2,
            "Retard_accueil": DELAY_3,

            "Décès_maternel": MAT_DEATH,
            "Décès_néonatal": NND,
            "Décès_infantile": IMD,
            "Date_décès": DOD,
            "Cause_décès": CAUSE,

            # Bloc enfant simplifié (doublon à enlever si inutile)
            "Sexe_enfant": sexe_enfant,
            "Poids_enfant": poids_naissance,
            "Allaitement": allaitement,
            "Vaccination_ok": vaccination,
            "Mortalité_infantile": mortalite_infantile,
            "Mortalité_maternelle": mortalite_maternelle
        }

        # Charger l’ancien fichier s’il existe, sinon créer un nouveau
        if os.path.exists(FICHIER):
            df = pd.read_excel(FICHIER)
            df = pd.concat([df, pd.DataFrame([nouvelle_reponse])], ignore_index=True)
        else:
            df = pd.DataFrame([nouvelle_reponse])

        # Sauvegarder dans Excel
        df.to_excel(FICHIER, index=False)

        # Convertir la date en texte pour éviter erreur pyarrow
        if "Date_décès" in df.columns:
            df["Date_décès"] = df["Date_décès"].astype(str)

        st.success("Réponse enregistrée dans le fichier ✅")
        st.dataframe(df.tail(5))  # afficher les 5 dernières réponses
