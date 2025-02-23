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
AIMPLOGGER_AIMPDETECTED="aimploggerthread_aimpdetected"

DETECTION_TRESHOLD = 10

class AIMPLoggerThread():
    def __init__(self):
        self.stop_flag = False
        dispatcher.connect(self.on_stop_request, signal=AIMPLOGGERTHREAD_STOP, sender=AIMPLOGGER_SENDER)

        self.logger_loop()

    def logger_loop(self):
        while True:
            #Busca una instancia de AIMP
            dispatcher.send(message="Searching AIMP instance...", signal=AIMPLOGGER_PRINT_SIGNAL, sender=AIMPLOGGERTHREAD_SENDER)

            client = self.wait_aimp()

            if client:
                dispatcher.send(message=f"Found: AIMP {client.get_version()[0]}", signal=AIMPLOGGER_PRINT_SIGNAL, sender=AIMPLOGGERTHREAD_SENDER)
                dispatcher.send(media_player = f"AIMP {client.get_version()[0]}", signal=AIMPLOGGER_AIMPDETECTED, sender=AIMPLOGGERTHREAD_SENDER)
            else:
                break

            if self.stop_flag:
                break

            #Loggea AIMP
            self.aimp_loop_thread(client)

            if self.stop_flag:
                break

            #dispatcher.send(message="AIMP Apagado", signal=AIMPLOGGER_PRINT_SIGNAL, sender=AIMPLOGGERTHREAD_SENDER)
            #Si la app quiere mandar un mensaje de dispatcher mientras el logger se cierra la app se congela?
            #Mientras se cierra el logger en la funcion stop llama a la funcion aimp_detected para no usar el dispatcher 
            dispatcher.send(media_player = "", signal=AIMPLOGGER_AIMPDETECTED, sender=AIMPLOGGERTHREAD_SENDER)

            #Cuando el AIMP se apague lo vuelve a buscar
        

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
    
    def aimp_loop_thread(self, client):
        #Compara un dict track_info con otro dict old_track_info para saber si la cancion fue cambiada
        track_info = {}
        old_track_info = {}
        #La cancion debe reproducirse hasta pasar el umbral de deteccion, y ahi se detectara y se sumara.
        detection_treshold_passed = True

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

            if playback_state == pyaimp.PlayBackState.Stopped:
                #print("No track being played")
                pass
            else: 
                old_track_info = track_info
                track_info = client.get_current_track_info()

                #Acaba de empezar?
                below_detection_treshold = (client.get_player_position() <= DETECTION_TRESHOLD * 1000) and (playback_state == pyaimp.PlayBackState.Playing)
                above_detection_treshold = (client.get_player_position() > DETECTION_TRESHOLD * 1000) and (playback_state == pyaimp.PlayBackState.Playing)
                song_changed = old_track_info != track_info

                #Aca haria toda la parte del registro. 
                #Si la cancion cambia activa el umbral de deteccion
                if song_changed:
                    detection_treshold_passed = False

                #Si esta bajo el umbral de deteccion lo activa (ponele que se reinicia la cancion)
                if below_detection_treshold:
                    detection_treshold_passed = False
                
                #Si el umbral esta activado y lo pasa, el umbral se desactiva, y registra la cancion sonando
                if above_detection_treshold and not detection_treshold_passed:
                    detection_treshold_passed = True
                    dispatcher.send(track_info=track_info, signal=AIMPLOGGER_ADDSONG_SIGNAL, sender=AIMPLOGGERTHREAD_SENDER)
        
    #
    def on_stop_request(self):
        self.stop_flag = True

class AIMPLogger():
    def __init__(self, controller = None):
        self.controller = controller
        self.started = False
        dispatcher.connect(self.add_song_played_received, signal=AIMPLOGGER_ADDSONG_SIGNAL, sender=AIMPLOGGERTHREAD_SENDER)
        dispatcher.connect(self.print_received, signal=AIMPLOGGER_PRINT_SIGNAL, sender=AIMPLOGGERTHREAD_SENDER)
        dispatcher.connect(self.aimp_detected, signal=AIMPLOGGER_AIMPDETECTED, sender=AIMPLOGGERTHREAD_SENDER)

    def set_controller(self, controller):
        self.controller = controller

    def start(self):
        if not self.started:
            self.started = True
            self.thread = threading.Thread(target=AIMPLoggerThread)
            self.thread.start()
            print("AIMPLogger: Started.")
    
    def stop(self):
        if self.started:
            self.started = False
            dispatcher.send(signal=AIMPLOGGERTHREAD_STOP, sender=AIMPLOGGER_SENDER)
            self.aimp_detected("") #Pone el reproductor detectado en None
            print("AIMPLogger: Stopped.")

    def is_thread_alive(self):
        return self.thread.is_alive()
    
    def add_song_played_received(self, track_info):
        #print("AIMPLogger: ADD SONG PLAYED RECIBIDO")
        self.controller.add_song_played(track_info["title"],track_info["album"],track_info["artist"])

    def aimp_detected(self, media_player):
        self.controller.ui_set_media_player(media_player)
        
    def print_received(self, message):
        self.controller.print(message)