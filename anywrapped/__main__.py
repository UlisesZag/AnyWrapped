'''
Any Wrapped

Estadisticas para reproductores de audio alternativos

Reproductores soportados:
AIMP
'''

import anywrapped.modules.aimp as aimp
import anywrapped.modules.database_model as database_model
import anywrapped.modules.ui as ui
import anywrapped.modules.controller as controller
import anywrapped.modules.systray as systray
import anywrapped.modules.configfile as configfile
import pywintypes
from tkinter.messagebox import showerror

def main():
    # execute only if run as the entry point into the program
    try:
        app_controller = controller.AppController()
        logger = aimp.AIMPLogger()
        dbmodel = database_model.DatabaseModel()
        gui = ui.TkApp()
        stray = systray.SystemTrayIcon()
        cfgfile = configfile.ConfigFile()

        app_controller.set_dbmodel(dbmodel)
        app_controller.set_view(gui)
        app_controller.set_logger(logger)
        app_controller.set_systray(stray)
        app_controller.set_configfile(cfgfile)

        logger.set_controller(app_controller)
        dbmodel.set_controller(app_controller)
        gui.set_controller(app_controller)
        stray.set_controller(app_controller)

        dbmodel.set_configfile(cfgfile)

        app_controller.start()
    except PermissionError or pywintypes.error:
        showerror("Permission Error", "Script was executed without enough permissions. Try running as an administrator.")

#La idea es que haya un objeto de logger por software reproductor, que se conecte al modelo de DB 
if __name__ == '__main__':
    main()