import React, { useState, useEffect } from "react";

const TimeDisplay: React.FC = () => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" });
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString([], {
      month: "long",
      day: "numeric",
      year: "numeric",
    });
  };

  return (
    <div className="border-2 border-white p-2 text-center bg-transparent rounded-lg">
      <div className="text-3xl font-bold text-white">{formatTime(currentTime)}</div>
      <div className="text-md text-white">{formatDate(currentTime)}</div>
    </div>
  );
};

export default TimeDisplay;
