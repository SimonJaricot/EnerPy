## Modelisation de la production éolienne
<br /> 
L'objectif est de découvrir si la production d'énergie éolienne et d'énergie solaire peut être prédite avec succès en utilisant les variables explicatives disponibles. 
Des méthodes de régression ont été appliquées pour prédire les valeurs numériques de la production, et des méthodes de classification ont également été essayées afin de prédire la production par classes.   


***Algorithmes d'apprentissage essayés***
- Random Forest classification
- K-nearest-neighbours classifiaction
- Regression lineaire / ElasticNetCV
- Polynomial Features + Linear Regression
- Random Forest Regression

***Procedure***

Au préalable, seules les données des quatre régions ayant la production d'énergie éolienne la plus élevée ont été sélectionnées à partir de l'ensemble de données original. Cela a été fait afin de réduire le grand nombre de valeurs très faibles provenant des régions produisant très peu d'énergie éolienne.  
<br /> 
Trois versions du jeu de données ont été utilisées :
* Dataset 1 : variable cible `production éolienne à la demi-heure` , variables explicatives : heure (divisée en 8 groupes de 3 heures chacun: nuit1, nuit2, matin1, matin2 etc.), mois, année, région, vitesse du vent, consommation (46,892 observations totales)
* Dataset 2 : variable cible `production éolienne journalière totale`, variables explicatives : mois, année, région, vitesse moyenne quotidienne du vent, température moyenne quotidienne, consommation journalière totale (5,844 observations totales
* Dataset 3 : equivant to Dataset 2 sans des valeurs extrêmes de la production éolienne (5,812 observations (32 observations exclues))
<br /> 
Pour chaque algorithme, une première tentative a été faite en utilisant uniquement les données d'une seule région, Hauts de France (la région avec la plus forte production d'énergie éolienne), et d'une seule année, avec un minimum de variables explicatives. Par la suite, des variables et des données ont été progressivement ajoutées comme suit afin d'observer l'effet sur les résultats:    

  
  
***Avec variable cible : production éolienne à la demi-heure*** : 

* Hauts de France / 2019 / variable explicative "Vitesse du vent" 
* Variables rajoutées : mois & heure 
* Données des années 2016 - 2018 rajoutées
* Données des 3 autres régions à forte production d'énergie éolienne rajoutées
* Variable rajoutée : Consommation  

***Avec variable cible : production éolienne journalière totale*** :   
* Hauts de France / 2016-2019/ variables explicatives :  vitesse moyenne quotidienne du vent, mois, année
* Variable rajoutée : température moyenne quotidienne
* Données des 3 autres régions à forte production d'énergie éolienne rajoutées
* Valeurs extrêmes de la production éolienne exclues (Dataset 3)  
  
De plus, la validation croisée a été appliqué régulièrement pour vérifier les résultats, et GridSearch a été utilisé pour identifier les paramètres optimaux.  

À noter :
La variable "Consommation" a été ajouté afin d'ajouter une estimation de la demande, plus précise que celle fournie par les autres variables. 
Cependant, il est clair que pour une prédiction de la production future, cette variable ne serait pas disponible, et il faudrait la remplacer par une prévision de la consommation. Il en va de même pour les variables de vitesse du vent et de température, qu'il faudrait également prévoir, afin de prédire la production future d'énergie éolienne.   

### Random Forest Classification  

Afin d'appliquer les algorithmes de classification, la variable cible a été divisée en cinq groupes de quintiles, comme suit : 112-1,818 MW / 1,818-3,355 MW / 3,355-5,611 MW / 5,611-9,793 MW / 9,793-27,094 MW (on constate  que l'amplitude du dernier groupe est très grande, en raison de la distribution deséquilibrée de la variable).  
Les meilleurs résultats ont été obtenus avec la variable cible "production éolienne journalière totale" et les données d'une seule région, Hauts de France, du 2016 au 2019, voici la matrice de confusion : 

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2339_-_RF_confusion_matrix.png" width=500 >  

***Interpretations***  
- l'algorithme ne parvient pas à prédire avec précision les cinq groupes, bien que les résultats ne soient pas complètement aléatoires. 
- les valeurs les plus basses (Q1) et les plus élévées (Q5) sont les plus bien prédites

### K-nearest-neighbours  

Pour cet algorithme aussi, les meilleurs résultats sont obtenue avec la variable cible "production éolienne journalière totale" et les données de Hauts de France, du 2016 au 2019, voici la matrice de confusion :

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2340_-_KNN_confusion_matrix.png" width=500 >  

***Interpretations***   
- Cet algorithme ne donné pas des résultats meilleurs, la matrice est très similaire à celle de l'algorithme Random Forest

***Résumé des meilleures metriques obtenues***  

| Algorithme | Precision | Recall | F1 score |
|------ | ------|-------|---------|
|Random Forest | 0.39 | 0.40 | 0.39 |
| K-nearest-neighbours | 0.41| 0.41 | 0.41 |  
  
N'ayant pas bien réussi avec ces algorithmes, passons aux algorithmes de régression


### Linear Regression / ElasticNetCV

<br />     
   
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2329_-_LinearRegression_wind_scores.png" width=485 align=left>  
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2330_-_LinearRegression_wind_RMSE.png" width=485 align=right>   
<br />   

***Interpretations***
<br /> 
- l'ajout des variables "mois" et "heure" (modèle '1' dans ce graphique), et l'ajout des données de 2016-2018 (modèle '2') et des autres régions (modèle '3') ne modifie guère les R2 scores test des premiers modèles, le R2 score test reste ~0.40. Par contre le RMSE test est réduit
- Quand la variable cible est la production éolienne journalière totale (modèle 5), les résultats (R2 score & RMSE) sont nettement meilleurs (R2 score test 0.54)
- L'ajout de la temperature (modèle '6') n'a pas d'effet
- L'ajout des données des autres régions (modèle '7') a légèrement aggravé les résultats. Cela pourrait être dû au fait que cela a introduit plus de variation dans les données.

### Polynomial Features + Linear Regression

<br />  

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2331_-_PolynomialFeatures_wind_scores.png" width=485 align=left>  
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2332_-_PolynomialFeatures_wind_RMSE.png" width=485 align=right>  
  
  <br />  

***Interpretations***
<br /> 
- Pour les premiers essais, les résultats ne sont guère différents de ceux de Linear Regression / ElasticNetCV
- Encore une fois, quand la variable cible est la production éolienne journalière totale, les résultats  sont nettement meilleurs, et ensuite l'ajout des données des autres régions a légèrement aggravé les résultats
- (Notez que dans le graphique de droite, on ne peut pas comparer les RMSE des premiers 4 essais aux autres, parce que la variable cible n'est pas à la même échelle)

### Random Forest Regression

<br />  

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2333_-_RFR_wind_scores.png" width=485 align=left>  
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2334_-_RFR_wind_RMSE.png" width=485 align=right>   
<br />

***Interpretations***
<br /> 
- Cette fois, on a commencé toute de suite avec la production éolienne journalière totale comme variable cible, obtenant un score similaire aux algorithmes précédents
- l'ajout des variables "temperature" (modèle '1' dans ce graphique) et "consommation" 'modèle '3') n'ont pas affecté les résultats
- Par contre, l'ajout des données des autres régions (modèle '2') a nettement amelioré les résultats, donnant la meilleure R2 score test globale de 0.63
- On constate un surapprentissage important, avec un grand écart observé entre les R2 scores pour les premiers modèles. Cela a été un peu réduit lorsque plus de données ont été ajoutées (modèle '2')

***Résumé des meilleures metriques obtenues***

| Algorithme | meilleur R2 score test| meilleur RMSE|
|------|--------|---------|
|LinearRegression/ ElasticNetCV | 0.54 | 0.69 || 
|PolynomialFeatures + LinearRegression | 0.50 | 3024 |
|RandomForest Regression |0.63 | 0.60|   


***Analyse des erreurs***
<br /> 
Prédictions obtenues à partir du meilleur modèle (vraies valeurs (x) & les prédictions (y)) :
<br /> 
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2325_-_ElasticNet_predictions.png" width=600> 
<br /> 
Les erreurs du meilleur modèle (vraies valeurs (x) et les résidus (y)) :
<br /> 
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2326_-_ElasticNet_residus.png" width=600> 

- la distribution des residus n'est pas de toute aléatoire
- Pour les valeurs de production éolienne > ~1500, les predictions sont trop basses
- Pour les valeurs < ~200, les predictions sont en générales trop élévées
   
***Conclusions et evolutions possibles***  

L'algorithme Random Forest Regression nous a donné les meilleurs résultats, avec un R2 score test de 63%. Cependant, c'est un résultat très modeste, avec une erreur quadratique moyenne significative de 0.60, et une distribution des erreurs deséquilibrée. Bien que toutes les variables soient plus ou moins corrélées avec la cible, il n'y a pas de variable fortement corrélée, ce qui rend difficile l'amélioration du modèle. On a constaté des résultats meilleurs lors de la modélisation de la production journalière au lieu de la demi-heure : prendre le total quotidien semblerait lisser les variations des données de la demi-heure.

  
Il existe des autres facteurs qui influenceront la production : le type d'éoliennes dans chaque région, la mise en place de nouvelles éoliennes pendant cette période, et aussi si les éoliennes fonctionnent à pleine capacité ou non. Pou aller plus loin, il serait intéressant de rechercher plus d'informations à ce sujet, et d'envisager comment cela pourrait être inclus dans un modèle.
<br />   

Concernant la relation entre la production et la vitesse du vent, selon des information trouvées sur le site site éducatif https://energyeducation.ca/encyclopedia/Wind_power, ce n'est pas du tout une relation simple : les éoliennes sont conçues pour fonctionner dans une plage spécifique de vitesses de vent (les limites de la plage sont appelées **cut-in speed** (vitesse d'enclenchement) et **cut-out speed** (vitesse d'arrêt) - voir leur graphique ci-dessous:   
<br /> 
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/Windpowercurve.png" width=400> 
<br /> 
La **cut-in speed** est le point auquel l'éolienne est capable de produire de l'électricité et entre cette vitesse et la **rated speed** (vitesse nominale), où la puissance maximale est atteinte, la **puissance de sortie augmentera de manière cubique avec la vitesse du vent**. La **cut-out speed** est le point auquel la turbine doit être arrêtée pour éviter d'endommager l'équipement. Il est clair qu'un modèle de régression linéaire ne donnera pas de bons résultats dans ce cas. De plus, les vitesses d'enclenchement et d'arrêt sont liées à la conception et à la taille de la turbine, et ces facteurs vont varier d'une région à l'autre (toutes ces informations sont tirées de la source citée ci-dessus).

<br /> 
