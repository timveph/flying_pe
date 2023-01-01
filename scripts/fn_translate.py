
translator_dict = {
                # helper spreadsheet: https://docs.google.com/spreadsheets/d/1y6ANROaiR45ZLqr5lUh2afah4hAjzpoRD1ASegqrxHs/edit#gid=0
                # tabs
                "Flight Tracker":{"pl":"Śledzenie lotów"}
                ,"Stats":{"pl":"Statystyki"}
                #flight_tracker.py
                ,'Next Flight': {'pl': 'Następny lot'}
                ,"local":{"pl":"lokalny"}
                ,"Number of queries left":{"pl":"Pozostały liczba zapytań"}
                ,"Unfortunately, we cannot track any flights":{"pl":"Niestety nie możemy śledzić żadnych lotów"}
                ,"**Live tracking** info from <u>1 hour</u> before the flight.":{"pl":"**Śledzenie na żywo** Informacje od <u>1 godzinę</u> przed lotem."}
                ,"The flight has landed at approximately ":{"pl":"Dzisiejszy lot wylądował w przybliżeniu "}
                ,"Flight {flight_iata} has landed at approximately ":{"pl":"Flight {Flight_iata} wylądował w przybliżeniu "}
                ,"**Departing**":{"pl":"**Odchodzenie**"}
                ,"Time remaining":{"pl":"Pozostały czas"}
                ,"total":{"pl":"całkowity"}
                ,"Speed":{"pl":"Prędkość"}
                ,"Distance Remaining":{"pl":"Pozostała odległość"}
                ,"Altitude":{"pl":"Wysokość"}
                ,"**Landing at**":{"pl":"**lądowanie w**"}
                ,"<sub>Number of queries left: ":{"pl":"<sub> Liczba pozostałych zapytań: "}
                # home.py
                ,"Flights":{"pl":"Loty"}
                ,"Distance (km)":{"pl":"Odległość (km)"}
                ,"Time on :airplane: (days)":{"pl":"Czas na :airplane: (dni)"}
                ,"Countries Visited":{"pl":"Odwiedzone kraje"}
                ,"Cities Visited":{"pl":"Odwiedzone miasta"}
                ,"Nights Away":{"pl":"Noce dalej"}
                ,"Loading...":{"pl":"Ładowanie..."}
                ,"<sub><u>Note:</u> **Bermuda** and **Barbados** are not represented on map. However, the metrics account for the trips to these countries.</sub>":{"pl":"<sub><u>Uwaga:</u> **Bermuda** i **Barbados** nie są reprezentowane na mapie. Jednak wskaźniki uwzględniają wycieczki do tych krajów. </sub>"}
                ,"There is no map info in plotly choropleth... Sorry.... but nothing I can do for now.":{"pl":"Nie ma informacji o mapie w plotly choropleth ... przepraszam ... ale na razie nic, co nie mogę zrobić."}
                # map hover text - home.py
                ,"Country Code":{"pl":"Kod pocztowy"}
                ,"Capital":{"pl":"Stolica"}
                ,"Visits":{"pl":"Odwiedziny"}
                ,"Sub-region Name":{"pl":"Nazwa podregionu"}
                ,"Nights away":{"pl":"Noce dalej"}
                }

def fn_translate(language, text):
    # If dict.get() finds no value with `word` it will return
    # None by default. We override it with an empty dictionary `{}`
    # so we can always call `.get` on the result.
    translated = translator_dict.get(text, {}).get(language)

    if language == 'en':
        # print(text)
        return text
    elif translated is None:
        # print(translated)
        return "Error translating"
    else:
        # print(translated)
        return translated