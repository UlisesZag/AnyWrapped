import anywrapped.modules.aimp as aimp
import time

#Controlador que cambia entre distintos loggers
class LoggerSwitch:
    def __init__(self, controller = None):
        self.loggers = {
            "None": None,
            "AIMP": aimp.AIMPLogger(controller=self)
        }
        self.active_logger = None
        self.controller = controller

    def set_controller(self, controller):
        self.controller = controller

    #Que loggers hay en el LoggerSwitch?
    def get_loggers(self):
        return list(self.loggers.keys())

    #Para el logger actual y corre otro logger
    def change_logger(self, logger:str):
        #Si hay un logger lo para
        if self.active_logger:
            self.active_logger.stop()

            #Queda bucleando hasta que el hilo se para por completo.
            while self.active_logger.is_thread_alive():
                time.sleep(0.001)
        
        #Luego prende el nuevo logger
        self.active_logger = self.loggers[logger]
        if self.active_logger:
            self.active_logger.start()
    
    #Funciones que se las pasa a controller
    
    def add_song_played(self, title, album, artist):
        self.controller.add_song_played(title, album, artist)

    def ui_set_media_player(self, media_player):
        self.controller.ui_set_media_player(media_player)

    def print(self, message):
        self.controller.print(message)

    def stop(self):
        self.active_logger.stop()