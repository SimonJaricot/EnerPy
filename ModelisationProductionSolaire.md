## Modelisation de la production solaire
<br /> 

***Algorithmes d'apprentissage essayés***
- Regression lineaire / ElasticNetCV
- Polynomial Features + Linear Regression
- Random Forest Regression

Au préalable, seules les données des quatre régions ayant la production d'énergie solaire la plus élevée ont été sélectionnées à partir de l'ensemble de données original. 
Cela a été fait afin de réduire le grand nombre de valeurs très faibles provenant des régions produisant très peu d'énergie solaire. De plus, 
les données correspondant à des niveaux de la variable "rayonnement solaire" inférieurs à 5 W/m2) ont été exclues du modèle, afin de rendre la distribution moins déséquilibrée. 
<br /> 
Deux versions du jeu de données ont été utilisées :
* Dataset 1 : variable cible `production solaire à la demi-heure` , variables explicatives : mois, année, région, rayonnement solaire global, vitesse du vent, consommation (29,564 observations totales)
* Dataset 2 : variable cible `production solaire journalière totale`, variables explicatives : mois, année, région, rayonnement solaire global moyen, 
vitesse moyenne quotidienne du vent, température moyenne/ maximale/minimale quotidienne, consommation journalière totale (5,844 observations totales)
  
***traitement des variables catégorielles***

Une méthode différente a été essayée pour le traitement des variables catégorielles (mois, année, région) : au lieu de les transformer en variables binaires en utilisant "pandas / getdummies", elles ont été remplacées par la valeur moyenne de la production pour la catégorie correspondante (par exemple, janvier a été remplacé par la valeur moyenne de la production de ce mois). J'ai voulu ainsi refléter la variation régulière de la production en fonction de ces variables. J'ai envisagé d'utiliser l'encodage ordinal, mais ma méthode m'a semblé plus précise.

***Procedure***
<br /> 
Pour chaque algorithme, une première tentative a été faite en utilisant uniquement les données d'une seule région, Nouvelle Aquitaine (la région avec la plus forte 
production d'énergie solaire), et d'une seule année, avec un minimum de variables explicatives. Par la suite, des variables et des données ont été progressivement ajoutées comme suit afin d'observer l'effet sur les résultats:    

  
  
***Avec variable cible : production solaire à la demi-heure*** : 

* Nouvelle-Aquitaine / 2019 / variable explicative "rayonnement solaire global" 
* Variables rajoutées : mois & vitesse du vent 
* Données des années 2016 - 2018 rajoutées
* Données des 3 autres régions à forte production d'énergie solaire rajoutées

***Avec variable cible : production solaire journalière totale*** :   
* Nouvelle-Aquitaine / 2016-2019/ variables explicatives :  rayonnement solaire global moyen, vitesse moyenne quotidienne du vent, mois, année
* Variables rajoutées : température moyenne/ maximale/minimale quotidienne  
  
De plus, la validation croisée a été appliqué régulièrement pour vérifier les résultats, et GridSearch a été utilisé pour identifier les paramètres optimaux.

À noter :
Des valeurs réelles observées du rayonnement solaire, vitesse du vent et de température ont été utilisées, mais évidemment, si l'on souhaite prédire la production future, 
il faudrait utiliser des valeurs prédites / prévues de ces variables.


### Linear Regression / ElasticNetCV

<br />     
   
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2335_-_LinearRegression_solar_scores.png" width=485 align=left>  
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2336_-_LinearRegression_solar_RMSE.png" width=485 align=right>   
<br />   

***Interpretations***
<br /> 
- l'ajout des variables "mois" et "vitesse du vent" au premier modèle ne change que légèrement les résultats, ce qui est surprenant compte tenu de leur corrélation observée avec la production solaire
- l'ajout des données de 2016-2018 (modèle '2' dans ce graphique) et des autres régions (modèle '3') donne des résultats avec une précision réduite et une erreur quadratique moyenne accrue : peut-être parce que les différences de production entre ces années et régions introduisent plus de variation dans les données
- Quand la variable cible est la production solaire journalière totale (modèle '4'), les résultats (R2 score & RMSE) sont nettement meilleurs (R2 score test 0.81)
- Ensuite l'ajout des données de temperature a amélioré les résultats, donnant le meilleur R2 obtenu : 0.84. 
- le train score est généralement légèrement plus élevé, indiquant un certain surapprentissage par chaque modèle

### Polynomial Features + Linear Regression

<br />  

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2337_-_PolyFeatures_solar_scores.png" width=485 align=left>  
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2338_-_PolyFeatures_solar_RMSE.png" width=485 align=right>  
  
  <br />  

***Interpretations***
<br /> 
- Pour les premiers essais, les résultats sont similaires de ceux de Linear Regression / ElasticNetCV
- Encore une fois, quand la variable cible est la production solaire journalière totale (modèle '5' dans ce graphique), les résultats sont nettement meilleurs (R2 score test : 0.88)
- Cette fois l'ajout de variables de temperature a légèrement aggravé les résultats (modèle '6'), ce qui est difficile à expliquer. Cependant, l'ensemble de données est relativement petit, ce qui peut rendre le modèle moins fiable
- Peu de surapprentissage, sauf dans le dernier modèle, où les scores divergent
- (Notez que dans le graphique de droite, on ne peut pas comparer les RMSE des premiers 5 essais aux autres, parce que la variable cible n'est pas à la même échelle)

### Random Forest Regression
<br />
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2343_-_SolarRFR_scores.png" width=485 align=left>  
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2344_-_SolarRFR_RMSE.png" width=485 align=right> 
<br />
<br />

***Interpretations***

- Cette fois, on a commencé toute de suite avec la production solaire journalière totale comme variable cible, obtenant un score similaire aux algorithmes précédents
- Cet algorithme a donné le meilleur R2 score test global de 0.91 (modèle '2' dans ce graphique : Nouvelle Aquitaine, 2016-2019)
- On constate un surapprentissage important, avec un grand écart observé entre les R2 scores pour les premiers modèles. Cela a été réduit lorsque plus de données ont été ajoutées (modèle '2')
- Cependant, l'ajout des données d'autres régions (modèle '3') a donné des résultats légèrement pires

***Résumé des meilleures metriques obtenues***

| Algorithme | meilleur R2 score test| meilleur RMSE|
|------|--------|---------|
|LinearRegression/ ElasticNetCV | 0.84|0.39  | 
|PolynomialFeatures + LinearRegression | 0.88 | 488 |
|RandomForestRegression | 0.91 | 0.29 |


***Analyse des erreurs***

Prédictions obtenues à partir du modèle d'ElasticNetCV (vraies valeurs (x) & les prédictions (y)) :
<br />
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2341_-_SolarLR_predictions.png" width=500 >  
- les prédictions sont étroitement regroupées autour de la ligne des vraies valeurs, sauf un point aberrante à droite
<br />
Les erreurs du ce modèle (vraies valeurs (x) et les résidus (y)) :
<br />
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2342_-_SolarLR_residus.png" width=500 >

- les résidus semblent également réparties, sauf ce point fortement aberrante en haut
   
***Conclusions et evolutions possibles***  

Les trois algorithmes ont donné de bons résultats, avec des R2 score test de ~84%. Ces résultats sont bien meilleurs que ceux obtenus pour 
la prédiction de la production d'énergie éolienne. Dans le cas de la production solaire, des variables plus fortement corrélées sont disponibles, 
ce qui permet de modéliser plus précisément la production.

Comme vu avec la modélisation de l'énergie éolienne, l'amélioration des résultats lors de la modélisation de la production journalière au lieu de la demi-heure est très nette.
Prendre le total quotidien semblerait lisser les variations des données de la demi-heure.

Selon cette source www.futura-sciences.com/planete les panneaux solaires perdent leur efficacité à haute température: “On estime ainsi qu'au-delà de 25 °C, une augmentation de 1 °C aboutit à une baisse de production de 0,45 % et sous des températures ambiantes de 35 °C ….peuvent perdre jusqu'à 30 % de leur rendement." Toujours selon cette source, le vent et l'humidité influencent également de manière significative la production solaire. La température maximale et la vitesse du vent ont été incluses dans nos modèles, mais il serait intéressant d'obtenir des données de température plus détaillées, par exemple 8 observations par jour, comme nous l'avons pour la vitesse du vent. Il serait intéressant aussi d'ajouter des données sur l'humidité.
