import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from my_package.calculateur_empreinte import CalculateurEmpreinteCarbone

#################################################
# Test de la classe CalculateurEmpreinteCarbone #
#################################################

### Importation des données
chemin = ("basecarbone_sample.csv")
data = pd.read_csv(chemin, sep=";")
df = pd.DataFrame(data)

### Création d'un objet CalculateurEmpreinteCarbone
calculateur = CalculateurEmpreinteCarbone(dataframe=df)
'''
### Test de la méthode poser_question():
questionnaire = calculateur.poser_question()
affichage = calculateur.affichage_empreinte_carbone(questionnaire)
print(affichage)
'''
### Generer une base de données aléatoires pour n simulations:Y
resultat = calculateur.simulate(1000)
print(resultat)

### Représentation graphique des résultats:
graphe = calculateur.representation_graphique(resultat)
print(graphe)






