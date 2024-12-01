import tkinter as tk
from tkinter import ttk
from utils import display

class Window(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(800, 500, self)
        self.title('Consultation des données de la base')
        display.defineGridDisplay(self, 1, 1)

        # Définition des onglets
        #TODO Q4 Créer des nouveaux onglets pour les nouvelles tables
        tabControl = ttk.Notebook(self)
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)
        tab4 = ttk.Frame(tabControl)
        tab5 = ttk.Frame(tabControl)
        tab6 = ttk.Frame(tabControl)
        tab7 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='Mesures (1000 1ères valeurs)')
        tabControl.add(tab2, text='Départements')
        tabControl.add(tab3, text='Régions')
        tabControl.add(tab4, text='Chauffage')
        tabControl.add(tab5, text='Photovoltaique')
        tabControl.add(tab6, text='Isolation')
        tabControl.add(tab7, text='Travaux')
        display.defineGridDisplay(tab1, 1, 2)
        display.defineGridDisplay(tab2, 1, 2)
        display.defineGridDisplay(tab3, 1, 2)
        display.defineGridDisplay(tab4, 1, 2)
        display.defineGridDisplay(tab5, 1, 2)
        display.defineGridDisplay(tab6, 1, 2)
        display.defineGridDisplay(tab7, 1, 2)
        tabControl.grid(row=0, column=0, sticky="nswe")

        # Mesures
        columns = ('code_departement', 'date_mesure', 'temperature_min_mesure', 'temperature_max_mesure', 'temperature_moy_mesure')
        query = """
            SELECT code_departement, date_mesure, temperature_min_mesure, temperature_max_mesure, temperature_moy_mesure
            FROM Mesures
            ORDER BY date_mesure
            LIMIT 1,1000
        """
        tree = display.createTreeViewDisplayQuery(tab1, columns, query)
        scrollbar = ttk.Scrollbar(tab1, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Départements
        columns = ('code_departement', 'nom_departement', 'code_region', 'zone_climatique')
        query = """
            SELECT code_departement, nom_departement, code_region, zone_climatique
            FROM Departements
            ORDER BY code_departement
        """
        tree = display.createTreeViewDisplayQuery(tab2, columns, query, 200)
        scrollbar = ttk.Scrollbar(tab2,orient='vertical',command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Régions
        columns = ('code_region', 'nom_region')
        query = """
            SELECT code_region, nom_region
            FROM Regions
            ORDER BY code_region
        """
        tree = display.createTreeViewDisplayQuery(tab3, columns, query, 250)
        scrollbar = ttk.Scrollbar(tab3,orient='vertical',command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        #TODO Q4 Afficher les données des nouvelles tables

        # Chauffage
        columns = ('energie_avant_travaux_chauffage', 'energie_installee_chauffage', 'generateur_chauffage', 'type_chaudiere_chauffage')
        query = """
            SELECT energie_avant_travaux_chauffage, energie_installee_chauffage, generateur_chauffage, type_chaudiere_chauffage
            FROM Chauffage
        """
        tree = display.createTreeViewDisplayQuery(tab4, columns, query, 250)
        scrollbar = ttk.Scrollbar(tab4, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Photovoltaique 

        columns = ('puissance_installee_photovoltaique', 'type_panneaux_photovoltaique')
        query = """
            SELECT puissance_installee_photovoltaique, type_panneaux_photovoltaique
            FROM Photovoltaique
        """
        tree = display.createTreeViewDisplayQuery(tab5, columns, query, 250)
        scrollbar = ttk.Scrollbar(tab5, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Isolation
        columns = ('poste_isolation', 'isolant_isolation', 'epaisseur_isolation', 'surface_isolation')
        query = """
            SELECT poste_isolation, isolant_isolation, epaisseur_isolation, surface_isolation
            FROM Isolation
        """
        tree = display.createTreeViewDisplayQuery(tab6, columns, query, 250)
        scrollbar = ttk.Scrollbar(tab6, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Travaux
        columns = ('cout_total_travaux', 'cout_induit_ht_Travaux', 'annee_travaux', 'type_logement_Travaux', 'annee_construction_logement_Travaux', 'code_departement', 'type_travaux')
        query = """
             SELECT  cout_total_travaux, cout_induit_ht_Travaux, annee_travaux, type_logement_Travaux, annee_construction_logement_Travaux, code_departement, type_travaux
             FROM Travaux
            """
        tree = display.createTreeViewDisplayQuery(tab7, columns, query, 250)
        scrollbar = ttk.Scrollbar(tab7, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")