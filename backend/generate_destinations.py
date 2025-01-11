import datetime
import re
from openai_api_call import openai_api_call
from generate_itinerary import get_itinerary
from generate_flights import get_flights
from generate_hotels import get_hotels
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the API key from the environment variables
openai_key = os.getenv('OPENAI_API_KEY')
serpapi_key = os.getenv('SERPAPI_KEY')

def destination_suggestion(dict_input):
    # Extract inputs from the dictionary
    start_date_input = dict_input['start_date_input']
    end_date_input = dict_input['end_date_input']
    budget_input = dict_input['budget_input']
    trip_type_input = dict_input['trip_type_input']
    
    # Convert the start date input to a datetime object to extract the month
    start_date = datetime.datetime.strptime(start_date_input, "%Y-%m-%d")
    trip_month = start_date.month

    # API call to get suggested places
    prompt_text = format_text(trip_month, trip_type_input)
    suggested_places = openai_api_call(prompt_text, openai_key)
    
    # Formatting the returned data for better usability
    places_formatted = format_places(suggested_places)
    dest_with_itinerary = get_itinerary(places_formatted, trip_type_input, trip_month, start_date_input, end_date_input,openai_key)
    dest_with_flight = get_flights(dest_with_itinerary, start_date_input, end_date_input, serpapi_key)
    final_destinations = get_hotels(dest_with_flight, start_date_input, end_date_input, int(budget_input), serpapi_key)
    
    if not final_destinations:
        return [{"No Result:"}]
    return final_destinations

    
def format_places(suggested_places):
   
    # Splitting the string into lines and stripping unnecessary whitespace
    lines = [line.strip() for line in suggested_places.strip().split('\n')]

    data = []
    for line in lines:
        parts = line.split('-')
        entry = {
            "location": re.sub(r"^[0-9]+\. ", "", parts[0].strip()),  # Removing leading numbers and extra spaces
            "country": parts[1].strip(),
            "airport": parts[2].strip()
        }
        data.append(entry)

    return data

def format_text(trip_month, trip_type_input):

    response_format = "Destination-Region/Country-Nearest Airport Code"
    example = "Gold Coast-Australia-OOL\nMaui-Hawaii-OGG\nJeffreys Bay-South Africa-PLZ\nSiargao-Philippines-IAO\nHossegor-France-BIQ"
    prompt_text = (
        f"I want to travel in {trip_month} and am interested in {trip_type_input}. "
        f"Please list the top 5 destinations in the world for this kind of trip. "
        f"Format each destination like this: {response_format}. "
        f"For example:\n{example}"
    )
    return prompt_text

