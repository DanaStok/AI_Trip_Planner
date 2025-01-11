from search_hotels import search_hotels

def get_hotels(destinations, checkin_date, checkout_date, budget,serpapi_key):
    for dest in destinations:
        hotel = search_hotels(dest['location'], checkin_date, checkout_date, int(budget),serpapi_key)
        dest['hotel'] = hotel
        
    return destinations

