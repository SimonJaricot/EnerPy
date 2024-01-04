import streamlit as st

import numpy as np
import pandas as pd

import demo_prod_sarimax as prod_sarimax
import demo_prod_poly as prod_poly

def app():
    st.markdown("## Modèle de prédiction de la Production Globale")
    st.markdown("### Choix du modèle")


    models = ('Choisissez un modèle', 'Régression Polynomiale', 'Série Temporelle SARIMAX')
    options = list(range(len(models)))

    value = st.selectbox("", options, format_func=lambda x: models[x])

    MODELS = {
        0: None,
        1: prod_poly,
        2: prod_sarimax
    }

    if value is not 0:
        model = MODELS[value]
        st.markdown('---')
        model.app()