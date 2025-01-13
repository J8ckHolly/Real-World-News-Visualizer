import React, { useMemo, useCallback, useRef } from 'react';
import * as THREE from 'three';
import { IRepData } from '@/types/index';


interface recCircNodesProps {
    repsGeoInfo: IRepData[];
    earthRadius: number;
    onNodeHover: (nodeRepsGeoInfo: IRepData | null) => void;
  }

const redCircleNode: React.FC<recCircNodesProps> = React.memo(
    ({ repsGeoInfo, earthRadius, onNodeHover }) =>{
     const earthRadiusRef = useRef(earthRadius)








    }



)