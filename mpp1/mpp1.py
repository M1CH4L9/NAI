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

daneTreningowe = wczytajDane('iris_training.txt')
daneTestowe = wczytajDane('iris_test.txt')

print(f"Wczytano {len(daneTreningowe)} próbek treningowych.")
print(f"Wczytano {len(daneTestowe)} próbek testowych.")