
## Production éolienne
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2301_-_Production_par_filiere_en_2019.png">  

On constate que la production solaire représente 1.5% de la production totale en 2019, et la production éolienne représente 4.19% (par comparaison, nucléaire représente 81% ).  
<br />   
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2302_-_Production_eolienne_par_jour_en_2019.png">  

On constate une très grande variation dans la production moyenne par demi-heure (100 - 1000 MW) avec moins de variation en été (100 - 400 MW en août). L'explication peut être la grande variation dans la puissance du vent d'un jour à l'autre et aussi l'ajustement de la production en fonction de la demande.  
<br />   
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2303_-_Production_eolienne_moyenne_par_region_2019.png"> 

On constate que presque 50% de la production moyenne vient de deux régions : Hauts de France & Grand Est.  
<br />   
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2304_-_Production_eolienne_2015_2019_selon_region.png">

On constate que la production augmente sensiblement, surtout entre 2017 & 2019.  
  
### Distribution des valeurs de production éolienne en 2019
La calculation des statistique de la variable "Production éolienne" avec 'Pandas/describe' montre une distribution très déséquilibrée, 
avec une valeur maximale (3,780 MW) bien au-dessus du quartile 75% (387 MW), indiquant la présence des valeurs extrêmes. De plus, la valeur minimale est négative, qui semble une valeur aberrante. 
<br />   
 
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2305_-_Distribution_production_eolienne_2019.png" width=500>

- le graphique confirme une distribution très desequilibrée : la grande majorité des valeurs sont moins de 200 MW
- très peu de valeurs > 1000   

### Analyse des corrélations
Variables explicatives disponibles:
- Variables quantitatives:
  - Vitesse du vent (8 observations par jour)
  - Température (moyenne, max, min quotidienne)
  - Consommation
- Variables temporelles:
  - Heure & Date
- Variables catégorielles:
  - Région

Les variables temporelles ont été considérées comme catégorielles, en les divisant comme suit: Heure (8 classes de 3 heures: nuit1, nuit2, matin1, matin2 etc.) / Jour de la semaine / Mois / Année
#### Variables catégorielles
Une seule région, Hauts de France, a été isolée, pour éliminer les différences de région. Ensuite des pivot tables ont été créés pour montrer la distribution de la production selon ces variables (la production a été groupée en quintiles afin de faciliter la visualisation et afin d'utiliser le test χ2 : Q1: 3-154 MW / Q2:154-360 MW / Q3:360-682 MW / Q4:682-1281 MW / Q5:1281-3732 MW)

Production éolienne / jour de la semaine:  

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2307_-_Crosstab_prod_jour.png" width=500>
- pas de tendance claire : qui peut signifier que la demande n'est pas moindre le weekend ou que la production éolienne n'est pas ajustée en conséquence d'une différence de demande les weekends      

<br />   
<br /> 
Production éolienne  / mois:  

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2308_-_Crosstab_prod_mois.png" width=500>
Cette fois les différences sont claires : 
- en hiver 30 - 40% des valeurs sont Q5 (1396 - 3421 MW) & Q1, Q2, Q3 ( 0 - 761 MW) représentent chacun environ 15% 
- entre mai et août moins de 10% des valeurs sont Q5 & Q1, Q2, Q3 représentent chacun environ 25%     
  
  
<br /> 
<br /> 

Production éolienne / heure:  

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2309_-_Crosstab_prod_heure.png" width=500>
- on observe des différences, mais c'est difficile d'en déduire beaucoup  

<br /> 
<br />   

Ensuite des tests statistiques ont été utilisés pour préciser des corrélations (rappel :  p-value < 5% : on rejette l'hypothèse "les variables sont indépendantes") :

|Variable|test χ2 / p-value|Niveau de corrélation (V Cramer)|
|--------|----------|---------|
|Jour de la semaine|0.00002|~0.1 = corrélation faible|
|Mois|0.00000|~0.57 = corrélation significative|
|Heure|0.00000|~0.2 = corrélation faible mais non-négligeable|

#### Variables quantitatives
Les données de température disponible consiste d'une seule observation par jour, contrairement aux données de vitesse de vent (8 observations par jour). Afin de fusionner les datasets, j'ai pris la somme de la production quotidienne, et la moyenne quotidienne de la vitesse du vent. 
<br /> 
Pairplot des corrélations:

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2310_-_Correlation_prod_eolienne_pairplot.png">  

- on constate que les relations entre "Eolien" & les variables de temperature sont du même type
- on observe le valeurs plus élévées de production eolienne en 2019, comme déjà vu dans le graphique ci-dessus

Calculation des coefficients de corrélation dans Pandas:   
<br /> 
- Correlation negative faible entre la production éolienne et temperature moyenne (Pearson coefficient -0.17)
- Correlation positive robuste entre la production éolienne et la vitesse du vent (0.71)
<br /> 
Production eolienne quotidien / Consommation:  

<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2311_-_Correlation_prod_eolienne_conso.png" width=600>  

- la distribution n'est pas totalement aleatoire, mais il n'y a pas de relation lineaire simple.   
<br /> 
Calculation des coefficients de corrélation dans Pandas:  
<br /> 
- p-value < 5% : on rejette l'hypothese que les variables sont independantes
- coefficient = 0.24, il y a une corrélation faible entre les deux variables.

#### Conclusion : toutes les variables ont une correlation (soit faible, soit robuste) avec la production éolienne, par consequent il sera utile de les inclure dans un modèle

### Valeurs aberrantes / extrêmes
<img src="https://github.com/DataScientest-Studio/EnerPy/blob/deborah_branch/Outputs/%2312_-_Boxplot_prod_eolienne_distribution.png" width=400 height=400>   

Ce graphique montre des valeurs aberrantes de la production éolienne chaque année. Un analyse des ces valeurs montre qu'elles correspondent aux jours où la vitesse du vent est très au dessus de la moyenne de 5.9 m/s pour la période 2016-2019 et la consommation aussi est très au-dessus de la moyenne 2016-2019 (35,000 MW) indiquant des journées de haute demande. Par consequent il s'agit probablement des vraies valeurs et non des erreurs. 

Une version des données sans ces valeurs extrêmes a été crée afin de l'utiliser ensuite dans la modelisation.

