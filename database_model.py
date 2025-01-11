import sqlite3

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
                           TimesListened int NOT NULL
                           );
                           ''')

        self.dbcon.commit() 
    
    def add_song_played(self, song, album, artist):
        #Obtiene los datos de cancion
        song_entry = self.dbcur.execute(f'''
                            SELECT Song FROM Songs WHERE Song="{artist} - {album} - {song}";
                           ''')
        
        #Si no existe crea la entrada de cancion
        if song_entry.fetchone() == None:
            self.dbcur.execute(f'''
                                INSERT INTO Songs (Song, Artist, Album, Title, TimesListened) 
                               VALUES ("{artist} - {album} - {song}", "{artist}", "{album}", "{song}", 1);
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

        self.dbcon.commit()

    def add_song_time(self, song, album, artist):
        pass

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