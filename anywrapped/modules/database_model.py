import sqlite3
import time
import os

'''
Modelo de la base de datos
'''

class DatabaseModel():
    def __init__(self):
        self.controller = None
        self.configfile = None

        self.dbcon = None
        self.dbcur = None

        self.global_stats = {}
    
    def set_controller(self, controller):
        self.controller = controller

    def set_configfile(self, cfgfile):
        self.configfile = cfgfile

    #Obtiene todas las bases de datos bajo el directorio dataases
    def get_databases(self):
        #Si la carpeta databases no existe la crea
        if not os.path.isdir("databases"):
            os.mkdir("databases")

        return os.listdir("databases")

    def get_database_by_index(self, index):
        databases = self.get_databases()
        return databases[index]

    #Se conecta a la base de datos
    def connect_db(self, filename = None):
        #Si la carpeta databases no existe la crea
        if not os.path.isdir("databases"):
            os.mkdir("databases")

        #check_same_thread=False es una negreada para no usar semaforos y no poner hilos de mas
        #Lo unico que escribe es el hilo del logger 
        if not filename:
            config = self.configfile.load_config()
            path = config["anywrapped"]["database"]
        else:
            path = filename

        self.dbcon = sqlite3.connect("databases/"+path, check_same_thread=False) 
        self.dbcur = self.dbcon.cursor()

        self.create_db()

    def disconnect_db(self):
        self.dbcon.close()
        self.dbcon = None
        self.dbcur = None

    #Crea la base de datos si es que no existe
    def create_db(self):
        self.dbcur.execute('''
                           CREATE TABLE IF NOT EXISTS Songs(
                           ID INTEGER PRIMARY KEY, 
                           Song varchar(255) NOT NULL, 
                           Artist varchar(255) NOT NULL, 
                           Album varchar(255) NOT NULL, 
                           Title varchar(255) NOT NULL, 
                           TimesListened int NOT NULL,
                           LastTimePlayed int 
                           );
                           ''')
        
        self.dbcur.execute( '''
                            CREATE TABLE IF NOT EXISTS Historial(
                            ID INTEGER PRIMARY KEY,
                            SongID INT NOT NULL,
                            Timestamp INT NOT NULL
                            );
                            ''')

        self.dbcon.commit() 
    
    def create_new_database(self, db):
        self.connect_db(filename=db)
        self.disconnect_db()

    def delete_database(self, db):
        if os.path.isfile("databases/"+db):
            os.remove("databases/"+db)

    def rename_database(self, oldname, newname):
        if os.path.isfile("databases/"+oldname):
            os.rename("databases/"+oldname, "databases/"+newname)

    #Agrega una cancion a la DB
    #Primero, agrega la cancion a la tabla Songs, o actualiza la cancion y le suma 1 a las reproducciones y actualiza el Timestamp
    #Segundo, agrega la cancion a la tabla Historial con su respectivo Timestamp
    def add_song_played(self, song, album, artist):
        #print("DBMODEL: ADDING PLAYED SONG . . .")
        self.connect_db()
        #Le saca las comillas para que SQL no se confunda
        song = song.replace("\"", "").replace("\'", "")
        album = album.replace("\"", "").replace("\'", "")
        artist = artist.replace("\"", "").replace("\'", "")

        #Obtiene los datos de cancion
        song_entry = self.dbcur.execute(f'''
                            SELECT Song FROM Songs WHERE Song="{artist} - {album} - {song}";
                           ''')
        
        #Si no existe crea la entrada de cancion
        if song_entry.fetchone() == None:
            self.dbcur.execute(f'''
                                INSERT INTO Songs (Song, Artist, Album, Title, TimesListened, LastTimePlayed) 
                               VALUES ("{artist} - {album} - {song}", "{artist}", "{album}", "{song}", 1, "{ int(time.time()) }");
                                ''')
        else:
            #Si existe, obtiene la cantidad de reproducciones y le suma uno
            res = self.dbcur.execute(f'''
                SELECT TimesListened FROM Songs WHERE Song=("{artist} - {album} - {song}");
                ''')
            
            times_listened = res.fetchone()[0] + 1 #La acaba de reproducir
            self.dbcur.execute(f'''
                UPDATE Songs SET TimesListened = {times_listened} WHERE Song = "{artist} - {album} - {song}";
                ''')

            #Actualiza ultima vez reproducida
            self.dbcur.execute(f'''
                UPDATE Songs SET LastTimePlayed = { int(time.time()) } WHERE Song = "{artist} - {album} - {song}";
                ''')

        #Agrega la cancion al historial
        res = self.dbcur.execute(f'''
            SELECT ID FROM Songs WHERE Song=("{artist} - {album} - {song}");
            ''')
        songid = res.fetchone()[0]
        self.dbcur.execute(f'''
            INSERT INTO Historial (SongID, Timestamp) VALUES ({songid}, { int(time.time()) });
            ''')

        self.dbcon.commit()
        self.disconnect_db()

    def get_song_by_id(self, id):
        self.connect_db()
        song = self.dbcur.execute(f'''
                                    SELECT * FROM Songs WHERE ID={id};
                                  ''').fetchone()
        self.disconnect_db()

        return song

    #Devuelve todas las canciones en la DB
    def get_songs_entries(self):
        self.connect_db()
        self.dbcur.execute('''
                            SELECT * FROM Songs
                           ''')
        entries = self.dbcur.fetchall()
        self.disconnect_db()
        return entries
    
    #Devuelve todos los artistas en la DB
    def get_artists(self):
        artists = []
        for entry in self.get_songs_entries():
            if not entry[2] in artists:
                artists.append(entry[2])

        return artists

    #Devuelve todas las reproducciones de toda la DB
    def get_total_reproductions(self):
        total_reps = 0
        for entry in self.get_songs_entries():
            total_reps += entry[5]
        
        return total_reps

    #Devuelve todas las reproducciones de un artista
    def get_artist_reproductions(self, artist):
        reps = 0
        for entry in self.get_songs_entries():
            if entry[2] == artist:
                reps += entry[5]
        
        return reps
    
    #Devuelve todas las reproducciones de un album
    def get_album_reproductions(self, artist, album):
        reps = 0
        for entry in self.get_songs_entries():
            if entry[2] == artist and entry[3] == album:
                reps += entry[5]
        
        return reps
    
    #Devuelve todas las reproducciones de una cancion
    def get_song_reproductions(self, artist, album, title):
        reps = 0
        for entry in self.get_songs_entries():
            if entry[2] == artist and entry[3] == album and entry[4] == title:
                reps += entry[5]
        
        return reps
    
    def get_most_played_songs(self, limit = 10, removeBlank = False):
        '''
        Obtiene las canciones mas reproducidos
        limit: devuelve los primeros [limit] mas escuchados
        removeBlank: saca las canciones sin nombre ("") de la lista
        '''
        songs = self.get_songs_entries()
        songs.sort(key=lambda tup: tup[5], reverse=True)

        if limit != 0:
            return songs[0:limit]
        else:
            return songs

    def get_most_played_artists(self, limit = 10, removeBlank = False):
        '''
        Obtiene los artistas mas reproducidos
        limit: devuelve los primeros [limit] mas escuchados
        removeBlank: saca los artistas sin nombre ("") de la lista
        '''
        artists_reps = []

        for artist in self.get_artists():
            if removeBlank and artist == "":
                continue

            artists_reps.append(
                (artist, self.get_artist_reproductions(artist))
            )

        artists_reps.sort(key=lambda tup: tup[1], reverse=True)
        
        if limit != 0:
            return artists_reps[0:limit]
        else:
            return artists_reps

    #Obtiene la tabla del historial
    def get_historial_table(self, limit = 0):
        self.connect_db()
        list_historial = self.dbcur.execute(f'''
                            SELECT * FROM Historial;
                           ''').fetchall()
        self.disconnect_db()
        
        return list_historial

    
    #La funcion invierte la tabla de la DB para que los mas recientes sean los primeros en la lista
    #limit: obtiene los primeros [limit] del historial
    def get_historial(self, limit = 0):
        hist = []
        #Obtiene la tabla, la invierte y luego la corta a limite
        if limit != 0:
            histlist = list(reversed(self.get_historial_table()))[0:limit]
        else:
            histlist = list(reversed(self.get_historial_table()))

        #Cada entry tiene un: ROWID, ID de la cancion, Timestamp de vez reproducida
        for entry in histlist:
            song = self.get_song_by_id(entry[1])
            hist.append([song, entry[2]]) #Appendea los datos de SONG + el timestamp del historial
        
        return hist