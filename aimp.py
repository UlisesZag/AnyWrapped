import pyaimp
import time

SLEEP_INTERVAL = 0.5

class AIMPLogger():
    def __init__(self):
        pass

    def set_controller(self, dbcontroller):
        self.dbmodel = dbcontroller
    
    #Funcion que espera una instancia de 
    def wait_aimp(self):
        client = None

        #Espera a una instancia de AIMP
        while True:
            try:
                client = pyaimp.Client()
                break
            except RuntimeError as re: # AIMP instance not found
                time.sleep(SLEEP_INTERVAL) #Pausa por SLEEP_INTERVAL segundos
        
        return client

    def aimp_loop(self):
        print("Searching AIMP instance...")

        client = self.wait_aimp()

        print(f"Found: AIMP {client.get_version()[0]}")

        #Loop principal
        while True:
            #AIMP sigue abierto?
            try:
                client.detect_aimp()
            except RuntimeError:
                break

            time.sleep(SLEEP_INTERVAL) #Pausa por SLEEP_INTERVAL segundos

            playback_state = client.get_playback_state() #Reproduciendo/Pausado/Detenido
            track_info = {}

            if playback_state == pyaimp.PlayBackState.Stopped:
                print("No track being played")
            else: 
                old_track_info = track_info
                track_info = client.get_current_track_info()

                #Pausado o Reproduciendo?
                str_state = "[Paused]" if playback_state == pyaimp.PlayBackState.Paused else "[Playing]"

                #Acaba de empezar?
                just_started = client.get_player_position() <= SLEEP_INTERVAL * 1100 and playback_state == pyaimp.PlayBackState.Playing
                song_changed = old_track_info == track_info


                #Aca haria toda la parte del registro. 
                if just_started or song_changed:
                    print(f"{str_state} { track_info["artist"] } - { track_info["album"] } - { track_info["title"] }")
                    self.dbmodel.add_song_played(track_info["title"],track_info["album"],track_info["artist"])
        
        print("AIMP Apagado")