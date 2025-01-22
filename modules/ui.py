'''
ui.py

El codigo de la UI. CliApp esta para prototipar la aplicacion
'''
from PySide6 import QtCore, QtWidgets, QtGui
import random
import sys
import threading

class GuiMainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

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


class GuiApp():
    def __init__(self):
        self.controller = None
    
    def set_controller(self, controller):
        self.controller = controller

    def start(self):
        app = QtWidgets.QApplication([])
        widget = GuiMainWindow()
        widget.show()

        sys.exit(app.exec())

class CliApp():
    def __init__(self):
        self.controller = None
    
    def set_controller(self, controller):
        self.controller = controller
    
    def start(self):
        print("--- AIMP Wrapped v0.1 --- Running ---")

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
        pass