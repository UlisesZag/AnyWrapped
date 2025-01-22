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
        
    def start(self):
        self.view.start()
        
        #Imprime las canciones mas reproducidas
        
        most_played = self.dbmodel.get_most_played_artists(limit=5, removeBlank=True)
        self.view.set_most_played_artists(most_played)
        
        most_played = self.dbmodel.get_most_played_songs(limit=5, removeBlank=True)
        self.view.set_most_played_songs(most_played)

        self.view.print("\n")

        self.logger.aimp_loop()
    
    def add_song_played(self, song, album, artist):
        self.dbmodel.add_song_played(song, album, artist)
    
    def print(self, msg):
        self.view.print(msg)