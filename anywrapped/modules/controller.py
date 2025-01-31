import sys
import anywrapped.modules.ui as ui

class AppController():
    def __init__(self):
        self.view = None
        self.dbmodel = None
        self.logger = None
        self.systray = None

    def set_view(self, view):
        self.view = view
    
    def set_dbmodel(self, dbmodel):
        self.dbmodel = dbmodel
    
    def set_logger(self, logger):
        self.logger = logger
    
    def set_systray(self, systray):
        self.systray = systray

    def get_most_played_artists(self, limit=10, removeBlank=False):
        return self.dbmodel.get_most_played_artists(limit, removeBlank)
    
    def get_most_played_songs(self, limit=10, removeBlank=False):
        return self.dbmodel.get_most_played_songs(limit, removeBlank)
        
    def start(self):
        self.logger.start()
        self.view.start()
    
    def add_song_played(self, song, album, artist):
        self.dbmodel.add_song_played(song, album, artist)

        self.get_historial() #Actualiza el historial en la GUI
        self.get_stats() #Actualiza los stats en la GUI
    
    def print(self, msg):
        if not self.view.is_withdrawed():
            self.view.print(msg)
    
    def get_historial(self):
        hist = self.dbmodel.get_historial(limit=-1)

        if not self.view.is_withdrawed():
            self.view.set_historial(hist)
    
    def get_stats(self):
        artists = self.get_most_played_artists(limit=0, removeBlank=True)

        if not self.view.is_withdrawed():
            self.view.set_most_played_artists(artists)

        songlist = self.get_most_played_songs(limit=0, removeBlank=True)

        if not self.view.is_withdrawed():
            self.view.set_most_played_songs(songlist)

    #Obtiene los artistas y las reproducciones, y lo setea en la UI
    def get_artists(self):
        artists = self.dbmodel.get_artists()

        artists_reproductions = []
        for artist in artists:
            artists_reproductions.append(self.dbmodel.get_artist_reproductions(artist))

        if not self.view.is_withdrawed():
            self.view.set_artists(artists, artists_reproductions)
    
    #Cierra toda la aplicacion
    def app_exit(self):
        self.logger.stop()
        
        self.view.stop()

        self.systray.stop()

        print("CONTROLLER: App Exited")


    def gui_close(self):
        #Cierra la GUI
        self.view.withdraw_window()
        #Luego arranca el icono
        self.systray.start() 

    def gui_open(self):
        #Para el icono del system tray
        self.systray.stop() 
        #Abre de nuevo la GUI
        self.view.show_window()