import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class KMeans {

    // Klasa pomocnicza do zwracania dwóch list z metody wczytajDane
    static class WczytaneDane {
        List<List<Double>> dane = new ArrayList<>();
        List<String> etykiety = new ArrayList<>();
    }

    public static WczytaneDane wczytajDane(String nazwaPliku) {
        WczytaneDane wynik = new WczytaneDane();

        try (BufferedReader br = new BufferedReader(new FileReader(nazwaPliku))) {
            String linia;
            while ((linia = br.readLine()) != null) {
                // czyszcze biale znaki
                linia = linia.trim();
                if (linia.isEmpty()) {
                    continue;
                }

                // split() dzieli po spacjach i tabulatorach
                String[] czesci = linia.split("\\s+");

                // ostatni element to zawsze gatunek irysa
                String gatunek = czesci[czesci.length - 1];
                wynik.etykiety.add(gatunek);

                // reszte zamieniam na double bo to wymiary
                List<Double> cechy = new ArrayList<>();
                for (int i = 0; i < czesci.length - 1; i++) {
                    // zamieniam przecinek na kropke zeby Double.parseDouble() nie wywalil bledu
                    String wartoscZKropka = czesci[i].replace(',', '.');
                    cechy.add(Double.parseDouble(wartoscZKropka));
                }

                // dodaje wyciagniete cechy do glownej listy
                wynik.dane.add(cechy);
            }
        } catch (IOException e) {
            System.out.println("Błąd podczas wczytywania pliku: " + e.getMessage());
        }

        return wynik;
    }

    public static void kMeans() {
        // wczytuje plik treningowy
        WczytaneDane wczytane = wczytajDane("iris_training.txt");
        List<List<Double>> dane = wczytane.dane;
        List<String> etykiety = wczytane.etykiety;

        // pobieram k od usera
        Scanner scanner = new Scanner(System.in);
        System.out.print("Podaj liczbę klastrów (k): ");
        int k = scanner.nextInt();

        // losuje poczatkowe centroidy ze zbioru
        List<List<Double>> centroidy = new ArrayList<>();
        List<Integer> indexy = new ArrayList<>();
        for (int i = 0; i < dane.size(); i++) {
            indexy.add(i);
        }
        Collections.shuffle(indexy); // mieszamy listę indeksów
        for (int i = 0; i < k; i++) {
            // musimy skopiować wartości punktu
            centroidy.add(new ArrayList<>(dane.get(indexy.get(i))));
        }

        int iteracja = 1;
        List<List<Integer>> grupy;

        while (true) {
            // przygotowuje puste listy na poszczegolne klastry
            grupy = new ArrayList<>();
            for (int i = 0; i < k; i++) {
                grupy.add(new ArrayList<>());
            }

            double sumaKwadratow = 0.0;

            // przypisuje punkty do najblizszego centroidu
            for (int i = 0; i < dane.size(); i++) {
                List<Double> punkt = dane.get(i);

                // poczatkowo ustawiam na nieskonczonosc
                double najmniejszaOdleglosc = Double.POSITIVE_INFINITY;
                int najlepszaGrupa = 0;

                // szukam najblizszego
                for (int c = 0; c < k; c++) {
                    double odleglosc = 0.0;
                    // licze kwadrat odleglosci euklidesowej
                    for (int wymiar = 0; wymiar < punkt.size(); wymiar++) {
                        odleglosc += Math.pow(punkt.get(wymiar) - centroidy.get(c).get(wymiar), 2);
                    }

                    if (odleglosc < najmniejszaOdleglosc) {
                        najmniejszaOdleglosc = odleglosc;
                        najlepszaGrupa = c;
                    }
                }

                // dodaje indeks punktu do odpowiedniej grupy i aktualizuje sume
                grupy.get(najlepszaGrupa).add(i);
                sumaKwadratow += najmniejszaOdleglosc;
            }

            System.out.println("Iteracja " + iteracja + ": Suma kwadratów odległości = " + sumaKwadratow);

            // licze nowe srodki klastrow
            List<List<Double>> noweCentroidy = new ArrayList<>();
            for (int c = 0; c < k; c++) {
                // jak do grupy nic nie trafilo to zostawiam stary srodek
                if (grupy.get(c).isEmpty()) {
                    noweCentroidy.add(new ArrayList<>(centroidy.get(c)));
                    continue;
                }

                // wektor samych zer do sumowania wymiarow
                List<Double> nowySrodek = new ArrayList<>(Collections.nCopies(dane.get(0).size(), 0.0));

                // sumuje cechy dla danego klastra
                for (int indeks : grupy.get(c)) {
                    List<Double> punkt = dane.get(indeks);
                    for (int wymiar = 0; wymiar < punkt.size(); wymiar++) {
                        nowySrodek.set(wymiar, nowySrodek.get(wymiar) + punkt.get(wymiar));
                    }
                }

                // wyliczam srednia
                for (int wymiar = 0; wymiar < nowySrodek.size(); wymiar++) {
                    nowySrodek.set(wymiar, nowySrodek.get(wymiar) / grupy.get(c).size());
                }

                noweCentroidy.add(nowySrodek);
            }

            // warunek stopu jesli centroidy sie juz nie ruszaja
            if (centroidy.equals(noweCentroidy)) {
                break;
            }

            // podmieniam zmienne na kolejna petle
            centroidy = noweCentroidy;
            iteracja++;
        }

        System.out.println("\n--- ALGORYTM ZAKOŃCZONY ---");

        // wypisuje sklady klastrow i licze ich entropie
        for (int c = 0; c < k; c++) {
            System.out.println("\nKLASTER " + (c + 1) + ":");

            // slownik do zliczania gatunkow
            Map<String, Integer> licznikGatunkow = new HashMap<>();

            System.out.println("Skład klastra (wypisuję nazwy gatunków i ich wartości):");
            for (int indeks : grupy.get(c)) {
                String gatunek = etykiety.get(indeks);
                List<Double> wartosci = dane.get(indeks);
                System.out.println(" - " + wartosci + " -> " + gatunek);

                // zliczam konkretny gatunek
                licznikGatunkow.put(gatunek, licznikGatunkow.getOrDefault(gatunek, 0) + 1);
            }

            int ileWKlastrze = grupy.get(c).size();
            double entropia = 0.0;

            // obliczam z wzoru na entropie
            if (ileWKlastrze > 0) {
                for (Map.Entry<String, Integer> wpis : licznikGatunkow.entrySet()) {
                    double p = (double) wpis.getValue() / ileWKlastrze;
                    // Math.log to logarytm naturalny, dzielimy przez log(2) aby mieć logarytm o podstawie 2
                    entropia -= p * (Math.log(p) / Math.log(2));
                }
            }

            System.out.println("> Zliczono gatunki: " + licznikGatunkow);
            System.out.println("> Entropia klastra: " + entropia);
        }
    }

    public static void zadanieEntropiaZKlawiatury() {
        System.out.println("\n--- ZADANIE Z ĆWICZEŃ: ENTROPIA ROZKŁADU ---");
        System.out.println("Podaj części (np. 10 5 5), oddzielone spacjami i wciśnij Enter:");

        Scanner scanner = new Scanner(System.in);
        String tekst = scanner.nextLine();

        // dziele stringa po spacji
        String[] elementy = tekst.trim().split("\\s+");

        // rzutuje to co wpisal uzytkownik na double
        List<Double> czestosci = new ArrayList<>();
        for (String element : elementy) {
            if (!element.isEmpty()) {
                czestosci.add(Double.parseDouble(element));
            }
        }

        // licze sume calkowita
        double sumaCzestosci = 0.0;
        for (Double c : czestosci) {
            sumaCzestosci += c;
        }

        double entropia = 0.0;
        for (Double c : czestosci) {
            // pomijam zera zeby nie bylo bledu w logarytmie
            if (c > 0) {
                double prawdopodobienstwo = c / sumaCzestosci;
                entropia -= prawdopodobienstwo * (Math.log(prawdopodobienstwo) / Math.log(2));
            }
        }

        System.out.println("Entropia podanego rozkładu wynosi: " + entropia);
    }

    public static void main(String[] args) {
        kMeans();
        zadanieEntropiaZKlawiatury();
    }
}