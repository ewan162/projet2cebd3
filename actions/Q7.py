import tkinter as tk
from tkinter import ttk, messagebox
from utils import display, db

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        display.centerWindow(800, 500, self)
        self.title("Q7 : gérer les travaux de rénovation")
        display.defineGridDisplay(self, 3, 1)

        ttk.Label(
            self,
            text="Gérer les travaux : ajout, modification et suppression",
            wraplength=500,
            anchor="center",
            font=("Helvetica", "10", "bold"),
        ).grid(sticky="we", row=0)

        # Affichage des travaux
        self.tree = display.createTreeViewDisplayQuery(
            self,
            columns=("id_travaux", "type_travaux", "cout_total_travaux", "cout_induit_ht_Travaux", "annee_travaux", "type_logement_Travaux", "annee_construction_logement_Travaux", "code_departement"),
            query="""
                SELECT id_travaux, type_travaux, cout_total_travaux, cout_induit_ht_Travaux, annee_travaux,
                       type_logement_Travaux, annee_construction_logement_Travaux, code_departement
                FROM Travaux
                ORDER BY id_travaux
            """,
            size=150,
        )
        self.tree.grid(row=1, sticky="nswe")

        # Boutons d'actions
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, sticky="nswe")
        tk.Button(button_frame, text="Ajouter", command=self.ajouter).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Modifier", command=self.modifier).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Supprimer", command=self.supprimer).grid(row=0, column=2, padx=10, pady=10)

    def ajouter(self):
        modifierfenetre(self, "Ajouter un travaux")

    def modifier(self):
        selection = self.tree.focus()
        if selection:
            id_travail = self.tree.item(selection)["values"][0]
            modifierfenetre(self, "Modifier travaux", id_travail)
        else:
            messagebox.showwarning("Veuillez sélectionner")

    def supprimer(self):
        selection = self.tree.focus()
        if selection:
            id_travail = self.tree.item(selection)["values"][0]
            cursor = db.data.cursor()
            cursor.execute("DELETE FROM Travaux WHERE id_travaux = ?", (id_travail,))
            db.data.commit()
            self.recharger()
            messagebox.showinfo("Bien supprimé !")
        else:
            messagebox.showwarning("Veuillez sélectionner")

    def recharger(self):
        self.tree.delete(*self.tree.get_children())
        cursor = db.data.cursor()
        result = cursor.execute(
            """
            SELECT id_travaux, type_travaux, cout_total_travaux, cout_induit_ht_Travaux, annee_travaux,
                   type_logement_Travaux, annee_construction_logement_Travaux, code_departement
            FROM Travaux
            ORDER BY id_travaux
            """
        )
        for row in result:
            self.tree.insert("", tk.END, values=row)


class modifierfenetre(tk.Toplevel):
    def __init__(self, parent, title, id_travail=None):
        
        super().__init__(parent)
        self.conn = db.data
        self.id_travail = id_travail
        self.title(title)
        self.geometry("400x400")
        # Utilisation de chatgpt pour cette partie que je n'ai pas reussi :
        self.entries = {}
        fields = [
            "Type de travaux",
            "Coût total",
            "Coût induit HT",
            "Année des travaux",
            "Type de logement",
            "Année de construction",
            "Code département",
        ]
        for i, field in enumerate(fields):
            tk.Label(self, text=field).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            var = tk.StringVar()
            entry = tk.Entry(self, textvariable=var)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = var
        #
        # Bouton sauvegarder
        tk.Button(self, text="Enregistrer", command=self.sauvegarder).grid(row=len(fields), column=0, columnspan=2, pady=10)

        if self.id_travail:
            self.charger()

    def charger(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT type_travaux, cout_total_travaux, cout_induit_ht_Travaux, annee_travaux,
                   type_logement_Travaux, annee_construction_logement_Travaux, code_departement
            FROM Travaux
            WHERE id_travaux = ?
            """,(self.id_travail,)
        )
        row = cursor.fetchone()
        if row:
            for value, var in zip(row, self.entries.values()):
                var.set(value)

    def sauvegarder(self):
        try:
            cursor = self.conn.cursor()
            resultats = [var.get() for var in self.entries.values()]
            if self.id_travail:
                query = """
                    UPDATE Travaux
                    SET type_travaux = ?, cout_total_travaux = ?, cout_induit_ht_Travaux = ?, annee_travaux = ?,
                        type_logement_Travaux = ?, annee_construction_logement_Travaux = ?, code_departement = ?
                    WHERE id_travaux = ?
                """
                cursor.execute(query, (*resultats, self.id_travail))
            else:
                query = """
                    INSERT INTO Travaux (type_travaux, cout_total_travaux, cout_induit_ht_Travaux, annee_travaux,
                                         type_logement_Travaux, annee_construction_logement_Travaux, code_departement)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(query, resultats)
            self.conn.commit()
            self.destroy()
            self.master.recharger()
            messagebox.showinfo("Enregistré !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'enregistrement : {str(e)}")

