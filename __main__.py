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
    print("===== [TOP MOST PLAYED ARTISTS] =====")
    for i, entry in enumerate(dbmodel.get_most_played_artists(removeBlank=True)):
        print(i+1, entry[0], "- Times played:", entry[1])

    print("\n=====  [TOP MOST PLAYED SONGS]  =====")
    for i, entry in enumerate(dbmodel.get_most_played_songs(removeBlank=True)):
        print(i+1, entry[2], "-", entry[3], "-", entry[4], "- Times played:", entry[5])

    print(f"\nTotal Reproductions: {dbmodel.get_total_reproductions()}\n")

    logger.set_controller(dbmodel)

    logger.aimp_loop()