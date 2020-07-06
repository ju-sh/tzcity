"""
Module to translate city names to time zone names
"""

__version__ = "0.0.2"

from typing import Dict, List
import re


class UnknownTZCityException(ValueError):
    """
    Exception raised when unable to recognize a time zone or
    city name
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


CITY_DICT: Dict[str, List[str]] = {
    "africa/abidjan": ["cote d'ivoire", "ivory coast", "yamoussaoukro"],
    "africa/accra": ["ghana"],
    "africa/addis_ababa": ["ethiopia"],
    "africa/algiers": ["algeria"],
    "africa/asmara": ["eritrea"],
    "africa/bamako": ["mali"],
    "africa/bangui": ["central african republic"],
    "africa/banjul": ["gambia"],
    "africa/bissau": ["guinea-bissau"],
    "africa/blantyre": ["malawi", "lilongwe"],
    "africa/brazzaville": ["rotc", "congo-brazzaville", "congo republic"],
    "africa/bujumbura": ["burundi"],
    "africa/cairo": ["egypt"],
    "africa/casablanca": ["morocco"],
    "africa/ceuta": [],
    "africa/conakry": ["guinea"],
    "africa/dakar": ["senegal"],
    "africa/dar_es_salaam": ["tanzania", "dodoma"],
    "africa/djibouti": ["djibouti"],
    "africa/douala": ["cameroon", "yaounde"],
    "africa/el_aaiun": ["western sahara", "laayoune"],
    "africa/freetown": ["sierra leone"],
    "africa/gaborone": ["botswana"],
    "africa/harare": ["zimbabwe"],
    "africa/johannesburg": ["pretoria"],
    "africa/juba": ["south sudan"],
    "africa/kampala": ["uganda"],
    "africa/khartoum": ["sudan"],
    "africa/kigali": ["rwanda"],
    "africa/kinshasa": [],
    "africa/lagos": ["nigeria", "abuja"],
    "africa/libreville": ["gabon"],
    "africa/lome": ["togo"],
    "africa/luanda": ["angola"],
    "africa/lubumbashi": [],
    "africa/lusaka": ["zambia"],
    "africa/malabo": ["equatorial guinea", "bata"],
    "africa/maputo": ["mozambique"],
    "africa/maseru": ["lesotho"],
    "africa/mbabane": ["swaziland", "eswatini"],
    "africa/mogadishu": ["somalia"],
    "africa/monrovia": ["liberia"],
    "africa/nairobi": ["kenya"],
    "africa/ndjamena": ["chad", "n'djamena"],
    "africa/niamey": ["niger"],
    "africa/nouakchott": ["mauritania"],
    "africa/ouagadougou": ["burkina faso"],
    "africa/porto-novo": ["benin", "cotonou"],
    "africa/sao_tome": ["sao tome and principe"],
    "africa/tripoli": ["libya"],
    "africa/tunis": ["tunisia"],
    "africa/windhoek": ["namibia"],
    "america/adak": [],
    "america/anchorage": [],
    "america/anguilla": [],
    "america/antigua": ["antigua and barbuda"],
    "america/araguaina": [],
    "america/argentina/buenos_aires": [],
    "america/argentina/catamarca": [],
    "america/argentina/cordoba": [],
    "america/argentina/jujuy": [],
    "america/argentina/la_rioja": [],
    "america/argentina/mendoza": [],
    "america/argentina/rio_gallegos": [],
    "america/argentina/salta": [],
    "america/argentina/san_luis": [],
    "america/argentina/tucuman": [],
    "america/argentina/ushuaia": [],
    "america/aruba": ["oranjestad"],
    "america/asuncion": ["paraguay"],
    "america/atikokan": [],
    "america/bahia": [],
    "america/bahia_banderas": [],
    "america/barbados": ["bridgetown"],
    "america/belem": [],
    "america/belize": ["belmopan"],
    "america/blanc-sablon": [],
    "america/boa_vista": [],
    "america/bogota": ["colombia"],
    "america/boise": [],
    "america/cambridge_bay": [],
    "america/campo_grande": [],
    "america/cancun": [],
    "america/caracas": ["venezuela"],
    "america/cayenne": ["french guiana"],
    "america/cayman": [],
    "america/chicago": [],
    "america/chihuahua": [],
    "america/costa_rica": ["costa rica", "san jose"],
    "america/creston": [],
    "america/cuiaba": [],
    "america/curacao": ["curacao", "willemstad"],
    "america/danmarkshavn": [],
    "america/dawson": [],
    "america/dawson_creek": [],
    "america/denver": [],
    "america/detroit": [],
    "america/dominica": ["roseau"],
    "america/edmonton": [],
    "america/eirunepe": [],
    "america/el_salvador": ["san salvador"],
    "america/fortaleza": [],
    "america/fort_nelson": [],
    "america/glace_bay": [],
    "america/goose_bay": [],
    "america/grand_turk": ["turks and caicos islands"],
    "america/grenada": [],
    "america/guadeloupe": [],
    "america/guatemala": ["guatemala city"],
    "america/guayaquil": ["quito"],
    "america/guyana": [],
    "america/halifax": [],
    "america/havana": ["cuba"],
    "america/hermosillo": [],
    "america/indiana/indianapolis": [],
    "america/indiana/tell_city": [],
    "america/indiana/vevay": [],
    "america/indiana/vincennes": [],
    "america/indiana/winamac": [],
    "america/inuvik": [],
    "america/iqaluit": [],
    "america/jamaica": ["kingston"],
    "america/juneau": [],
    "america/kentucky/louisville": [],
    "america/kralendijk": ["bonaire"],
    "america/la_paz": ["bolivia", "sucre"],
    "america/lima": ["peru"],
    "america/los_angeles": [],
    "america/lower_princes": [],
    "america/maceio": [],
    "america/managua": ["nicaragua"],
    "america/manaus": [],
    "america/marigot": ["collectivity of saint martin"],
    "america/martinique": ["fort-de-france", "fort de france"],
    "america/matamoros": [],
    "america/mazatlan": [],
    "america/menominee": [],
    "america/merida": [],
    "america/metlakatla": [],
    "america/mexico_city": [],
    "america/miquelon": ["saint pierre and miquelon"],
    "america/moncton": [],
    "america/monterrey": [],
    "america/montevideo": ["uruguay"],
    "america/montserrat": [],
    "america/nassau": ["bahamas"],
    "america/new_york": ["washington dc"],
    "america/nipigon": [],
    "america/nome": [],
    "america/noronha": [],
    "america/north_dakota/beulah": [],
    "america/nuuk": [],
    "america/ojinaga": [],
    "america/panama": ["panama city"],
    "america/pangnirtung": [],
    "america/paramaribo": ["suriname"],
    "america/phoenix": [],
    "america/port-au-prince": ["haiti", "port au prince"],
    "america/port_of_spain": ["trinidad and tobago"],
    "america/porto_velho": [],
    "america/puerto_rico": ["san juan"],
    "america/punta_arenas": [],
    "america/rainy_river": [],
    "america/rankin_inlet": [],
    "america/recife": [],
    "america/regina": [],
    "america/resolute": [],
    "america/rio_branco": [],
    "america/santarem": [],
    "america/santiago": [],
    "america/santo_domingo": ["dominican republic"],
    "america/sao_paulo": [],
    "america/scoresbysund": ["ittoqqortoormiit"],
    "america/sitka": [],
    "america/st_barthelemy": ["gustavia"],
    "america/st_johns": [],
    "america/st_kitts": ["basseterre", "saint kitts and nevis"],
    "america/st_lucia": ["saint lucia", "castries"],
    "america/st_vincent": ["saint vincent and the grenadines"],
    "america/swift_current": [],
    "america/tegucigalpa": ["honduras"],
    "america/thule": ["thule air base", "pituffik"],
    "america/thunder_bay": [],
    "america/tijuana": [],
    "america/toronto": ["ottawa"],
    "america/tortola": ["british virgin islands"],
    "america/vancouver": [],
    "america/whitehorse": [],
    "america/winnipeg": [],
    "america/yakutat": [],
    "america/yellowknife": [],
    "antarctica/casey": [],
    "antarctica/davis": [],
    "antarctica/dumontdurville": ["dumont d'urville"],
    "antarctica/macquarie": [],
    "antarctica/mawson": [],
    "antarctica/mcmurdo": [],
    "antarctica/palmer": [],
    "antarctica/rothera": [],
    "antarctica/syowa": [],
    "antarctica/troll": [],
    "antarctica/vostok": [],
    "arctic/longyearbyen": [],
    "asia/aden": ["yemen", "sana", "sanaa", "sana'a"],
    "asia/almaty": ["nur-sultan", "astana"],
    "asia/amman": ["jordan"],
    "asia/anadyr": [],
    "asia/aqtau": [],
    "asia/aqtobe": ["aktobe"],
    "asia/ashgabat": ["turkmenistan"],
    "asia/atyrau": ["kazakhstan"],
    "asia/baghdad": ["iraq"],
    "asia/bahrain": ["manama"],
    "asia/baku": ["azerbaijan"],
    "asia/bangkok": ["thailand"],
    "asia/barnaul": [],
    "asia/beirut": ["lebanon"],
    "asia/bishkek": ["kyrgyzstan"],
    "asia/brunei": ["bandar seri begawan"],
    "asia/chita": [],
    "asia/choibalsan": [],
    "asia/colombo": ["sri lanka"],
    "asia/damascus": ["syria"],
    "asia/dhaka": ["bangladesh"],
    "asia/dili": ["timor-leste"],
    "asia/dubai": ["uae", "united arab emirates", "abu dhabi", "sharjah"],
    "asia/dushanbe": ["tajikistan"],
    "asia/famagusta": [],
    "asia/gaza": [],
    "asia/hebron": [],
    "asia/ho_chi_minh": ["hanoi", "vietnam", "ho chi minh city"],
    "asia/hong_kong": [],
    "asia/hovd": [],
    "asia/irkutsk": [],
    "asia/jakarta": [],
    "asia/jayapura": [],
    "asia/jerusalem": ["tel aviv", "acre", "haifa"],
    "asia/kabul": ["afghanistan"],
    "asia/kamchatka": [],
    "asia/karachi": ["pakistan", "islamabad", "rawalpindi", "lahore"],
    "asia/kathmandu": ["nepal"],
    "asia/khandyga": [],
    "asia/kolkata": ["india", "new delhi", "delhi"],
    "asia/krasnoyarsk": [],
    "asia/kuala_lumpur": [],
    "asia/kuching": [],
    "asia/kuwait": ["kuwait city"],
    "asia/macau": ["macao"],
    "asia/magadan": [],
    "asia/makassar": [],
    "asia/manila": ["philippines"],
    "asia/muscat": ["oman"],
    "asia/nicosia": [],
    "asia/novokuznetsk": [],
    "asia/novosibirsk": [],
    "asia/omsk": [],
    "asia/oral": [],
    "asia/phnom_penh": ["cambodia"],
    "asia/pontianak": [],
    "asia/pyongyang": ["north korea"],
    "asia/qatar": ["doha"],
    "asia/qostanay": [],
    "asia/qyzylorda": [],
    "asia/riyadh": ["saudi arabia"],
    "asia/sakhalin": [],
    "asia/samarkand": [],
    "asia/seoul": ["south korea"],
    "asia/shanghai": ["beijing", "guangzhou", "chongqing", "tianjin",
                      "chengdu", "nanjing", "wuhan", "xi'an", "hangzhou"],
    "asia/singapore": ["singapore"],
    "asia/srednekolymsk": [],
    "asia/taipei": ["taiwan"],
    "asia/tashkent": [],
    "asia/tbilisi": ["georgia"],
    "asia/tehran": ["iran"],
    "asia/thimphu": ["bhutan"],
    "asia/tokyo": ["japan", "kyoto", "yokoama", "osaka", "hiroshima"],
    "asia/tomsk": [],
    "asia/ulaanbaatar": [],
    "asia/urumqi": ["xinjiang"],
    "asia/ust-nera": [],
    "asia/vientiane": ["laos"],
    "asia/vladivostok": [],
    "asia/yakutsk": [],
    "asia/yangon": ["myanmar", "naypyidaw"],
    "asia/yekaterinburg": [],
    "asia/yerevan": ["armenia"],
    "atlantic/azores": [],
    "atlantic/bermuda": [],
    "atlantic/canary": [],
    "atlantic/cape_verde": ["praia"],
    "atlantic/faroe": ["faroe islands", "torshavn"],
    "atlantic/madeira": [],
    "atlantic/reykjavik": ["iceland"],
    "atlantic/south_georgia": ["south georgia and the south sandwich islands",
                               "sgssi"],
    "atlantic/stanley": ["falkland islands", "malvinas"],
    "atlantic/st_helena": ["saint helena, ascension and tristan da cunha"],
    "australia/adelaide": [],
    "australia/brisbane": [],
    "australia/broken_hill": [],
    "australia/currie": [],
    "australia/darwin": [],
    "australia/eucla": [],
    "australia/hobart": [],
    "australia/lindeman": [],
    "australia/lord_howe": [],
    "australia/melbourne": [],
    "australia/perth": [],
    "australia/sydney": [],
    "europe/amsterdam": [],
    "europe/andorra": ["andorra la vella"],
    "europe/astrakhan": [],
    "europe/athens": ["greece"],
    "europe/belgrade": ["serbia"],
    "europe/berlin": [],
    "europe/bratislava": ["slovakia"],
    "europe/brussels": ["belgium"],
    "europe/bucharest": ["romania"],
    "europe/budapest": ["hungary"],
    "europe/busingen": [],
    "europe/chisinau": ["moldova"],
    "europe/copenhagen": ["aarhus", "ronne"],
    "europe/dublin": ["ireland"],
    "europe/gibraltar": ["gibraltar"],
    "europe/guernsey": [],
    "europe/helsinki": ["finland"],
    "europe/isle_of_man": [],
    "europe/istanbul": ["turkey", "ankara"],
    "europe/jersey": ["saint helier"],
    "europe/kaliningrad": [],
    "europe/kiev": ["kyiv"],
    "europe/kirov": [],
    "europe/lisbon": [],
    "europe/ljubljana": ["slovenia"],
    "europe/london": ["united kingdom", "uk", "edinburg", "glasgow",
                      "cardiff", "belfast"],
    "europe/luxembourg": ["luxembourg city"],
    "europe/madrid": [],
    "europe/malta": ["valletta"],
    "europe/mariehamn": ["aland islands"],
    "europe/minsk": ["belarus"],
    "europe/monaco": ["monaco"],
    "europe/moscow": ["st petersburg"],
    "europe/oslo": ["norway"],
    "europe/paris": [],
    "europe/podgorica": ["montenegro"],
    "europe/prague": ["czech republic"],
    "europe/riga": ["latvia"],
    "europe/rome": ["italy"],
    "europe/samara": [],
    "europe/san_marino": ["san marino"],
    "europe/sarajevo": ["bosnia and herzegovina", "bosnia", "herzegovina"],
    "europe/saratov": [],
    "europe/simferopol": [],
    "europe/skopje": ["north macedonia"],
    "europe/sofia": ["bulgaria"],
    "europe/stockholm": ["sweden"],
    "europe/tallinn": ["estonia"],
    "europe/tirane": ["albania"],
    "europe/ulyanovsk": [],
    "europe/uzhgorod": [],
    "europe/vaduz": ["liechtenstein"],
    "europe/vatican": ["vatican city"],
    "europe/vienna": ["austria"],
    "europe/vilnius": ["lithuania"],
    "europe/volgograd": [],
    "europe/warsaw": ["poland"],
    "europe/zagreb": ["croatia"],
    "europe/zaporozhye": [],
    "europe/zurich": ["switzerland"],
    "indian/antananarivo": ["madagascar"],
    "indian/chagos": [],
    "indian/christmas": ["christmas island", "flying fish cove"],
    "indian/cocos": ["cocos islands", "keeling islands"],
    "indian/comoro": ["comoros", "moroni"],
    "indian/kerguelen": ["kerguelen island", "desolation island"],
    "indian/mahe": ["seychelles"],
    "indian/maldives": ["male"],
    "indian/mauritius": ["port louis"],
    "indian/mayotte": [],
    "indian/reunion": ["reunion"],
    "pacific/apia": ["samoa"],
    "pacific/auckland": ["wellington"],
    "pacific/bougainville": ["papua new guinea"],
    "pacific/chatham": ["chatham islands"],
    "pacific/chuuk": [],
    "pacific/easter": [],
    "pacific/efate": ["vanuatu"],
    "pacific/enderbury": [],
    "pacific/fakaofo": [],
    "pacific/fiji": ["suva"],
    "pacific/funafuti": ["tuvalu"],
    "pacific/galapagos": [],
    "pacific/gambier": [],
    "pacific/guadalcanal": ["solomon islands", "honiara"],
    "pacific/guam": ["dededo", "hagatna"],
    "pacific/honolulu": ["hawaii"],
    "pacific/kiritimati": [],
    "pacific/kosrae": [],
    "pacific/kwajalein": [],
    "pacific/majuro": [],
    "pacific/marquesas": [],
    "pacific/nauru": ["denigomodu", "yaren"],
    "pacific/niue": ["alofi"],
    "pacific/norfolk": ["norfolk island"],
    "pacific/noumea": ["new caledonia"],
    "pacific/pago_pago": ["american samoa"],
    "pacific/palau": ["koror", "ngerulmud"],
    "pacific/pitcairn": ["pitcairn islands", "adamstown"],
    "pacific/pohnpei": [],
    "pacific/port_moresby": ["papua new guinea"],
    "pacific/rarotonga": ["cook islands", "avarua"],
    "pacific/saipan": ["northern mariana islands"],
    "pacific/tahiti": [],
    "pacific/tarawa": [],
    "pacific/tongatapu": ["tonga"],
    "pacific/wallis": ["wallis and futuna", "mata utu"],
}


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

    raise UnknownTZCityException(f"Could not find the time zone for: {city}!")


def capitalize(name: str) -> str:
    """
    Return capitalized form of the input city or tz name.

    Raises UnknownTZCityException on unknown pattern
    """

    # For tz names (which have a '/')
    if '/' in name:
        tz, city = name.split('/')
        tz = tz.title()
        city = city.replace('_', ' ')
        city = caps_city(city)
        city = city.replace(' ', '_')
        return f"{tz}/{city}"
    return caps_city(name)


def caps_city(name: str) -> str:
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
                    raise UnknownTZCityException(
                        f"Could not capitalize '{word}'. Unknown pattern")
            else:
                new_word = word.title()
        new_words.append(new_word)
    return ' '.join(new_words)
