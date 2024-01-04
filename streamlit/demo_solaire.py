import streamlit as st

import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import ElasticNetCV
from sklearn.model_selection import train_test_split
from sklearn import preprocessing


sns.set_style = "seaborn-whitegrid"

sns.set(
    rc={
        "font.style": "normal",
        "axes.facecolor": "white",
        "grid.color": ".8",
        "grid.linestyle": "-",
        "figure.facecolor": "white",
        "figure.titlesize": 25,
        "text.color": "black",
        "xtick.color": "black",
        "ytick.color": "black",
        "axes.labelcolor": "black",
        "axes.grid": True,
        "axes.labelsize": 14,
        "xtick.labelsize": 12,
        "font.size": 14,
        "ytick.labelsize": 12,
        "legend.title_fontsize": 12
    }
)

def app():
    st.markdown("## Modèle de prédiction de la Production Solaire")
    st.markdown("### Modèle ElasticNetCV")

    descriptions = """
        Le modèle ElasticNetCV porte sur les années allant de 2016 à 2019 puisque les données concernant le vent et les températures ne sont pas disponibles pour les années précédentes.

        Nous allons nous concentrer sur:

        * *Données régionales*: Nouvelle-Aquitaine
        * *Variable cible*: production solaire moyenne
        * *Variables explicatives*: année, mois, vitesse du vent (moyenne), températures (min, max, mean), rayonnement solaire

        Les paramètres customisable pour le modèle sont:
        * cv = nombre de K-Folds
        * l1_ratio = divisé en deux, soit Lasso (proche de 1), soit de Ridge (proche de 0)
        * alphas = 
        * test_size = taille de l'échantillon de tests

    """

    st.markdown(descriptions)

    df = pd.read_csv("data/deb.csv")

    # on prend Nouvelle Aquitaine
    NAQ = df.loc[(df["Région"] == "Nouvelle-Aquitaine")]
    NAQ = NAQ.drop(['Région','Day', 'Date', 'Eolien_sum(MW)','Consommation-sum(MW)'], axis=1)
    # affichez dataframe head
    # preparation des données :
        
    # on remplace les variables Annéé et Mois par la production moyenne pour cet année
    # (pour indiquer l'influence attendue de ces variables sur la production)

    encode = {"Annee": {2016: 2104, 2017: 2257, 2018: 2788, 2019:3016}, 
            "Month": {1: 955, 2: 1812, 3: 2419, 4: 3026, 5:3361, 6:3597, 
                        7:3752, 8:3859, 9:3069, 10:2264, 11: 1407, 12:938}}
    NAQ = NAQ.replace(encode)

    # normalisation des données
    scaler = preprocessing.StandardScaler().fit(NAQ)
    NAQ[NAQ.columns] = pd.DataFrame(scaler.transform(NAQ), index=NAQ.index)
    
    with st.form('solaire'):

        test_size = st.slider("Choississez la taille de l'échantillon de test:", .10, .80, .25, .05)

        cv = st.number_input('CV:', min_value=2, max_value=10, value=8, step=1)

        l1 = st.selectbox("L1 Ratio:", ((0.1, 0.25, 0.5), (0.75, 0.85, 0.99))) 

        alphas = st.selectbox("Alphas:", ((0.001, 0.02, 0.1, 0.25), (0.5, 0.75, 0.9, 1)))

        submitted = st.form_submit_button("Prédire !")

    if submitted:
        predict_encv(NAQ, test_size, cv, l1, alphas, scaler) 

def predict_encv(data, test_size, cv, l1, alphas, scaler):
    # Separer target & variables explicatives
    features = data.drop('Solaire_sum(MW)', axis=1)
    target = data['Solaire_sum(MW)']

    # Separer train & test
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=test_size)

    # Application du model : ElasticNetCV
    model_en = ElasticNetCV(cv=cv, l1_ratio=l1, alphas=alphas, n_jobs=-1)
    model_en.fit(X_train, y_train)

    # calculer les scores
    pred_train = model_en.predict(X_train)
    pred_test = model_en.predict(X_test)

    Scoretrain = model_en.score(X_train, y_train)
    Scoretest = model_en.score(X_test, y_test)

    str_score = 'Train Score R2: ' + str(round(Scoretrain, 4))
    if Scoretrain > .80:     st.success(str_score)
    elif Scoretrain > .60:   st.warning(str_score)
    else:                    st.error(str_score)

    str_score = 'Test Score R2: ' + str(round(Scoretest, 4))
    if Scoretrain > .80:     st.success(str_score)
    elif Scoretrain > .60:   st.warning(str_score)
    else:                    st.error(str_score)

    moy = scaler.mean_[0]
    ec = scaler.scale_[0]
    predictions = pd.DataFrame({'true': (y_test*ec)+moy, 'predicted': np.round((pred_test*ec)+moy)}, 
             index=X_test.index)

    fig, ax = plt.subplots(figsize = (16,8))

    
    plt.plot((predictions.true.min(), predictions.true.max()), (predictions.true.min(), predictions.true.max()), color='#5930F2', lw=3, alpha=.5)
    plt.scatter(predictions.true, predictions.predicted, s=75, marker='o', color='#16E4CA', alpha=.7)
    plt.xlabel('Valeurs réelles')
    plt.ylabel('Prédictions')

    plt.xlim([1900, 3500])
    plt.ylim([1900, 3500])

    st.pyplot(fig)