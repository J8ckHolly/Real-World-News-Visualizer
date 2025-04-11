import React, { useMemo, useState, useRef } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { MeshLineGeometry, MeshLineMaterial } from 'meshline/dist';
import { latLongToVector3, createGreatCircleArc } from './network-arc';
import { IRepData } from '@/types/index';

interface ArcBetweenNodesProps {
  startNode: IRepData;
  endNode: IRepData; 
  earthRadius: number;
}

export const MultipleArcs: React.FC<{
  startNode: IRepData;
  endNodes: IRepData[];
  earthRadius: number;
}> = ({ startNode, endNodes, earthRadius }) => {
  return (
    <>
      {endNodes.map((endNode, i) => (
        <ArcBetweenNodes
          key={i}
          startNode={startNode}
          endNode={endNode}
          earthRadius={earthRadius}
        />
      ))}
    </>
  );
};

const ArcBetweenNodes: React.FC<ArcBetweenNodesProps> = ({ startNode, endNode, earthRadius }) => {
  const materialRef = useRef<THREE.ShaderMaterial>(null!);
  const geometry = useMemo(() => {
    const start = latLongToVector3(startNode.latitude, startNode.longitude, earthRadius);
    const end = latLongToVector3(endNode.latitude, endNode.longitude, earthRadius);
    const points = createGreatCircleArc(start, end, earthRadius);

    const geo = new MeshLineGeometry();
    geo.setPoints(points);
    return geo;
  }, [startNode, endNode, earthRadius]);

  const material = useMemo(() => {
    return new MeshLineMaterial({
      lineWidth: 0.01,
      color: new THREE.Color('#00ff00'),
      dashArray: .2,
      dashRatio: 0.5,
      transparent: true,
      depthTest: false,
    } as any); // 👈 tell TS to chill
  }, []);

  useFrame(() => {
    if (materialRef.current) {
      materialRef.current.uniforms.dashOffset.value -= 0.003;
    }
  });

  return (
    <mesh>
      <primitive object={geometry} attach="geometry" />
      <primitive object={material} attach="material" ref={materialRef} />
    </mesh>
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
