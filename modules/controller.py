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
        self.view.print(f"PLAYING: {artist} - {album} - {song}")
        self.dbmodel.add_song_played(song, album, artist)
    
    def print(self, msg):
        self.view.print(msg)
    
    def get_historial(self):
        hist = self.dbmodel.get_historial(limit=20)
        self.view.set_historial(hist)
    
    def app_exit(self):
        self.logger.stop()
        sys.exit()