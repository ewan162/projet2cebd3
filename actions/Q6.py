import tkinter as tk
from utils import display
from utils import db
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(1500, 800, self)
        self.title('F4 : températures en Isère en 2018')
        display.defineGridDisplay(self, 1, 1)
        query = """
                WITH FraicheurChaleurRecord AS (
                    SELECT strftime('%Y-%m-%d', date_mesure) AS date, MIN(temperature_moy_mesure) AS minrecord, MAX(temperature_moy_mesure) AS maxrecord
                    FROM Mesures
                    GROUP BY strftime('%m-%d', date_mesure)
                ),
                TempFroidDep AS (
                    SELECT strftime('%Y-%m-%d', date_mesure) AS date, temperature_moy_mesure AS tempfroiddep
                    FROM Mesures
                    WHERE code_departement = (
                        SELECT code_departement
                        FROM Mesures
                        JOIN Departements USING (code_departement)
                        WHERE zone_climatique = 'H1' AND strftime('%Y', date_mesure) = '2018'
                        GROUP BY code_departement
                        ORDER BY AVG(temperature_moy_mesure)
                    )
                    AND strftime('%Y', date_mesure) = '2018'
                    GROUP BY date
                ),
                TempChaleurDep AS (
                    SELECT strftime('%Y-%m-%d', date_mesure) AS date, temperature_moy_mesure AS tempchauddep
                    FROM Mesures
                    WHERE code_departement = (
                        SELECT code_departement
                        FROM Mesures
                        JOIN Departements USING (code_departement)
                        WHERE zone_climatique = 'H1' AND strftime('%Y', date_mesure) = '2018'
                        GROUP BY code_departement
                        ORDER BY AVG(temperature_moy_mesure) DESC
                    )
                    AND strftime('%Y', date_mesure) = '2018'
                    GROUP BY date
                )
                SELECT date, minrecord, maxrecord, tempfroiddep, tempchauddep
                FROM FraicheurChaleurRecord
                LEFT JOIN TempFroidDep USING (date)
                LEFT JOIN TempChaleurDep USING (date)
                ORDER BY date;
                """

        # SELECT date_mesure, temperature_min_mesure, temperature_max_mesure, 0, 30
        # FROM Mesures
        # WHERE code_departement = 38 AND strftime('%Y', date_mesure) = '2018'
        # Extraction des données et affichage dans le tableau
        result = []
        try:
            cursor = db.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            print("Erreur : " + repr(e))

        # Extraction et préparation des valeurs à mettre sur le graphique
        graph1 = []
        graph2 = []
        graph3 = []
        graph4 = []
        tabx = []
        for row in result:
            tabx.append(row[0])
            graph1.append(row[1])
            graph2.append(row[2])
            graph3.append(row[3])
            graph4.append(row[4])

        # Formatage des dates pour l'affichage sur l'axe x
        datetime_dates = [datetime.strptime(date, '%Y-%m-%d') for date in tabx]

        # Ajout de la figure et du subplot qui contiendront le graphique
        fig = Figure(figsize=(15, 8), dpi=100)
        plot1 = fig.add_subplot(111)

        # Affichage des courbes
        plot1.plot(range(len(datetime_dates)), graph1, color='#00FFFF', label='records de fraîcheur historiques pour chaque jour de l’année (toutes années confondues, toutes zones climatiques confondues)')
        plot1.plot(range(len(datetime_dates)), graph2, color='#FF8300', label='records de chaleur historiques pour chaque jour de l’année (toutes années confondues, toutes zones climatiques confondues)')
        plot1.plot(range(len(datetime_dates)), graph3, color='#0000FF', label='températures du département le plus froid de la zone H1 pour chaque jour de l’année 2018')
        plot1.plot(range(len(datetime_dates)), graph4, color='#FF0000', label='températures du département le plus chaud de la zone H1 pour chaque jour de l’année 2018.')

        # Configuration de l'axe x pour n'afficher que le premier jour de chaque mois
        xticks = [i for i, date in enumerate(datetime_dates) if date.day == 1]
        xticklabels = [date.strftime('%Y-%m-%d') for date in datetime_dates if date.day == 1]
        plot1.set_xticks(xticks)
        plot1.set_xticklabels(xticklabels, rotation=45)
        plot1.legend()

        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig,  master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()


