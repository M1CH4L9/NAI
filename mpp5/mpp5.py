import math
import random

def wczytaj_dane(nazwa_pliku):
    #listy na wartosci i etykiety
    dane = []
    etykiety = []
    
    with open(nazwa_pliku, 'r') as plik:
        for linia in plik:
            #czyszcze biale znaki
            linia = linia.strip()
            if len(linia) == 0:
                continue
                
            #split() bez argumentu dzieli po spacjach i tabulatorach
            czesci = linia.split()
            
            #ostatni element to zawsze gatunek irysa
            gatunek = czesci[-1]
            etykiety.append(gatunek)
            
            #reszte zamieniam na floaty bo to wymiary
            cechy = []
            for i in range(len(czesci) - 1):
                #zamieniam przecinek na kropke zeby float() nie wywalil bledu
                wartosc_z_kropka = czesci[i].replace(',', '.')
                cechy.append(float(wartosc_z_kropka))
            
            #dodaje wyciagniete cechy do glownej listy
            dane.append(cechy)
            
    return dane, etykiety

def k_means():
    #wczytuje plik treningowy
    dane, etykiety = wczytaj_dane('iris_training.txt') 
    
    #pobieram k od usera
    k = int(input("Podaj liczbę klastrów (k): "))
    
    #losuje poczatkowe centroidy ze zbioru
    centroidy = random.sample(dane, k)
    
    iteracja = 1
    
    while True:
        #przygotowuje puste listy na poszczegolne klastry
        grupy = []
        for _ in range(k):
            grupy.append([])
            
        suma_kwadratow = 0.0
        
        #przypisuje punkty do najblizszego centroidu
        for i in range(len(dane)):
            punkt = dane[i]
            
            #poczatkowo ustawiam na nieskonczonosc
            najmniejsza_odleglosc = float('inf')
            najlepsza_grupa = 0
            
            #szukam najblizszego
            for c in range(k):
                odleglosc = 0.0
                #licze kwadrat odleglosci euklidesowej
                for wymiar in range(len(punkt)):
                    odleglosc += (punkt[wymiar] - centroidy[c][wymiar]) ** 2
                
                if odleglosc < najmniejsza_odleglosc:
                    najmniejsza_odleglosc = odleglosc
                    najlepsza_grupa = c
            
            #dodaje indeks punktu do odpowiedniej grupy i aktualizuje sume
            grupy[najlepsza_grupa].append(i)
            suma_kwadratow += najmniejsza_odleglosc
            
        print(f"Iteracja {iteracja}: Suma kwadratów odległości = {suma_kwadratow}")
        
        #licze nowe srodki klastrow
        nowe_centroidy = []
        for c in range(k):
            #jak do grupy nic nie trafilo to zostawiam stary srodek
            if len(grupy[c]) == 0:
                nowe_centroidy.append(centroidy[c])
                continue
                
            #wektor samych zer do sumowania wymiarow
            nowy_srodek = [0.0 for _ in range(len(dane[0]))]
            
            #sumuje cechy dla danego klastra
            for indeks in grupy[c]:
                punkt = dane[indeks]
                for wymiar in range(len(punkt)):
                    nowy_srodek[wymiar] += punkt[wymiar]
                    
            #wyliczam srednia
            for wymiar in range(len(nowy_srodek)):
                nowy_srodek[wymiar] /= len(grupy[c])
                
            nowe_centroidy.append(nowy_srodek)
            
        #warunek stopu jesli centroidy sie juz nie ruszaja
        if centroidy == nowe_centroidy:
            break
            
        #podmieniam zmienne na kolejna petle
        centroidy = nowe_centroidy
        iteracja += 1
        
    print("\n--- ALGORYTM ZAKOŃCZONY ---")
    
    #wypisuje sklady klastrow i licze ich entropie
    for c in range(k):
        print(f"\nKLASTER {c+1}:")
        
        #slownik do zliczania gatunkow
        licznik_gatunkow = {}
        
        print("Skład klastra (wypisuję nazwy gatunków i ich wartości):")
        for indeks in grupy[c]:
            gatunek = etykiety[indeks]
            wartosci = dane[indeks]
            print(f" - {wartosci} -> {gatunek}") 
            
            #zliczam konkretny gatunek
            if gatunek in licznik_gatunkow:
                licznik_gatunkow[gatunek] += 1
            else:
                licznik_gatunkow[gatunek] = 1
                
        ile_w_klastrze = len(grupy[c])
        entropia = 0.0
        
        #obliczam z wzoru na entropie
        if ile_w_klastrze > 0:
            for gatunek, ilosc in licznik_gatunkow.items():
                p = ilosc / ile_w_klastrze
                entropia -= p * math.log2(p)
                
        print(f"> Zliczono gatunki: {licznik_gatunkow}")
        print(f"> Entropia klastra: {entropia}")

def zadanie_entropia_z_klawiatury():
    print("\n--- ZADANIE Z ĆWICZEŃ: ENTROPIA ROZKŁADU ---")
    tekst = input("Podaj częstości (np. 10 5 5), oddzielone spacjami i wciśnij Enter:\n")
    
    #dziele stringa po spacji
    elementy = tekst.split()
    
    #rzutuje to co wpisal uzytkownik na float
    czestosci = []
    for element in elementy:
        czestosci.append(float(element))
        
    #licze sume calkowita
    suma_czestosci = 0.0
    for c in czestosci:
        suma_czestosci += c
        
    entropia = 0.0
    for c in czestosci:
        #pomijam zera zeby nie bylo bledu w logarytmie
        if c > 0:
            prawdopodobienstwo = c / suma_czestosci
            entropia -= prawdopodobienstwo * math.log2(prawdopodobienstwo)
            
    print(f"Entropia podanego rozkładu wynosi: {entropia}")

if __name__ == "__main__":
    k_means()
    zadanie_entropia_z_klawiatury()


#!!!
#IF Z ZAPĘTLENIEM, JEŻELI TRZEBA
#!!!

# if __name__ == "__main__":
#     while True:
#         # Odpalamy główny algorytm
#         k_means()
        
#         # Odpalamy zadanie z ćwiczeń
#         zadanie_entropia_z_klawiatury()
        
#         print("\n" + "="*40)
#         wybor = input("Czy chcesz uruchomić program ponownie? (wpisz 'nie' aby wyjść, lub cokolwiek innego aby kontynuować): ")
        
#         if wybor.strip().lower() == 'nie':
#             print("Zamykanie programu...")
#             break
#         print("="*40 + "\n")
