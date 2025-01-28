'''
ui.py

El codigo de la UI. CliApp esta para prototipar la aplicacion
'''
from PySide6 import QtCore, QtWidgets, QtGui
import random
import sys
import threading
import datetime
import matplotlib

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import matplotlib.pyplot as plt

import tkinter as tk
import ttkbootstrap as ttk


#Ventana principal de la aplicacion
class TkApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="vapor")
        self.controller = None

        matplotlib.use("TkAgg")

        self.title("AnyWrapped v0.1")
        self.geometry("800x500")
        #self.resizable(False, False)
        
        self.main_frame = TkMainFrame(self)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
    
    def set_controller(self, controller):
        self.controller = controller

    def start(self):
        #self.app = QtWidgets.QApplication([])
        #self.widget = PySideMainWindow(self)
        #self.widget.show()

        #self.controller.get_stats()
        #self.controller.get_historial()

        #sys.exit(self.app.exec())

        self.controller.get_stats()
        self.mainloop()
    
    def print(self, msg):
        pass

    def set_most_played_songs(self, songlist):
        #self.widget.reset_most_played_songs()
        #for i, song in enumerate(songlist):
        #    self.widget.add_most_played_songs(i, song)
        self.main_frame.set_most_played_songs(songlist)

    def set_most_played_artists(self, songlist):
        #self.widget.reset_most_played_artists()
        #for i, artist in enumerate(songlist):
        #    self.widget.add_most_played_artists(i, artist)
        self.main_frame.set_most_played_artists(songlist)

    def set_historial(self, histlist):
        #self.widget.reset_historial()
        #for entry in histlist:
        #    dt = datetime.datetime.fromtimestamp(entry[1])
        #    self.widget.add_historial(f"{dt} {entry[0][2]} - {entry[0][3]} - {entry[0][4]}")
        pass

    def set_stats(self):
        pass

    def set_artists(self, artists, artists_reproductions):
        pass

    def app_exit(self):
        pass


#Frame principal dentro de la ventana principal. Tendra los datos, etc
class TkMainFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        self.test_label = ttk.Label(self, text="AnyWrapped v0.1", bootstyle="primary")
        self.test_label.grid(column=0, row=0, sticky=tk.EW)

        self.main_notebook = ttk.Notebook(self, bootstyle="primary")
        self.stats_frame = TkStatsFrame(self)
        self.main_notebook.add(self.stats_frame, text="Main Stats")
        self.main_notebook.add(ttk.Frame(), text="History")
        self.main_notebook.add(ttk.Frame(), text="Settings")
        self.main_notebook.grid(column=0, row=1, sticky=tk.NSEW)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
    
    def set_most_played_artists(self, songlist):
        self.stats_frame.set_most_played_artists(songlist)
    
    def set_most_played_songs(self, songlist):
        self.stats_frame.set_most_played_songs(songlist)

class TkStatsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        self.most_played_artists_labelframe = ttk.Labelframe(self, text="Most Played Artists")
        self.most_played_artists_labelframe.pack(expand=1, fill="both")
        self.most_played_artists_labelframe.columnconfigure(0, weight=1)
        self.most_played_artists_labelframe.rowconfigure(0, weight=1)

        self.most_played_artists_treeview = ttk.Treeview(self.most_played_artists_labelframe,
                                                         columns=("artist", "reproductions"))
        self.most_played_artists_treeview.heading("artist", text="Artist")
        self.most_played_artists_treeview.heading("reproductions", text="Reproductions")
        self.most_played_artists_treeview.grid(row=0, column=0, sticky=tk.NSEW)

        self.most_played_songs_labelframe = ttk.Labelframe(self, text="Most Played Songs")
        self.most_played_songs_labelframe.pack(expand=1, fill="both")
        self.most_played_songs_labelframe.columnconfigure(0, weight=1)
        self.most_played_songs_labelframe.rowconfigure(0, weight=1)

        self.most_played_songs_treeview = ttk.Treeview(self.most_played_songs_labelframe,
                                                         columns=("artist", "album", "title", "reproductions"))
        self.most_played_songs_treeview.heading("artist", text="Artist")
        self.most_played_songs_treeview.heading("album", text="Album")
        self.most_played_songs_treeview.heading("title", text="Title")
        self.most_played_songs_treeview.heading("reproductions", text="Reproductions")
        self.most_played_songs_treeview.grid(row=0, column=0, sticky=tk.NSEW)

        

    def set_most_played_artists(self, songlist):
        print("Updating Songlist")

        self.reset_most_played_artists()
        
        for song in songlist:
            print(song)
            self.most_played_artists_treeview.insert('', tk.END, values=song)

    def reset_most_played_artists(self):
        self.most_played_artists_treeview.delete(*self.most_played_artists_treeview.get_children())

    def set_most_played_songs(self, songlist):
        self.reset_most_played_songs()

        for song in songlist:
            print(song)
            self.most_played_songs_treeview.insert('', tk.END, values=(song[2], song[3], song[4], song[5]))

    def reset_most_played_songs(self):
        self.most_played_songs_treeview.delete(*self.most_played_songs_treeview.get_children())


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