import io
import sqlite3
import requests
import urllib.parse
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pydub import AudioSegment
import random
import os

# --- INICJALIZACJA BAZY DANYCH ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS songs")
    # Dodaliśmy kolumnę 'category'
    cursor.execute('''
        CREATE TABLE songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT,
            title TEXT,
            search_query TEXT,
            category TEXT
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM songs")
    if cursor.fetchone()[0] == 0:
        # Polskie piosenki z podziałem na kategorie
       # Gigantyczna baza polskich piosenek (prawie 100 utworów)
        # Gigantyczna baza polskich piosenek (blisko 300 utworów)
        sample_songs = [
            # --- HIP-HOP ---
            ("Taco Hemingway", "Deszcz na betonie", "taco hemingway deszcz na betonie", "hiphop"),
            ("Taco Hemingway", "Fifi Hollywood", "taco hemingway fifi hollywood", "hiphop"),
            ("Taco Hemingway", "Polskie Tango", "taco hemingway polskie tango", "hiphop"),
            ("Paktofonika", "Jestem Bogiem", "paktofonika jestem bogiem", "hiphop"),
            ("Paktofonika", "Chwile ulotne", "paktofonika chwile ulotne", "hiphop"),
            ("Mata", "Patointeligencja", "mata patointeligencja", "hiphop"),
            ("Mata", "Kiss cam", "mata kiss cam", "hiphop"),
            ("Mata", "Schodki", "mata schodki", "hiphop"),
            ("Quebonafide", "Candy", "quebonafide candy", "hiphop"),
            ("Quebonafide", "Bubbletea", "quebonafide bubbletea", "hiphop"),
            ("Quebonafide", "Half dead", "quebonafide half dead", "hiphop"),
            ("PRO8L3M", "Flary", "pro8l3m flary", "hiphop"),
            ("PRO8L3M", "Molly", "pro8l3m molly", "hiphop"),
            ("PRO8L3M", "Interpol", "pro8l3m interpol", "hiphop"),
            ("Sokół", "Chcemy być wyżej", "sokol chcemy byc wyzej", "hiphop"),
            ("White 2115", "California", "white 2115 california", "hiphop"),
            ("White 2115", "RiRi", "white 2115 riri", "hiphop"),
            ("O.S.T.R.", "Lubię być sam", "ostr lubie byc sam", "hiphop"),
            ("O.S.T.R.", "Mówiłaś mi", "ostr mowilas mi", "hiphop"),
            ("Kizo", "Disney", "kizo disney", "hiphop"),
            ("Kizo", "Hero", "kizo hero", "hiphop"),
            ("Kabe", "Nad ranem", "kabe nad ranem", "hiphop"),
            ("Pezet", "Gdyby miało nie być jutra", "pezet gdyby mialo nie byc jutra", "hiphop"),
            ("Pezet", "Ukryty w mieście krzyk", "pezet ukryty w miescie krzyk", "hiphop"),
            ("Pezet", "Magenta", "pezet magenta", "hiphop"),
            ("Tede", "Wielkie Joł", "tede wielkie jol", "hiphop"),
            ("Tede", "Drin za drinem", "tede drin za drinem", "hiphop"),
            ("WWO", "Każdy ponad każdym", "wwo kazdy ponad kazdym", "hiphop"),
            ("WWO", "Mogę wszystko", "wwo moge wszystko", "hiphop"),
            ("WWO", "Sen", "wwo sen", "hiphop"),
            ("Kaliber 44", "Plus i minus", "kaliber 44 plus i minus", "hiphop"),
            ("Kaliber 44", "Film", "kaliber 44 film", "hiphop"),
            ("Hemp Gru", "Droga", "hemp gru droga", "hiphop"),
            ("Hemp Gru", "Klucz", "hemp gru klucz", "hiphop"),
            ("GrubSon", "Na szczycie", "grubson na szczycie", "hiphop"),
            ("GrubSon", "Naprawimy to", "grubson naprawimy to", "hiphop"),
            ("Paluch", "Szaman", "paluch szaman", "hiphop"),
            ("Paluch", "Gdybyś kiedyś", "paluch gdys kiedys", "hiphop"),
            ("Szpaku", "UFO", "szpaku ufo", "hiphop"),
            ("Szpaku", "Hinata", "szpaku hinata", "hiphop"),
            ("Bedoes 2115", "Opowieści z Doliny Smoków", "bedoes opowiesci z doliny smokow", "hiphop"),
            ("Bedoes 2115", "Eldorado", "bedoes eldorado", "hiphop"),
            ("Żabson", "Kush", "zabson kush", "hiphop"),
            ("Żabson", "DMT", "zabson dmt", "hiphop"),
            ("Oki", "Jeżyk!", "oki jezyk", "hiphop"),
            ("Oki", "Siri", "oki siri", "hiphop"),
            ("Kukon", "Ogrodowa", "kukon ogrodowa", "hiphop"),
            ("Malik Montana", "Jagodzianki", "malik montana jagodzianki", "hiphop"),
            ("Malik Montana", "Do tańca", "malik montana do tanca", "hiphop"),
            ("ReTo", "Billy Kid", "reto billy kid", "hiphop"),
            ("ReTo", "Papierosy", "reto papierosy", "hiphop"),
            ("Kinny Zimmer", "Rozmazana kreska", "kinny zimmer rozmazana kreska", "hiphop"),
            ("Guzior", "Fala", "guzior fala", "hiphop"),
            ("Guzior", "Blueberry", "guzior blueberry", "hiphop"),
            ("Tymek", "Język Ciała", "tymek jezyk ciala", "hiphop"),
            ("Tymek", "Rainman", "tymek rainman", "hiphop"),
            ("KęKę", "Smutek", "keke smutek", "hiphop"),
            ("KęKę", "Wyjebane", "keke wyjebane", "hiphop"),
            ("Ten Typ Mes", "L.O.V.E.", "ten typ mes love", "hiphop"),
            ("Słoń", "Love Forever", "slon love forever", "hiphop"),
            ("Chivas", "Narcyz", "chivas narcyz", "hiphop"),
            ("Slums Attack", "Głucha noc", "slums attack glucha noc", "hiphop"),
            ("Molesta Ewenement", "Wiedziałem, że tak będzie", "molesta wiedzialem ze tak bedzie", "hiphop"),
            ("Zeus", "Hipotermia", "zeus hipotermia", "hiphop"),
            ("Avi", "Toast", "avi toast", "hiphop"),
            ("Białas", "Bliźniaczki", "bialas blizniaczki", "hiphop"),
            ("Szpaku", "Gugu", "szpaku gugu", "hiphop"),
            ("Kizo", "Pogo", "kizo pogo", "hiphop"),
            ("Sobel", "Fiołkowe pole", "sobel fiolkowe pole", "hiphop"),
            ("Sobel", "Impreza", "sobel impreza", "hiphop"),
            ("Young Igi", "Bestia", "young igi bestia", "hiphop"),
            ("Żabson", "Incepcja", "zabson incepcja", "hiphop"),
            ("O.S.T.R.", "Spuchnięte miasto", "ostr spuchniete miasto", "hiphop"),
            ("Donguralesko", "Chcę ci dać", "donguralesko chce ci dac", "hiphop"),
            ("Trzeci Wymiar", "Dla mnie masz stajla", "trzeci wymiar dla mnie masz stajla", "hiphop"),
            ("Jeden Osiem L", "Jak zapomnieć", "jeden osiem l jak zapomniec", "hiphop"),
            ("Mezo", "Sacrum", "mezo sacrum", "hiphop"),
            ("Liber", "Skarby", "liber skarby", "hiphop"),
            ("Buka", "Orchidee", "buka orchidee", "hiphop"),

            # --- KLASYKI ---
            ("Krzysztof Krawczyk", "Chciałem być", "krzysztof krawczyk chcialem byc", "klasyki"),
            ("Krzysztof Krawczyk", "Bo jesteś ty", "krzysztof krawczyk bo jestes ty", "klasyki"),
            ("Krzysztof Krawczyk", "Parostatek", "krzysztof krawczyk parostatek", "klasyki"),
            ("Krzysztof Krawczyk", "Za tobą pójdę jak na bal", "krzysztof krawczyk za toba pojde jak na bal", "klasyki"),
            ("Maryla Rodowicz", "Małgośka", "maryla rodowicz malgoska", "klasyki"),
            ("Maryla Rodowicz", "Niech żyje bal", "maryla rodowicz niech zyje bal", "klasyki"),
            ("Maryla Rodowicz", "Kolorowe jarmarki", "maryla rodowicz kolorowe jarmarki", "klasyki"),
            ("Budka Suflera", "Jolka, Jolka pamiętasz", "budka suflera jolka", "klasyki"),
            ("Budka Suflera", "Takie tango", "budka suflera takie tango", "klasyki"),
            ("Budka Suflera", "Bal wszystkich świętych", "budka suflera bal wszystkich swietych", "klasyki"),
            ("Lady Pank", "Zawsze tam gdzie ty", "lady pank zawsze tam gdzie ty", "klasyki"),
            ("Lady Pank", "Mniej niż zero", "lady pank mniej niz zero", "klasyki"),
            ("Lady Pank", "Kryzysowa narzeczona", "lady pank kryzysowa narzeczona", "klasyki"),
            ("Lady Pank", "Tańcz głupia tańcz", "lady pank tancz glupia tancz", "klasyki"),
            ("Perfect", "Autobiografia", "perfect autobiografia", "klasyki"),
            ("Perfect", "Nie płacz Ewka", "perfect nie placz ewka", "klasyki"),
            ("Perfect", "Chcemy być sobą", "perfect chcemy byc soba", "klasyki"),
            ("Dżem", "Wehikuł czasu", "dzem wehikul czasu", "klasyki"),
            ("Dżem", "Sen o Victorii", "dzem sen o victorii", "klasyki"),
            ("Dżem", "Whisky", "dzem whisky", "klasyki"),
            ("Dżem", "List do M.", "dzem list do m", "klasyki"),
            ("Czesław Niemen", "Sen o Warszawie", "czeslaw niemen sen o warszawie", "klasyki"),
            ("Czesław Niemen", "Dziwny jest ten świat", "czeslaw niemen dziwny jest ten swiat", "klasyki"),
            ("Maanam", "Krakowski spleen", "maanam krakowski spleen", "klasyki"),
            ("Maanam", "Cykady na Cykladach", "maanam cykady", "klasyki"),
            ("Maanam", "Szare miraże", "maanam szare miraze", "klasyki"),
            ("Kombii", "Pokolenie", "kombii pokolenie", "klasyki"),
            ("Kombi", "Słodkiego miłego życia", "kombi slodkiego milego zycia", "klasyki"),
            ("Anna Jantar", "Tyle słońca w całym mieście", "anna jantar tyle slonca", "klasyki"),
            ("Anna Jantar", "Nic nie może wiecznie trwać", "anna jantar nic nie moze", "klasyki"),
            ("Lombard", "Przeżyj to sam", "lombard przezyj to sam", "klasyki"),
            ("Lombard", "Szklana pogoda", "lombard szklana pogoda", "klasyki"),
            ("Republika", "Biała flaga", "republika biala flaga", "klasyki"),
            ("Republika", "Mamona", "republika mamona", "klasyki"),
            ("T.Love", "Warszawa", "tlove warszawa", "klasyki"),
            ("T.Love", "Chłopaki nie płaczą", "tlove chlopaki nie placza", "klasyki"),
            ("T.Love", "King", "tlove king", "klasyki"),
            ("Kult", "Arahja", "kult arahja", "klasyki"),
            ("Kult", "Polska", "kult polska", "klasyki"),
            ("Kult", "Baranek", "kult baranek", "klasyki"),
            ("Myslovitz", "Długość dźwięku samotności", "myslovitz dlugosc dzwieku samotnosci", "klasyki"),
            ("Myslovitz", "Scenariusz dla moich sąsiadów", "myslovitz scenariusz", "klasyki"),
            ("Hey", "Teksański", "hey teksanski", "klasyki"),
            ("Hey", "Moja i twoja nadzieja", "hey moja i twoja", "klasyki"),
            ("Wilki", "Baśka", "wilki baska", "klasyki"),
            ("Wilki", "Urke", "wilki urke", "klasyki"),
            ("Wilki", "Son of the blue sky", "wilki son of the blue sky", "klasyki"),
            ("O.N.A.", "Kiedy powiem sobie dość", "ona kiedy powiem sobie dosc", "klasyki"),
            ("Kasia Kowalska", "Spowiedź", "kasia kowalska spowiedz", "klasyki"),
            ("Kasia Kowalska", "Coś optymistycznego", "kasia kowalska cos optymistycznego", "klasyki"),
            ("Kayah", "Prawy do lewego", "kayah prawy do lewego", "klasyki"),
            ("Kayah", "Śpij kochanie, śpij", "kayah spij kochanie", "klasyki"),
            ("Edyta Górniak", "To nie ja", "edyta gorniak to nie ja", "klasyki"),
            ("Edyta Górniak", "Dumka na dwa serca", "edyta gorniak dumka", "klasyki"),
            ("Bajm", "Beata z Albatrosa", "bajm beata", "klasyki"),
            ("Bajm", "Co mi Panie dasz", "bajm co mi panie dasz", "klasyki"),
            ("Bajm", "Biała armia", "bajm biala armia", "klasyki"),
            ("Czerwone Gitary", "Dozwolone od lat 18", "czerwone gitary dozwolone", "klasyki"),
            ("Czerwone Gitary", "Nie spoczniemy", "czerwone gitary nie spoczniemy", "klasyki"),
            ("Skaldowie", "Wiosna", "skaldowie wiosna", "klasyki"),
            ("Skaldowie", "Prześliczna wiolonczelistka", "skaldowie przesliczna", "klasyki"),
            ("Zbigniew Wodecki", "Zacznij od Bacha", "zbigniew wodecki zacznij od bacha", "klasyki"),
            ("Zbigniew Wodecki", "Lubię wracać tam gdzie byłem", "zbigniew wodecki lubie wracac", "klasyki"),
            ("Zbigniew Wodecki", "Chałupy Welcome To", "zbigniew wodecki chalupy", "klasyki"),
            ("Andrzej Zaucha", "Byłaś serca biciem", "andrzej zaucha bylas serca biciem", "klasyki"),
            ("Andrzej Zaucha", "C'est la vie", "andrzej zaucha cest la vie", "klasyki"),
            ("Krystyna Prońko", "Jesteś lekiem na całe zło", "krystyna pronko jestes lekiem", "klasyki"),
            ("Ryszard Rynkowski", "Dziewczyny lubią brąz", "ryszard rynkowski dziewczyny lubia braz", "klasyki"),
            ("Ryszard Rynkowski", "Jedzie pociąg z daleka", "ryszard rynkowski jedzie pociag", "klasyki"),
            ("Elektryczne Gitary", "Kiler", "elektryczne gitary kiler", "klasyki"),
            ("Elektryczne Gitary", "Dzieci wybiegły", "elektryczne gitary dzieci", "klasyki"),
            ("Chłopcy z Placu Broni", "O Ela", "chlopcy z placu broni o ela", "klasyki"),
            ("Chłopcy z Placu Broni", "Kocham wolność", "chlopcy kocham wolnosc", "klasyki"),
            ("Oddział Zamknięty", "Ten wasz świat", "oddzial zamkniety ten wasz swiat", "klasyki"),
            ("Oddział Zamknięty", "Andzia", "oddzial zamkniety andzia", "klasyki"),
            ("Kancelarya", "Zabiorę Cię", "kancelarya zabiore cie", "klasyki"),
            ("Ira", "Nadzieja", "ira nadzieja", "klasyki"),
            ("Ira", "Ona jest ze snu", "ira ona jest ze snu", "klasyki"),
            ("Sztywny Pal Azji", "Wieża radości, wieża samotności", "sztywny pal azji wieza", "klasyki"),
            ("Róże Europy", "Jedwab", "roze europy jedwab", "klasyki"),
            ("Kobranocka", "Kocham Cię jak Irlandię", "kobranocka kocham cie", "klasyki"),
            ("Piersi", "Bałkanica", "piersi balkanica", "klasyki"),
            ("Big Cyc", "Makumba", "big cyc makumba", "klasyki"),
            ("Marek Grechuta", "Dni, których nie znamy", "marek grechuta dni ktorych nie znamy", "klasyki"),
            ("Marek Grechuta", "Będziesz moją panią", "marek grechuta bedziesz moja pania", "klasyki"),
            ("Jerzy Połomski", "Bo z dziewczynami", "jerzy polomski bo z dziewczynami", "klasyki"),
            ("Grzegorz Turnau", "Cichosza", "grzegorz turnau cichosza", "klasyki"),

            # --- POPULARNE (POP / NA CZASIE) ---
            ("Dawid Podsiadło", "Małomiasteczkowy", "dawid podsiadlo malomiasteczkowy", "popularne"),
            ("Dawid Podsiadło", "W dobrą stronę", "dawid podsiadlo w dobra strone", "popularne"),
            ("Dawid Podsiadło", "Nie ma fal", "dawid podsiadlo nie ma fal", "popularne"),
            ("Dawid Podsiadło", "Trójkąty i kwadraty", "dawid podsiadlo trojkaty", "popularne"),
            ("Dawid Podsiadło", "Pastempomat", "dawid podsiadlo pastempomat", "popularne"),
            ("Sanah", "Szampan", "sanah szampan", "popularne"),
            ("Sanah", "Melodia", "sanah melodia", "popularne"),
            ("Sanah", "Ale jazz!", "sanah ale jazz", "popularne"),
            ("Sanah", "Nic dwa razy", "sanah nic dwa razy", "popularne"),
            ("Mrozu", "Złoto", "mrozu zloto", "popularne"),
            ("Mrozu", "Za daleko", "mrozu za daleko", "popularne"),
            ("Mrozu", "Aura", "mrozu aura", "popularne"),
            ("Kortez", "Hej Wy", "kortez hej wy", "popularne"),
            ("Kortez", "Zostań", "kortez zostan", "popularne"),
            ("Daria Zawiałow", "Hej Hej!", "daria zawialow hej hej", "popularne"),
            ("Daria Zawiałow", "Szarówka", "daria zawialow szarowka", "popularne"),
            ("Daria Zawiałow", "Za krótki sen", "daria zawialow za krotki sen", "popularne"),
            ("Kwiat Jabłoni", "Dziś późno pójdę spać", "kwiat jabloni dzis pozno", "popularne"),
            ("Kwiat Jabłoni", "Od nowa", "kwiat jabloni od nowa", "popularne"),
            ("Vito Bambino", "Nudy", "vito bambino nudy", "popularne"),
            ("Vito Bambino", "Poszło", "vito bambino poszlo", "popularne"),
            ("Męskie Granie Orkiestra", "Początek", "meskie granie poczatek", "popularne"),
            ("Męskie Granie Orkiestra", "I Ciebie też, bardzo", "meskie granie i ciebie tez bardzo", "popularne"),
            ("Męskie Granie Orkiestra", "Supermoce", "meskie granie supermoce", "popularne"),
            ("Ignacy", "Czekam na znak", "ignacy czekam na znak", "popularne"),
            ("Brodka", "Granda", "brodka granda", "popularne"),
            ("Brodka", "Varsovie", "brodka varsovie", "popularne"),
            ("Ralph Kaminski", "Kosmiczne energie", "ralph kaminski kosmiczne", "popularne"),
            ("Artur Rojek", "Syreny", "artur rojek syreny", "popularne"),
            ("Artur Rojek", "Beksa", "artur rojek beksa", "popularne"),
            ("Krzysztof Zalewski", "Miłość Miłość", "krzysztof zalewski milosc", "popularne"),
            ("Krzysztof Zalewski", "Kurier", "krzysztof zalewski kurier", "popularne"),
            ("Igo", "Helena", "igo helena", "popularne"),
            ("Kaśka Sochacka", "Niebo było różowe", "kaska sochacka niebo bylo rozowe", "popularne"),
            ("Kaśka Sochacka", "Ciche dni", "kaska sochacka ciche dni", "popularne"),
            ("Nosowska", "Brawa dla Państwa", "nosowska brawa dla panstwa", "popularne"),
            ("Natalia Przybysz", "Miód", "natalia przybysz miod", "popularne"),
            ("Mery Spolsky", "Bigotka", "mery spolsky bigotka", "popularne"),
            ("Margaret", "Thank You Very Much", "margaret thank you very much", "popularne"),
            ("Margaret", "Heartbeat", "margaret heartbeat", "popularne"),
            ("Roksana Węgiel", "Anyone I Want To Be", "roksana wegiel anyone", "popularne"),
            ("Roksana Węgiel", "Dobrze jest, jak jest", "roksana wegiel dobrze jest", "popularne"),
            ("Viki Gabor", "Superhero", "viki gabor superhero", "popularne"),
            ("Sylwia Grzeszczak", "Tamta dziewczyna", "sylwia grzeszczak tamta dziewczyna", "popularne"),
            ("Sylwia Grzeszczak", "Księżniczka", "sylwia grzeszczak ksiezniczka", "popularne"),
            ("Sylwia Grzeszczak", "Małe rzeczy", "sylwia grzeszczak male rzeczy", "popularne"),
            ("Ewa Farna", "Ewakuacja", "ewa farna ewakuacja", "popularne"),
            ("Ewa Farna", "Cicho", "ewa farna cicho", "popularne"),
            ("Ewa Farna", "Znak", "ewa farna znak", "popularne"),
            ("Cleo", "Za krokiem krok", "cleo za krokiem krok", "popularne"),
            ("Cleo", "Łowcy Gwiazd", "cleo lowcy gwiazd", "popularne"),
            ("Donatan & Cleo", "My Słowianie", "donatan cleo my slowianie", "popularne"),
            ("Smolasty", "Duże oczy", "smolasty duze oczy", "popularne"),
            ("Smolasty", "Pijemy za lepszy czas", "smolasty pijemy", "popularne"),
            ("Tribbs", "Ostatni raz zatańczysz ze mną", "tribbs ostatni raz", "popularne"),
            ("Oskar Cyms", "Daj mi znać", "oskar cyms daj mi znac", "popularne"),
            ("Blanka", "Solo", "blanka solo", "popularne"),
            ("Jann", "Gladiator", "jann gladiator", "popularne"),
            ("Bryska", "Odbicie", "bryska odbicie", "popularne"),
            ("Bryska", "Kraksa", "bryska kraksa", "popularne"),
            ("B.R.O", "Jeszcze będzie pięknie", "bro jeszcze bedzie pieknie", "popularne"),
            ("Baranovski", "Czułe miejsce", "baranovski czule miejsce", "popularne"),
            ("Baranovski", "Lubię być z nią", "baranovski lubie byc", "popularne"),
            ("Krystian Ochman", "River", "krystian ochman river", "popularne"),
            ("Michał Szpak", "Color Of Your Life", "michal szpak color", "popularne"),
            ("Gromee", "Light Me Up", "gromee light me up", "popularne"),
            ("C-BooL", "Never Go Away", "cbool never go away", "popularne"),
            ("Doda", "Melodia ta", "doda melodia ta", "popularne"),
            ("Doda", "Dżaga", "doda dzaga", "popularne"),
            ("Ewelina Lisowska", "W stronę słońca", "ewelina lisowska w strone slonca", "popularne"),
            ("Ewelina Lisowska", "Nieodporny rozum", "ewelina lisowska nieodporny rozum", "popularne"),
            ("Jula", "Za każdym razem", "jula za kazdym razem", "popularne"),
            ("Sarsa", "Naucz mnie", "sarsa naucz mnie", "popularne"),
            ("Ania Dąbrowska", "Z tobą nie umiem wygrać", "ania dabrowska z toba nie umiem", "popularne"),
            ("Ania Dąbrowska", "Porady na zdrady", "ania dabrowska porady", "popularne"),
            ("Natalia Szroeder", "Lustra", "natalia szroeder lustra", "popularne"),
            ("Lanberry", "Piątek", "lanberry piatek", "popularne"),
            ("Lanberry", "Ostatni most", "lanberry ostatni most", "popularne"),
            ("Reni Jusis", "Zakręcona", "reni jusis zakrecona", "popularne"),
            ("Kasia Cerekwicka", "Na kolana", "kasia cerekwicka na kolana", "popularne"),
            ("Paweł Domagała", "Weź nie pytaj", "pawel domagala wez nie pytaj", "popularne"),
            ("Kamil Bednarek", "Cisza", "kamil bednarek cisza", "popularne"),
            ("Enej", "Radio Hello", "enej radio hello", "popularne"),
            ("Enej", "Skrzydlate ręce", "enej skrzydlate rece", "popularne"),
            ("LemON", "Napraw", "lemon napraw", "popularne"),
            ("Mesajah", "Każdego dnia", "mesajah kazdego dnia", "popularne")
        ]
        cursor.executemany("INSERT INTO songs (artist, title, search_query, category) VALUES (?, ?, ?, ?)", sample_songs)
        conn.commit()
    
    conn.close()
    yield

app = FastAPI(lifespan=lifespan)

# --- KONFIGURACJA CORS ---
# Pozwala frontendowi (React/Svelte) na komunikację z tym serwerem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # W środowisku dev pozwalamy na wszystko
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GuessRequest(BaseModel):
    song_id: int
    guess_text: str

# --- NOWY ENDPOINT: Losowanie piosenki ---
@app.get("/api/random-song/{category}")
def get_random_song(category: str):
    """Losuje ID piosenki z wybranej kategorii."""
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM songs WHERE category = ?", (category.lower(),))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Brak piosenek w tej kategorii")
    
    # Zwraca losowe ID z dostępnych w danej kategorii
    return {"song_id": random.choice(rows)[0]}
@app.get("/api/audio/{song_id}")
def get_audio_by_id(song_id: int, duration: float = 1.0):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT artist, title, search_query FROM songs WHERE id = ?", (song_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Utwór nie istnieje")
    
    artist, title, query = row
    
    # 🔴 DEBUG: Zobaczysz w konsoli, co dokładnie szukamy
    print(f"DEBUG: Szukam w iTunes frazy: {query}")
    
    url = f"https://itunes.apple.com/search?term={query.replace(' ', '+')}&entity=song&limit=1"
    res = requests.get(url)
    data = res.json()

    if data['resultCount'] == 0:
        print(f"DEBUG: iTunes nie znalazł utworu dla: {query}")
        raise HTTPException(status_code=404, detail="Nie znaleziono utworu w serwisie")
    
    preview_url = data['results'][0]['previewUrl']
    
    filename = f"temp_{song_id}.m4a"
    output_filename = f"output_{song_id}.m4a"
    
    audio_res = requests.get(preview_url)
    with open(filename, "wb") as f:
        f.write(audio_res.content)
    
    os.system(f"ffmpeg -y -i {filename} -t {duration} {output_filename}")
        
    return FileResponse(output_filename, media_type="audio/mp4")
@app.post("/api/guess")
def check_guess(request: GuessRequest):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT artist, title FROM songs WHERE id = ?", (request.song_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Błąd gry")

    db_artist, db_title = row
    
    # Zamieniamy wszystko na małe litery
    user_guess = request.guess_text.lower().strip()
    
    # 1. Sprawdzamy idealne dopasowanie (takie, jakie wysyła nasza lista podpowiedzi z myślnikiem)
    exact_match = f"{db_artist} - {db_title}".lower()
    
    # 2. Tworzymy wariant "luźny" (bez myślników), gdyby gracz wpisywał tekst ręcznie
    loose_match = f"{db_artist} {db_title}".lower()
    user_guess_loose = user_guess.replace("-", " ").replace("  ", " ")

    # Uznajemy za poprawne, jeśli pasuje idealnie z listy, LUB gracz wpisał ręcznie sensowny fragment
    is_correct = (
        user_guess == exact_match or 
        (user_guess_loose in loose_match and len(user_guess_loose) > 3)
    )

    return {
        "correct": is_correct,
        "correct_artist": db_artist,
        "correct_title": db_title
    }

@app.get("/api/songs")
def get_all_songs():
    """Zwraca listę wszystkich utworów z bazy na potrzeby podpowiedzi."""
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT artist, title FROM songs")
    rows = cursor.fetchall()
    conn.close()
    
    # Łączymy artystę i tytuł w jeden ładny string
    return [f"{row[0]} - {row[1]}" for row in rows]