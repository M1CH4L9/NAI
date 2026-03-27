import random


#ta sama część ze wczytaniem pliku z mpp1
def wczytajDane(nazwaPliku):
    dane = []
    with open(nazwaPliku, 'r') as plik:
        for linia in plik:
            linia = linia.strip()
            if not linia:
                continue

            elementy = linia.split()
            # gatunek ostatnia kolumna
            gatunek = elementy.pop()

            wymiary = []
            for x in elementy:
                wymiary.append(float(x.replace(',', '.')))

            dane.append((wymiary, gatunek))
    return dane


# wczytywanie danych
daneTreningowe = wczytajDane('iris_training.txt')
daneTestowe = wczytajDane('iris_test.txt')

# Sprawdzenie ile mamy atrybutów, żeby program był uniwersalny
liczbaAtrybutow = len(daneTreningowe[0][0])

class Perceptron:
    def __init__(self, liczbaAtrybutow):
        self.weights = []

        #(uniwersalność), program se akceptuje tyle ile chce atrybutów
        for _ in range(liczbaAtrybutow):
            self.weights.append(random.uniform(-1.0, 1.0))

        #losowanie początkowego prgu
        self.threshold = random.uniform(-1.0, 1.0)

        #jak duże kroki podczas nauki robimy
        self.stalaUczenia = 0.01

    #liczymy se wyjście perceptronu
    def Compute(self, inputs):
        suma = 0.0

        #mnożym każde wejście przez wage i suma :)
        for i in range(len(inputs)):
            suma += inputs[i] * self.weights[i]

        #sprawdzamy czy suma przekracza próg
        if suma >= self.threshold:
            return 1
        else:
            return 0

    #metoda do trenowania algorytmem delty
    def Ucz(self, inputs, oczekiwaneWyjscie):
        aktualneWyjscie = self.Compute(inputs)

        #obliczamy se błąd:
        #0 zgadł
        #1 lub -1 jeśli się pomylił
        blad = oczekiwaneWyjscie - aktualneWyjscie

        #jesli sie pomylił, poprawiamy wagi i próg
        if blad != 0:
            for i in range(len(self.weights)):
                self.weights[i] += self.stalaUczenia * blad * inputs[i]

            #aktualizacja progu
            self.threshold -= self.stalaUczenia * blad

#tworzymy se obiekt
perceptron = Perceptron(liczbaAtrybutow)

#ustalamy ile razy chcemy "przemielić" cały zbiór
liczbaEpok = 100

print("Rozpoczynam trenowanie perceptronu. . .")

for epoka in range(liczbaEpok):
    bledywEpoce = 0

    #przechodzimy, przez każdy kwiatek
    for wymiary, gatunek in daneTreningowe:

        if gatunek == 'Iris-setosa':
            oczekiwaneWyjscie = 1
        else:
            oczekiwaneWyjscie = 0

        #zliczamy błędy (żebyśmy se wiedzieli czy się uczy)
        aktualne = perceptron.Compute(wymiary)
        if aktualne != oczekiwaneWyjscie:
            bledywEpoce += 1

        #uruchamiamy algorytm delty dla tego kwiatka
        perceptron.Ucz(wymiary, oczekiwaneWyjscie)

    #żeby wiedzieć co się dzieje drukujemy postęp co 10 epok
    if (epoka + 1) % 10 == 0 or bledywEpoce == 0:
        print(f"Epoka {epoka + 1}: błędnych klasyfikacji = {bledywEpoce}")

    #jeśli algorytm przestał się mylić na zbiorze treningowym, przerywamy pętlę
    if bledywEpoce == 0:
        print(f"Sukces!!! Perceptron nauczył się bezbłędnie w {epoka + 1} epoce.\n")
        break

poprawne = 0
wszystkie = len(daneTestowe)

for wymiary, prawdziwyGatunek in daneTestowe:
    #tłumaczymy prawdziwy gatunek
    if prawdziwyGatunek == 'Iris-setosa':
        oczekiwaneWyjscie = 1
    else:
        oczekiwaneWyjscie = 0

    #pytamy perceptrona
    odpowiedz = perceptron.Compute(wymiary)

    #sprawdzamy czy zgadł
    if odpowiedz == oczekiwaneWyjscie:
        poprawne += 1

dokladnosc = (poprawne / wszystkie) * 100

print("----------Wyniki testu-----------")
print(f"Prawidłowo sklasyfikowanych próbek: {poprawne}")
print(f"Wszystkich próbek: {wszystkie}")
print(f"Dokładność klasyfikacji: {dokladnosc:.2f}%")
print("----------------------------------\n")

#ręczne sprawdzanie danych
while True:
    print("------------------------------------------")
    nowyWektor = []
    bladWprowadzania = False

    for i in range(liczbaAtrybutow):
        wprowadzonyTekst = input(f"Bardzo proszę, podaj cechę {i + 1}: ")
        try:
            nowyWektor.append(float(wprowadzonyTekst.replace(',', '.')))
        except ValueError:
            print(f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Błąd: Wprowadź poprawne liczby.")
            print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            bladWprowadzania = True
            break

    if not bladWprowadzania:
        wynikKlasyfikacji = perceptron.Compute(nowyWektor)
        if wynikKlasyfikacji == 1:
            print(f"\nWynik klasyfikacji perceptronu: Iris-setosa (1)")
        else:
            print(f"\nWynik klasyfikacji perceptronu: Inny gatunek (0)")

    decyzja = input("\nCzy szanowny osobnik ma życzenie zakończyć działanie tego programu (tak/nie): ")
    if decyzja.strip().lower() in ['tak', 't']:
        print("\nZakończono program. :)")
        break













# # --- opcjonalne zadanie na ćwiczenia ---
# print("\n---Zadanie do wykonania podczas zajęć---")
# wagi_str = input("Podaj 2 wagi (oddzielone spacją): ").split()
# prog_str = input("Podaj próg perceptronu: ")
# sygnaly_str = input("Podaj 2 sygnały wejściowe (oddzielone spacją): ").split()
#
# # Tworzymy "ręczny" perceptron z 2 wejściami
# p_zajecia = Perceptron(2)
# p_zajecia.weights = [float(wagi_str[0].replace(',', '.')), float(wagi_str[1].replace(',', '.'))]
# p_zajecia.threshold = float(prog_str.replace(',', '.'))
#
# wejscia_zajecia = [float(sygnaly_str[0].replace(',', '.')), float(sygnaly_str[1].replace(',', '.'))]
# odpowiedz_zajecia = p_zajecia.Compute(wejscia_zajecia)
# print(f"Odpowiedź perceptronu dla podanych danych: {odpowiedz_zajecia}")