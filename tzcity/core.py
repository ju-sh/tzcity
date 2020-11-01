"""
Core functionality of tzcity
"""

import re

from tzcity.data import CITY_DICT


def tzcity(city: str) -> str:
    """
    Find the time zone associated with a city.

    Return time zone name itself if argument is a time zone.
    """
    tz_value = ''
    city = city.strip().lower()
    for tz in CITY_DICT:

        # Complete tz name
        if tz == city:
            tz_value = tz
            break

        # tz city name
        tz_city = tz.split('/')[-1].replace('_', ' ')
        if city == tz_city:
            tz_value = tz
            break

        # city associated with tz
        if city in CITY_DICT[tz]:
            tz_value = tz
            break
    if tz_value:
        return capitalize(tz_value)

    raise ValueError(f"{city}: Ambiguous or unknown time zone")


def capitalize(name: str) -> str:
    """
    Return capitalized form of the input city or tz name.

    Raises ValueError on unknown pattern
    """

    # a tz name
    if name in CITY_DICT:
        # tz names will have at least one '/'
        tzfull, city = name.rsplit('/', maxsplit=1)
        if '/' in tzfull:
            # 3-part tz names
            continent, country = tzfull.split('/')
            continent = continent.title()
            country = country.title()
        else:
            # normal 2-part tz names
            continent = ""
            country = tzfull.title()
        city = city.replace('_', ' ')
        city = _caps_city(city)
        city = city.replace(' ', '_')
        if continent:
            return f"{continent}/{country}/{city}"
        return f"{country}/{city}"

    # Not a tz name
    return _caps_city(name)


def _caps_city(name: str) -> str:
    """
    Capitalize city names appropriately.
    For use of capitalize() function.
    Cannot handle tz names.

    Accepts a city name.

    Returns capitalized version of input city name
    """

    SPECIAL_PATTERNS = {
        # For 'Andorra la vella', 'Port of Prince', 'Dar es Salaam', etc
        'lower': ['la', 'de', 'da', 'and', 'of', 'the', 'es'],

        # For 'UK', 'UAE', 'Washington DC', etc
        'upper': ['uk', 'uae', 'sgssi', 'dc'],

        # For 'Port-au-Prince', 'Fort-de-France', etc
        'hyphen': ['au', 'de'],
    }

    # For 'McMurdo', 'Dumont d'Urville', 'N'Djamena', etc
    # length of each value must be same as its key.
    OTHERS = {'mc': 'Mc', "d'": "d'", "n'": "N'"}

    name = name.lower()  # no strip() as split() will handle that
    words = name.split()

    new_words = []
    for word in words:
        new_word: str = ''
        if word in SPECIAL_PATTERNS['lower']:
            new_word = word.lower()
        elif word in SPECIAL_PATTERNS['upper']:
            new_word = word.upper()
        elif any([f"-{x}-" in word for x in SPECIAL_PATTERNS['hyphen']]):
            pre, hyphen, post = word.replace('-', ' ').split()
            new_word = f"{pre.title()}-{hyphen}-{post.title()}"
        else:
            re_str = ')|('.join(OTHERS)
            re_str = rf"({re_str})"
            re_match = re.match(re_str, word)
            if re_match is not None:
                match_str = re_match.group(0)
                if len(word) > len(match_str):
                    repl_str = OTHERS[match_str]
                    new_word = f"{repl_str}{word[len(match_str):].title()}"
                else:
                    raise ValueError(f"{word} Could not capitalize")
            else:
                new_word = word.title()
        new_words.append(new_word)
    return ' '.join(new_words)
