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
            ("Paktofonika", "Jestem Bogiem", "Paktofonika Jestem Bogiem Kinematografia official audio", "hiphop"),
            ("Paktofonika", "Chwile ulotne", "Paktofonika Chwile ulotne Kinematografia official audio", "hiphop"),
            ("Taco Hemingway", "Deszcz na betonie", "Taco Hemingway Deszcz na betonie Marmur official audio", "hiphop"),
            ("Taco Hemingway", "Fifi Hollywood", "Taco Hemingway Fifi Hollywood Cafe Belga official audio", "hiphop"),
            ("Taco Hemingway", "Polskie Tango", "Taco Hemingway Polskie Tango Pocztówka z WWA official audio", "hiphop"),
            ("Mata", "Patointeligencja", "Mata Patointeligencja 100 dni po maturze official audio", "hiphop"),
            ("Mata", "Kiss cam", "Mata Kiss cam Młody Matczak official audio", "hiphop"),
            ("Mata", "Schodki", "Mata Schodki 100 dni po maturze official audio", "hiphop"),
            ("Quebonafide", "Candy", "Quebonafide Candy Egzotyka official audio", "hiphop"),
            ("Quebonafide", "Bubbletea", "Quebonafide Bubbletea Romantic Psycho official audio", "hiphop"),
            ("PRO8L3M", "Molly", "PRO8L3M Molly Art Brut official audio", "hiphop"),
            ("PRO8L3M", "Flary", "PRO8L3M Flary Art Brut 2 official audio", "hiphop"),
            ("Sokół", "Prawda", "Sokół Prawda Wojtek Sokół official audio", "hiphop"),
            ("Bedoes 2115", "05:05", "Bedoes 05:05 Opowieści z Doliny Smoków official audio", "hiphop"),
            ("Bedoes 2115", "Eldorado", "Bedoes Eldorado Kwiat polskiej młodzieży official audio", "hiphop"),
            ("O.S.T.R.", "Lubię być sam", "O.S.T.R. Lubię być sam Jazz w wolnych chwilach official audio", "hiphop"),
            ("Pezet", "Ukryty w mieście krzyk", "Pezet Ukryty w mieście krzyk Muzyka Klasyczna official audio", "hiphop"),
            ("Pezet", "Gdyby miało nie być jutra", "Pezet Gdyby miało nie być jutra Muzyka Klasyczna official audio", "hiphop"),
            ("Tede", "Drin za drinem", "Tede Drin za drinem Note official audio", "hiphop"),
            ("Kizo", "Disney", "Kizo Disney Posejdon official audio", "hiphop"),
            ("Kizo", "Hero", "Kizo Hero Hero official audio", "hiphop"),
            ("Malik Montana", "Jagodzianki", "Malik Montana Jagodzianki Import/Export official audio", "hiphop"),
            ("Guzior", "Blueberry", "Guzior Blueberry Pleśń official audio", "hiphop"),
            ("Guzior", "Fala", "Guzior Fala Evil Twin official audio", "hiphop"),
            ("Kukon", "Ogrodowa", "Kukon Ogrodowa Ogrodowa official audio", "hiphop"),
            ("Szpaku", "UFO", "Szpaku UFO ATU official audio", "hiphop"),
            ("Szpaku", "Hinata", "Szpaku Hinata Atypowy official audio", "hiphop"),
            ("Paluch", "Szaman", "Paluch Szaman Czerwony Dywan official audio", "hiphop"),
            ("White 2115", "California", "White 2115 California California official audio", "hiphop"),
            ("WWO", "Każdy ponad każdym", "WWO Każdy ponad każdym We własnej osobie official audio", "hiphop"),
            ("Molesta Ewenement", "Wiedziałem że tak będzie", "Molesta Wiedziałem że tak będzie Skandal official audio", "hiphop"),
            ("Slums Attack", "Głucha noc", "Slums Attack Głucha noc Na legalu official audio", "hiphop"),
            ("Zeus", "Hipotermia", "Zeus Hipotermia Zeus nie żyje official audio", "hiphop"),
            ("Ten Typ Mes", "L.O.V.E.", "Ten Typ Mes L.O.V.E. Kandydaci na szaleńców official audio", "hiphop"),
            ("KęKę", "Smutek", "KęKę Smutek Takie rzeczy official audio", "hiphop"),
            ("Białas", "Bliźniaczki", "Białas Bliźniaczki H8M5 official audio", "hiphop"),
            ("Avi", "Toast", "Avi Toast Spis cudzołożnic official audio", "hiphop"),
            ("Kabe", "Nad ranem", "Kabe Nad ranem King Kong official audio", "hiphop"),
            ("Reto", "Billy Kid", "Reto Billy Kid Billy Kid official audio", "hiphop"),
            ("Buka", "Orchidee", "Buka Orchidee Pokój 003 official audio", "hiphop"),
            ("Tymek", "Język ciała", "Tymek Język ciała Tymek official audio", "hiphop"),
            ("Sobel", "Fiołkowe pole", "Sobel Fiołkowe pole Pułapka na motyle official audio", "hiphop"),
            ("Sobel", "Impreza", "Sobel Impreza Pułapka na motyle official audio", "hiphop"),
            ("Oki", "Jeżyk!", "Oki Jeżyk! 47playground official audio", "hiphop"),
            ("Żabson", "Kush", "Żabson Kush Internaziomal official audio", "hiphop"),
            ("Donguralesko", "Chcę ci dać", "Donguralesko Chcę ci dać El Polako official audio", "hiphop"),
            ("Trzeci Wymiar", "Dla mnie masz stajla", "Trzeci Wymiar Dla mnie masz stajla Cztery pory rapu official audio", "hiphop"),
            ("Jeden Osiem L", "Jak zapomnieć", "Jeden Osiem L Jak zapomnieć Wideoteka official audio", "hiphop"),
            ("Mezo", "Sacrum", "Mezo Sacrum Mezokracja official audio", "hiphop"),
            ("Liber", "Skarby", "Liber Skarby Bógmacher official audio", "hiphop"),
            ("Dawid Podsiadło", "Małomiasteczkowy", "Dawid Podsiadło Małomiasteczkowy Małomiasteczkowy official audio", "popularne"),
            ("Dawid Podsiadło", "W dobrą stronę", "Dawid Podsiadło W dobrą stronę Annoyance and Disappointment official audio", "popularne"),
            ("Dawid Podsiadło", "Nie ma fal", "Dawid Podsiadło Nie ma fal Małomiasteczkowy official audio", "popularne"),
            ("Sanah", "Szampan", "Sanah Szampan Królowa dram official audio", "popularne"),
            ("Sanah", "Melodia", "Sanah Melodia Królowa dram official audio", "popularne"),
            ("Sanah", "Ale jazz!", "Sanah Ale jazz Irenka official audio", "popularne"),
            ("Mrozu", "Złoto", "Mrozu Złoto Aura official audio", "popularne"),
            ("Mrozu", "Za daleko", "Mrozu Za daleko Złote bloki official audio", "popularne"),
            ("Kortez", "Hej Wy", "Kortez Hej Wy Mój dom official audio", "popularne"),
            ("Kortez", "Zostań", "Kortez Zostań Bumerang official audio", "popularne"),
            ("Daria Zawiałow", "Hej Hej!", "Daria Zawiałow Hej Hej Helsinki official audio", "popularne"),
            ("Daria Zawiałow", "Szarówka", "Daria Zawiałow Szarówka Helsinki official audio", "popularne"),
            ("Kwiat Jabłoni", "Dziś późno pójdę spać", "Kwiat Jabłoni Dziś późno pójdę spać Niemożliwe official audio", "popularne"),
            ("Vito Bambino", "Nudy", "Vito Bambino Nudy Poczekalnia official audio", "popularne"),
            ("Męskie Granie Orkiestra", "Początek", "Męskie Granie Orkiestra Początek Męskie Granie 2018 official audio", "popularne"),
            ("Brodka", "Granda", "Brodka Granda Granda official audio", "popularne"),
            ("Ralph Kaminski", "Kosmiczne energie", "Ralph Kaminski Kosmiczne energie Pies official audio", "popularne"),
            ("Artur Rojek", "Syreny", "Artur Rojek Syreny Składam się z ciągłych powtórzeń official audio", "popularne"),
            ("Krzysztof Zalewski", "Miłość Miłość", "Krzysztof Zalewski Miłość Miłość Zalewski Złoto official audio", "popularne"),
            ("Kaśka Sochacka", "Ciche dni", "Kaśka Sochacka Ciche dni Ciche dni official audio", "popularne"),
            ("Nosowska", "Brawa dla Państwa", "Nosowska Brawa dla Państwa Brawa dla Państwa official audio", "popularne"),
            ("Natalia Przybysz", "Miód", "Natalia Przybysz Miód Prąd official audio", "popularne"),
            ("Mery Spolsky", "Bigotka", "Mery Spolsky Bigotka Dekalog Mery Spolsky official audio", "popularne"),
            ("Margaret", "Thank You Very Much", "Margaret Thank You Very Much All I Need official audio", "popularne"),
            ("Roksana Węgiel", "Anyone I Want To Be", "Roksana Węgiel Anyone I Want To Be Roksana Węgiel official audio", "popularne"),
            ("Viki Gabor", "Superhero", "Viki Gabor Superhero Getaway official audio", "popularne"),
            ("Sylwia Grzeszczak", "Tamta dziewczyna", "Sylwia Grzeszczak Tamta dziewczyna Tamta dziewczyna official audio", "popularne"),
            ("Sylwia Grzeszczak", "Księżniczka", "Sylwia Grzeszczak Księżniczka Komponując siebie official audio", "popularne"),
            ("Ewa Farna", "Ewakuacja", "Ewa Farna Ewakuacja Ewakuacja official audio", "popularne"),
            ("Ewa Farna", "Cicho", "Ewa Farna Cicho Cicho official audio", "popularne"),
            ("Cleo", "Za krokiem krok", "Cleo Za krokiem krok Supernova official audio", "popularne"),
            ("Donatan & Cleo", "My Słowianie", "Donatan Cleo My Słowianie Hiper/Chimera official audio", "popularne"),
            ("Smolasty", "Duże oczy", "Smolasty Duże oczy Ghetto Playboy official audio", "popularne"),
            ("Tribbs", "Ostatni raz zatańczysz ze mną", "Tribbs Ostatni raz zatańczysz ze mną Ostatni raz zatańczysz ze mną official audio", "popularne"),
            ("Oskar Cyms", "Daj mi znać", "Oskar Cyms Daj mi znać Daj mi znać official audio", "popularne"),
            ("Blanka", "Solo", "Blanka Solo Solo official audio", "popularne"),
            ("Jann", "Gladiator", "Jann Gladiator Gladiator official audio", "popularne"),
            ("Bryska", "Odbicie", "Bryska Odbicie Odbicie official audio", "popularne"),
            ("Krystian Ochman", "River", "Krystian Ochman River Ochman official audio", "popularne"),
            ("Michał Szpak", "Color Of Your Life", "Michał Szpak Color Of Your Life Color Of Your Life official audio", "popularne"),
            ("Gromee", "Light Me Up", "Gromee Light Me Up Light Me Up official audio", "popularne"),
            ("C-BooL", "Never Go Away", "C-BooL Never Go Away Never Go Away official audio", "popularne"),
            ("Doda", "Melodia ta", "Doda Melodia ta Aquaria official audio", "popularne"),
            ("Ewelina Lisowska", "W stronę słońca", "Ewelina Lisowska W stronę słońca Aero-Plan official audio", "popularne"),
            ("Jula", "Za każdym razem", "Jula Za każdym razem Na krawędzi official audio", "popularne"),
            ("Sarsa", "Naucz mnie", "Sarsa Naucz mnie Zapomnij mi official audio", "popularne"),
            ("Ania Dąbrowska", "Z tobą nie umiem wygrać", "Ania Dąbrowska Z tobą nie umiem wygrać Bawię się świetnie official audio", "popularne"),
            ("Natalia Szroeder", "Lustra", "Natalia Szroeder Lustra NATinterpretacje official audio", "popularne"),
            ("Lanberry", "Piątek", "Lanberry Piątek Piątek official audio", "popularne"),
            ("Reni Jusis", "Zakręcona", "Reni Jusis Zakręcona Zakręcona official audio", "popularne"),
            ("Kasia Cerekwicka", "Na kolana", "Kasia Cerekwicka Na kolana Feniks official audio", "popularne"),
            ("Paweł Domagała", "Weź nie pytaj", "Paweł Domagała Weź nie pytaj 1984 official audio", "popularne"),
            ("Kamil Bednarek", "Cisza", "Kamil Bednarek Cisza Jestem official audio", "popularne"),
            ("Enej", "Radio Hello", "Enej Radio Hello Folklore official audio", "popularne"),
            ("Enej", "Skrzydlate ręce", "Enej Skrzydlate ręce Folkhorod official audio", "popularne"),
            ("LemON", "Napraw", "LemON Napraw Scarlett official audio", "popularne"),
            ("Mesajah", "Każdego dnia", "Mesajah Każdego dnia Ludzie prości official audio", "popularne"),
            ("Krzysztof Krawczyk", "Bo jesteś ty", "Krzysztof Krawczyk Bo jesteś ty Bo jesteś ty official audio", "klasyki"),
            ("Krzysztof Krawczyk", "Parostatek", "Krzysztof Krawczyk Parostatek Parostatek official audio", "klasyki"),
            ("Lady Pank", "Mniej niż zero", "Lady Pank Mniej niż zero Lady Pank official audio", "klasyki"),
            ("Lady Pank", "Kryzysowa narzeczona", "Lady Pank Kryzysowa narzeczona Lady Pank official audio", "klasyki"),
            ("Perfect", "Nie płacz Ewka", "Perfect Nie płacz Ewka Perfect official audio", "klasyki"),
            ("Dżem", "Sen o Victorii", "Dżem Sen o Victorii Cegła official audio", "klasyki"),
            ("Dżem", "Whisky", "Dżem Whisky Cegła official audio", "klasyki"),
            ("Maanam", "Cykady na Cykladach", "Maanam Cykady na Cykladach Nocny patrol official audio", "klasyki"),
            ("Kombi", "Słodkiego miłego życia", "Kombi Słodkiego miłego życia Kombi official audio", "klasyki"),
            ("Lombard", "Szklana pogoda", "Lombard Szklana pogoda Szklana pogoda official audio", "klasyki"),
            ("T.Love", "Chłopaki nie płaczą", "T.Love Chłopaki nie płaczą Chłopaki nie płaczą official audio", "klasyki"),
            ("Kult", "Polska", "Kult Polska Posłuchaj to do ciebie official audio", "klasyki"),
            ("Kult", "Baranek", "Kult Baranek Ostateczny krach systemu korporacji official audio", "klasyki"),
            ("Hey", "Moja i twoja nadzieja", "Hey Moja i twoja nadzieja Fire official audio", "klasyki"),
            ("Wilki", "Urke", "Wilki Urke 4 official audio", "klasyki"),
            ("Kult", "Celina", "Kult Celina Ostateczny krach systemu korporacji official audio", "klasyki"),
            ("Varius Manx", "Orła cień", "Varius Manx Orła cień Elf official audio", "klasyki"),
            ("Varius Manx", "Piosenka księżycowa", "Varius Manx Piosenka księżycowa Emu official audio", "klasyki"),
            ("Edyta Bartosiewicz", "Sen", "Edyta Bartosiewicz Sen Sen official audio", "klasyki"),
            ("Edyta Bartosiewicz", "Jenny", "Edyta Bartosiewicz Jenny Sen official audio", "klasyki"),
            ("Nosowska", "Nomada", "Nosowska Nomada Nomada official audio", "popularne"),
            ("Hey", "Teksański", "Hey Teksański Fire official audio", "klasyki"),
            ("Myslovitz", "Długość dźwięku samotności", "Myslovitz Długość dźwięku samotności Miłość w czasach popkultury official audio", "klasyki"),
            ("Myslovitz", "Peggy Brown", "Myslovitz Peggy Brown Aille official audio", "klasyki"),
            ("Hania Rani", "Eden", "Hania Rani Eden Esja official audio", "popularne"),
            ("Brodka", "Varsovie", "Brodka Varsovie LA official audio", "popularne"),
            ("Brodka", "Game Change", "Brodka Game Change Brut official audio", "popularne"),
            ("Organek", "Mississippi w ogniu", "Organek Mississippi w ogniu Głupi official audio", "popularne"),
            ("Organek", "Głupi ja", "Organek Głupi ja Głupi official audio", "popularne"),
            ("Coma", "Leszek Żukowski", "Coma Leszek Żukowski Leszek Żukowski official audio", "klasyki"),
            ("Coma", "Spadam", "Coma Spadam Pierwsze wyjście z mroku official audio", "klasyki"),
            ("Pidżama Porno", "Twoja generacja", "Pidżama Porno Twoja generacja Bułgarskie centrum official audio", "klasyki"),
            ("Pidżama Porno", "Ezoteryczny Poznań", "Pidżama Porno Ezoteryczny Poznań Koniec wieku official audio", "klasyki"),
            ("Strachy Na Lachy", "Dzień dobry kocham cię", "Strachy Na Lachy Dzień dobry kocham cię Autor official audio", "popularne"),
            ("Strachy Na Lachy", "Żyję w kraju", "Strachy Na Lachy Żyję w kraju Zakazane piosenki official audio", "popularne"),
            ("Renata Przemyk", "Babę zesłał Bóg", "Renata Przemyk Babę zesłał Bóg Ya Hozna official audio", "klasyki"),
            ("Anita Lipnicka", "I wszystko się może zdarzyć", "Anita Lipnicka I wszystko się może zdarzyć Wszystko się może zdarzyć official audio", "klasyki"),
            ("Varius Manx", "Zanim zrozumiesz", "Varius Manx Zanim zrozumiesz Elf official audio", "klasyki"),
            ("Andrzej Piaseczny", "Imię deszczu", "Andrzej Piaseczny Imię deszczu Piasek official audio", "popularne"),
            ("Andrzej Piaseczny", "Chodź, przytul, przebacz", "Andrzej Piaseczny Chodź przytul przebacz Spis rzeczy ulubionych official audio", "popularne"),
            ("Robert Gawliński", "O sobie samym", "Robert Gawliński O sobie samym Solo official audio", "klasyki"),
            ("Kasia Kowalska", "A to co mam", "Kasia Kowalska A to co mam Gemini official audio", "klasyki"),
            ("Kasia Kowalska", "Prowadź mnie", "Kasia Kowalska Prowadź mnie Gemini official audio", "klasyki"),
            ("Urszula", "Konik na biegunach", "Urszula Konik na biegunach Konik na biegunach official audio", "klasyki"),
            ("Urszula", "Dmuchawce latawce wiatr", "Urszula Dmuchawce latawce wiatr The Best Of official audio", "klasyki"),
            ("Budka Suflera", "Jolka Jolka pamiętasz", "Budka Suflera Jolka Jolka pamiętasz Za ostatni grosz official audio", "klasyki"),
            ("Budka Suflera", "Bal wszystkich świętych", "Budka Suflera Bal wszystkich świętych Bal wszystkich świętych official audio", "klasyki"),
            ("Bajm", "Szklanka wody", "Bajm Szklanka wody Szklanka wody official audio", "klasyki"),
            ("Bajm", "Ta sama chwila", "Bajm Ta sama chwila Szklanka wody official audio", "klasyki"),
            ("Big Cyc", "Makumba", "Big Cyc Makumba Z gitarą wśród zwierząt official audio", "klasyki"),
            ("Big Cyc", "Dres", "Big Cyc Dres Dres official audio", "klasyki"),
            ("Elektryczne Gitary", "Dzieci", "Elektryczne Gitary Dzieci Wielka radość official audio", "klasyki"),
            ("Elektryczne Gitary", "Kiler", "Elektryczne Gitary Kiler Kiler official audio", "klasyki"),
            ("Republika", "Mamona", "Republika Mamona Masakra official audio", "klasyki"),
            ("Republika", "Obcy astronom", "Republika Obcy astronom Nowe sytuacje official audio", "klasyki"),
            ("Obywatel G.C.", "Nie pytaj mnie o Polskę", "Obywatel G.C. Nie pytaj mnie o Polskę Obywatel G.C. official audio", "klasyki"),
            ("De Mono", "Kochać inaczej", "De Mono Kochać inaczej Oh Yeah official audio", "klasyki"),
            ("De Mono", "Statki na niebie", "De Mono Statki na niebie Stop official audio", "klasyki"),
            ("Golden Life", "Dobro", "Golden Life Dobro Golden Live official audio", "klasyki"),
            ("Varius Manx", "Pocałuj noc", "Varius Manx Pocałuj noc Elf official audio", "klasyki"),
            ("Krzysztof Antkowiak", "Zakazany owoc", "Krzysztof Antkowiak Zakazany owoc Zakazany owoc official audio", "klasyki"),
            ("Mieczysław Szcześniak", "Dumka na dwa serca", "Mieczysław Szcześniak Dumka na dwa serca Dumka official audio", "klasyki"),
            ("Varius Manx", "Ten sen", "Varius Manx Ten sen Emu official audio", "klasyki"),
            ("Kayah", "Supermenka", "Kayah Supermenka Zebra official audio", "klasyki"),
            ("Kayah", "Testosteron", "Kayah Testosteron Stereo typ official audio", "klasyki"),
            ("Brodka", "Miał być ślub", "Brodka Miał być ślub Album official audio", "popularne"),
            ("Afromental", "Radio Song", "Afromental Radio Song Playing with Pop official audio", "popularne"),
            ("Afromental", "Pray 4 Love", "Afromental Pray 4 Love Playing with Pop official audio", "popularne"),
            ("Pectus", "To co chciałbym ci dać", "Pectus To co chciałbym ci dać Pectus official audio", "popularne"),
            ("Feel", "A gdy jest już ciemno", "Feel A gdy jest już ciemno Feel official audio", "popularne"),
            ("Feel", "Jak anioła głos", "Feel Jak anioła głos Feel official audio", "popularne"),
            ("Video", "Idziemy na całość", "Video Idziemy na całość Video official audio", "popularne"),
            ("Video", "Papieros", "Video Papieros Nie obchodzi nas film official audio", "popularne"),
            ("Piotr Rogucki", "Piosenka pisana nocą", "Piotr Rogucki Piosenka pisana nocą LOK official audio", "popularne"),
            ("Chemia", "Hero", "Chemia Hero The Best of Chemia official audio", "popularne"),
            ("Riverside", "02 Panic Room", "Riverside 02 Panic Room Rapid Eye Movement official audio", "popularne"),
            ("Happysad", "Zanim pójdę", "Happysad Zanim pójdę Wszystko jedno official audio", "popularne"),
            ("Happysad", "Łydka", "Happysad Łydka Mów mi dobrze official audio", "popularne"),
            ("Enej", "Tak smakuje życie", "Enej Tak smakuje życie Folkhorod official audio", "popularne"),
            ("Red Lips", "To co nam było", "Red Lips To co nam było To co nam było official audio", "popularne"),
            ("Natalia Nykiel", "Bądź duży", "Natalia Nykiel Bądź duży Lupus Electro official audio", "popularne"),
            ("Natalia Nykiel", "Error", "Natalia Nykiel Error Error official audio", "popularne"),
            ("Monika Brodka", "Ten", "Monika Brodka Ten Album official audio", "popularne"),
            ("Ania Wyszkoni", "Czy ten pan i pani", "Ania Wyszkoni Czy ten pan i pani Pan i Pani official audio", "popularne"),
            ("Ania Wyszkoni", "Wiem że jesteś tam", "Ania Wyszkoni Wiem że jesteś tam Pan i Pani official audio", "popularne"),
            ("Gosia Andrzejewicz", "Pozwól żyć", "Gosia Andrzejewicz Pozwól żyć Gosia Andrzejewicz official audio", "popularne"),
            ("Verba", "Młode wilki", "Verba Młode wilki Młode wilki official audio", "hiphop"),
            ("Verba", "Nie łam mi serca", "Verba Nie łam mi serca Nie łam mi serca official audio", "hiphop"),
            ("Ascetoholix", "Suczki", "Ascetoholix Suczki Apogeum official audio", "hiphop"),
            ("Mezo", "Aniele", "Mezo Aniele Mezokracja official audio", "hiphop"),
            ("Doniu", "Uciekaj", "Doniu Uciekaj Monolog motyl official audio", "hiphop"),
            ("Onar", "Wszystko co mam", "Onar Wszystko co mam Wszystko co mam official audio", "hiphop"),
            ("Pezet", "Seniorita", "Pezet Seniorita Muzyka Poważna official audio", "hiphop"),
            ("O.S.T.R.", "Kochana Polsko", "O.S.T.R. Kochana Polsko Tylko dla dorosłych official audio", "hiphop"),
            ("O.S.T.R.", "Śpij spokojnie", "O.S.T.R. Śpij spokojnie Jazz w wolnych chwilach official audio", "hiphop"),
            ("Łona", "Konfident", "Łona Konfident Koniec żartów official audio", "hiphop"),
            ("Łona", "Nie pytaj nas", "Łona Nie pytaj nas Koniec żartów official audio", "hiphop"),
            ("Fisz", "Czerwona sukienka", "Fisz Czerwona sukienka Na wylot official audio", "hiphop"),
            ("Emade", "Nieodkryty", "Emade Nieodkryty Album official audio", "hiphop"),
            ("Peja", "Na dnie", "Peja Na dnie Na legalu official audio", "hiphop"),
            ("Peja", "Kc", "Peja Kc Kc official audio", "hiphop"),
            ("Hemp Gru", "Klucz", "Hemp Gru Klucz Klucz official audio", "hiphop"),
            ("Hemp Gru", "To jest to", "Hemp Gru To jest to Klucz official audio", "hiphop"),
            ("ZIP Skład", "Śródmieście", "ZIP Skład Śródmieście Chleb powszedni official audio", "hiphop"),
            ("Warszafski Deszcz", "Aluminium", "Warszafski Deszcz Aluminium Nastukafszy official audio", "hiphop"),
            ("Molesta", "Armagedon", "Molesta Armagedon Skandal official audio", "hiphop"),
            ("Grammatik", "Friko", "Grammatik Friko Światła miasta official audio", "hiphop"),
            ("Grammatik", "Każdy ma takie chwile", "Grammatik Każdy ma takie chwile Światła miasta official audio", "hiphop"),
            ("Sokół i Marysia Starosta", "Reset", "Sokół Reset Czysta brudna prawda official audio", "hiphop"),
            ("Sokół i Marysia Starosta", "Wyścig szczurów", "Sokół Wyścig szczurów Czysta brudna prawda official audio", "hiphop"),
            ("Bisz", "Wilk chodnikowy", "Bisz Wilk chodnikowy Wilk chodnikowy official audio", "hiphop"),
            ("Bisz", "Banicja", "Bisz Banicja Wilk chodnikowy official audio", "hiphop"),
            ("Quebonafide", "Zorza", "Quebonafide Zorza Egzotyka official audio", "hiphop"),
            ("Quebonafide", "Bumerang", "Quebonafide Bumerang Eklektyka official audio", "hiphop"),
            ("Taconafide", "Tamagotchi", "Taconafide Tamagotchi Soma official audio", "hiphop"),
            ("Taconafide", "Art-B", "Taconafide Art-B Soma official audio", "hiphop"),
            ("Bedoes", "Gustaw", "Bedoes Gustaw Kwiat polskiej młodzieży official audio", "hiphop"),
            ("Bedoes", "Michelangelo", "Bedoes Michelangelo Opowieści z Doliny Smoków official audio", "hiphop"),
            ("White 2115", "California", "White 2115 California California official audio", "hiphop"),
            ("White 2115", "Morgan", "White 2115 Morgan Młody Łajcior official audio", "hiphop"),
            ("Mata", "Biblioteka trap", "Mata Biblioteka trap 100 dni po maturze official audio", "hiphop"),
            ("Mata", "Gore", "Mata Gore Młody Matczak official audio", "hiphop"),
            ("Otsochodzi", "Nie, nie", "Otsochodzi Nie, nie Nowy kolor official audio", "hiphop"),
            ("Otsochodzi", "Nowy kolor", "Otsochodzi Nowy kolor Nowy kolor official audio", "hiphop"),
            ("Jan-rapowanie", "Jeszcze będzie przepięknie", "Jan-rapowanie Jeszcze będzie przepięknie Uśmiech official audio", "hiphop"),
            ("Jan-rapowanie", "Siedem", "Jan-rapowanie Siedem Uśmiech official audio", "hiphop"),
            ("PlanBe", "Złoty chłopak", "PlanBe Złoty chłopak Złoty chłopak official audio", "hiphop"),
            ("PlanBe", "Kobiety", "PlanBe Kobiety Złoty chłopak official audio", "hiphop"),
            ("Wac Toja", "Kapitan", "Wac Toja Kapitan Turboofficial official audio", "hiphop"),
            ("Wac Toja", "Cały hajs", "Wac Toja Cały hajs Cały hajs official audio", "hiphop"),
            ("Borixon", "Moja bani", "Borixon Moja bani Moja bani official audio", "hiphop"),
            ("Borixon", "Koko Chanel", "Borixon Koko Chanel Koko Chanel official audio", "hiphop"),
            ("Solar", "Wszystko ok", "Solar Wszystko ok Wszystko ok official audio", "hiphop"),
            ("Solar", "Pierwszy raz", "Solar Pierwszy raz Pierwszy raz official audio", "hiphop"),
            ("Białas", "H8M5", "Białas H8M5 H8M5 official audio", "hiphop"),
            ("Białas", "To nie jest hip-hop", "Białas To nie jest hip-hop H8M5 official audio", "hiphop"),
            ("Kali", "Dobrego dnia", "Kali Dobrego dnia Dobrego dnia official audio", "hiphop"),
            ("Kali", "Gdy zgaśnie słońce", "Kali Gdy zgaśnie słońce Gdy zgaśnie słońce official audio", "hiphop"),
            ("KęKę", "Wyścig szczurów", "KęKę Wyścig szczurów Nowe rzeczy official audio", "hiphop"),
            ("KęKę", "Takie rzeczy", "KęKę Takie rzeczy Takie rzeczy official audio", "hiphop"),
            ("KęKę", "Presja", "KęKę Presja Trzecie rzeczy official audio", "hiphop"),
            ("KęKę", "Moja osoba", "KęKę Moja osoba Nowe rzeczy official audio", "hiphop"),
            ("Ten Typ Mes", "My", "Ten Typ Mes My Kandydaci na szaleńców official audio", "hiphop"),
            ("Ten Typ Mes", "Jak to", "Ten Typ Mes Jak to Alkopoligamia official audio", "hiphop"),
            ("VNM", "Pro", "VNM Pro Pro official audio", "hiphop"),
            ("VNM", "Halflife", "VNM Halflife Halflife official audio", "hiphop"),
            ("Małpa", "Nie byłem nigdy", "Małpa Nie byłem nigdy Kilka numerów o czymś official audio", "hiphop"),
            ("Małpa", "Pozwól mi nie chcieć", "Małpa Pozwól mi nie chcieć Kilka numerów o czymś official audio", "hiphop"),
            ("BisZ", "Potwór", "Bisz Potwór Wilk chodnikowy official audio", "hiphop"),
            ("BisZ", "Wiatraki", "Bisz Wiatraki Wilk chodnikowy official audio", "hiphop"),
            ("Hades", "Nowa szkoła", "Hades Nowa szkoła Nowe dobro to zło official audio", "hiphop"),
            ("Hades", "Życie jest piękne", "Hades Życie jest piękne Nowe dobro to zło official audio", "hiphop"),
            ("Sarius", "Wszystko", "Sarius Wszystko Antihype official audio", "hiphop"),
            ("Sarius", "Dziecko wojny", "Sarius Dziecko wojny Antihype official audio", "hiphop"),
            ("Dwa Sławy", "Multitasking", "Dwa Sławy Multitasking Dandys status official audio", "hiphop"),
            ("Dwa Sławy", "Do rana", "Dwa Sławy Do rana Dandys status official audio", "hiphop"),
            ("Rasmentalism", "Słodko-gorzki", "Rasmentalism Słodko-gorzki Za młodzi na Heroda official audio", "hiphop"),
            ("Rasmentalism", "Wyjście", "Rasmentalism Wyjście Za młodzi na Heroda official audio", "hiphop"),
            ("Parias", "Hip-hop", "Parias Hip-hop Parias official audio", "hiphop"),
            ("Parias", "Mamy ten styl", "Parias Mamy ten styl Parias official audio", "hiphop"),
            ("W.E.N.A.", "Wszystko gra", "W.E.N.A. Wszystko gra Nowa definicja official audio", "hiphop"),
            ("W.E.N.A.", "Ważny", "W.E.N.A. Ważny Niepamięć official audio", "hiphop"),
            ("Tau", "Bóg jest miłością", "Tau Bóg jest miłością Remedium official audio", "hiphop"),
            ("Tau", "Wyżej", "Tau Wyżej Remedium official audio", "hiphop"),
            ("Kabe", "Albinos", "Kabe Albinos King Kong official audio", "hiphop"),
            ("Kabe", "Każdy dzień", "Kabe Każdy dzień King Kong official audio", "hiphop"),
            ("White 2115", "California", "White 2115 California California official audio", "hiphop"),
            ("White 2115", "Sen", "White 2115 Sen Młody Łajcior official audio", "hiphop"),
            ("Mata", "Blumental", "Mata Blumental Młody Matczak official audio", "hiphop"),
            ("Mata", "La la la", "Mata La la la Młody Matczak official audio", "hiphop"),
            ("Young Multi", "Plecak", "Young Multi Plecak Plecak official audio", "hiphop"),
            ("Young Multi", "Diamenty", "Young Multi Diamenty Diamenty official audio", "hiphop"),
            ("Bedoes", "1998", "Bedoes 1998 Opowieści z Doliny Smoków official audio", "hiphop"),
            ("Bedoes", "Zanim wstanie dzień", "Bedoes Zanim wstanie dzień Kwiat polskiej młodzieży official audio", "hiphop"),
            ("Quebonafide", "Bumerang", "Quebonafide Bumerang Eklektyka official audio", "hiphop"),
            ("Quebonafide", "Luis Nazario de Lima", "Quebonafide Luis Nazario de Lima Egzotyka official audio", "hiphop"),
            ("Tymek", "Rainman", "Tymek Rainman Tymek official audio", "hiphop"),
            ("Tymek", "Anioły i demony", "Tymek Anioły i demony Tymek official audio", "hiphop"),
            ("Sobel", "Drobna zabawa", "Sobel Drobna zabawa Pułapka na motyle official audio", "hiphop"),
            ("Sobel", "Alien", "Sobel Alien Pułapka na motyle official audio", "hiphop"),
            ("Oki", "Jakie to uczucie", "Oki Jakie to uczucie 47playground official audio", "hiphop"),
            ("Oki", "Dla mnie", "Oki Dla mnie 47playground official audio", "hiphop"),
            ("Żabson", "Floyd Mayweather", "Żabson Floyd Mayweather Internaziomal official audio", "hiphop"),
            ("Żabson", "Sekret", "Żabson Sekret Internaziomal official audio", "hiphop"),
            ("Kukon", "Piję w Klubie", "Kukon Piję w Klubie Ogrodowa official audio", "hiphop"),
            ("Kukon", "Dobre czasy", "Kukon Dobre czasy Ogrodowa official audio", "hiphop"),
            ("Białas", "Dzieciaki", "Białas Dzieciaki H8M5 official audio", "hiphop"),
            ("Białas", "Wszystko ok", "Białas Wszystko ok H8M5 official audio", "hiphop"),
            ("Avi", "Góry", "Avi Góry Spis cudzołożnic official audio", "hiphop"),
            ("Avi", "Le petit mort", "Avi Le petit mort Spis cudzołożnic official audio", "hiphop"),
            ("Dawid Podsiadło", "To co masz Ty", "Dawid Podsiadło To co masz Ty Małomiasteczkowy official audio", "popularne"),
            ("Dawid Podsiadło", "Najnowszy klip", "Dawid Podsiadło Najnowszy klip Małomiasteczkowy official audio", "popularne"),
            ("Sanah", "Invisible Dress", "Sanah Invisible Dress Królowa dram official audio", "popularne"),
            ("Sanah", "Kolońska i szlugi", "Sanah Kolońska i szlugi Irenka official audio", "popularne"),
            ("Mrozu", "Jak nie my to kto", "Mrozu Jak nie my to kto Rollercoaster official audio", "popularne"),
            ("Mrozu", "Bohema", "Mrozu Bohema Rollercoaster official audio", "popularne"),
            ("Kortez", "Stąd do Warszawy", "Kortez Stąd do Warszawy Mój dom official audio", "popularne"),
            ("Kortez", "Dobry moment", "Kortez Dobry moment Mój dom official audio", "popularne"),
            ("Daria Zawiałow", "Kaonashi", "Daria Zawiałow Kaonashi Wojny i noce official audio", "popularne"),
            ("Daria Zawiałow", "Malinowy chruśniak", "Daria Zawiałow Malinowy chruśniak A kysz! official audio", "popularne"),
            ("Kwiat Jabłoni", "Wodymidaj", "Kwiat Jabłoni Wodymidaj Mogło być nic official audio", "popularne"),
            ("Kwiat Jabłoni", "Mogło być nic", "Kwiat Jabłoni Mogło być nic Mogło być nic official audio", "popularne"),
            ("Vito Bambino", "Bunkrów nie ma", "Vito Bambino Bunkrów nie ma Poczekalnia official audio", "popularne"),
            ("Vito Bambino", "Uciekaj", "Vito Bambino Uciekaj Poczekalnia official audio", "popularne"),
            ("Brodka", "Up In The Hill", "Brodka Up In The Hill Brut official audio", "popularne"),
            ("Brodka", "Wszystko czego dziś chcę", "Brodka Wszystko czego dziś chcę Wszystko czego dziś chcę official audio", "popularne"),
            ("Ralph Kaminski", "Autobusy", "Ralph Kaminski Autobusy Pies official audio", "popularne"),
            ("Ralph Kaminski", "Bal u Rafała", "Ralph Kaminski Bal u Rafała Bal u Rafała official audio", "popularne"),
            ("Artur Rojek", "Beksa", "Artur Rojek Beksa Składam się z ciągłych powtórzeń official audio", "popularne"),
            ("Artur Rojek", "Sportowe życie", "Artur Rojek Sportowe życie Składam się z ciągłych powtórzeń official audio", "popularne"),
            ("Krzysztof Zalewski", "Kurier", "Krzysztof Zalewski Kurier Kurier official audio", "popularne"),
            ("Krzysztof Zalewski", "Polsko", "Krzysztof Zalewski Polsko Zalewski Złoto official audio", "popularne"),
            ("Kaśka Sochacka", "Wiśniewa", "Kaśka Sochacka Wiśniewa Ciche dni official audio", "popularne"),
            ("Kaśka Sochacka", "Boje się o ciebie", "Kaśka Sochacka Boje się o ciebie Ciche dni official audio", "popularne"),
            ("Nosowska", "Ja pas", "Nosowska Ja pas Brawa dla Państwa official audio", "popularne"),
            ("Nosowska", "Karat", "Nosowska Karat Brawa dla Państwa official audio", "popularne"),
            ("Natalia Przybysz", "Nazywam się niebo", "Natalia Przybysz Nazywam się niebo Prąd official audio", "popularne"),
            ("Natalia Przybysz", "Królowa śniegu", "Natalia Przybysz Królowa śniegu Prąd official audio", "popularne"),
            ("Mery Spolsky", "Miło było panią poznać", "Mery Spolsky Miło było panią poznać Dekalog Mery Spolsky official audio", "popularne"),
            ("Mery Spolsky", "Ukąszenie", "Mery Spolsky Ukąszenie Dekalog Mery Spolsky official audio", "popularne"),
            ("Margaret", "Byle jak", "Margaret Byle jak Gaja Hornby official audio", "popularne"),
            ("Margaret", "In My Cabana", "Margaret In My Cabana In My Cabana official audio", "popularne"),
            ("Roksana Węgiel", "Lay Low", "Roksana Węgiel Lay Low Roksana Węgiel official audio", "popularne"),
            ("Viki Gabor", "Afera", "Viki Gabor Afera Getaway official audio", "popularne"),
            ("Sylwia Grzeszczak", "Małe rzeczy", "Sylwia Grzeszczak Małe rzeczy Sen o przyszłości official audio", "popularne"),
            ("Sylwia Grzeszczak", "Flagi serc", "Sylwia Grzeszczak Flagi serc Tamta dziewczyna official audio", "popularne"),
            ("Ewa Farna", "Bumerang", "Ewa Farna Bumerang Ewakuacja official audio", "popularne"),
            ("Ewa Farna", "Bez łez", "Ewa Farna Bez łez Cicho official audio", "popularne"),
            ("Cleo", "Łowcy gwiazd", "Cleo Łowcy gwiazd Supernova official audio", "popularne"),
            ("Donatan & Cleo", "Brać", "Donatan Cleo Brać Hiper/Chimera official audio", "popularne"),
            ("Smolasty", "Fake Love", "Smolasty Fake Love Ghetto Playboy official audio", "popularne"),
            ("Tribbs", "Piękna młoda", "Tribbs Piękna młoda Piękna młoda official audio", "popularne"),
            ("Oskar Cyms", "Niech mi ktoś powiedzieć", "Oskar Cyms Niech mi ktoś powiedzieć Niech mi ktoś official audio", "popularne"),
            ("Blanka", "Cara Mia", "Blanka Cara Mia Cara Mia official audio", "popularne"),
            ("Jann", "Need a Girl", "Jann Need a Girl Need a Girl official audio", "popularne"),
            ("Bryska", "Lato (p*epie je)", "Bryska Lato Bryska official audio", "popularne"),
            ("Krystian Ochman", "Światłocienie", "Krystian Ochman Światłocienie Ochman official audio", "popularne"),
            ("Michał Szpak", "Real Hero", "Michał Szpak Real Hero Real Hero official audio", "popularne"),
            ("Gromee", "One Last Time", "Gromee One Last Time Light Me Up official audio", "popularne"),
            ("C-BooL", "Catch", "C-BooL Catch Catch official audio", "popularne"),
            ("Doda", "Fake Love", "Doda Fake Love Aquaria official audio", "popularne"),
            ("Ewelina Lisowska", "Jutra nie będzie", "Ewelina Lisowska Jutra nie będzie Aero-Plan official audio", "popularne"),
            ("Jula", "Nie zatrzymasz mnie", "Jula Nie zatrzymasz mnie Na krawędzi official audio", "popularne"),
            ("Sarsa", "Indiana", "Sarsa Indiana Zapomnij mi official audio", "popularne"),
            ("Ania Dąbrowska", "Charlie, Charlie", "Ania Dąbrowska Charlie, Charlie Bawię się świetnie official audio", "popularne"),
            ("Natalia Szroeder", "Powietrze", "Natalia Szroeder Powietrze NATinterpretacje official audio", "popularne"),
            ("Lanberry", "Każdy moment", "Lanberry Każdy moment Piątek official audio", "popularne"),
            ("Reni Jusis", "Kiedyś Cię znajdę", "Reni Jusis Kiedyś Cię znajdę Zakręcona official audio", "popularne"),
            ("Kasia Cerekwicka", "S.O.S.", "Kasia Cerekwicka S.O.S. Feniks official audio", "popularne"),
            ("Paweł Domagała", "Czasami", "Paweł Domagała Czasami 1984 official audio", "popularne"),
            ("Kamil Bednarek", "Chwile jak te", "Kamil Bednarek Chwile jak te Jestem official audio", "popularne"),
            ("Enej", "Lili", "Enej Lili Folkhorod official audio", "popularne"),
            ("Enej", "Symetryczno-Liryczna", "Enej Symetryczno-Liryczna Folkhorod official audio", "popularne"),
            ("LemON", "Będę z Tobą", "LemON Będę z Tobą Scarlett official audio", "popularne"),
            ("Mesajah", "Lepsza połowa", "Mesajah Lepsza połowa Ludzie prości official audio", "popularne"),
            ("Krzysztof Krawczyk", "Mój przyjacielu", "Krzysztof Krawczyk Mój przyjacielu Bo jesteś ty official audio", "klasyki"),
            ("Krzysztof Krawczyk", "Za Tobą pójdę jak na bal", "Krzysztof Krawczyk Za Tobą pójdę jak na bal Parostatek official audio", "klasyki"),
            ("Lady Pank", "Wciąż bardziej obcy", "Lady Pank Wciąż bardziej obcy Lady Pank official audio", "klasyki"),
            ("Lady Pank", "Fabryka małp", "Lady Pank Fabryka małp Lady Pank official audio", "klasyki"),
            ("Perfect", "Chcemy być sobą", "Perfect Chcemy być sobą Perfect official audio", "klasyki"),
            ("Dżem", "Wehikuł czasu", "Dżem Wehikuł czasu Cegła official audio", "klasyki"),
            ("Dżem", "List do M.", "Dżem List do M. Cegła official audio", "klasyki"),
            ("Maanam", "Lucciola", "Maanam Lucciola Nocny patrol official audio", "klasyki"),
            ("Kombi", "Black and White", "Kombi Black and White Kombi official audio", "klasyki"),
            ("Lombard", "Adriatyk, ocean gorący", "Lombard Adriatyk, ocean gorący Szklana pogoda official audio", "klasyki"),
            ("T.Love", "Ajrisz", "T.Love Ajrisz Chłopaki nie płaczą official audio", "klasyki"),
            ("Kult", "Brooklyńska rada żydów", "Kult Brooklyńska rada żydów Ostateczny krach systemu korporacji official audio", "klasyki"),
            ("Kult", "Lewy czerwcowy", "Kult Lewy czerwcowy Ostateczny krach systemu korporacji official audio", "klasyki"),
            ("Hey", "Teksański", "Hey Teksański Fire official audio", "klasyki"),
            ("Wilki", "Son of the Blue Sky", "Wilki Son of the Blue Sky Wilki official audio", "klasyki"),
            ("KęKę", "Zgoda", "KęKę Zgoda Trzecie rzeczy official audio", "hiphop"),
            ("KęKę", "Takie rzeczy", "KęKę Takie rzeczy Takie rzeczy official audio", "hiphop"),
            ("Ten Typ Mes", "Głupia piosenka", "Ten Typ Mes Głupia piosenka Kandydaci na szaleńców official audio", "hiphop"),
            ("Ten Typ Mes", "Mieć czy być", "Ten Typ Mes Mieć czy być Alkopoligamia official audio", "hiphop"),
            ("VNM", "Obiecana", "VNM Obiecana Pro official audio", "hiphop"),
            ("VNM", "Kilka dni", "VNM Kilka dni Halflife official audio", "hiphop"),
            ("Małpa", "Supa Dupa Fly", "Małpa Supa Dupa Fly Kilka numerów o czymś official audio", "hiphop"),
            ("Małpa", "Filigranowe szczęście", "Małpa Filigranowe szczęście Kilka numerów o czymś official audio", "hiphop"),
            ("BisZ", "Koniec", "Bisz Koniec Wilk chodnikowy official audio", "hiphop"),
            ("BisZ", "Indygo", "Bisz Indygo Wilk chodnikowy official audio", "hiphop"),
            ("Hades", "Światła miasta", "Hades Światła miasta Nowe dobro to zło official audio", "hiphop"),
            ("Hades", "Właśnie tak", "Hades Właśnie tak Nowe dobro to zło official audio", "hiphop"),
            ("Sarius", "Złoty chłopak", "Sarius Złoty chłopak Antihype official audio", "hiphop"),
            ("Sarius", "Wiktoria", "Sarius Wiktoria Antihype official audio", "hiphop"),
            ("Dwa Sławy", "Tom Cruise", "Dwa Sławy Tom Cruise Dandys status official audio", "hiphop"),
            ("Dwa Sławy", "Cukier", "Dwa Sławy Cukier Dandys status official audio", "hiphop"),
            ("Rasmentalism", "Dobre dni", "Rasmentalism Dobre dni Za młodzi na Heroda official audio", "hiphop"),
            ("Rasmentalism", "Nie mam czasu", "Rasmentalism Nie mam czasu Za młodzi na Heroda official audio", "hiphop"),
            ("Parias", "Ona", "Parias Ona Parias official audio", "hiphop"),
            ("Parias", "Dzień dobry", "Parias Dzień dobry Parias official audio", "hiphop"),
            ("W.E.N.A.", "Wszystko ok", "W.E.N.A. Wszystko ok Nowa definicja official audio", "hiphop"),
            ("W.E.N.A.", "Ważne", "W.E.N.A. Ważne Niepamięć official audio", "hiphop"),
            ("Tau", "Bóg jest wielki", "Tau Bóg jest wielki Remedium official audio", "hiphop"),
            ("Tau", "Raper", "Tau Raper Remedium official audio", "hiphop"),
            ("Kabe", "Złoto", "Kabe Złoto King Kong official audio", "hiphop"),
            ("Kabe", "Albinos", "Kabe Albinos King Kong official audio", "hiphop"),
            ("White 2115", "California", "White 2115 California California official audio", "hiphop"),
            ("White 2115", "Więcej", "White 2115 Więcej Młody Łajcior official audio", "hiphop"),
            ("Mata", "Blumental", "Mata Blumental Młody Matczak official audio", "hiphop"),
            ("Mata", "Prawda", "Mata Prawda Młody Matczak official audio", "hiphop"),
            ("Young Multi", "Plecak", "Young Multi Plecak Plecak official audio", "hiphop"),
            ("Young Multi", "Diamenty", "Young Multi Diamenty Diamenty official audio", "hiphop"),
            ("Bedoes", "1998", "Bedoes 1998 Opowieści z Doliny Smoków official audio", "hiphop"),
            ("Bedoes", "Zanim wstanie dzień", "Bedoes Zanim wstanie dzień Kwiat polskiej młodzieży official audio", "hiphop"),
            ("Quebonafide", "Bumerang", "Quebonafide Bumerang Eklektyka official audio", "hiphop"),
            ("Quebonafide", "Luis Nazario de Lima", "Quebonafide Luis Nazario de Lima Egzotyka official audio", "hiphop"),
            ("Tymek", "Rainman", "Tymek Rainman Tymek official audio", "hiphop"),
            ("Tymek", "Anioły i demony", "Tymek Anioły i demony Tymek official audio", "hiphop"),
            ("Sobel", "Drobna zabawa", "Sobel Drobna zabawa Pułapka na motyle official audio", "hiphop"),
            ("Sobel", "Alien", "Sobel Alien Pułapka na motyle official audio", "hiphop"),
            ("Oki", "Jakie to uczucie", "Oki Jakie to uczucie 47playground official audio", "hiphop"),
            ("Oki", "Dla mnie", "Oki Dla mnie 47playground official audio", "hiphop"),
            ("Żabson", "Floyd Mayweather", "Żabson Floyd Mayweather Internaziomal official audio", "hiphop"),
            ("Żabson", "Sekret", "Żabson Sekret Internaziomal official audio", "hiphop"),
            ("Kukon", "Piję w Klubie", "Kukon Piję w Klubie Ogrodowa official audio", "hiphop"),
            ("Kukon", "Dobre czasy", "Kukon Dobre czasy Ogrodowa official audio", "hiphop"),
            ("Białas", "Dzieciaki", "Białas Dzieciaki H8M5 official audio", "hiphop"),
            ("Białas", "Wszystko ok", "Białas Wszystko ok H8M5 official audio", "hiphop"),
            ("Avi", "Góry", "Avi Góry Spis cudzołożnic official audio", "hiphop"),
            ("Avi", "Le petit mort", "Avi Le petit mort Spis cudzołożnic official audio", "hiphop"),
            ("Dawid Podsiadło", "To co masz Ty", "Dawid Podsiadło To co masz Ty Małomiasteczkowy official audio", "popularne"),
            ("Dawid Podsiadło", "Najnowszy klip", "Dawid Podsiadło Najnowszy klip Małomiasteczkowy official audio", "popularne"),
            ("Sanah", "Invisible Dress", "Sanah Invisible Dress Królowa dram official audio", "popularne"),
            ("Sanah", "Kolońska i szlugi", "Sanah Kolońska i szlugi Irenka official audio", "popularne"),
            ("Mrozu", "Jak nie my to kto", "Mrozu Jak nie my to kto Rollercoaster official audio", "popularne"),
            ("Mrozu", "Bohema", "Mrozu Bohema Rollercoaster official audio", "popularne"),
            ("Kortez", "Stąd do Warszawy", "Kortez Stąd do Warszawy Mój dom official audio", "popularne"),
            ("Kortez", "Dobry moment", "Kortez Dobry moment Mój dom official audio", "popularne"),
            ("Daria Zawiałow", "Kaonashi", "Daria Zawiałow Kaonashi Wojny i noce official audio", "popularne"),
            ("Daria Zawiałow", "Malinowy chruśniak", "Daria Zawiałow Malinowy chruśniak A kysz! official audio", "popularne"),
            ("Kwiat Jabłoni", "Wodymidaj", "Kwiat Jabłoni Wodymidaj Mogło być nic official audio", "popularne"),
            ("Kwiat Jabłoni", "Mogło być nic", "Kwiat Jabłoni Mogło być nic Mogło być nic official audio", "popularne"),
            ("Vito Bambino", "Bunkrów nie ma", "Vito Bambino Bunkrów nie ma Poczekalnia official audio", "popularne"),
            ("Vito Bambino", "Uciekaj", "Vito Bambino Uciekaj Poczekalnia official audio", "popularne"),
            ("Brodka", "Up In The Hill", "Brodka Up In The Hill Brut official audio", "popularne"),
            ("Brodka", "Wszystko czego dziś chcę", "Brodka Wszystko czego dziś chcę Wszystko czego dziś chcę official audio", "popularne"),
            ("Ralph Kaminski", "Autobusy", "Ralph Kaminski Autobusy Pies official audio", "popularne"),
            ("Ralph Kaminski", "Bal u Rafała", "Ralph Kaminski Bal u Rafała Bal u Rafała official audio", "popularne"),
            ("Artur Rojek", "Beksa", "Artur Rojek Beksa Składam się z ciągłych powtórzeń official audio", "popularne"),
            ("Artur Rojek", "Sportowe życie", "Artur Rojek Sportowe życie Składam się z ciągłych powtórzeń official audio", "popularne"),
            ("Krzysztof Zalewski", "Kurier", "Krzysztof Zalewski Kurier Kurier official audio", "popularne"),
            ("Krzysztof Zalewski", "Polsko", "Krzysztof Zalewski Polsko Zalewski Złoto official audio", "popularne"),
            ("Kaśka Sochacka", "Wiśniewa", "Kaśka Sochacka Wiśniewa Ciche dni official audio", "popularne"),
            ("Kaśka Sochacka", "Boje się o ciebie", "Kaśka Sochacka Boje się o ciebie Ciche dni official audio", "popularne"),
            ("Nosowska", "Ja pas", "Nosowska Ja pas Brawa dla Państwa official audio", "popularne"),
            ("Nosowska", "Karat", "Nosowska Karat Brawa dla Państwa official audio", "popularne"),
            ("Natalia Przybysz", "Nazywam się niebo", "Natalia Przybysz Nazywam się niebo Prąd official audio", "popularne"),
            ("Natalia Przybysz", "Królowa śniegu", "Natalia Przybysz Królowa śniegu Prąd official audio", "popularne"),
            ("Mery Spolsky", "Miło było panią poznać", "Mery Spolsky Miło było panią poznać Dekalog Mery Spolsky official audio", "popularne"),
            ("Mery Spolsky", "Ukąszenie", "Mery Spolsky Ukąszenie Dekalog Mery Spolsky official audio", "popularne"),
            ("Margaret", "Byle jak", "Margaret Byle jak Gaja Hornby official audio", "popularne"),
            ("Margaret", "In My Cabana", "Margaret In My Cabana In My Cabana official audio", "popularne"),
            ("Roksana Węgiel", "Lay Low", "Roksana Węgiel Lay Low Roksana Węgiel official audio", "popularne"),
            ("Viki Gabor", "Afera", "Viki Gabor Afera Getaway official audio", "popularne"),
            ("Sylwia Grzeszczak", "Małe rzeczy", "Sylwia Grzeszczak Małe rzeczy Sen o przyszłości official audio", "popularne"),
            ("Sylwia Grzeszczak", "Flagi serc", "Sylwia Grzeszczak Flagi serc Tamta dziewczyna official audio", "popularne"),
            ("Ewa Farna", "Bumerang", "Ewa Farna Bumerang Ewakuacja official audio", "popularne"),
            ("Ewa Farna", "Bez łez", "Ewa Farna Bez łez Cicho official audio", "popularne"),
            ("Cleo", "Łowcy gwiazd", "Cleo Łowcy gwiazd Supernova official audio", "popularne"),
            ("Donatan & Cleo", "Brać", "Donatan Cleo Brać Hiper/Chimera official audio", "popularne"),
            ("Smolasty", "Fake Love", "Smolasty Fake Love Ghetto Playboy official audio", "popularne"),
            ("Tribbs", "Piękna młoda", "Tribbs Piękna młoda Piękna młoda official audio", "popularne"),
            ("Oskar Cyms", "Niech mi ktoś powiedzieć", "Oskar Cyms Niech mi ktoś powiedzieć Niech mi ktoś official audio", "popularne"),
            ("Blanka", "Cara Mia", "Blanka Cara Mia Cara Mia official audio", "popularne"),
            ("Jann", "Need a Girl", "Jann Need a Girl Need a Girl official audio", "popularne"),
            ("Bryska", "Lato (p*epie je)", "Bryska Lato Bryska official audio", "popularne"),
            ("Krystian Ochman", "Światłocienie", "Krystian Ochman Światłocienie Ochman official audio", "popularne"),
            ("Michał Szpak", "Real Hero", "Michał Szpak Real Hero Real Hero official audio", "popularne"),
            ("Gromee", "One Last Time", "Gromee One Last Time Light Me Up official audio", "popularne"),
            ("C-BooL", "Catch", "C-BooL Catch Catch official audio", "popularne"),
            ("Doda", "Fake Love", "Doda Fake Love Aquaria official audio", "popularne"),
            ("Ewelina Lisowska", "Jutra nie będzie", "Ewelina Lisowska Jutra nie będzie Aero-Plan official audio", "popularne"),
            ("Jula", "Nie zatrzymasz mnie", "Jula Nie zatrzymasz mnie Na krawędzi official audio", "popularne"),
            ("Sarsa", "Indiana", "Sarsa Indiana Zapomnij mi official audio", "popularne"),
            ("Ania Dąbrowska", "Charlie, Charlie", "Ania Dąbrowska Charlie, Charlie Bawię się świetnie official audio", "popularne"),
            ("Natalia Szroeder", "Powietrze", "Natalia Szroeder Powietrze NATinterpretacje official audio", "popularne"),
            ("Lanberry", "Każdy moment", "Lanberry Każdy moment Piątek official audio", "popularne"),
            ("Reni Jusis", "Kiedyś Cię znajdę", "Reni Jusis Kiedyś Cię znajdę Zakręcona official audio", "popularne"),
            ("Kasia Cerekwicka", "S.O.S.", "Kasia Cerekwicka S.O.S. Feniks official audio", "popularne"),
            ("Paweł Domagała", "Czasami", "Paweł Domagała Czasami 1984 official audio", "popularne"),
            ("Kamil Bednarek", "Chwile jak te", "Kamil Bednarek Chwile jak te Jestem official audio", "popularne"),
            ("Enej", "Lili", "Enej Lili Folkhorod official audio", "popularne"),
            ("Enej", "Symetryczno-Liryczna", "Enej Symetryczno-Liryczna Folkhorod official audio", "popularne"),
            ("LemON", "Będę z Tobą", "LemON Będę z Tobą Scarlett official audio", "popularne"),
            ("Mesajah", "Lepsza połowa", "Mesajah Lepsza połowa Ludzie prości official audio", "popularne"),
            ("Krzysztof Krawczyk", "Mój przyjacielu", "Krzysztof Krawczyk Mój przyjacielu Bo jesteś ty official audio", "klasyki"),
            ("Krzysztof Krawczyk", "Za Tobą pójdę jak na bal", "Krzysztof Krawczyk Za Tobą pójdę jak na bal Parostatek official audio", "klasyki"),
            ("Lady Pank", "Wciąż bardziej obcy", "Lady Pank Wciąż bardziej obcy Lady Pank official audio", "klasyki"),
            ("Lady Pank", "Fabryka małp", "Lady Pank Fabryka małp Lady Pank official audio", "klasyki"),
            ("Perfect", "Chcemy być sobą", "Perfect Chcemy być sobą Perfect official audio", "klasyki"),
            ("Dżem", "Wehikuł czasu", "Dżem Wehikuł czasu Cegła official audio", "klasyki"),
            ("Dżem", "List do M.", "Dżem List do M. Cegła official audio", "klasyki"),
            ("Maanam", "Lucciola", "Maanam Lucciola Nocny patrol official audio", "klasyki"),
            ("Kombi", "Black and White", "Kombi Black and White Kombi official audio", "klasyki"),
            ("Lombard", "Adriatyk, ocean gorący", "Lombard Adriatyk, ocean gorący Szklana pogoda official audio", "klasyki"),
            ("T.Love", "Ajrisz", "T.Love Ajrisz Chłopaki nie płaczą official audio", "klasyki"),
            ("Kult", "Brooklyńska rada żydów", "Kult Brooklyńska rada żydów Ostateczny krach systemu korporacji official audio", "klasyki"),
            ("Kult", "Lewy czerwcowy", "Kult Lewy czerwcowy Ostateczny krach systemu korporacji official audio", "klasyki"),
            ("Hey", "Teksański", "Hey Teksański Fire official audio", "klasyki"),
            ("Wilki", "Son of the Blue Sky", "Wilki Son of the Blue Sky Wilki official audio", "klasyki")
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
    cursor.execute("SELECT DISTINCT artist, title FROM songs")
    rows = cursor.fetchall()
    conn.close()
    
    # Łączymy artystę i tytuł w jeden ładny string
    return [f"{row[0]} - {row[1]}" for row in rows]