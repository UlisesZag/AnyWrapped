import pystray
import threading
from PIL import Image

#Clase para el manejador del system tray
class SystemTrayIcon():
    def __init__(self):
        self.icon = None
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def is_running(self):
        return self.icon._running

    def start(self):
        image = Image.open("assets/strayico.ico")
        menu = (pystray.MenuItem("AnyWrapped", None),
                pystray.MenuItem('Open GUI', self.open_gui),
                pystray.MenuItem('Exit Program',self.app_exit))
        self.icon = pystray.Icon("AnyWrapped v0.1", image, "AnyWrapped v0.1", menu)

        self.icon.run()
    
    def stop(self):
        self.icon.stop()
        print("SYSTRAY: Stopped")
    
    def open_gui(self):
        self.icon.stop()
        self.controller.ui_open()
    
    def app_exit(self):
        self.controller.app_exit()
        
    def icon_loop(self, icon):
        icon.visible = True