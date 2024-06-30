from serpapi import GoogleSearch

def search_flights(origin, destination, start_date, end_date, serpapi_key):
    params = {
        "api_key": f"{serpapi_key}", 
        "engine": "google_flights",
        "q": f"flights from {origin} to {destination}",
        "flight_origin": origin,
        "flight_destination": destination,
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": start_date,  
        "type": '1',  # Round trip
        "return_date": end_date,  
    }

    # Search for flights
    search = GoogleSearch(params)
    try:
        flights_data = search.get_dict()
    except Exception as e:
        return {"Error": str(e)}

    flight_options = flights_data.get('best_flights', []) + flights_data.get('other_flights', [])

    if not flight_options:
        return {"Apologies": "No flights found for the specified search criteria."}

    # Initializing variables
    cheapest_flight_price = float('inf')
    cheapest_flight = None

    # Iterating over each flight option to find the cheapest one
    for option in flight_options:
        price = option['price']
        if price < cheapest_flight_price:
            cheapest_flight_price = price
            cheapest_flight = option

    if not cheapest_flight:
        return {"Sorry": "Could not determine the cheapest flight from available options."}

    #find return flight
    try:
        params['departure_token'] = cheapest_flight['departure_token']
        search = GoogleSearch(params)
        return_flights_data = search.get_dict()
        if not return_flights_data or not return_flights_data['other_flights']:
            return {"Error": "Could not determine the return flight or no return flights available."}
    except Exception as e:
        return {"Error": str(e)}
    
    if not return_flights_data:
        return {"Sorry" : "Could not determine the return flight."}

    # Extracting layover details, if any
    out_layovers = cheapest_flight['layovers']
    in_layovers = return_flights_data['other_flights'][0]['layovers']
    
    # Construct layover string for out-going flight
    if out_layovers:
        out_layover_details = layover_finder(out_layovers)
    else:
        out_layover_details = "Direct flight"
        
    # Construct layover string for in-going flight   
    if in_layovers:
        in_layover_details = layover_finder(in_layovers)
    else:
        in_layover_details = "Direct flight"
    

    # Creating a dictionary to store flight details
    flight_details = {
        "Price": "${:,.0f}".format(cheapest_flight_price),
        "Flight Type": cheapest_flight['type'],
        "Airline": cheapest_flight['flights'][0]['airline'],
        "Out-Going Departure": f"Departs from {cheapest_flight['flights'][0]['departure_airport']['name']} at {cheapest_flight['flights'][0]['departure_airport']['time']}",
        "Out-Going Arrival": f"Arrives at {cheapest_flight['flights'][len(cheapest_flight['flights'])-1]['arrival_airport']['name']} at {cheapest_flight['flights'][len(cheapest_flight['flights'])-1]['arrival_airport']['time']}",
        "Out-Going Layover Details": out_layover_details,
        "In-Coming Departure": f"Departs from {return_flights_data['other_flights'][0]['flights'][0]['departure_airport']['name']} at {return_flights_data['other_flights'][0]['flights'][0]['departure_airport']['time']}",
        "In-Coming Arrival": f"Arrives at {return_flights_data['other_flights'][0]['flights'][len(return_flights_data['other_flights'][0]['flights'])-1]['arrival_airport']['name']} at {return_flights_data['other_flights'][0]['flights'][len(return_flights_data['other_flights'][0]['flights'])-1]['arrival_airport']['time']}",
        "In-Coming Layover Details": in_layover_details
    }

    return flight_details

def format_duration(minutes):
    """Convert minutes to a string formatted as hours and minutes."""
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}h {remaining_minutes}m" if hours else f"{remaining_minutes}m"

def layover_finder(trip_itinerary):
    layover_details = ""
    order = ["First", "Second", "Third", "Fourth"]
    i = 0
    for layover in trip_itinerary:
        layover_duration = layover['duration']
        formatted_layover = format_duration(layover_duration)
        if len(trip_itinerary) == 1:
            layover_details += f"Layover at {layover['name']} for {formatted_layover}\n"
        else:
            layover_details += f"{order[i]} Layover at {layover['name']} for {formatted_layover}\n "
            i += 1
    return layover_details
        
