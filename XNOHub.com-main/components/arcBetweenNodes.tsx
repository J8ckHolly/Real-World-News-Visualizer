import React, { useMemo, useState } from 'react';
import * as THREE from 'three';
import { Line } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';
import { latLongToVector3, createGreatCircleArc } from './network-arc';
import { IRepData } from '@/types/index';

interface ArcBetweenNodesProps {
  startNode: IRepData;
  endNode: IRepData;
  earthRadius: number;
}

const ArcBetweenNodes: React.FC<ArcBetweenNodesProps> = ({ startNode, endNode, earthRadius }) => {
  const startPos = useMemo(() => latLongToVector3(startNode.latitude, startNode.longitude, earthRadius), [
    startNode.latitude,
    startNode.longitude,
    earthRadius
  ]);

  const endPos = useMemo(() => latLongToVector3(endNode.latitude, endNode.longitude, earthRadius), [
    endNode.latitude,
    endNode.longitude,
    earthRadius
  ]);

  const arcPoints = useMemo(() => {
    return createGreatCircleArc(startPos, endPos, earthRadius);
  }, [startPos, endPos, earthRadius]);

  // State for controlling the progress of the pulsating effect
  const [progress, setProgress] = useState(0);

  // Use the frame hook to animate the progress
  useFrame((state, delta) => {
    setProgress((prevProgress) => {
      const newProgress = prevProgress + delta * 0.5; // Adjust speed by changing multiplier
      if (newProgress >= 1) {
        return 1; // Cap the progress at 1 (end of arc)
      }
      return newProgress;
    });
  });

  // Calculate the visible portion of the arc based on progress
  const visibleArcLength = progress * getTotalArcLength(arcPoints);
  let currentLength = 0;
  const visiblePoints: THREE.Vector3[] = [];

  for (let i = 1; i < arcPoints.length; i++) {
    const segmentLength = arcPoints[i].distanceTo(arcPoints[i - 1]);
    currentLength += segmentLength;

    // If the segment is within the visible portion, add it to the visible points
    if (currentLength <= visibleArcLength) {
      visiblePoints.push(arcPoints[i - 1]);
    } else {
      // Add the fraction of the last segment based on how far the progress has gone
      const remainingLength = visibleArcLength - (currentLength - segmentLength);
      const t = remainingLength / segmentLength;
      visiblePoints.push(arcPoints[i - 1].lerp(arcPoints[i], t));
      break;
    }
  }

  return (
    <Line
      points={visiblePoints}
      color={new THREE.Color(0x00ff00)} // Green color for the arc
      lineWidth={2}
      transparent
      opacity={1} // No opacity fade, the tail is disappearing visually based on the points
    />
  );
};

// Helper function to calculate the total length of the arc
const getTotalArcLength = (points: THREE.Vector3[]): number => {
  let totalLength = 0;
  for (let i = 1; i < points.length; i++) {
    totalLength += points[i].distanceTo(points[i - 1]);
  }
  return totalLength;
};

export default ArcBetweenNodes;
