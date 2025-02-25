'use client';

import React, { useState, useEffect } from 'react';
import ThreeSceneClient from './three-scene-client';
import { RepsData } from '@/data/defualtMergedRepsData';

const ThreeSceneClientWrapper: React.FC = () => {
  const [serverDateTime, setServerDateTime] = useState<Date | null>(null);

  useEffect(() => {
    setServerDateTime(new Date());
  }, []);

  if (RepsData.length === 0) {
    return <div className="font-[40px]">Loading data... Bitch ...</div>;
  }

  return (
    <ThreeSceneClient repsGeoInfo={RepsData} serverDateTime={serverDateTime} />
  );
};

export default ThreeSceneClientWrapper;
