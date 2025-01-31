'''
ui.py

El codigo de la UI. CliApp esta para prototipar la aplicacion
'''
import random
import sys
import threading
import datetime

import tkinter as tk
from tkinter.messagebox import showinfo
import ttkbootstrap as ttk
import ttkbootstrap.tableview as ttktableview
from PIL import ImageTk, Image

#Ventana principal de la aplicacion
class TkApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="vapor")
        self.controller = None

        self.withdrawed = False

        self.title("AnyWrapped v0.1 - By AnonymousTaikoCat")
        self.geometry("1000x700")
        #self.resizable(False, False)
        
        self.main_frame = TkMainFrame(self)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.gui_close)
    
    def set_controller(self, controller):
        self.controller = controller
    
    #Getter para checkear si la ventana esta visible o no
    def is_withdrawed(self):
        return self.withdrawed

    #Start: obtiene los datos y mainloop
    def start(self):
        self.update_data()

        self.controller.gui_close()
        
        self.mainloop()
    
    #Obtiene todos los datos de la UI
    def update_data(self):
        self.controller.get_stats()
        self.controller.get_historial()

    def print(self, msg):
        pass

    def set_most_played_songs(self, songlist):
        self.main_frame.set_most_played_songs(songlist)

    def set_most_played_artists(self, songlist):
        self.main_frame.set_most_played_artists(songlist)

    def set_historial(self, histlist):
        self.main_frame.set_historial(histlist)

    def set_stats(self):
        pass

    def set_artists(self, artists, artists_reproductions):
        pass

    #Da un mensaje de que no se cierra completamente y cierra la ventana
    def gui_close(self):
        showinfo("AnyWrapped fun fact:", "AnyWrapped will keep running as a background task. To fully close the program, use the icon in the system tray.")
        self.controller.gui_close()

    #Cierra la ventana
    def withdraw_window(self):
        self.withdrawed = True
        self.withdraw()

    #Muestra la ventana cerrada
    def show_window(self):
        self.withdrawed = False
        self.after(0, self.deiconify)
        self.update_data()

    #Para toda la GUI
    def stop(self):
        self.show_window()
        self.quit()
        print("GUI: Stopped")

    


#Frame principal dentro de la ventana principal. Tendra los datos, etc
class TkMainFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        self.logo_image = ImageTk.PhotoImage(Image.open("assets/logo.png"))
        self.test_label = ttk.Label(self, image=self.logo_image, anchor=tk.CENTER)
        self.test_label.grid(column=0, row=0, sticky=tk.EW)
        self.columnconfigure(0, weight=1)
    

        self.main_notebook = ttk.Notebook(self, bootstyle="primary")
        self.stats_frame = TkStatsFrame(self)
        self.history_frame = TkHistoryFrame(self)
        self.settings_frame = TkSettingsFrame(self)
        self.main_notebook.add(self.stats_frame, text="Main Stats")
        self.main_notebook.add(self.history_frame, text="History")
        self.main_notebook.add(self.settings_frame, text="Settings")
        self.main_notebook.grid(column=0, row=1, sticky=tk.NSEW, ipadx=5, ipady=5)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
    
    def set_most_played_artists(self, songlist):
        self.stats_frame.set_most_played_artists(songlist)
    
    def set_most_played_songs(self, songlist):
        self.stats_frame.set_most_played_songs(songlist)

    def set_historial(self, histlist):
        self.history_frame.set_historial(histlist)

#Frame para los stats generales
class TkStatsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        self.most_played_artists_labelframe = ttk.Labelframe(self, text="Most Played Artists")
        self.most_played_artists_labelframe.pack(expand=1, fill="both", padx=5, pady=5)
        self.most_played_artists_labelframe.columnconfigure(0, weight=1)
        self.most_played_artists_labelframe.rowconfigure(0, weight=1)

        self.most_played_artists_treeview = ttk.Treeview(self.most_played_artists_labelframe,
                                                         columns=("artist", "reproductions"),
                                                         bootstyle="info")
        self.most_played_artists_treeview["show"] = "headings" #Para que no muestre la primera columna vacia
        self.most_played_artists_treeview.heading("artist", text="Artist")
        self.most_played_artists_treeview.heading("reproductions", text="Reproductions")
        self.most_played_artists_treeview.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.most_played_artists_scrollbar = ttk.Scrollbar(self.most_played_artists_labelframe, 
                                                orient=tk.VERTICAL, 
                                                command=self.most_played_artists_treeview.yview,
                                                bootstyle="info")
        self.most_played_artists_treeview.configure(yscrollcommand=self.most_played_artists_scrollbar.set)
        self.most_played_artists_scrollbar.grid(row=0, column=1, sticky=tk.NS, padx=5, pady=5)

        self.most_played_songs_labelframe = ttk.Labelframe(self, text="Most Played Songs")
        self.most_played_songs_labelframe.pack(expand=1, fill="both", padx=5, pady=5)
        self.most_played_songs_labelframe.columnconfigure(0, weight=1)
        self.most_played_songs_labelframe.rowconfigure(0, weight=1)

        self.most_played_songs_treeview = ttk.Treeview(self.most_played_songs_labelframe,
                                                         columns=("artist", "album", "title", "reproductions"),
                                                         bootstyle="info")
        self.most_played_songs_treeview["show"] = "headings" #Para que no muestre la primera columna vacia
        self.most_played_songs_treeview.heading("artist", text="Artist")
        self.most_played_songs_treeview.heading("album", text="Album")
        self.most_played_songs_treeview.heading("title", text="Title")
        self.most_played_songs_treeview.heading("reproductions", text="Reproductions")
        self.most_played_songs_treeview.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.most_played_songs_scrollbar = ttk.Scrollbar(self.most_played_songs_labelframe, 
                                                orient=tk.VERTICAL, 
                                                command=self.most_played_songs_treeview.yview,
                                                bootstyle="info")
        self.most_played_songs_treeview.configure(yscrollcommand=self.most_played_songs_scrollbar.set)
        self.most_played_songs_scrollbar.grid(row=0, column=1, sticky=tk.NS, padx=5, pady=5)

    def set_most_played_artists(self, songlist):
        self.reset_most_played_artists()
        
        for song in songlist:
            self.most_played_artists_treeview.insert('', tk.END, values=(song[0], f"Played {song[1]} times."))

    def reset_most_played_artists(self):
        self.most_played_artists_treeview.delete(*self.most_played_artists_treeview.get_children())

    def set_most_played_songs(self, songlist):
        self.reset_most_played_songs()

        for song in songlist:
            self.most_played_songs_treeview.insert('', tk.END, values=(song[2], song[3], song[4], f"Played {song[5]} times."))

    def reset_most_played_songs(self):
        self.most_played_songs_treeview.delete(*self.most_played_songs_treeview.get_children())

#Frame para el historial
class TkHistoryFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.history_labelframe = ttk.Labelframe(self, text="History")
        self.history_labelframe.pack(expand=1, fill="both", padx=5, pady=5)

        self.history_labelframe.rowconfigure(0, weight=1)
        self.history_labelframe.columnconfigure(0, weight=1)

        '''
        self.history_treeview = ttk.Treeview(self.history_labelframe, 
                                             columns=("date", "artist", "album", "title"),
                                             bootstyle="info")
        self.history_treeview.heading("date", text="Date")
        self.history_treeview.heading("artist", text="Artist")
        self.history_treeview.heading("album", text="Album")
        self.history_treeview.heading("title", text="Title")
        self.history_treeview["show"] = "headings"
        self.history_treeview.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.history_scrollbar = ttk.Scrollbar(self.history_labelframe, 
                                                orient=tk.VERTICAL, 
                                                command=self.history_treeview.yview,
                                                bootstyle="info")
        self.history_treeview.configure(yscrollcommand=self.history_scrollbar.set)
        self.history_scrollbar.grid(row=0, column=1, sticky=tk.NS, padx=5, pady=5)
        '''

        coldata = [
            "Date",
            "Artist",
            "Album",
            "Title"
        ]

        self.history_tableview = ttktableview.Tableview(master=self.history_labelframe, 
                                                        coldata=coldata, 
                                                        rowdata=[],
                                                        pagesize=50,
                                                        paginated=True,
                                                        searchable=True,
                                                        bootstyle="info",
                                                        autoalign=True)
        self.history_tableview.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.history_scrollbar = ttk.Scrollbar(self.history_labelframe, 
                                                orient=tk.VERTICAL, 
                                                command=self.history_tableview.view.yview,
                                                bootstyle="info")
        self.history_tableview.configure(yscrollcommand=self.history_scrollbar.set)
        self.history_scrollbar.grid(row=0, column=1, sticky=tk.NS, padx=5, pady=5)
    
    def set_historial(self, histlist):
        self.reset_historial()
        for entry in histlist:
            dt = datetime.datetime.fromtimestamp(entry[1])
            #self.history_treeview.insert('', tk.END, values=(dt, entry[0][2], entry[0][3], entry[0][4]))
            self.history_tableview.insert_row('end', [dt, entry[0][2], entry[0][3], entry[0][4]])
        
        self.history_tableview.load_table_data()
    
    def reset_historial(self):
        #self.history_treeview.delete(*self.history_treeview.get_children())
        self.history_tableview.delete_rows(None, None)
        pass

class TkArtistsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.artists_labelframe = ttk.Labelframe(self, text="History")
        self.artists_labelframe.pack(expand=1, fill="both", padx=5, pady=5)

        self.artists_labelframe.rowconfigure(0, weight=1)
        self.artists_labelframe.columnconfigure(0, weight=1)

        self.artists_treeview = ttk.Treeview(self.artists_labelframe, 
                                             columns=("artist", "reproductions"),
                                             bootstyle="info")
        self.artists_treeview.heading("artist", text="Artist")
        self.artists_treeview.heading("reproductions", text="Reproductions")
        self.artists_treeview["show"] = "headings"
        self.artists_treeview.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.artists_scrollbar = ttk.Scrollbar(self.artists_labelframe, 
                                                orient=tk.VERTICAL, 
                                                command=self.artists_treeview.yview,
                                                bootstyle="info")
        self.artists_treeview.configure(yscrollcommand=self.artists_scrollbar.set)
        self.artists_scrollbar.grid(row=0, column=1, sticky=tk.NS, padx=5, pady=5)

class TkSettingsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.var_database = tk.StringVar(self, "stats")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.database_labelframe = ttk.Labelframe(self, text="Database Settings")
        self.database_labelframe.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=5)

        self.database_label = ttk.Label(self.database_labelframe, text="Database: ")
        self.database_label.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)

        self.database_combobox = ttk.Combobox(self.database_labelframe, state="readonly", values=["stats", "test1", "test3"], textvariable=self.var_database)
        self.database_combobox.grid(column=1, row=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)

        self.database_add_button = ttk.Button(self.database_labelframe, text="Add")
        self.database_add_button.grid(column=0, row=1, padx=5, pady=5, sticky=tk.NSEW)

        self.database_rename_button = ttk.Button(self.database_labelframe, text="Rename")
        self.database_rename_button.grid(column=1, row=1, padx=5, pady=5, sticky=tk.NSEW)

        self.database_delete_button = ttk.Button(self.database_labelframe, text="Delete")
        self.database_delete_button.grid(column=2, row=1, padx=5, pady=5, sticky=tk.NSEW)

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