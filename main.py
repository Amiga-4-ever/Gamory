import tkinter as tk
from tkinter.simpledialog import askstring 
from tkinter import *
from tkinter import messagebox
from highscore import HighscoreManager
from PIL import Image, ImageTk # verarbeitet die Bilder
import random
import pygame

#pygame mixer initialisieren
pygame.mixer.init()

# Ausgabe zentrieren
def zentriere_fenster(root, fenster_breite, fenster_hoehe):
    # Bildschirmgröße ermitteln
    screen_breite = root.winfo_screenwidth()
    screen_hoehe = root.winfo_screenheight()

    # Position des Fensters berechnen
    x_position = (screen_breite - fenster_breite) // 2
    y_position = (screen_hoehe - fenster_hoehe) // 2

    # Fenster zentrieren
    root.geometry(f"{fenster_breite}x{fenster_hoehe}+{x_position}+{y_position}")

root = tk.Tk()
root.title("Gamory")

# Fenstergröße definieren
fenster_breite = 1000
fenster_hoehe = 900

# Fenster zentrieren
zentriere_fenster(root, fenster_breite, fenster_hoehe)

icon = PhotoImage(file="img/memory_icon.png") # Icon in Titelleiste
root.iconphoto(True, icon)
root.resizable(width=False, height=False) # Fenstergröße nicht veränderbar
root.configure(bg="cadetblue2")

class Memoryfeld:
    def __init__(self, root):

        # Memorykarten
        self.bilderListe = [
            "img/arcade.png", "img/board-game.png", "img/disk.png", 
            "img/game-over.png", "img/gameboy.png","img/ghost.png",
            "img/ghostred.png", "img/joystick.png","img/minecraft.png",
            "img/pacman.png","img/pikachu.png","img/ping-pong.png",
            "img/playstation.png","img/racing-car.png","img/rubik.png",
            "img/soccer.png","img/space-invaders.png","img/switch.png",
            "img/swords.png", "img/tennis.png", "img/tetris.png"
        ]

        # Sind 21 Bilder vorhanden?
        assert len(self.bilderListe) == 21, "Es müssen genau 21 verschiedene Bilder vorhanden sein."

        # Karten duplizieren
        self.memorykarte = self.bilderListe * 2
         # Überprüfen, ob wir jetzt exakt 42 Karten (6x7) haben
        assert len(self.memorykarte) == 42, "Die Anzahl der Karten muss exakt 42 betragen."
        # mischen
        random.shuffle(self.memorykarte)

        # Speicher für Karten
        self.umgedrehteKarten = []
        self.gemerkteKarten = []

        # int-Variablen für Punkte
        self.Player1Punkte = 0
        self.computerPunkte = 0

        # Startspieler
        self.aktuellerSpieler = "Player1"  

        # Spielfeldbeschriftung für Punkte
        self.Player1PunkteLabel = tk.Label(root, text="Punkte Spieler: 0", bg="cadetblue2")
        self.Player1PunkteLabel.pack()
        self.computerPunkteLabel = tk.Label(root, text="Punkte Computer: 0", bg="cadetblue2")
        self.computerPunkteLabel.pack()

        # Spielfeldraster 
        self.spielfeld = tk.Frame(root)
        self.spielfeld.pack()

        # Kartenrückseite
        self.rueckseite = self.lade_bild("img/line.png")

        # Buttons für die Karten
        self.buttons = []
        self.bilder = [] # Bildobjekte speichern


        for i in range(6): # Zeilen
            row = []
            for j in range(7): # 7 Spalten
                btn = tk.Button(self.spielfeld, image = self.rueckseite, width=128, height=128, bg="white", command=lambda i=i, j=j: self.karte_waehlen(i, j))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

        self.karten_Bilder = self.lade_kartenbilder()

    def lade_bild(self, dateipfad):
        bild = Image.open(dateipfad).convert("RGBA") # Alphakanal sicherstellen
        # weißen Hintergrund erstellen
        background = Image.new("RGB", bild.size, (255,255,255))
        # Transparente Bereiche weiß auffüllen
        background.paste(bild, mask=bild.getchannel("A")) 
        return ImageTk.PhotoImage(background)



    def lade_kartenbilder(self):
        # lädt Bilder und speichert sie Dictionary
        bilder = {}
        for karte in self.memorykarte:
            if karte not in bilder:
                bilder[karte] = self.lade_bild(karte)
        return bilder
    
    def karte_waehlen(self, i, j):
        # weniger als 2 Karten aufgedeckt und ob angeklickte Karte nicht bereits Teil eines aufgedeckten Paares ist
        if len(self.umgedrehteKarten) < 2 and not self.buttons[i][j]['state'] == 'disabled':
            karte = self.memorykarte[i * 7 + j] # Listeneintrag bestimmen
            self.buttons[i][j].config(image=self.karten_Bilder[karte]) # greift auf Bild zu und zeigt es an
            self.buttons[i][j]['state'] = 'disabled' # deaktivieren, damit sie nicht noch einmal angeklickt werden kann
            self.umgedrehteKarten.append((i,j, karte)) # speichern für spätere Überprüfung, ob Karten identisch sind

            if len(self.umgedrehteKarten) == 2:
                root.after(1337, self.ueberpruefe_paar)

    def ueberpruefe_paar(self):
        # Tupel mit Position und Bild
        (i1, j1, karte1), (i2, j2, karte2) = self.umgedrehteKarten

        if karte1 == karte2:
            # Audio abspielen
            pygame.mixer.music.load("img/found.mp3")
            pygame.mixer.music.play()
            # Paar gefunden, Punkte vergeben und notieren
            if self.aktuellerSpieler == "Player1":
                self.Player1Punkte += 1
                self.Player1PunkteLabel.config(text=f"Punkte Spieler: {self.Player1Punkte}")
            else:
                self.computerPunkte += 1
                self.computerPunkteLabel.config(text=f"Punkte Computer: {self.computerPunkte}")

        else:
            # kein Paar: Bild wieder entfernen, Button mit Status "normal" wieder aktiviert für nächste Aktion
            self.buttons[i1][j1].config(image=self.rueckseite, state='normal')
            self.buttons[i2][j2].config(image=self.rueckseite, state='normal')
            # Spieler wechseln
            self.aktuellerSpieler = "Computer" if self.aktuellerSpieler == "Player1" else "Player1"

        self.umgedrehteKarten = [] # Leeren, um neue Karten aufdecken zu können

        # Spielende überprüfen
        self.maxPunkte = self.Player1Punkte + self.computerPunkte
        if self.maxPunkte == 21:
            self.spiel_beenden()
        elif self.aktuellerSpieler == "Computer":
            self.computer_zieht()

    def spiel_beenden(self):
        # Punkte und Gewinner ermitteln
        gewinner = "Player1" if self.Player1Punkte > self.computerPunkte else "Computer"
        messagebox.showinfo("Spiel beendet", f"{gewinner} hat gewonnen!\n"
                                            f"Punkte Spieler: {self.Player1Punkte}\n"
                                            f"Punkte Computer: {self.computerPunkte}")

        # Wenn Player1 gewinnt, Name für Highscore-Liste eintragen
        if self.Player1Punkte > self.computerPunkte:
            name = askstring("Highscore", "Trage deinen Namen für die Highscoreliste ein:")
            if name:  # Nur eintragen, wenn ein Name eingegeben wurde
                highscore_manager.neuer_eintrag(name, self.Player1Punkte)

        # Nach Highscore-Eintrag fragen, ob ein neues Spiel gestartet werden soll
        antwort = messagebox.askquestion("Neues Spiel", "Möchtest du ein neues Spiel starten?")
        if antwort == "yes":
            self.neues_Spiel()
        else:
            root.quit()

    def neues_Spiel(self):
        # alle Felder zurücksetzen
        self.Player1Punkte = 0
        self.computerPunkte = 0
        # mit config aktualisieren, nicht neu erstellen!
        self.Player1PunkteLabel.config(text="Punkte Spieler: 0")
        self.computerPunkteLabel.config(text="Punkte Computer: 0")
        # Karten neu mischen
        random.shuffle(self.memorykarte)

        # Spielfeld zurücksetzen
        for i in range(6):
            for j in range(7):
                self.buttons[i][j].config(image=self.rueckseite, state='normal')

    def computer_zieht(self):
        # Zufällige Karte auswählen, die noch nicht aufgedeckt wurde
        moegliche_zuege = [(i, j) for i in range(6) for j in range(7) if self.buttons[i][j]['state'] == 'normal']
        if moegliche_zuege:
            i1, j1 = random.choice(moegliche_zuege)
            self.karte_waehlen(i1, j1)

            # Nochmal eine Karte auswählen
            moegliche_zuege = [(i, j) for i in range(6) for j in range(7) if self.buttons[i][j]['state'] == 'normal']
            i2, j2 = random.choice(moegliche_zuege)
            self.karte_waehlen(i2, j2)

highscore_manager = HighscoreManager()

def info_anzeigen():
    messagebox.showinfo("Über Gamory", "Programm: Gamory\nVersion: 1.0\nProgrammierer: Amiga4ever\nIcons created by Smashicons - Flaticon")

# Menübar
menu = Menu(root, background="cadetblue")
root.config(menu=menu)
filemenu = Menu(menu, background="cadetblue")
menu.add_cascade(label="Spiel", menu=filemenu)
filemenu.add_command(label="Neues Spiel", command=lambda: spiel.neues_Spiel())
filemenu.add_command(label="Highscoreliste", command=lambda: highscore_manager.anzeigen())
filemenu.add_command(label="Über", command=lambda: info_anzeigen())
filemenu.add_separator()
filemenu.add_command(label="Spiel beenden", command=root.quit)

# Spielfeld initialisieren
spiel = Memoryfeld(root)

root.mainloop()