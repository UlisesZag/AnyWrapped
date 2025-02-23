import sys
import anywrapped.modules.ui as ui

class AppController():
    def __init__(self):
        self.view = None
        self.dbmodel = None
        self.logger = None
        self.systray = None
        self.configfile = None

    ################## CONEXIONES ###########################

    def set_view(self, view):
        self.view = view
    
    def set_dbmodel(self, dbmodel):
        self.dbmodel = dbmodel
    
    def set_logger(self, logger):
        self.logger = logger
    
    def set_systray(self, systray):
        self.systray = systray

    def set_configfile(self, configfile):
        self.configfile = configfile

    def start(self):
        config = self.configfile.load_config()
        self.ui_set_selected_logger(config["anywrapped"]["logger"])
        self.logger.change_logger(config["anywrapped"]["logger"])
        self.view.start()
    
    ############### DBMODEL ##########################
    def get_most_played_artists(self, limit=10, removeBlank=False):
        return self.dbmodel.get_most_played_artists(limit, removeBlank)
    
    def get_most_played_songs(self, limit=10, removeBlank=False):
        return self.dbmodel.get_most_played_songs(limit, removeBlank)

    def add_song_played(self, song, album, artist):
        self.dbmodel.add_song_played(song, album, artist)

        self.ui_get_historial() #Actualiza el historial en la GUI
        self.ui_get_stats() #Actualiza los stats en la GUI
    
    ################### UI ##############################

    def print(self, msg: str):
        if not self.view.is_withdrawed():
            self.view.print(msg)
    
    def ui_get_historial(self):
        hist = self.dbmodel.get_historial(limit=0)

        if not self.view.is_withdrawed():
            self.view.set_historial(hist)
    
    def ui_get_stats(self):
        artists = self.get_most_played_artists(limit=0, removeBlank=True)

        if not self.view.is_withdrawed():
            self.view.set_most_played_artists(artists)

        songlist = self.get_most_played_songs(limit=0, removeBlank=True)

        if not self.view.is_withdrawed():
            self.view.set_most_played_songs(songlist)

    def ui_get_config(self):
        #Obtiene la configuracion
        config = self.configfile.load_config()
        databases = self.dbmodel.get_databases()
        self.view.set_config(config, databases)
    
    def ui_get_loggers(self):
        #Obtiene los loggers disponibles
        loggers = self.logger.get_loggers()
        self.view.set_loggers(loggers)

    #De logger a UI, setea que reproductor esta ejecutandose
    def ui_set_media_player(self, media_player: str):
        self.view.set_media_player(media_player)

    #Actualiza el logger seleccionado
    def ui_set_selected_logger(self, logger):
        self.view.set_selected_logger(logger)

    #Obtiene los artistas y las reproducciones, y lo setea en la UI
    def get_artists(self):
        artists = self.dbmodel.get_artists()

        artists_reproductions = []
        for artist in artists:
            artists_reproductions.append(self.dbmodel.get_artist_reproductions(artist))

        if not self.view.is_withdrawed():
            self.view.set_artists(artists, artists_reproductions)

    def ui_close(self):
        #Cierra la GUI
        self.view.withdraw_window()
        #Luego arranca el icono
        self.systray.start() 

    def ui_open(self):
        #Para el icono del system tray
        self.systray.stop() 
        #Abre de nuevo la GUI
        self.view.show_window()
    
    ########################### CONFIGFILE ##################################
    def cfg_database_selected(self, db):
        #De la configuracion de la UI, lo guarda en el configfile
        config = self.configfile.load_config()
        config["anywrapped"]["database"] = db
        self.configfile.save_config(config)

        #Luego actualiza todas las demas tablas, etc
        self.ui_get_historial()
        self.ui_get_stats()
        self.ui_get_config()

    #Crea una nueva base de datos
    def cfg_add_database(self, db: str):
        self.dbmodel.create_new_database(db)
        self.cfg_database_selected(db)

    def cfg_delete_database(self, db: str):
        databases = self.dbmodel.get_databases()
        db_index = databases.index(db)

        self.dbmodel.delete_database(db)
        #Actualiza la lista de databases
        databases = self.dbmodel.get_databases()

        #Si el indice de la db es mayor a la cantidad de dbs lo acomoda al ultimo
        if len(databases)-1 < db_index:
            db_index -= 1
        
        #NO HAY MAS DATABASES???? crea uno por default
        if len(databases) == 0:
            db_index = 0
            self.cfg_add_database("stats.db")

        #Que db tengo que poner ahora?
        newdb = self.dbmodel.get_database_by_index(db_index)

        self.cfg_database_selected(newdb)

    def cfg_rename_database(self, oldname: str, newname: str):
        self.dbmodel.rename_database(oldname, newname)
        self.cfg_database_selected(newname)

    def cfg_logger_selected(self, logger):
        self.logger.change_logger(logger)
        config = self.configfile.load_config()
        config["anywrapped"]["logger"] = logger
        self.configfile.save_config(config)
    

    #Cierra toda la aplicacion
    def app_exit(self):
        self.logger.stop()
        
        self.view.stop()

        self.systray.stop()

        print("CONTROLLER: App Exited")

    