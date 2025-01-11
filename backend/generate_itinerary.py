from openai_api_call import openai_api_call
from datetime import datetime, timedelta


def get_itinerary(places_formatted, trip_type_input, trip_month, start_date_input, end_date_input,openai_key):
    itineraries = []
    for destination in places_formatted:
        prompt_text = format_text(destination, trip_type_input, trip_month, start_date_input, end_date_input)
        suggested_activity = openai_api_call(prompt_text,openai_key)
        
        # Add the itinerary to the destination's dictionary
        destination['itinerary'] = suggested_activity
        itineraries.append(destination)
    
    return itineraries

def format_text(destination, trip_type_input, trip_month, start_date_input, end_date_input):
     # Parse the input dates
    start_date = datetime.strptime(start_date_input, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_input, '%Y-%m-%d')
    
    # Calculate the duration of the trip in days
    trip_duration = (end_date - start_date).days + 1
    
    # Generate an itinerary template that includes each day
    itinerary_template = ''
    for day in range(trip_duration):
        day_date = (start_date + timedelta(days=day)).date()
        itinerary_template += f"Day {day + 1}, {day_date}: [Insert activities related to {trip_type_input}]\n"
        
    prompt_text = (
        f"I want to travel to {destination['location']}, {destination['country']} in {trip_month}. "
        f"I am interested in activities related to {trip_type_input}. "
        f"My trip dates are from {start_date_input} to {end_date_input}. "
        f"Please format the response as follows: {itinerary_template}."
        f"Give me a response of a maximum of 1000 characters!"
    )
    
    return prompt_text
