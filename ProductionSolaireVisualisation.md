## Production solaire  

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2313_-_Production_solaire_par_jour.png">  

On constate une très grande variation dans la production solaire moyenne, de > 50 MW en hiver jusqu'à > 200 MW en été, et une grande variation hebdomadaire, 
qui pourraient s'expliquer par la variation des conditions météorologiques (des jours avec peu de soleil même en été).  

<br /> 
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2314_-_Production_solaire_moyenne_par_region_2019.png">  

On constate que presque 50% de la production solaire moyenne vient de deux régions : Nouvelle Aquitaine & Occitanie.

<br /> 
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2315_-_Production_solaire__par_heure_2019.png"> 

On voit la courbe attendue, avec son pic vers 13:00 et des valeurs de zero pendant la nuit.

<br /> 
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2316_-_Production_solaire_2015_2019_selon_region.png">

On constate une augmentation importante de production solaire du 2015 au 2019.

### Distribution des valeurs de production solaire en 2019
La calculation des statistique des variables "Production solaire" & "Rayonnement solaire" avec 'Pandas/describe' montre des distributions très déséquilibrées, 
avec 25% ou plus des valeurs zero, ce qui n'est pas étonnant étant donné que l'ensemble de données contient des observations pendant la nuit et comprend des régions 
qui ont une production solaire très basse (voir graphique de production par région ci-dessus). On constate aussi des valeurs maximales bien au-dessus du quartile 75%, 
indiquant les présence des valeurs extrêmes.  

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2317_-_Distribution_production_solaire_2019.png" width=500>

Ce graphique montre que la grande majorité des valeurs sont moins de 100 MW; il y a quelques valeurs extrêmes jusqu'au 2100 MW.  

Afin de réduire ce déséquilibre dans les données, seules les quatre régions les plus productives (couvrant environ 75% de la production totale) 
ont été retenues dans l'ensemble de données : Nouvelle-Aquitaine, Occitanie, Auvergne-Rhône-Alpes, Provence-Alpes-Côte d'Azur.  
De plus, les valeurs négligeables (< 5 ) de la variable "Rayonnement solaire" ont été exclues.
Après ces changements, l'ensemble de données comprend 29,564 observation (au lieu de 46,892).  

### Analyse des corrélations
Variables explicatives disponibles:
- Variables quantitatives:
  - Rayonnement solaire global (W/m2) (8 observations par jour)
  - Température (moyenne, max, min quotidienne)
  - Consommation
- Variables temporelles:
  - Heure & Date
- Variables catégorielles:
  - Région

Les variables temporelles ont été considérées comme catégorielles, en les divisant comme suit: Heure (8 classes de 3 heures: matin1, matin2 etc) / Jour de la semaine / Mois / Année
#### Variables catégorielles
Une seule région, Nouvelle Aquitaine (la région la plus productive en énergie solaire), a été isolée, pour éliminer les différences de région. 
Ensuite des tableaux croisés ont été créés pour montrer la distribution de la production selon ces variables ; la production a été groupée en quintiles afin de faciliter la visualisation et afin d'utiliser le test χ2 : Q1: -1 - 0 MW / Q2:0 - 118 MW / Q3:118 - 434 MW / Q4:434 - 1184 MW/ Q5:1184 - 2107 MW.
<br /> 
Production solaire / jour de la semaine:  

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2318_-_Crosstab_prodsolar_jour.png" width=500>

On ne constate pas de difference entre les jours, qui peut signifier que la demande n'est pas moindre le weekend, ou que la production solaire n'est pas ajustée selon la demande, qui semble logique, compte tenu de la faible quantité d'énergie solaire produite (par rapport au nucléaire par exemple).  
<br /> 
Production solaire / mois :   

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2319_-_Crosstab_prodsolar_mois.png" width=500>  

Comme attendu, ici les differences sont claires : 
- en été ~30% des valeurs sont Q5 / par contre, entre octobre & fevrier il y a peu de valeurs en Q5.
- il y a beaucoup de valeurs en Q1 pour tous les mois, qui correspondraient aux valeurs basses du rayonnement solaire tôt le matin, et le soir.  
<br /> 
Production solaire / heure :   
Une correlation forte entre l'heure et la production solaire est évidente, et le tableau la confirme :   

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2320_-_Crosstab_prodsolar_heure.png" width=500>

- Comme attendu, la nuit 100% des valeurs sont Q1, l'après-midi majoritairement Q4 & Q5.   
<br />   
Ensuite des tests statistiques ont été utilisés pour préciser des corrélations (rappel :  p-value < 5% : on rejette l'hypothèse "les variables sont indépendantes") :

|Variable|test χ2 / p-value|Niveau de corrélation (V Cramer)|
|--------|----------|---------|
|Jour de la semaine|0.98| variables peuvent être indépendantes  |
|Mois|0.00000|~0.83 = corrélation forte|

#### Variables quantitatives
Les données de température disponible consiste d'une seule observation par jour, contrairement aux données du rayonnement solaire (8 observations par jour). Comme précisé auparavant, afin de fusionner les ensembles de données, on a pris la somme de la production quotidienne, et la moyenne quotidienne du rayonnement solaire.    
  
  
Pairplot des corrélations:

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2321_-_Pairplot_prodsolar_correlations.png">  

- la relation entre "Solaire_sum" & "Rayonnement solaire_mean" est clairement lineaire, mais pour "Solaire_sum" & les variables de temperature la relation n'est pas très claire.
- on constate des valeurs très aberrantes de la production solaire en 2018

Calculation des coefficients de corrélation dans Pandas: 
- Correlation negative robuste entre "Solaire_sum" & "Vitesse_vent_mean" (Pearson coefficient -0.57)
- Correlation positive très forte entre "Solaire_sum" & "Rayonnement_solaire_mean" (0.94)
- Correlation positive robuste entre "Solaire_sum" & les variables de temperature, surtout "TMax" (0.76)  
  
  
Production solaire quotidien / Consommation:  

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2322_-_Correlation_prod_solaire_conso.png" width=600>  

- les valeurs élévées de production solaire correspondent généralement aux valeurs plûtot basses de la consommation, qui pourrait s'expliquer par la production solaire élévée en été, quand on peut s'attendre un niveau de consommation plus bas
- L'augmentation de production solaire du 2016 au 2019 est bien visible.   

Calculation des coefficients de corrélation dans Pandas ((une seule année à été isolée, pour éliminer la difference due à l'augmentation annuelle de la production solaire):  

- p-value < 5% : on rejette l'hypothese que les variables sont independantes
- coefficient = -0.59, il y a une corrélation negative robuste entre les deux variables.

#### Conclusion : toutes les variables sauf le jour de la semaine ont une correlation (soit positive, soit negatjve) avec la production solaire, par consequent il sera utile de les inclure dans un modèle.

### Valeurs aberrantes / extrêmes
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2323_-_Boxplot_prod_solaire.png" width=400 height=400>   

Ce graphique montre des valeurs aberrantes de la production solaire chaque année. Un analyse des ces valeurs montre qu'elles correspondent aux jours 
où le rayonnement solaire moyenne (301.5 W/m2) était loin au-dessus de la moyenne de 153 W/m2 pour la période 2016-2019, et la temperature max aussi (32.9°C) est très au-dessus de la moyenne du 17.4°C pour 2016-2019. Par consequent il s'agit probablement des vraies valeurs et non des erreurs. 

Une version des données sans ces valeurs extrêmes a été crée afin de l'utiliser ensuite dans la modelisation (cette version contient 17527 observations).
