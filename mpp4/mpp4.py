# Funkcja wczytująca pliki - przekopiowana z mpp1/mpp2 (z drobną modyfikacją by wczytać pliki mpp4)
def wczytajDane(nazwaPliku):
    dane = []
    with open(nazwaPliku, 'r') as plik:
        for linia in plik:
            linia = linia.strip()
            if not linia:
                continue

            elementy = linia.split()
            # gatunek to ostatnia kolumna
            gatunek = elementy.pop()

            wymiary = []
            for x in elementy:
                wymiary.append(float(x.replace(',', '.')))
            
            dane.append((wymiary, gatunek))

    return dane

# Główna funkcja klasyfikatora Naiwnego Bayesa
def klasyfikujBayes(wektor, daneTreningowe, unikalneGatunki, unikalneWartosciAtrybutu1, wypiszWygladzanie=False):
    najlepszyGatunek = None
    najwiekszePrawdopodobienstwo = -1.0 # Prawdopodobieństwo nie zejdzie poniżej 0

    for gatunek in unikalneGatunki:
        # 1. Prawdopodobieństwo a priori klasy P(C) - ile tego gatunku jest w całym zbiorze
        iloscWKlasie = 0
        for w, g in daneTreningowe:
            if g == gatunek:
                iloscWKlasie += 1
                
        prawdopodobienstwoKlasy = iloscWKlasie / len(daneTreningowe)

        # 2. Prawdopodobieństwo warunkowe P(x|C)
        prawdopodobienstwoWarunkowe = 1.0

        for i in range(len(wektor)):
            # Ręczne zliczanie wystąpień konkretnej wartości cechy dla danego gatunku
            iloscWystapien = 0
            for w, g in daneTreningowe:
                if g == gatunek and w[i] == wektor[i]:
                    iloscWystapien += 1

            if i == 0:
                # --- Wygładzanie Laplace'a TYLKO dla pierwszego atrybutu (zgodnie z poleceniem) ---
                p_przed = iloscWystapien / iloscWKlasie
                # Do licznika dodajemy 1, a do mianownika liczbę unikalnych wartości tej cechy
                p_po = (iloscWystapien + 1) / (iloscWKlasie + len(unikalneWartosciAtrybutu1))
                
                prawdopodobienstwoWarunkowe *= p_po

                if wypiszWygladzanie:
                    print(f"   [Wygładzanie - {gatunek}] Atrybut 1 (wartość {wektor[i]}): P(przed) = {p_przed:.4f} -> P(po) = {p_po:.4f}")
            else:
                # --- Brak wygładzania dla reszty atrybutów ---
                if iloscWystapien == 0:
                    # Żeby nie mnożyć przez 0 (co zepsułoby cały wynik), dajemy bardzo małą liczbę
                    prawdopodobienstwoWarunkowe *= 0.000001
                else:
                    prawdopodobienstwoWarunkowe *= (iloscWystapien / iloscWKlasie)

        # 3. Mnożymy wszystko razem: P(C|x) = P(C) * P(x1|C) * P(x2|C)...
        prawdopodobienstwoCalkowite = prawdopodobienstwoKlasy * prawdopodobienstwoWarunkowe

        # Wybieramy gatunek, który osiągnął najwyższy wynik
        if prawdopodobienstwoCalkowite > najwiekszePrawdopodobienstwo:
            najwiekszePrawdopodobienstwo = prawdopodobienstwoCalkowite
            najlepszyGatunek = gatunek

    return najlepszyGatunek


# -------------------------------------------------------------
# GŁÓWNA CZĘŚĆ PROGRAMU
# -------------------------------------------------------------

# Wczytywanie danych
daneTreningowe = wczytajDane('iris_training.txt')
daneTestowe = wczytajDane('iris_test.txt')

liczbaAtrybutow = len(daneTreningowe[0][0])

# Szukamy unikalnych gatunków (żeby wiedzieć jakie są)
unikalneGatunki = []
for wymiary, gatunek in daneTreningowe:
    if gatunek not in unikalneGatunki:
        unikalneGatunki.append(gatunek)

# Szukamy unikalnych wartości dla pierwszego atrybutu (potrzebne do wygładzania)
unikalneWartosciAtrybutu1 = []
for wymiary, gatunek in daneTreningowe:
    if wymiary[0] not in unikalneWartosciAtrybutu1:
        unikalneWartosciAtrybutu1.append(wymiary[0])

# Raport wygładzania przed głównym testowaniem (dla pierwszej lepszej wartości z brzegu)
print("\n=== RAPORT WYGŁADZANIA (Atrybut 1) ===")
przykladowaWartosc = unikalneWartosciAtrybutu1[0]
for gatunek in unikalneGatunki:
    iloscWKlasie = 0
    for w, g in daneTreningowe:
        if g == gatunek:
            iloscWKlasie += 1
            
    iloscWystapien = 0
    for w, g in daneTreningowe:
        if g == gatunek and w[0] == przykladowaWartosc:
            iloscWystapien += 1
            
    p_przed = iloscWystapien / iloscWKlasie
    p_po = (iloscWystapien + 1) / (iloscWKlasie + len(unikalneWartosciAtrybutu1))
    print(f"Klasa: {gatunek:15} | Wartość cechy: {przykladowaWartosc} | P(przed) = {p_przed:.4f} | P(po) = {p_po:.4f}")


# Przygotowanie słownika na macierz omyłek
macierzOmylek = {}
for g1 in unikalneGatunki:
    macierzOmylek[g1] = {}
    for g2 in unikalneGatunki:
        macierzOmylek[g1][g2] = 0

# Testowanie na całym zbiorze testowym
poprawne = 0
wszystkie = len(daneTestowe)

for wektorTestowy, prawdziwyGatunek in daneTestowe:
    # Wypiszemy wygładzanie na ekran tylko dla ręcznego wpisywania, żeby tutaj nie zaspamować konsoli
    zgadniety = klasyfikujBayes(wektorTestowy, daneTreningowe, unikalneGatunki, unikalneWartosciAtrybutu1, wypiszWygladzanie=False)
    
    # Dodajemy do macierzy omyłek informację co było naprawdę, a co wymyślił program
    macierzOmylek[prawdziwyGatunek][zgadniety] += 1
    
    if zgadniety == prawdziwyGatunek:
        poprawne += 1

dokladnosc = (poprawne / wszystkie) * 100

print("\n----------Wyniki testu-----------")
print(f"Prawidłowo sklasyfikowanych próbek: {poprawne}")
print(f"Wszystkich próbek: {wszystkie}")
print(f"Dokładność klasyfikacji: {dokladnosc:.2f}%")

print("\n----------Macierz Omyłek---------")
# Rysowanie nagłówków tabeli
naglowki = "Rzeczywisty \\ Przewidziany\t"
for g in unikalneGatunki:
    # Skracam nazwę, żeby się ładnie mieściło w tabeli (np. Iris-setosa -> setosa)
    naglowki += f"{g.split('-')[1]}\t\t"
print(naglowki)

# Rysowanie wierszy macierzy
for prawdziwy in unikalneGatunki:
    wiersz = f"{prawdziwy.split('-')[1]:<25}\t"
    for zgadniety in unikalneGatunki:
        wiersz += f"{macierzOmylek[prawdziwy][zgadniety]}\t\t"
    print(wiersz)
print("----------------------------------\n")

# Interakcja z użytkownikiem (identycznie jak w mpp1/mpp2)
while True:
    print("------------------------------------------")
    nowyWektor = []
    bladWprowadzania = False

    for i in range(liczbaAtrybutow):
        wprowadzonyTekst = input(f"Bardzo proszę, podaj cechę {i+1}: ")
        try:
            nowyWektor.append(float(wprowadzonyTekst.replace(',', '.')))
        except ValueError:
            print(f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Błąd: Wprowadź poprawne liczby.")
            print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            bladWprowadzania = True
            break

    if not bladWprowadzania:
        # W trybie ręcznym pokazujemy jak liczby zmieniają się przy wygładzaniu na bieżąco
        print("\nWyniki wygładzania dla Twojego wektora:")
        wynikKlasyfikacji = klasyfikujBayes(nowyWektor, daneTreningowe, unikalneGatunki, unikalneWartosciAtrybutu1, wypiszWygladzanie=True)
        print(f"\nWynik klasyfikacji Naiwny Bayes: {wynikKlasyfikacji}")

    decyzja = input("\nCzy szanowny osobnik ma życzenie zakończyć działanie tego programu (tak/nie): ")
    if decyzja.strip().lower() in ['tak', 't']:
        print("\nZakończono program. :)")
        break