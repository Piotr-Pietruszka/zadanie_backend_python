import pytest
from main_file import Voivodeship
from main_file import best_pass_rate
import csv


class TestClass(object):
    v_list = []

    @pytest.mark.parametrize('i, year, gender, expected',
                             [(0, '2018', '', 298748.222), (2, '2011', 'kobiety', 10485.0)])
    def test_average_number_taking(self, i, year, gender, expected):  # parametry: numer wojwództwa, rok, plec, wartosc oczekiwana
        self.add_v_list('Liczba_osób_które_przystapiły_lub_zdały_egzamin_maturalny.csv')
        assert round(TestClass.v_list[i].average_number_taking(year, gender=gender), 3) == expected

    @pytest.mark.parametrize('i, year, gender, expected',
                             [(4, '2010', '', 82.3209), (6, '2012', 'mężczyźni', 82.3448872235)])
    def test_calculate_pass_rate(self, i, year, gender, expected):
        TestClass.v_list[i].calculate_pass_rate(show=False, gender=gender)
        assert round(TestClass.v_list[i].pass_rate[year], 4) == round(expected, 4)

    @pytest.mark.parametrize('i, gender, expected',
                             [(4, '', ('2010', '2011')), (16, '', ('2016', '2017'))])
    def test_check_regression(self, i, gender, expected):
        TestClass.v_list[i].check_regression(gender=gender)
        assert expected in TestClass.v_list[i].regression_years

    @pytest.mark.parametrize('i, j, year, gender, expected',
                             [(2, 5, '2010', '', 2), (10, 13, '2017', '', 10)])
    def test_compare_pass_rate(self, i, j, year, gender, expected):
        assert TestClass.v_list[i].compare_pass_rate(v=TestClass.v_list[j], year=year) == TestClass.v_list[expected].name

    @pytest.mark.parametrize('year, gender, expected',
                             [('2016', '', 'Małopolskie'), ('2014', 'kobiety', 'Podlaskie')])
    def test_best_pass_rate(self, year, gender, expected):
        assert best_pass_rate(TestClass.v_list, year=year, gender=gender) == expected

    def add_v_list(self, f_name):
        TestClass.v_list = []
        with open(f_name) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            t = ""
            for row in reader:
                if t != row['Terytorium']:
                    t = row['Terytorium']
                    TestClass.v_list.append(Voivodeship(t, f_name))

