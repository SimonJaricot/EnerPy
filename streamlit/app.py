import streamlit as st

import numpy as np
import pandas as pd
import time

import home_page as home
import demo_prod_glob as prod_glob
import demo_conso_glob as conso_glob

import demo_solaire as prod_solaire
import demo_eolien as prod_eolien

########################################################
############     Navigation dans l'app      ############
########################################################

MENU = {
    "Projet EnerPy": home,
    "Production Globale": prod_glob,
    "Consommation Globale": conso_glob,
    "Production Solaire": prod_solaire,
    "Production Eolienne": prod_eolien,
}

# Centre l'image en créant des colonnes
col1, col2, col3 = st.sidebar.beta_columns([2,6,2])
with col1: st.write("") # Vide
with col2: st.image('img/datascientest.png') # Image centrée
with col3: st.write("") # Vide

st.sidebar.markdown("# EnerPy")
st.sidebar.markdown('## Menu')

selection = st.sidebar.radio(
    label='',
    options=list(MENU.keys()),
    index=0)

menu = MENU[selection]
menu.app()



contact_view = """
**Participants**  
* Deborah Kerr
* Didier Pezet
* Simon Jaricot

*Promotion Data Analyst Juin-2021 Bootcamp*
"""

st.sidebar.markdown(contact_view)