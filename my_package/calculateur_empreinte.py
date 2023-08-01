# -*- coding: utf-8 -*-
"""
Created on 2023-05-13 12:00:00

@author: Rajeeth-A
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class CalculateurEmpreinteCarbone:
    """Classe permettant de demander les informations d'un utilisateur et de
    calculer l'empreinte carbone d'un utilisateur mais qui permet également de
    simuler des calculs sur une base de données.
    """

    def __init__(self, dataframe):
        """Constructeur de la classe CalculateurEmpreinteCarbone."""
        self.choix_motorisation = ["diesel", "essence", "electricite"]
        self.choix_energie = ["gaz", "fioul", "electricite", "granules bois"]
        self.dataframe = dataframe
        self.avion = 0
        self.tgv = 0
        self.voiture = 0
        self.metro = 0
        self.rer = 0
        self.energie = 0
        self.repas_vege = 0
        self.emission = (self.avion + self.tgv +
                        self.voiture + self.metro +
                        self.rer + self.energie +
                        self.repas_vege)

    def poser_question(self):
        """_sommaire_
        Cette fonction recupère les informations de l'utilisateur et les stocke.
        Args:
            None
        Returns:
            _dict_: _informations de l'utilisateur_
        """
        reponse_utilisateur = {}
        questionnaire = [
                        "Avion",
                        "TGV",
                        "Voiture",
                        "Motorisation",
                        "Metro",
                        "RER",
                        "Energie",
                        "Repas_vege"
                        ]

        for question in questionnaire:
            reponse_utilisateur[question] = -1
            while reponse_utilisateur[question] == -1:
                if not question in ("Motorisation", "Repas_vege", "Energie"):
                    reponse_utilisateur[question] = (
                            int(input(f"Entrez votre utilisation annuelle {question} en km: ")
                            ))
                elif question == "Motorisation":
                    reponse_utilisateur[question] = (
                            input(
                    "Entrez le type de moteur de votre voiture ? (Essence, Diesel, Electricite) "
                                ))
                    reponse_utilisateur_minus = reponse_utilisateur[question].lower()
                elif question == "Energie":
                    reponse_utilisateur[question] = (
                            input(
                        "Entrez votre type d'énergie ? (Gaz, Fioul, Electricite, Granules bois) ")
                            )
                    reponse_utilisateur_minus = reponse_utilisateur[question].lower()
                    reponse_utilisateur["heure"] = int(input(
                        "Entrez votre utilisation en heure (par jours) : "))
                else:
                    reponse_utilisateur[question] = (
                        int(input(
                        "Entrez votre quantité de nourriture vegan préparé annuellement : "
                              ))
                                )
                if question in ("Motorisation", "Energie"):
                    if reponse_utilisateur[question].isalpha():
                        reponse_utilisateur[question] = reponse_utilisateur_minus
                    else:
                        print("ERREUR : Veuillez rentrer uniquement",
                              "des lettres pour cette question")
                        reponse_utilisateur[question] = -1
                else:
                    try:
                        reponse_utilisateur[question] = (
                            int(reponse_utilisateur[question])
                            )
                    except ValueError:
                        print("ERREUR : Veuillez rentrer uniquement",
                              "des chiffres pour cette question")
                        reponse_utilisateur[question] = -1

        return reponse_utilisateur

    def calculateur_empreinte(self, reponses):
        """_sommaire_
        Cette fonction calcule la consommation annuelle d'empreinte
        carbone en fonction des réponses fournies par l'utilisateur.
        Args:
            reponses (dict): Informations de l'utilisateur sous la forme d'un dictionnaire.

        Returns:
            tuple: Un tuple contenant l'émission annuelle d'empreinte carbone :
                (avion, tgv, voiture, metro, rer, energie, repas_vege)

        """
        co2_postes = {}

        colonne = self.dataframe['Nom base français'].unique().tolist()
        for nom_poste in colonne:
            emission_poste = self.dataframe[self.dataframe["Nom base français"] == nom_poste]
            co2_poste = (emission_poste["Total poste non décomposé"].sum()
                        / len(emission_poste)
                        )
            co2_postes[nom_poste] = co2_poste

        energie_emission = 486.0 + 396.0 + 546.0

        motorisation = reponses["Motorisation"].lower()
        if motorisation == "diesel":
            motorisation_emission = 0.251
        elif motorisation == "essence":
            motorisation_emission = 0.259
        else:
            motorisation_emission = co2_postes["Electricité"]


        energie = reponses["Energie"]
        if energie == "gaz":
            energie_emission += 2.15
        elif energie == "fioul":
            energie_emission += 3.25
        elif energie == "granules bois":
            energie_emission += 111
        else:
            energie_emission += 0.0571

        self.avion = (reponses['Avion'] * co2_postes["Avion"]) / 1000
        self.tgv = (reponses['TGV'] * co2_postes["TGV"]) / 1000
        self.voiture = (reponses['Voiture'] + motorisation_emission) / 1000
        self.metro = (reponses["Metro"] * co2_postes["Métro"]) / 1000
        self.rer = (reponses['RER'] * co2_postes["RER"]) / 1000
        self.energie = (
            energie_emission + reponses['heure'] * 366
            )  / 1000
        self.repas_vege = (
            (reponses['Repas_vege'] * 0.5) + (
                728 - reponses['Repas_vege']) * 2.04
            ) / 1000

        self.emission = (self.avion +
                         self.tgv +
                         self.voiture +
                         self.metro +
                         self.rer +
                         self.energie +
                         self.repas_vege)

        emission_transport = self.avion + self.tgv + self.voiture + self.metro + self.rer
        emission_alimentation = self.repas_vege
        emission_energie = self.energie

        return (
                self.avion,
                self.tgv,
                self.voiture,
                self.metro,
                self.rer,
                self.energie,
                self.repas_vege,
                self.emission,
                emission_transport,
                emission_alimentation,
                emission_energie
                )

    def affichage_empreinte_carbone(self, reponses):
        """_sommaire_
        Affiche l'empreinte carbone annuelle ainsi que le détail des émissions par catégorie.
        Donne également un message indicatif pour savoir si l'utilisateur se situe au-dessus,
        en dessous ou dans la moyenne des Français.
        Args:
            reponses (int): Base de donnée

        Returns:
            Detaille de l'empreinte carbone de l'utilisateur par poste
        """
        (self.avion,
         self.tgv, self.voiture, self.metro,
         self.rer, self.energie,
         self.repas_vege, self.emission) = self.calculateur_empreinte(reponses)[:8]
        print(f"\nVotre empreinte carbone annuelle est de {self.emission} tonnes de CO2")

        if 8 < self.emission < 10:
            print("Vous êtes dans la moyenne des Français")
        elif self.emission >= 10:
            print("Vous êtes au-dessus de la moyenne des Français",
                  "pensez aux développements durables")
        else:
            print("Vous êtes en dessous de la moyenne des Français, Félicitations !")

        transport = self.avion + self.tgv + self.voiture + self.metro + self.rer
        alimentation = self.repas_vege
        energie = self.energie

        print("\nDétail par catégorie :")
        print("Transport:", transport, "t de CO2")
        print("Alimentation:", alimentation, "t de CO2")
        print("Energie:", energie, "t de CO2")

        choix_detail = input("\nVoulez-vous plus de détails ? (oui/non) ")
        if choix_detail == "oui":
            print("\nDétail par poste :")
            print("Avion:", self.avion, "t de CO2")
            print("TGV:", self.tgv, "t de CO2")
            print("Voiture:", self.voiture, "t de CO2")
            print("Metro:", self.metro, "t de CO2")
            print("RER:", self.rer, "t de CO2")
            print("Energie:", self.energie, "t de CO2")
            print("Repas végétarien:", self.repas_vege, "t de CO2")
            print("Emission", self.emission, "t de CO2")

    def simulate(self, num_simulations):
        """_sommaire_
        Effectue des simulations aléatoires pour générer une base de données 
        contenant des réponses aléatoires et les émissions de CO2 correspondantes.
        Args:
            n (int): Nombre total de simulation

        Returns:
            _DataFrame_: _Base de donnée avec n simulation remplis de manières aléatoires_
        """
        dataset = []
        for _ in range(num_simulations):
            reponses = {
                "Avion": np.random.randint(0, 5000),
                "TGV": np.random.randint(0, 5000),
                "Voiture": np.random.randint(0, 7500),
                "Motorisation": np.random.choice(self.choix_motorisation),
                "Metro": np.random.randint(0, 5000),
                "RER": np.random.randint(0, 5000),
                "Energie": np.random.choice(self.choix_energie),
                "heure": np.random.randint(0, 12),
                "Repas_vege": np.random.randint(0, 728)
            }
            reponses["Emission"] = self.calculateur_empreinte(reponses)[7]
            transport, alimentation, energie = self.calculateur_empreinte(reponses)[8:]

            reponses["Alimentation"] = alimentation
            reponses["Transport"] = transport
            reponses["Logement"] = energie
            dataset.append(reponses)

        return pd.DataFrame(dataset)

    def representation_graphique(self, dataframe):
        """_summary_
        Génère une représentation graphique des émissions de CO2 moyennes par catégorie,
        en utilisant un graphique à barres.
        Args:
            dataframe (df): Base de donnée

        Returns:
            Graphique à barre: Représentation graphique des émissions de CO2 moyennes par catégorie
        """
        categories = ['Alimentation', 'Transport', 'Logement']
        _, axes = plt.subplots()
        for _, category in enumerate(categories):
            data_y = [dataframe[category].mean()]
            axes.bar(category, data_y, label=category)
        axes.set_ylabel('Emission de CO2 (tCO2e/hab.)')
        axes.set_title("Empreinte carbone moyenne d'un Français")
        axes.legend()
        plt.show()
