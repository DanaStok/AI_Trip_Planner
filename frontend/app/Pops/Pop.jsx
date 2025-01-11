import React from 'react';
import './pop.css';

const ShopPopup = ({ content, onClose, image, title }) => {
  // Function to determine the appropriate width class based on content length
  const getWidthClass = () => {
    if (content.length > 800) {
      return "w-160"; // Extra wide width (768px) for very long content
    } else if (content.length > 500) {
      return "w-128"; // Wider width (512px) for moderately long content
    }
    return "w-96"; // Default width (384px) for shorter content
  };

  // Determine classes for layout based on title
  const layoutClasses = title === "Price" ? "flex items-center justify-center text-center" : "flex flex-col items-center p-4";
  const contentAlignmentClass = title === "Price" ? "items-center justify-center" : "flex-grow";

  return (
    <div className="fixed inset-0 flex items-center justify-center">
      <div className={`card ${getWidthClass()} bg-base-100 shadow-xl image-full`}>
        <figure><img src={image} alt="Destination picture" onError={() => console.log('Error loading image')} /></figure>
        <div className={`card-body ${layoutClasses} w-full`} style={{ color: 'white' }}>
          <h2 className="card-title">{title}</h2>
          <div className={`popup-content w-full ${contentAlignmentClass}`} style={{ whiteSpace: 'pre-wrap', overflowY: 'auto' }}>
            <p>{content}</p>
          </div>
          <div className="card-actions w-full flex justify-end">
            <button className="btn btn-primary" onClick={onClose}>Close</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ShopPopup;
