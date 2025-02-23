import os
import json
import time

#Objeto que maneja el archivo de configuracion
class ConfigFile:
    def __init__(self):
        self.controller = None

        self.config_rw = False # Flag para evitar errores de multithreading

    #Crea una nueva configuracion
    def new_config(self):
        config = {
            "anywrapped": {
                "database": "stats.db",
                "logger": "AIMP"
            },
            "AIMP": {
                "detection_treshold_seconds": 10
            }
        }

        return config

    #Carga la configuracion desde un archivo config.cfg
    def load_config(self):
        while self.config_rw:
            time.sleep(0.1)

        self.config_rw = True #Bloquea la apertura del archivo

        #Crea un archivo nuevo si no existe
        if not os.path.exists("config.cfg"):
            config = self.new_configfile()
            with open("config.cfg", "w") as fp:
                json.dump(config, fp)

        #Carga el archivo
        config = {}
        with open("config.cfg") as fp:
            config = json.load(fp)

        self.config_rw = False #Desbloquea la apertura del archivo
        
        #Retorna el config
        return config

    #Escribe la configuracion en un archivo config.cfg
    def save_config(self, config):
        while self.config_rw:
            time.sleep(0.1)

        self.config_rw = True #Bloquea la apertura del archivo

        #Guarda el archivo
        with open("config.cfg", "w") as fp:
            json.dump(config, fp)

        self.config_rw = False #Desbloquea la apertura del archivo