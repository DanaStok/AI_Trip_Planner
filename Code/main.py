from typing import List
from generate_destinations import destination_suggestion
from generate_image import generate_image
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class DestinationRequest(BaseModel):
    start_date_input: str
    end_date_input: str
    budget_input: float
    trip_type_input: str
   
class Destination(BaseModel):
    location: str
    country: str
    airport: str 


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/suggest_destination/")
async def search_for_locations(request: DestinationRequest):
    try:
        # Correct way to access data from Pydantic model
        print("Received data:", request.model_dump())
        response = destination_suggestion(request.model_dump())  
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/generate_images/")
async def generate_images(request: Destination): 
    try:
        generate_image(request.model_dump())  
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))