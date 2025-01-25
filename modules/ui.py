'''
ui.py

El codigo de la UI. CliApp esta para prototipar la aplicacion
'''
from PySide6 import QtCore, QtWidgets, QtGui
import random
import sys
import threading
import datetime

class GuiMainWindow(QtWidgets.QWidget):
    def __init__(self, root):
        super().__init__()

        self.root = root

        self.setFixedSize(QtCore.QSize(400, 300))

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("AnyWrapped v0.1",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

        self.list_historial = QtWidgets.QListWidget()
        self.list_historial.addItems([
            "La mama de la mama",
            "Scooby doo papa",
            "Dame tu cosita"
        ])
        self.layout.addWidget(self.list_historial)

    @QtCore.Slot()
    def magic(self):
        self.text.setText("This doesnt wrap anything rn")
        print("LOLOLOLOLOLOLOL")
    
    def add_historial(self, song):
        self.list_historial.addItems([
            song
        ])


class GuiApp():
    def __init__(self):
        self.controller = None
    
    def set_controller(self, controller):
        self.controller = controller

    def start(self):
        self.app = QtWidgets.QApplication([])
        self.widget = GuiMainWindow(self)
        self.widget.show()

        artists = self.controller.get_most_played_artists(limit=5, removeBlank=True)
        self.set_most_played_artists(artists)

        songlist = self.controller.get_most_played_songs(limit=5, removeBlank=True)
        self.set_most_played_artists(songlist)

        sys.exit(self.app.exec())
    
    def print(self, msg):
        pass

    def set_most_played_songs(self, songlist):
        for i, song in enumerate(songlist):
            self.widget.add_historial(f"{i+1}: {song[1]} (Played {song[5]} times)")

    def set_most_played_artists(self, songlist):
        pass

    def set_historial(self, histlist):
        pass

#Prototipo para luego implementar una GUI de verdad
class CliApp():
    def __init__(self):
        self.controller = None
        self.most_played_songs = []
        self.most_played_artists = []
    
    def set_controller(self, controller):
        self.controller = controller
    
    def start(self):
        self.print("--- AIMP Wrapped v0.1 --- Running ---")

        self.set_stats()

        self.print("\nType HELP to get a list of commands")

        #Una pequeña linea de comandos para testear IO
        while True:
            command = input(">").lower()

            if command == "hist":
                self.controller.get_historial()
            if command == "stats":
                self.set_stats()
            if command == "help":
                self.show_help()
            if command == "exit":
                self.controller.app_exit()

    def print(self, msg):
        print(msg)
    
    #Actualiza las canciones mas reproducidas en la GUI
    def set_most_played_songs(self, songlist):
        self.print("\nMost played songs:")
        for i, song in enumerate(songlist):
            self.print(f"{i+1}: {song[1]} (Played {song[5]} times)")
    
    #Actualiza los artistas mas reproducidos en la GUI
    def set_most_played_artists(self, songlist):
        self.print("\nMost played artists:")
        for i, song in enumerate(songlist):
            self.print(f"{i+1}: {song[0]} (Played {song[1]} times)")

    def set_historial(self, histlist):
        for entry in histlist:
            dt = datetime.datetime.fromtimestamp(entry[1])
            print(dt, entry[0][2], "-", entry[0][3], "-", entry[0][4])
        
    
    #Configura todos los stats
    def set_stats(self):
        artists = self.controller.get_most_played_artists(limit=5, removeBlank=True)
        self.set_most_played_artists(artists)

        songlist = self.controller.get_most_played_songs(limit=5, removeBlank=True)
        self.set_most_played_songs(songlist)

    # Para el comando help
    def show_help(self):
        print('''
COMMANDS:
stats: show most played songs and artists.
hist: show historial (20 most recent).
exit: closes the app.
              ''')