from time import strftime
import streamlit as st
import feather
import pandas as pd
import numpy as np

from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tools.eval_measures import rmse, meanabs

import matplotlib.pyplot as plt
import matplotlib.transforms as mtrans

import seaborn as sns

import datetime

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

def plot_predictions(obs = None, preds = None, preds_labels='Predictions', title='Predictions'):

    fig, ax = plt.subplots(figsize = (16,8))

    if obs is not None:
        sns.lineplot(x=obs.index, y=obs['prod'], label='Obersations', color=colors['purple'], alpha=.5)
    
    if preds is not None:
        sns.lineplot(x=preds.index, y=preds.values, label=preds_labels, color=colors['green'], linewidth=3, alpha=.8)

    plt.xlabel('Années', labelpad=20)
    #Permet de centrer l'année sur la colonne
    trans = mtrans.Affine2D().translate(15, 0)
    for t in ax.get_xticklabels():
        t.set_transform(t.get_transform()+trans)

    plt.xticks(rotation=45)
    plt.ylabel('Production en TW', labelpad=20)
    plt.yticks(rotation=45)

    plt.title(title, pad=30, size=20)
    plt.legend(loc='best')

    st.pyplot(fig)


def app():

    st.markdown("### SARIMAX")

    data = pd.read_feather('data/timeserie_preds.ftr')
    data = data.set_index('date_heure')

    st.write("Voici les observations de la production d'énergie globale en France entre Janvier 2013 et Décembre 2020")

    plot_predictions(obs=data, title='Observations')

    st.write("Le modèle SARIMAX possède deux paramètres, différenciation simple et différenciation saisonnière, définis comme ceci:")

    simple = """
        **Simple (p, d, q)**, **Saisonnière (P, D, Q)** et **k**:

        * **p & P**: Auto Regression (S**AR**IMAX) - Relation linéaire entre l'instant *t* et les précédents
        * **d & D**: Differencing (SAR**I**MAX) - Degré permettant de stationnariser un Time Serie (supprime la tendance)
        * **q & Q**: Moving Average (SARI**MA**X) - Moyenne sur différentes périodes antérieures à l'instant *t*
        * **k**: Saisonnalité (**S**ARIMAX) - Annuelle (12), hebdomadaire (7), etc.
        * **X** *est pour Exogenous, ou Exogène en français, qui signifie "donnée extérieure"*, c'est à dire la variable à analyser
    
        La syntaxe suivante permet de visualiser les paramètres: *SARIMAX(p, d, q)(P, D, Q)k*

        Afin de trouver automatiquement les meilleurs paramètres, notre modèle utilise *auto_arima* du package *pmdarima*.
    
    """

    st.info(simple)

    with st.form('sarimax'):
        
        start_date = datetime.datetime.strptime('2019-01-01', '%Y-%m-%d').date()
        st.write('Date de début: ', start_date)
        end_date = st.date_input('Choississez une date de fin:', datetime.datetime.now(), on_change=None)

        col1, col2, col3 = st.beta_columns([3,3,3])
        with col1: ar_1 = st.number_input('Simple(p, x, x)', min_value=0, max_value=2, value=1, step=1)
        with col2: ar_2 = st.number_input('Simple(x, d, x)', min_value=0, max_value=2, value=0, step=1)
        with col3: ar_3 = st.number_input('Simple (x, x, q)', min_value=0, max_value=2, value=0, step=1)
            
        col1, col2, col3 = st.beta_columns([3,3,3])
        with col1: ma_1 = st.number_input('Saisonnière(P, x, x)', min_value=0, max_value=2, value=2, step=1)
        with col2: ma_2 = st.number_input('Saisonnière(x, D, x)', min_value=0, max_value=2, value=1, step=1)
        with col3: ma_3 = st.number_input('Saisonnière(x, x, Q)', min_value=0, max_value=2, value=0, step=1)

        submitted = st.form_submit_button("Prédire !")

    if submitted:
        
        if start_date >= end_date:
            st.error('Huuum, la date de début doit être antérieure à la date de fin.')
            st.stop()

        values = (int(ar_1), int(ar_2), int(ar_3)), (int(ma_1), int(ma_2), int(ma_3), 12)

        predict_sarimax(data, values[0], values[1], start_date, end_date)


def predict_sarimax(data, order, seasonnal, start, end):

            predictions_label = "SARIMAX" + str(order) + str(seasonnal)

            mod = SARIMAX(endog=data.iloc[:72]['prod'], order=order, seasonal_order=seasonnal)
            res = mod.fit()

            sds = pd.date_range(start=data.index.min() , end=start, freq='MS')    
            eds = pd.date_range(start=start , end=end, freq='MS')

            start_date_sarimax = len(sds)
            end_date_sarimax = start_date_sarimax + len(eds) -1
            delta_preds = res.predict(start_date_sarimax, end_date_sarimax).rename('Prediction')

            plot_predictions(preds=delta_preds, obs=data.iloc[72:], preds_labels=predictions_label)