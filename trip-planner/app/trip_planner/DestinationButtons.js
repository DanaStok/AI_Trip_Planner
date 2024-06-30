'use client';
import React, { useState } from 'react';
import ShopPopup from '../Pops/Pop.jsx';
import PicsPopup from '../Pops/Pics.jsx';
import { sendImageRequest } from './handle_images.js';
import './buttons.css'


const DestinationButtons = ({ destinations }) => {
  const [showPopup, setShowPopup] = useState(false);
  const [popupType, setPopupType] = useState('');
  const [popupContent, setPopupContent] = useState({});
  const [popupImage, setPopupImage] = useState('');
  const [showPicsPopup, setShowPicsPopup] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [dropdownVisible, setDropdownVisible] = useState(false);

  const handleLinkClick = async (content, type, image) => {
    setDropdownVisible(false);
    try {
      setIsLoading(true)
      // Conditionally make the API call for type 'FOMO'
      if (type === 'FOMO') {
        await sendImageRequest(content);
        console.log("Send this location:", content.location);
        // Assuming response contains the content for the popup, update state with the response data
        setPopupContent(content.location); // Adjust based on actual response structure
        setPopupType(type);
        setShowPicsPopup(true);
      } else {
        // For other types, update state directly
        setPopupContent(content);
        setPopupType(type);
        setPopupImage(image);
        setShowPopup(true);
      }
    } catch (error) {
      console.error("Failed to send image request:", error);
      // Handle error appropriately, maybe set some error message in state and show in UI
    }finally {
      setIsLoading(false); // Set loading state to false after the API call is complete
    }
  };

  const handleClosePopup = () => {
    setShowPopup(false);
    setShowPicsPopup(false);
    setPopupType('');
    setPopupContent({});
    setPopupImage('');
  };

  const toggleDropdown = () => setDropdownVisible(!dropdownVisible);

  return (
    <div className="mt-8">
        {isLoading && (
          <div className="absolute inset-0 flex justify-center items-center bg-black bg-opacity-50 z-50">
            <span className="loading loading-spinner loading-lg text-white"></span>
          </div>
        )}
      <div className="flex justify-around items-center flex-wrap w-full">
        {destinations.map((destination, index) => (
          <div key={index} className="dropdown dropdown-hover">
            <div tabIndex={0} role="button" className="btn m-1" onClick={toggleDropdown}>
              {destination.location}, {destination.country}
            </div>
            {dropdownVisible && (
            <ul tabIndex={0} className="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
              <li><a href="#" onClick={() => handleLinkClick(formatDetails(destination.flight), 'Flight', '/images/background.png')}>Flight Details</a></li>
              <li><a href="#" onClick={() => handleLinkClick(formatDetails(destination.hotel), 'Hotel', '/images/background.png')}>Hotel Details</a></li>
              <li><a href="#" onClick={() => handleLinkClick(destination.itinerary, 'Itinerary', '/images/background.png')}>Itinerary</a></li>
              <li><a href="#" onClick={() => handleLinkClick(getPrice(destination.hotel, destination.flight), 'Price', '/images/background.png')}>Total Price</a></li>
              <li><a href="#" onClick={() => handleLinkClick(destination, 'FOMO', '')}>Give me FOMO</a></li>
            </ul>
            )}
          </div>
        ))}
      </div>

      {showPopup && (
        <ShopPopup content={popupContent} image={popupImage} title={popupType} onClose={handleClosePopup} />
      )}
      {showPicsPopup && (
        <PicsPopup location={popupContent} type={popupType} onClose={handleClosePopup} />
      )}
    </div>
  );
};

// Function to format flight details into a JSX element with keys in bold
const formatDetails = (details) => {
  return (
    <div>
      {Object.entries(details).map(([key, value], index) => (
        <div key={index}>
          <strong>{key}</strong>: {value}
        </div>
      ))}
    </div>
  );
};


const getPrice = (hotel, flight) => {
  // Helper function to remove the dollar sign and convert the price to a number
  const extractAndConvertPrice = (priceStr) => {
    // Ensure priceStr is defined and a string
    if (typeof priceStr !== 'string') {
      return 0;
    }
    const price = parseInt(priceStr.replace('$', '').replace(/,/g, ''), 10);
    // Check if the result is NaN (Not a Number) and if so, return 0
    return isNaN(price) ? 0 : price;
  };

  // Extract prices from both hotel and flight
  const hotelPrice = extractAndConvertPrice(hotel['Price']);
  const flightPrice = extractAndConvertPrice(flight['Price']);

  const totalPrice = hotelPrice + flightPrice;

  // Format the total price back into a string with a dollar sign
  return `$${totalPrice}`;
};



export default DestinationButtons;
