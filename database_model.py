import sqlite3
import time

class DatabaseModel():
    def __init__(self):
        self.dbcon = None
        self.dbcur = None

        self.global_stats = {}

    #Se conecta a la base de datos
    def connect_db(self):
        self.dbcon = sqlite3.connect("stats.db")
        self.dbcur = self.dbcon.cursor()

        self.create_db()

    #Base de datos vacia? La crea
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
    
    def add_song_played(self, song, album, artist):
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

    def get_songs_entries(self):
        self.dbcur.execute('''
                            SELECT * FROM Songs
                           ''')
        entries = self.dbcur.fetchall()
        return entries

    def get_total_reproductions(self):
        total_reps = 0
        for entry in self.get_songs_entries():
            total_reps += entry[5]
        
        return total_reps

    def get_artist_reproductions(self, artist):
        reps = 0
        for entry in self.get_songs_entries():
            if entry[2] == artist:
                reps += entry[5]
        
        return reps
    
    def get_album_reproductions(self, artist, album):
        reps = 0
        for entry in self.get_songs_entries():
            if entry[2] == artist and entry[3] == album:
                reps += entry[5]
        
        return reps
    
    def get_song_reproductions(self, artist, album, title):
        reps = 0
        for entry in self.get_songs_entries():
            if entry[2] == artist and entry[3] == album and entry[4] == title:
                reps += entry[5]
        
        return reps
    
    def get_artists(self):
        artists = []
        for entry in self.get_songs_entries():
            if not entry[2] in artists:
                artists.append(entry[2])

        return artists
    
    def get_most_played_songs(self, limit = 10, removeBlank = False):
        songs = self.get_songs_entries()
        songs.sort(key=lambda tup: tup[5], reverse=True)
        return songs[0:limit]

    def get_most_played_artists(self, limit = 10, removeBlank = False):
        artists_reps = []

        for artist in self.get_artists():
            if removeBlank and artist == "":
                continue

            artists_reps.append(
                (artist, self.get_artist_reproductions(artist))
            )

        artists_reps.sort(key=lambda tup: tup[1], reverse=True)
        
        return artists_reps[0:limit]
