import cmd
import csv


class Voivodeship:
    def __init__(self, name, f_name):
        self.name = name
        self.f_name = f_name
        self.pass_rate = dict()
        self.regression_years = []

    def average_number_taking(self, year, gender=''):  # obliczenie średniej przystpujących do danego roku włącznie
        with open(self.f_name) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            suma = 0
            i = 0.0
            for row in reader:
                if (self.name == row['Terytorium']) and (int(row['Rok']) <= int(year)) and (
                        row['Przystąpiło/zdało '] == 'przystąpiło'):
                    if (row['Płeć '] == gender) or (gender == ''):
                        suma += int(row['Liczba osób'])
                        i += 1.0
        if gender == '':
            print(2*suma / i)
            return 2*suma / i
        else:
            print(suma / i)
            return suma / i

    def calculate_pass_rate(self, gender='', show=True):  # obliczanie zdawalności
        with open(self.f_name) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")

            self.pass_rate = {}
            passed = dict()

            for row in reader:
                if row['Terytorium'] == self.name and (row['Płeć '] == gender or gender == ''):
                    if row['Przystąpiło/zdało '] == 'przystąpiło':
                        if not row['Rok'] in self.pass_rate:
                            self.pass_rate[row['Rok']] = 0
                        self.pass_rate[row['Rok']] += int(row['Liczba osób'])
                    else:
                        if not row['Rok'] in passed:
                            passed[row['Rok']] = 0
                        passed[row['Rok']] += int(row['Liczba osób'])

            for row in passed:
                self.pass_rate[row] = float(100*passed[row]/self.pass_rate[row])

            if show:
                for year, value in self.pass_rate.items():
                    print(year, " - ", round(value, 4), "%")

    def check_regression(self, gender=''):  # znalezienie regresji wsrod wojewodztw
        self.regression_years = []
        previous_p_r = -2  # zdawalnosc z poprzedniego roku
        self.calculate_pass_rate(gender, show=False)
        for year, p_r in self.pass_rate.items():
            if p_r < previous_p_r:
                self.regression_years.append((str(int(year)-1), year))
            previous_p_r = p_r

    def compare_pass_rate(self, v, gender='', year='0'):  # porownanie zdawalnosci miedzy wojewodztwami
        self.calculate_pass_rate(gender=gender, show=False)
        v.calculate_pass_rate(gender=gender, show=False)

        for i in self.pass_rate:
            if self.pass_rate[i] > v.pass_rate[i]:
                print(i, ' - ', self.name)
                if i == year:
                    return self.name
            elif self.pass_rate[i] == v.pass_rate[i]:
                print(i, ' - ', self.name, v.name)
                if i == year:
                    return self.name
            else:
                print(i, ' - ', v.name)
                if i == year:
                    return v.name


def best_pass_rate(v_list, year, gender=''):
    best_p_r = 1

    for i in v_list:
        i.calculate_pass_rate(gender=gender, show=False)

    for i in range(1, len(v_list)):
        if v_list[i].pass_rate[year] > v_list[best_p_r].pass_rate[year]:
            best_p_r = i
    print(v_list[best_p_r].name)
    return v_list[best_p_r].name


class MaturityExam(cmd.Cmd):  # obsluga konsoli

    v_list = []

    def add_v_list(self, f_name):
        MaturityExam.v_list = []
        with open(f_name) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            t = ""
            for row in reader:
                if t != row['Terytorium']:
                    t = row['Terytorium']
                    MaturityExam.v_list.append(Voivodeship(t, f_name))

    def do_average_number_taking(self,  arg):
        """obliczenie średniej osob przystępujących co roku do matury, dla wojewodztwa, do danego roku włącznie.
        \rParametry: nazwa wojewodztwa, rok, plec (opcjonalnie)
        """
        arg_t = parse(arg)  # rozdzielenie argumentow
        if len(arg_t) >= 2 and len(arg_t) <= 3:  # sprawdzenie czy jest dana odpowiednia ilosc elementow
            i = self.find_voivodeship(arg_t[0])
        else:
            i = -2

        if i > 0:  # sprawdzenie poprawnosci danego roku
            if int(arg_t[1]) < 2010 or int(arg_t[1]) > 2018:
                i = -4

        if len(arg_t) == 3 and i >= 0:  # obsluga opcjoanlnego parametru dotyczacego plci
            if arg_t[2] != "m" and arg_t[2] != "k" and arg_t[2] != "kobiety" and arg_t[2] != "mężczyźni":
                i = -3
            elif arg_t[2] == "m":
                arg_t[2] = "mężczyźni"
            elif arg_t[2] == "k":
                arg_t[2] = "kobiety"

        if len(arg_t) == 2 and i >= 0:
            print(arg_t[0], ", ", arg_t[1])
            self.v_list[i].average_number_taking(arg_t[1])
        elif i >= 0:
            print(arg_t[0], ", ", arg_t[1], ", ", arg_t[2])
            self.v_list[i].average_number_taking(arg_t[1], arg_t[2])
        else:
            print("Niepoprawne argumenty")

    def do_calculate_pass_rate(self, arg):
        """obliczenie zdawalnosci wojewodztwa na przestrzeni lat.
        \rParametry: nazwa wojewodztwa, plec (opcjanalnie)
        """
        arg_t = parse(arg)
        if len(arg_t) > 0 and len(arg_t) <= 2:
            i = self.find_voivodeship(arg_t[0])
        else:
            i = -2

        if len(arg_t) == 2 and i >= 0:
            if arg_t[1] != "m" and arg_t[1] != "k" and arg_t[1] != "kobiety" and arg_t[1] != "mężczyźni":
                i = -3
            elif arg_t[1] == "m":
                arg_t[1] = "mężczyźni"
            elif arg_t[1] == "k":
                arg_t[1] = "kobiety"

        if len(arg_t) == 1 and i >= 0:
            print(arg_t[0])
            self.v_list[i].calculate_pass_rate()
        elif i >= 0:
            print(arg_t[0], ", ", arg_t[1])
            self.v_list[i].calculate_pass_rate(arg_t[1])
        else:
            print("Niepoprawne parametry")

    def do_check_regression(self, arg):
        """sprawdzenie regrsji województw na przestrzeni lat.
        \rParametry: plec (opcjonalnie)
        """
        arg_t = parse(arg)
        if len(arg_t) == 0 or len(arg_t) == 1:
            i = 1
        else:
            i = -2

        if len(arg_t) == 1:
            if arg_t[0] != "m" and arg_t[0] != "k" and arg_t[0] != "kobiety" and arg_t[0] != "mężczyźni":
                i = -3
            elif arg_t[0] == "m":
                arg_t[0] = "mężczyźni"
            elif arg_t[0] == "k":
                arg_t[0] = "kobiety"
            i = 2

        if i == 1:
            for v in self.v_list:
                v.check_regression()
        elif i == 2:
            print(arg_t[0])
            for v in self.v_list:
                v.check_regression(gender=arg_t[0])
        else:
            print("Niepoprawne parametry")

        if i > 0:
            for v in self.v_list:
                for year in v.regression_years:
                    print(v.name, year[0], "->", year[1])

    def do_compare_pass_rate(self, arg):
        """Porownanie zdawalnosci dwóch województw na przestrzeni lat
        \rParametry: nazwa pierwszego województwa, nazwa drugiego województwa, płeć (opcjonalnie)
        """
        arg_t = parse(arg)
        if len(arg_t) == 2 or len(arg_t) == 3:
            i = self.find_voivodeship(arg_t[0])
            j = self.find_voivodeship(arg_t[1])
        else:
            i = -2
            j = -2

        if len(arg_t) == 3 and i >= 0 and j >= 0:
            if arg_t[2] != "m" and arg_t[2] != "k" and arg_t[2] != "kobiety" and arg_t[2] != "mężczyźni":
                i = -3
            elif arg_t[2] == "m":
                arg_t[2] = "mężczyźni"
            elif arg_t[2] == "k":
                arg_t[2] = "kobiety"

        if len(arg_t) == 2 and i >= 0 and j >= 0:
            self.v_list[i].compare_pass_rate(self.v_list[j])
        elif i >= 0 and j >= 0:
            print(arg_t[2])
            self.v_list[i].compare_pass_rate(self.v_list[j], gender=arg_t[2])
        else:
            print("Niepoprawne parametry")

    def do_best_pass_rate(self, arg):
        """Znalezienie najlepszego wojewodztwa, pod względem zdawalności, w danym roku.
        \rParametry: rok, plec (opcjonalnie)
        """
        arg_t = parse(arg)
        if len(arg_t) == 1 or len(arg_t) == 2:
            i = 1
        else:
            i = -2

        if i > 0:
            if int(arg_t[0]) < 2010 or int(arg_t[0]) > 2018:
                    i = -4

        if len(arg_t) == 2 and i >= 0:
            if arg_t[1] != "m" and arg_t[1] != "k" and arg_t[1] != "kobiety" and arg_t[1] != "mężczyźni":
                i = -3
            elif arg_t[1] == "m":
                arg_t[1] = "mężczyźni"
            elif arg_t[1] == "k":
                arg_t[1] = "kobiety"
            i = 2

        if i == 1:
            best_pass_rate(self.v_list, arg_t[0], gender='')
        elif i == 2:
            print(arg_t[1])
            best_pass_rate(self.v_list, arg_t[0], gender= arg_t[1])
        else:
            print("Niepoprawne parametry")

    def do_exit(self, arg):
        """Wyjście z programu
        """
        return True

    def find_voivodeship(self, name):
        for i in range(len(self.v_list)):
            if name == self.v_list[i].name:
                return i
        return -1

    def print_v_list(self):
        print("Lista województw:")
        for i in MaturityExam.v_list:
            print(i.name)
        print("\n")


def parse(arg):
    return list(arg.split())


def main():
    f_name = 'Liczba_osób_które_przystapiły_lub_zdały_egzamin_maturalny.csv'

    m_e = MaturityExam()
    m_e.add_v_list(f_name)
    m_e.print_v_list()
    m_e.cmdloop()


if __name__ == '__main__':
    main()
