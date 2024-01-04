from google.protobuf import descriptor
import streamlit as st

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


from sklearn.preprocessing import StandardScaler, PolynomialFeatures   
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error

from functions import colors

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

    st.markdown("### Régression Polynomiale")

    data = pd.read_feather('data/lr_prod.ftr')

    description = """
        Dans le modèle polynomial suivant, nous allons pouvoir modifier certains paramètres afin de mesurer la performance de celui-ci.

        * *Taille de l'échantillon de test*: définie l'amplitude du jeu de donnée qui servira aux tests. Par, extention, cela défini aussi la taille du jeu d'entrainement.
        * *Degré Polynomial*:
            * 1 = affine
            * 2 = quadratique
            * 3 = cubique
            * 4 = quartique
            * 5 = quintique
    """

    st.write(description)

    with st.form('poly'):

        test_size = st.slider("Choississez la taille de l'échantillon de test:", .10, .80, .25, .05)

        degree = st.number_input('Degré Polynomial;', min_value=1, max_value=5, value=2, step=1)

        submitted = st.form_submit_button("Prédire !")
        

    if submitted:
        predict_poly(data, test_size, degree)


def predict_poly(data, test_size, degree):
    
    # On garde en test 2019 et 2020
    data_test = data[data['annee'] >= 2019]
    # On entraine sur 2013 à 2018
    data = data[data['annee'] < 2019]

    target = data['total_prod']
    features = data.drop(columns='total_prod')

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=test_size)

    poly = PolynomialFeatures(int(degree)) # Degré 3
    scaler = StandardScaler() # On utilise un StandardScaler
    lr = LinearRegression(n_jobs=-1) # Modèle linéaire

    # Création du Pipeline
    pipeline=make_pipeline(poly, scaler, lr)
    # Entrainement du Pipeline
    pipeline.fit(X_train,y_train)
    # Prédictions des données de test
    y_pred = pipeline.predict(X_test)

    score = pipeline.score(X_test, y_test)
    str_score = 'Test Score R2: ' + str(score)
    if score > .80:     st.success(str_score)
    elif score > .60:   st.warning(str_score)
    else:               st.error(str_score)

    score = pipeline.score(X_train, y_train)
    str_score = 'Train Score R2: ' + str(score)
    if score > .80:     st.success(str_score)
    elif score > .60:   st.warning(str_score)
    else:               st.error(str_score)

    # Prédictions sur les données de Tests
    X = data_test.drop(columns=['total_prod'])
    y = data_test['total_prod']

    # Affichages des métriques
    train_rmse_str = 'Train RMSE: ' + str(round(np.sqrt(mean_squared_error(y_test, y_pred)), 4))
    st.info(train_rmse_str)

    test_pred = pipeline.predict(X)
    test_rsme_str = 'Test RMSE: ' + str(round(np.sqrt(mean_squared_error(y, test_pred)), 4))
    st.info(test_rsme_str)

    fig, ax = plt.subplots(figsize = (16,8))

    plt.plot(test_pred, label='Prédictions', color=colors['green'], lw=3)
    plt.plot(y.values, label='Observations', alpha=.5, color=colors['purple'])

    plt.xlabel('Jours')
    plt.ylabel('Enegergie en GW')

    plt.xlim([0, 730])

    plt.title('Prévisons et valeurs réelles du modèle Polynomial')

    plt.legend()

    st.pyplot(fig)