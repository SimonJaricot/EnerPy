from google.protobuf import descriptor
from scipy.sparse.base import MAXPRINT
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

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
    st.markdown("## Modèle de prédiction de la Production Eolienne")
    st.markdown("### Modèle de Regression Random Forest")

    descriptions = """
        Nous allons nous tester notre modèle sur les années allant de 2016 à 2019.  
        En effet, les données concernant le vent et les températures ne sont pas disponibles pour les années précédentes.

        Nous allons nous concentrer sur:

        * *Données régionales*: Hauts de France, Grand Est, Occitanie, Centre Val de Loire
        * *Variable cible*: production éolienne quotidienne
        * *Variables explicatives*: vitesse du vent (moyenne), températures (moyenne), régions, années, mois, jour de la semaine

        Les paramètres optimaux selon `GridSearch` sont:
        * max_depth = 8
        * n_estimators = 50

        Il est possible de les modifier ci-dessous, ainsi que la taille de l'échantillon de tests.

    """

    st.markdown(descriptions)
    #import des données
    df = pd.read_csv("data/deb.csv")
    Regions = df.loc[(df["Région"] == "Hauts-de-France") | (df["Région"] == "Grand Est") 
                | (df["Région"] == "Occitanie") | (df["Région"] == "Centre-Val de Loire")]
    # supprimer les colonnes que nous n'allons pas utiliser
    Regions = Regions.drop(['Date','Solaire_sum(MW)','Rayonnement_solaire_mean(W/m2)','Consommation-sum(MW)',
                    'TMin (°C)','TMax (°C)'], axis=1)

    # Preparation des données :
    Categories = Regions[['Annee','Month', 'Day', 'Région']]
    Data = Regions.drop(['Annee','Month','Day','Région'], axis=1)

    scaler = preprocessing.StandardScaler().fit(Data)
    Data[Data.columns] = pd.DataFrame(scaler.transform(Data), index=Data.index)

    Data = Data.join(Categories)
    Data = pd.get_dummies(data=Data, columns=['Annee', 'Month', 'Day','Région'])

    with st.form('form'):
        
        test_size = st.slider("Choississez la taille de l'échantillon de test:", .10, .80, .25, .05)

        n_estimators = st.selectbox("n_estimators", (50, 100, 250, 500, 1000))

        max_depth = st.selectbox("max_depth", (8, 16, 24, 32))

        submitted = st.form_submit_button("Prédire !")

    if submitted:

        # Separer target & variables explicatives et séparer train & test
        data = Data.drop('Eolien_sum(MW)', axis=1)
        target = Data['Eolien_sum(MW)']

        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=test_size)
        model = RandomForestRegressor(max_depth=max_depth, max_features='auto', n_estimators=n_estimators, n_jobs=-1)
        model.fit(X_train, y_train) 

        # prédiction sur train set & calculation RMSE et R2 score
        pred_train= model.predict(X_train)
        train_rmse = np.sqrt(mean_squared_error(y_train,pred_train))
        scoretrain = r2_score(y_train, pred_train)

        # prédiction sur test set & calculation RMSE et R2 score
        pred_test = model.predict(X_test)
        test_rmse = np.sqrt(mean_squared_error(y_test,pred_test))
        scoretest = r2_score(y_test, pred_test)

        # affichez les scores
        str_score = 'Test Score R2: ' + str(round(scoretest, 4))
        if scoretest > .80:     st.success(str_score)
        elif scoretest > .60:   st.warning(str_score)
        else:                   st.error(str_score)

        str_score = 'Train Score R2: ' + str(round(scoretrain, 4))
        if scoretrain > .80:     st.success(str_score)
        elif scoretrain > .60:   st.warning(str_score)
        else:                    st.error(str_score)

        st.info('Test RMSE: ' + str(round(test_rmse, 4)))
        st.info('Train RMSE: ' + str(round(train_rmse, 4)))

        # afficher les predictions
        moy = scaler.mean_[0]
        ec = scaler.scale_[0]
        predictions = pd.DataFrame({'true': (y_test*ec)+moy, 'predicted': np.round((pred_test*ec)+moy)}, 
                index=X_test.index)
        
        # afficher un nuage de points
        fig, ax = plt.subplots(figsize = (16,8))

        plt.plot((predictions.true.min(), predictions.true.max()), (predictions.true.min(), predictions.true.max()), color='#5930F2', lw=3, alpha=.5)
        plt.scatter(predictions.true, predictions.predicted, s=75, marker='o', color='#16E4CA', alpha=.7)
        
        plt.xlabel('Valeurs réelles')
        plt.ylabel('Prédictions')

        st.pyplot(fig)