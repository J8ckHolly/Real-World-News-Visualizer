import React from 'react';
import countryData from "flag-icons/country.json";
import "/node_modules/flag-icons/css/flag-icons.min.css";
import "./Gateway.css"

interface GatewayProps {
  country: string;
  swap: (param: string) => void; // Void function
}

const getCountryCode = (countryName: string): string | undefined => {
    const country = countryData.find((country) => country.name === countryName);
    return country ? country.code : undefined;
}

const GatewayComponent: React.FC<GatewayProps> = ({ country, swap }) => {
  const swapClick = () => {
    swap(country);
  }
  let CC = getCountryCode(country)

  if (!CC) {
      CC = 'unknown'; // Or any default value you prefer
  }
  return (
    <div onClick={swapClick}>
    <span className={`fi fi-${CC.toLowerCase()} extendedFlag flag-icon`}></span>
    </div>
  );
};

export default GatewayComponent;

