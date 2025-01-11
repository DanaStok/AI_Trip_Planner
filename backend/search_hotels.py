from serpapi import GoogleSearch

def search_hotels(location, checkin_date, checkout_date, budget,serpapi_key):
    params = {
        "api_key": f"{serpapi_key}",
        "engine": "google_hotels",
        "q": f"hotels in {location}",
        "check_in_date": checkin_date,
        "check_out_date": checkout_date,
        "currency": "USD",
        "max_price": budget, 
        "sort_by": '3' #sort low price to high price 
    }

    search = GoogleSearch(params)
    options = search.get_dict()
    
    hotel_options = options.get('properties', [])
    
    if not hotel_options:
        return {"Apologies": "No hotels found for the specified search criteria."}
    
    best_hotel = hotel_options[-1]
    best_hotel_details = { 
        "Name": (best_hotel['name']),
        "Type": best_hotel['type'],
        "Price": best_hotel['total_rate']['before_taxes_fees'],
        
        
    }
    return best_hotel_details
            