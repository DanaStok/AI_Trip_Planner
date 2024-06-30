'use client';
import React, { useState, useEffect } from 'react';
import { sendDestinationRequest } from './handle_search.js';
import DestinationButtons from './DestinationButtons.js';

export default function TripPlanner() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [budget, setBudget] = useState(0);
  const [tripType, setTripType] = useState('');
  const [destinations, setDestinations] = useState([]);
  const [minEndDate, setMinEndDate] = useState('');
  const [today, setToday] = useState('');
  const [isLoading, setIsLoading] = useState(false); // Declare isLoading state

  useEffect(() => {
    const todayDate = new Date().toISOString().split('T')[0];
    setToday(todayDate);
    setStartDate(todayDate);
  }, []);

  useEffect(() => {
    if (startDate) {
      setMinEndDate(startDate);
      if (endDate && endDate < startDate) {
        setEndDate(startDate);
      }
    }
  }, [startDate, endDate]);
  
  useEffect(() => {
    if (budget !== undefined && budget < 0) {
      setBudget(0);
    }
  }, [budget]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true); // Start loading
    try {
      const response = await sendDestinationRequest(startDate, endDate, budget, tripType);
      console.log(response);
      setDestinations(Array.isArray(response) ? response : []);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false); // Stop loading regardless of outcome
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 mt-[-25vh]">
      <h1 className="text-4xl font-bold mb-8">Trip Planner</h1>
      <form onSubmit={handleSubmit} className="flex flex-wrap justify-center items-center gap-4 w-full px-4">
        <div className="flex flex-col w-full max-w-xs">
          <label htmlFor="startDate" className="mb-1 font-semibold" style={{ paddingLeft: '20px' }}>Start Date</label>
          <input
            type="date"
            id="startDate"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="input input-bordered"
            min={today}
          />
        </div>
        <div className="flex flex-col w-full max-w-xs">
          <label htmlFor="endDate" className="mb-1 font-semibold" style={{ paddingLeft: '20px' }}>End Date</label>
          <input
            type="date"
            id="endDate"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="input input-bordered"
            min={minEndDate}
          />
        </div>
        <div className="flex flex-col w-full max-w-xs">
          <label htmlFor="budget" className="mb-1 font-semibold" style={{ paddingLeft: '20px' }}>Hotel Budget $</label>
          <input
            type="number"
            id="budget"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
            className="input input-bordered"
          />
        </div>
        <div style={{paddingTop: '30px'}}>
          <select
            value={tripType}
            onChange={(e) => setTripType(e.target.value)}
            className="input input-bordered max-w-xs"
          >
            <option value="">Select Trip Type</option>
            <option value="leisure">Leisure</option>
            <option value="business">Business</option>
            <option value="adventure">Adventure</option>
            <option value="romantic">Romantic</option>
            <option value="family">Family</option>
            <option value="ski">Ski</option>
          </select>
        </div>
        <button type="submit" className="btn btn-outline btn-success">
          Submit
        </button>
      </form>
      {destinations.length > 0 && <DestinationButtons destinations={destinations} />}
      {isLoading && (
        <div className="absolute inset-0 flex justify-center items-center bg-black bg-opacity-50 z-50">
          <span className="loading loading-spinner loading-lg text-white"></span>
        </div>
      )}
    </main>
  );  
}
