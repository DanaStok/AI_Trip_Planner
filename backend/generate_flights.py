from search_flights import search_flights


def get_flights(destinations, start_date, end_date,serpapi_key):
    for trip in destinations:
        flight = search_flights('TLV', trip['airport'], start_date, end_date,serpapi_key)
        print(flight)
        trip['flight'] = flight
        
    return destinations

