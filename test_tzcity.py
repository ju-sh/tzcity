import pytest

import tzcity

class TestFindTZ:
    @pytest.mark.parametrize('city,expected', [
        ('lOnDon', 'Europe/London'),
        ('port au prince', 'America/Port-au-Prince'),
        ('africa/dar_es_salaam', 'Africa/Dar_es_Salaam'),
    ])
    def test_valid(self, city, expected):
        assert tzcity.find_tz(city) == expected

    @pytest.mark.parametrize('city', [
        'wonderland'
    ])
    def test_invalid(self, city):
        with pytest.raises(ValueError):
            tzcity.find_tz(city)

class TestCapIt:
    @pytest.mark.parametrize('name,expected', [
        ('rio de janeiro', 'Rio de Janeiro'),
        ('uae', 'UAE'),
        ("cote d'ivoire", "Cote d'Ivoire"),
        ("n'djamena", "N'Djamena"),
        ('atlantic/cape_verde', 'Atlantic/Cape_Verde'),
        ('america/port_of_spain', 'America/Port_of_Spain'),
    ])
    def test_valid(self, name, expected):
        assert tzcity.cap_it(name) == expected

    @pytest.mark.parametrize('name', [
        "d'",
    ])
    def test_invalid(self, name):
        with pytest.raises(ValueError):
            tzcity.cap_it(name)

class TestCapsify:
    @pytest.mark.parametrize('name,expected', [
        ('mcmurdo', 'McMurdo'),
        ('rio de janeiro', 'Rio de Janeiro'),
        ('andorra la vella', 'Andorra la Vella'),
        ('port of spain', 'Port of Spain'),
        ('uae', 'UAE'),
        ("cote d'ivoire", "Cote d'Ivoire"),
        ("n'djamena", "N'Djamena"),
        ("dar es salaam", "Dar es Salaam"),
        ("dumont d'urville", "Dumont d'Urville"),
        ('port-au-prince', 'Port-au-Prince'),
        ('fort-de-france', 'Fort-de-France'),
    ])
    def test_valid(self, name, expected):
        assert tzcity.capsify(name) == expected
        
    @pytest.mark.parametrize('name', [
        "d'",
    ])
    def test_invalid(self, name):
        with pytest.raises(ValueError):
            tzcity.capsify(name)
