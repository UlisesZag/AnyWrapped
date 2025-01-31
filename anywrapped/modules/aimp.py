import pyaimp
import time
import threading
from pydispatch import dispatcher

SLEEP_INTERVAL = 0.5

AIMPLOGGER_SENDER="aimplogger_sender"
AIMPLOGGER_PRINT_SIGNAL="aimplogger_print_signal"
AIMPLOGGER_ADDSONG_SIGNAL="aimplogger_addsong_signal"

AIMPLOGGERTHREAD_SENDER="aimplogger_sender"
AIMPLOGGERTHREAD_PRINT_SIGNAL="aimplogger_print_signal"
AIMPLOGGERTHREAD_ADDSONG_SIGNAL="aimplogger_addsong_signal"
AIMPLOGGERTHREAD_STOP="aimplogger_stop"


class AIMPLoggerThread():
    def __init__(self):
        self.stop_flag = False
        dispatcher.connect(self.on_stop_request, signal=AIMPLOGGERTHREAD_STOP, sender=AIMPLOGGER_SENDER)

        self.aimp_loop_thread()

    #Funcion que espera una instancia de AIMP y devuelve el cliente
    def wait_aimp(self):
        client = None

        #Espera a una instancia de AIMP
        while True:
            #Request de parar?
            if self.stop_flag:
                break

            try:
                client = pyaimp.Client()
                break
            except RuntimeError as re: # AIMP instance not found
                time.sleep(SLEEP_INTERVAL) #Pausa por SLEEP_INTERVAL segundos
        
        return client
    
    def aimp_loop_thread(self):
        dispatcher.send(message="Searching AIMP instance...", signal=AIMPLOGGER_PRINT_SIGNAL, sender=AIMPLOGGERTHREAD_SENDER)

        client = self.wait_aimp()

        if client:
            dispatcher.send(message=f"Found: AIMP {client.get_version()[0]}", signal=AIMPLOGGER_PRINT_SIGNAL, sender=AIMPLOGGERTHREAD_SENDER)

        #Loop principal
        while True:
            #Request de parar?
            if self.stop_flag:
                break

            #AIMP sigue abierto?
            try:
                client.detect_aimp()
            except RuntimeError:
                break

            time.sleep(SLEEP_INTERVAL) #Pausa por SLEEP_INTERVAL segundos

            playback_state = client.get_playback_state() #Reproduciendo/Pausado/Detenido
            track_info = {}

            if playback_state == pyaimp.PlayBackState.Stopped:
                #print("No track being played")
                pass
            else: 
                old_track_info = track_info
                track_info = client.get_current_track_info()

                #Pausado o Reproduciendo?
                str_state = "[Paused]" if playback_state == pyaimp.PlayBackState.Paused else "[Playing]"

                #Acaba de empezar?
                just_started = client.get_player_position() <= SLEEP_INTERVAL * 1200 and playback_state == pyaimp.PlayBackState.Playing
                song_changed = old_track_info == track_info

                #Aca haria toda la parte del registro. 
                if just_started or song_changed:
                    #print("AIMPLoggerThread: ADD SONG PLAYED ENVIADO")
                    dispatcher.send(track_info=track_info, signal=AIMPLOGGER_ADDSONG_SIGNAL, sender=AIMPLOGGERTHREAD_SENDER)
        
        dispatcher.send(message="AIMP Apagado", signal=AIMPLOGGER_PRINT_SIGNAL, sender=AIMPLOGGERTHREAD_SENDER)
    
    #
    def on_stop_request(self):
        self.stop_flag = True

class AIMPLogger():
    def __init__(self):
        dispatcher.connect(self.add_song_played_received, signal=AIMPLOGGER_ADDSONG_SIGNAL, sender=AIMPLOGGERTHREAD_SENDER)
        dispatcher.connect(self.print_received, signal=AIMPLOGGER_PRINT_SIGNAL, sender=AIMPLOGGERTHREAD_SENDER)

    def set_controller(self, controller):
        self.controller = controller

    def start(self):
        self.thread = threading.Thread(target=AIMPLoggerThread)
        self.thread.start()
    
    def stop(self):
        dispatcher.send(signal=AIMPLOGGERTHREAD_STOP, sender=AIMPLOGGER_SENDER)
        print("LOGGER: Stopped")
    
    def add_song_played_received(self, track_info):
        #print("AIMPLogger: ADD SONG PLAYED RECIBIDO")
        self.controller.add_song_played(track_info["title"],track_info["album"],track_info["artist"])

    def print_received(self, message):
        self.controller.print(message)