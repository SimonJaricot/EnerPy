import streamlit as st

import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

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

    st.markdown("## Modèle de prédiction de la Consommation Globale")
    st.markdown("### Modèle de Classification Random Forest")

    data = pd.read_feather('data/lr_conso.ftr')

    description = """
        Dans le modèle Random Forest Classifier, nous allons pouvoir modifier quelques paramètres afin de mesurer la performance de celui-ci.

        * *Le nombre de classes*: Définie par défaut à 10.
        * *La méthode de découpage*: `pandas.qcut` ou `pandas.cut`.
        * *Taille de l'échantillon de test*: définie l'amplitude du jeu de donnée qui servira aux tests. Par, extention, cela défini aussi la taille du jeu d'entrainement. 
        * *n_estimators*: nombre d'arbre.
        * *max_depth*: profondeur de l'arbre.

    """

    st.write(description)

    with st.form('poly'):

        n = st.number_input('Nombre de classes:', min_value=4, max_value=20, value=10, step=1)
        cut = st.selectbox("Méthode de découpage", ('qcut', 'cut'))

        test_size = st.slider("Choississez la taille de l'échantillon de test:", .10, .80, .25, .05)

        n_estimators = st.selectbox("n_estimators", (1250, 1000, 750))

        max_depth = st.selectbox("max_depth", (32, 16, 8))

        submitted = st.form_submit_button("Prédire !")
        

    if submitted:
        predict_rfc(data, test_size, n, cut, n_estimators, max_depth)

def predict_rfc(data, test_size, n, cut, n_estimators, max_depth):

    deciles = np.linspace(0, 1, n+1)
    labels = np.linspace(0, n-1, n)

    data['conso_class'] = pd.qcut(data['consommation'], q=deciles, labels=labels).astype(int)
    if cut == "cut":
        data['conso_class'] = pd.cut(data['consommation'], bins=n, labels=labels).astype(int)

    features = data.drop(columns=['consommation', 'conso_class'])
    target = data['conso_class']

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=test_size)

    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, n_jobs=-1)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    #print('Accuracy:', round(accuracy_score(y_test, y_pred), 4))

    score = round(accuracy_score(y_test, y_pred), 4)
    str_score = 'Accuracy: ' + str(score)

    if score > .80:     st.success(str_score)
    elif score > .60:   st.warning(str_score)
    else:               st.error(str_score)


    matrix = confusion_matrix(y_test, y_pred)
    matrix = matrix.astype('float') / matrix.sum(axis=1)[:, np.newaxis]

    palette = sns.light_palette(colors['purple'], as_cmap=True)

    fig, ax = plt.subplots(figsize = (16,8))
    ax = sns.heatmap(matrix, annot=True, cmap=palette)

    ax.set_xlabel('Predictions')
    ax.set_ylabel('Réels')
    ax.set_title('Confusion Matrix de Random Forest Classifier', size=20)

    st.pyplot(fig)

    explaination = """
        ### Pourquoi les classes sont mal prédites avec `qcut`?

        Le problème, dans cette modélisation, est rencontré lors du découpage de la consommation en classes.  
        En effet, les classes n'ont pas la même étendue. Par exemple, les classes 1 et 2 ont une étendue plus faible que la classe la plus haute.
        La raison à cela se trouve dans la distribution des données de consommation.

        Voilà pourquoi la matrice de confusion nous donne des erreurs sur les classes généralement inférieures.

        ### Pourquoi les classes sont mal prédites avec `cut`?

        Le risque d'erreur provient du découpage avec certaines classes en sous effectif. Donc l'apprentissage peut avoir un problème d'*underfitting* pour les classes moins bien représentées.

    """

    st.markdown(explaination)