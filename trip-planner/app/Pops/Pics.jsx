import React, { useState } from 'react';

const PicsPopup = ({ location, onClose, title }) => {
  const formattedLocation = location.replace(/ /g, '_');
  const images = Array.from({ length: 4 }, (_, i) => `/images/${formattedLocation}_image_${i + 1}.png`);
  const [currentIndex, setCurrentIndex] = useState(0);

  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className=" w-96 image-full">
        <div className="carousel w-full rounded-box">
          <div key={currentIndex}>
            <img
              src={images[currentIndex]}
              className="w-full"
              alt={`${location} Image ${currentIndex + 1}`}
              onError={() => console.log('Error loading image')}
            />
          </div>
        </div>
        <div className="card-body">
          <div className="card-actions justify-end">
            <button className="btn btn-primary" onClick={handleNext}>
              Next
            </button>
            <button className="btn btn-primary" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PicsPopup;