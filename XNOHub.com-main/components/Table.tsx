import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMapMarkerAlt } from '@fortawesome/free-solid-svg-icons';
import "/node_modules/flag-icons/css/flag-icons.min.css";

type TableProps = {
  title: string;
  location: string;
  description: string;
  countryCode: string; // Add this prop for the country flag
};

const Table: React.FC<TableProps> = ({ title, location, description, countryCode }) => {
  return (
    <div className="bg-white text-black border-4 border-black p-6 relative">
      
      <div className="absolute top-2 left-2">
      <span className={`fi fi-${countryCode.toLowerCase()} fis absolute rounded-full`} />
      </div>
      <div className="flex flex-col items-center justify-between h-auto w-96 rounded-lg shadow-md relative">
      {/* Title */}
      <h3 className="font-bold text-lg mb-2">{title}</h3>

      {/* Location with location pin icon */}
      <p className="text-sm mb-2 flex items-center">
        <FontAwesomeIcon icon={faMapMarkerAlt} className=" text-red-500 mr-2" />
        {location}
      </p>

      {/* Description */}
      <p className="text-base text-left">{description}</p>
      </div>
    </div>
  );
};

export default Table;
