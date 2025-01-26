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
        self.setFixedSize(QtCore.QSize(800, 720))

        self.layout = QtWidgets.QVBoxLayout(self)

        #Titulo de la aplicacion
        self.title_label = QtWidgets.QLabel("AnyWrapped v0.1",
                                     alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        #Boton de testeo
        self.button = QtWidgets.QPushButton("Click me!")
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.magic)

        #Label de artistas mas reproducidos
        self.artists_label = QtWidgets.QLabel("Most Played Artists",
                                     alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.artists_label)

        #Lista de artistas mas reproducidos
        self.list_most_played_artists = QtWidgets.QListWidget()
        self.layout.addWidget(self.list_most_played_artists)

        #Label de artistas mas reproducidos
        self.songs_label = QtWidgets.QLabel("Most Played Songs",
                                     alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.songs_label)

        #Lista de canciones mas reproducidas
        self.list_most_played_songs = QtWidgets.QListWidget()
        self.layout.addWidget(self.list_most_played_songs)

        #Label historial
        self.historial_label = QtWidgets.QLabel("Historial",
                                     alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.historial_label)

        #Historial
        self.list_historial = QtWidgets.QListWidget()
        self.layout.addWidget(self.list_historial)
    
    def closeEvent(self, event):
        self.root.app_exit()
        event.accept() # let the window close


    #Funcion de testeo para el boton
    @QtCore.Slot()
    def magic(self):
        self.title_label.setText("This doesnt wrap anything rn")
        print("LOLOLOLOLOLOLOL")

    #Agrega una cancion a la lista de canciones mas reproducidas
    def add_most_played_songs(self, i, song):
        self.list_most_played_songs.addItems([
            f"{i+1}: {song[1]} (Played {song[5]} times)"
        ])

    def reset_most_played_songs(self):
        while self.list_most_played_songs.count() != 0:
            self.list_most_played_songs.takeItem(0)
    
    #Agrega un artista a la lista de artista mas reproducidas
    def add_most_played_artists(self, i, artists):
        self.list_most_played_artists.addItems([
            f"{i+1}: {artists[0]} (Played {artists[1]} times)"
        ])

    def reset_most_played_artists(self):
        while self.list_most_played_artists.count() != 0:
            self.list_most_played_artists.takeItem(0)

    #Agrega una entrada al historial
    def add_historial(self, song):
        self.list_historial.addItems([
            song
        ])
    
    def reset_historial(self):
        while self.list_historial.count() != 0:
            self.list_historial.takeItem(0)


class GuiApp():
    def __init__(self):
        self.controller = None
    
    def set_controller(self, controller):
        self.controller = controller

    def start(self):
        self.app = QtWidgets.QApplication([])
        self.widget = GuiMainWindow(self)
        self.widget.show()

        self.controller.get_stats()
        self.controller.get_historial()

        sys.exit(self.app.exec())
    
    def print(self, msg):
        pass

    def set_most_played_songs(self, songlist):
        self.widget.reset_most_played_songs()
        for i, song in enumerate(songlist):
            self.widget.add_most_played_songs(i, song)

    def set_most_played_artists(self, songlist):
        self.widget.reset_most_played_artists()
        for i, artist in enumerate(songlist):
            self.widget.add_most_played_artists(i, artist)

    def set_historial(self, histlist):
        self.widget.reset_historial()
        for entry in histlist:
            dt = datetime.datetime.fromtimestamp(entry[1])
            self.widget.add_historial(f"{dt} {entry[0][2]} - {entry[0][3]} - {entry[0][4]}")

    def set_stats(self):
        pass

    def set_artists(self, artists, artists_reproductions):
        pass

    def app_exit(self):
        self.controller.app_exit()

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

        self.controller.get_stats()

        self.print("\nType HELP to get a list of commands")

        #Una pequeña linea de comandos para testear IO
        while True:
            command = input(">").lower()

            if command == "hist":
                self.controller.get_historial()
            elif command == "stats":
                self.set_stats()
            elif command == "artists":
                self.controller.get_artists()
            elif command == "help":
                self.show_help()
            elif command == "exit":
                self.controller.app_exit()
            else:
                self.print("Unrecognized command. Type HELP to get a list of commands.")

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
    
    def set_artists(self, artists, artists_reproductions):
        self.print("ARTISTS:")
        for i,artist in enumerate(artists):
            self.print(f"{artist} (played {artists_reproductions[i]} times).")

    # Para el comando help
    def show_help(self):
        print('''
COMMANDS:
stats: show most played songs and artists.
hist: show historial (20 most recent).
artists: show full list of played artists and their reproductions.
exit: closes the app.
''')