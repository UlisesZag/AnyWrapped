import sys

class AppController():
    def __init__(self):
        self.view = None
        self.dbmodel = None
        self.logger = None

    def set_view(self, view):
        self.view = view
    
    def set_dbmodel(self, dbmodel):
        self.dbmodel = dbmodel
    
    def set_logger(self, logger):
        self.logger = logger

    def get_most_played_artists(self, limit=10, removeBlank=False):
        return self.dbmodel.get_most_played_artists(limit, removeBlank)
    
    def get_most_played_songs(self, limit=10, removeBlank=False):
        return self.dbmodel.get_most_played_songs(limit, removeBlank)
        
    def start(self):
        self.logger.start()

        self.view.start()

        self.view.print("\n")
    
    def add_song_played(self, song, album, artist):
        #self.view.print(f"PLAYING: {artist} - {album} - {song}\n")
        self.dbmodel.add_song_played(song, album, artist)

        self.get_historial() #Actualiza el historial en la GUI
        self.get_stats() #Actualiza los stats en la GUI
    
    def print(self, msg):
        self.view.print(msg)
    
    def get_historial(self):
        hist = self.dbmodel.get_historial(limit=-1)
        self.view.set_historial(hist)
    
    def get_stats(self):
        artists = self.get_most_played_artists(limit=10, removeBlank=True)
        self.view.set_most_played_artists(artists)

        songlist = self.get_most_played_songs(limit=10, removeBlank=True)
        self.view.set_most_played_songs(songlist)

    #Obtiene los artistas y las reproducciones, y lo setea en la UI
    def get_artists(self):
        artists = self.dbmodel.get_artists()

        artists_reproductions = []
        for artist in artists:
            artists_reproductions.append(self.dbmodel.get_artist_reproductions(artist))

        self.view.set_artists(artists, artists_reproductions)
    
    #Cierra toda la aplicacion
    def app_exit(self):
        self.logger.stop()
        sys.exit()