# zadanie_backend_python
By uruchomić projekt należy odpalić plik main_file.py w konsoli (plik 'Liczba_osób_które_przystapiły_lub_zdały_egzamin_maturalny.csv' powinien znajdować sięw tym samym folderze).

Po uruchomieniu zostanie wypisana lista województw (w programie Polska jest traktowana jako województwo).
Następnie będzie można wpisywać komendy:

1) average_number_taking  - oblicza średnią osób, które przystąpiły do egzaminu maturalnego do danego roku włącznie (zad 1)

parametry: nazwa województwa, rok, płeć (opcjonalnie)
2) calculate_pass_rate  - oblicza procentową zdawalność dla danego województwa na przestrzeni lat (zad 2)

parametry: nazwa województwa, płeć (opcjonalnie)
3) best_pass_rate  - podaje województwo o najlepszej zdawalności w danym roku (zad 3)

parametry: rok, płeć (opcjonalnie)
4) check_regression  - znajduje województwa, które zanotowały spadek zdawalności i podaje, w których latach to nastąpiło (zad 4)
   parametry: płeć (opcjonalnie)
5) compare_pass_rate  - porównuje dwa wojwództwa pod względem zdawalności na przestrzeni lat (wypisuje województwo o większej zdawalności)    (zad 5)
   
   parametry: nazwa pierwszego województwa, nazwa drugiego województwa, płeć (opcjonalnie)
6) help  - komenda help pokazuje listę komend, a help nazwa_komendy, jej krótki opis.
7) exit  - zamyka program

Argumenty komend należy wprowadzać po spacji, kolejność jest istotna.

Parametr opcjonalny dotyczący rozróżniania ze względu na płeć ma opcje:  kobiety, mężczyźni (lub skrótowo odpowiednio: k, m). Nie podanie paramtru skutkuje wykonaniem komendy bez rozróżniania.

Wybrane testy jednostkowe zawarte są w pliku test.py.




