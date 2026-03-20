def wczytajDane(nazwaPliku):

    dane = []

    with open(nazwaPliku, 'r') as plik:
        for linia in plik:
            linia = linia.strip()
            if not linia:
                continue

            elementy = linia.split()
            #gatunek ostatnia kolumna
            gatunek = elementy.pop()

            wymiary = []
            for x in elementy:
                wymiary.append(float(x.replace(',', '.')))
            
            dane.append((wymiary, gatunek))

    return dane

#twierdzenie pitagorasa
def liczOdleglosc(wektor1, wektor2):
    sumaKwadratow = 0

    for i in range(len(wektor1)):
        roznica = wektor1[i] - wektor2[i]
        sumaKwadratow += roznica ** 2

    odleglosc = sumaKwadratow ** 0.5
    return odleglosc


def klasyfikujKNN(wektorTestowy, daneTreningowe, k):
    odleglosci = []

    for wymiaryTreningowe, gatunekTreningowy in daneTreningowe:
        odleglosc = liczOdleglosc(wektorTestowy, wymiaryTreningowe)
        odleglosci.append((odleglosc, gatunekTreningowy))

    odleglosci.sort()

    najblizsiSasiedzi = odleglosci[:k]

    glosy = {}
    for odleglosc, gatunek in najblizsiSasiedzi:
        if gatunek in glosy:
            glosy[gatunek] += 1
        else:
            glosy[gatunek] = 1

    zwyciezkiGatunek = None
    najwiecejGlosow = 0

    for gatunek, liczbaGlosow in glosy.items():
        if liczbaGlosow > najwiecejGlosow:
            najwiecejGlosow = liczbaGlosow
            zwyciezkiGatunek = gatunek

    return zwyciezkiGatunek





#wczytywanie danych
daneTreningowe = wczytajDane('iris_training.txt')
daneTestowe = wczytajDane('iris_test.txt')


#pobierz k
k = int(input("Podaj wartość k: "))


#testowanie na całym zbiorze testowym
poprawne = 0
wszystkie = len(daneTestowe)

for wektorTestowy, prawdziwyGatunek in daneTestowe:
    zgadniety = klasyfikujKNN(wektorTestowy, daneTreningowe, k)
    if zgadniety == prawdziwyGatunek:
        poprawne += 1

dokladnosc = (poprawne / wszystkie) * 100

print("\n----------Wyniki testu-----------")
print(f"Prawidłowo sklasyfikowanych próbek: {poprawne}")
print(f"Wszystkich próbek: {wszystkie}")
print(f"Dokładność klasyfikacji: {dokladnosc:.2f}%")
print("----------------------------------\n")


liczbaAtrybutow = len(daneTreningowe[0][0])

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
        wynikKlasyfikacji = klasyfikujKNN(nowyWektor, daneTreningowe, k)
        print(f"\nWynik klasyfikacji k-NN: {wynikKlasyfikacji}")

    decyzja = input("\nCzy szanowny osobnik ma życzenie zakończyć działanie tego programu (tak/nie): ")
    if decyzja.strip().lower() in ['tak', 't']:
        print("\nZakończono program.")
        break



# # Osobny, mały skrypt tylko pod zadanie z ćwiczeń (opcjonalnie do pokazania)
# w1 = [float(x) for x in input("Podaj 1 wektor: ").split()]
# w2 = [float(x) for x in input("Podaj 2 wektor: ").split()]
# print("Odległość:", liczOdleglosc(w1, w2))
