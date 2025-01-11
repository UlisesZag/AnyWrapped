'''
Any Wrapped

Estadisticas para reproductores de audio alternativos

Reproductores soportados:
AIMP
'''

import aimp
import database_model


#La idea es que haya un objeto de logger por software reproductor, que se conecte al modelo de DB 
if __name__ == "__main__":
    logger = aimp.AIMPLogger()
    
    dbmodel = database_model.DatabaseModel()
    dbmodel.connect_db()

    #Testeo de la DB
    print("DATABASE:")
    for entry in dbmodel.get_songs_entries():
        print(entry)
    
    print("ARTISTS - REPRODUCTIONS:")
    for entry in dbmodel.get_artists():
        print(entry, "-", dbmodel.get_artist_reproductions(entry))

    print(f"Total Reproductions: {dbmodel.get_total_reproductions()}")

    logger.set_controller(dbmodel)

    logger.aimp_loop()