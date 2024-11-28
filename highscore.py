import json
import tkinter as tk

class HighscoreManager:
    def __init__(self, datei="highscores.json"):
        self.datei = datei
        self.highscores = self.lade_highscores()

    def lade_highscores(self):
        try:
            with open(self.datei, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []  # Keine Datei vorhanden, leere Liste zurückgeben

    def speichere_highscores(self):
        with open(self.datei, "w") as f:
            json.dump(self.highscores, f, indent=4)

    def neuer_eintrag(self, name, punkte):
        self.highscores.append({"name": name, "punkte": punkte})
        # Nach Punkten sortieren (absteigend)
        self.highscores.sort(key=lambda x: x["punkte"], reverse=True)
        # Nur die Top 10 behalten
        self.highscores = self.highscores[:10]
        self.speichere_highscores()

    def anzeigen(self):
        # Ein einfaches GUI zur Anzeige
        fenster = tk.Toplevel()
        fenster.title("Highscoreliste")
        fenster.geometry("300x400")
        fenster.configure(bg="white")

        label = tk.Label(fenster, text="Highscores", font=("Arial", 18), bg="white")
        label.pack(pady=10)

        for eintrag in self.highscores:
            tk.Label(fenster, text=f"{eintrag['name']} - {eintrag['punkte']} Punkte", bg="white", font=("Arial", 12)).pack()

        tk.Button(fenster, text="Schließen", command=fenster.destroy).pack(pady=10)
