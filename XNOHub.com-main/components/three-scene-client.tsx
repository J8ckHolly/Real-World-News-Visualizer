'use client';

import React, {
  useRef,
  useState,
  useEffect,
  useCallback,
  useMemo
} from 'react';
import { Canvas } from '@react-three/fiber';
import {
  OrbitControls,
  Stars,
  PerspectiveCamera,
  Stats
} from '@react-three/drei';
import * as THREE from 'three';
import { IRepData } from '@/types/index'; 
import ThreeMesh from '@/components/three-mesh';
import { CloudMesh } from '@/components/three-cloud-mesh';
import { ConfirmationHistoryTable } from '@/components/confirmation-history-table'; //Eventually -Understand
import { useConfirmations } from '@/providers/confirmation-provider'; //Eventually - Understand
import { parseNanoAmount } from '@/lib/parse-nano-amount';//Eventually - Understand
import { Vector3 } from 'three';
//import { scaleRocketCount } from '@/lib/scale-rocket-count';// Kill
import { Button } from '@/components/ui/button';
import { Rocket, Eye, Globe } from 'lucide-react'; // Understand
//import RocketAnimationManager from '@/components/rocket-animation-manager'; //Kill
import { APP_CONFIG } from '@/constants/config'; //Understand - Keep
import { StarlinkMesh } from '@/components/starlink-mesh'; //Kill -understand



function getRandomPositionOnGlobe(radius: number = 1.2): Vector3 {
  const phi = Math.random() * Math.PI * 2;
  const theta = Math.acos(Math.random() * 2 - 1);

  const x = radius * Math.sin(theta) * Math.cos(phi);
  const y = radius * Math.sin(theta) * Math.sin(phi);
  const z = radius * Math.cos(theta);

  return new Vector3(x, y, z);
}

const calculatePosition = (
  lat: number,
  long: number,
  radius: number
): THREE.Vector3 => {
  const phi = (90 - lat) * (Math.PI / 180);
  const theta = (long + 180) * (Math.PI / 180);
  const x = -radius * Math.sin(phi) * Math.cos(theta);
  const y = radius * Math.cos(phi);
  const z = radius * Math.sin(phi) * Math.sin(theta);
  return new THREE.Vector3(x, y, z);
}; 

const calculatePolarCoordinates = (
  x: number, 
  y: number, 
  z: number
 ): THREE.Vector3 => {
  const radius = Math.sqrt(x * x + y * y + z * z); // Calculate the radial distance
  
  const theta = Math.atan2(y, x); // Azimuthal angle (in radians) in the XY-plane
  
  const psi = Math.acos(z / radius); // Polar angle (in radians) from the Z-axis
  
  return new THREE.Vector3(radius, theta, psi);
};

const getCameraPolarPos = () => {return;}; //Depent on hoverNode
const calculateNodePolarPos = () => {return;} //Depent on hoverNode 


interface ThreeSceneClientProps {
  repsGeoInfo: IRepData[];
  serverDateTime: Date | null;
}

const ThreeSceneClient: React.FC<ThreeSceneClientProps> = ({
  repsGeoInfo,
  serverDateTime
}) => {
  const EarthRadiusInKm = 6357; // Earth's equatorial radius in kilometers
  const lightRef = useRef<THREE.DirectionalLight>(null);
  const [simulationTime, setSimulationTime] = useState<Date>(
    serverDateTime || new Date()
  );
  const [hoveredNode, setHoveredNode] = useState<IRepData | null>(null);
  const { confirmationHistory: confirmations } = useConfirmations();
  const [launchQueue, setLaunchQueue] = useState<Vector3[]>([]);
  const [NodePos, setNodePos] = useState<THREE.Vector3>(new THREE.Vector3());
  const [NodePosPolar, setNodePosPolar] = useState<THREE.Vector3>(new THREE.Vector3());
  const [hoverNodePol, setHoverNodePol] = useState<THREE.Vector3>(new THREE.Vector3());
  const [isRocketView, setIsRocketView] = useState(false);
  const cameraRef = useRef<THREE.PerspectiveCamera>(null);
  const [activeRocketIndex, setActiveRocketIndex] = useState<number | null>(
    null
  ); // Track the active rocket index
  const [rocketCount, setRocketCount] = useState(0);
  const rocketManagerRef = useRef<{
    addRocket: (position: Vector3) => void;
  } | null>(null);
  const [distanceFromEarth, setDistanceFromEarth] = useState<number>(0); // State to hold distance
  const [isStarlinkView, setIsStarlinkView] = useState(false);
  const [activeStarlinkIndex, setActiveStarlinkIndex] = useState<number | null>(
    null
  );
  
  useEffect(() =>{
  if (hoveredNode) {
    setNodePos(calculatePosition(hoveredNode.latitude, hoveredNode.longitude, 1));
    setNodePosPolar(calculatePolarCoordinates(NodePos.x, NodePos.y, NodePos.z));
  }
}, [hoveredNode]
  );

  useEffect(() =>{
    if(cameraRef.current){
    setHoverNodePol(calculatePolarCoordinates(cameraRef.current.position.x,
      cameraRef.current.position.y,
      cameraRef.current.position.z
    ))
  }
  }, [hoveredNode]
  );



  const moveToNextRocket = useCallback(() => {
    if (isRocketView && rocketCount > 0) {
      setActiveRocketIndex((prevIndex) => {
        if (prevIndex === null) return 0;
        return (prevIndex + 1) % rocketCount;
      });
    }
  }, [isRocketView, rocketCount]);

  const toggleStarlinkView = useCallback(() => {
    setIsStarlinkView((prev) => !prev);
    if (!isStarlinkView) {
      setActiveStarlinkIndex(0);
    } else {
      setActiveStarlinkIndex(null);
    }
    setIsRocketView(false); // Disable rocket view when entering starlink view
  }, [isStarlinkView]);

  const moveToNextStarlink = useCallback(() => {
    if (isStarlinkView) {
      setActiveStarlinkIndex((prev) => {
        if (prev === null) return 0;
        return (prev + 1) % 6; // Assuming 6 satellites
      });
    }
  }, [isStarlinkView]);

  useEffect(() => {
    if (serverDateTime) {
      setSimulationTime(serverDateTime);
    }
  }, [serverDateTime]);


  const handleRocketComplete = (id: string) => {
    setRocketCount((prevCount) => prevCount - 1);
  };

  const handleRocketCountChange = useCallback((count: number) => {
    setRocketCount(count);
    if (count === 0) {
      setIsRocketView(false);
      setActiveRocketIndex(null);
    }
  }, []);

  useEffect(() => {
    if (launchQueue.length > 0 && activeRocketIndex === null) {
      setActiveRocketIndex(0); // Set the first rocket as active only if it's null
    }
  }, [launchQueue, activeRocketIndex]); // Add activeRocketIndex to dependencies

  const lookAtNode = useCallback((node: IRepData) => {
    if (cameraRef.current) {
      // Adjust the camera's position slightly so it's not inside the node
      /*
      const offset = EarthRadiusInKm + 50; // Distance from the node
      const targetPosition = new THREE.Vector3(node.latitude, node.longitude, 0);
      const cameraPosition = new THREE.Vector3(targetPosition.x, targetPosition.y, offset);
      const currentCameraPosition = cameraRef.current.position.clone();
      const direction = targetPosition.clone().sub(currentCameraPosition).normalize();
      const lerpSpeed = 0.1; // Adjust this value to control how fast the camera moves
      cameraRef.current.position.lerp(cameraPosition, lerpSpeed);
      const lookAtRotation = new THREE.Quaternion().setFromUnitVectors(
        cameraRef.current.getWorldDirection(new THREE.Vector3()).normalize(), // Current camera direction
        direction // Desired direction (towards the node)
      );
      cameraRef.current.quaternion.slerp(lookAtRotation, lerpSpeed);
      cameraRef.current.lookAt(targetPosition);
      cameraRef.current.lookAt(0, 0, 0); // Make the camera look at the node
      */
    }
  }, []);

  useEffect(() => {
    if (hoveredNode) {
      lookAtNode(hoveredNode);
    }
  }, [hoveredNode, lookAtNode]);

  // New function to reset to Earth view
  const resetToEarthView = () => {
    setIsRocketView(false);

    setTimeout(() => {
      if (cameraRef.current) {
        cameraRef.current.position.set(0, 0, 5);
        cameraRef.current.lookAt(new THREE.Vector3(0, 0, 0)); // Look at the center of the Earth
      }
    }, 100);
  };

  // Memoize camera settings
  const cameraSettings = useMemo(
    () => ({
      fov: 45,
      position: [0, 2, 4] as [number, number, number]
    }),
    []
  );

  // Memoize Stars props
  const starsProps = useMemo(
    () => ({
      radius: 300,
      depth: 60,
      count: 20000,
      factor: 7,
      saturation: 0,
      fade: true
    }),
    []
  );

  // Memoize light settings
  const lightSettings = useMemo(
    () => ({
      directional: {
        color: 0xffffff,
        intensity: 2
      },
      ambient: {
        intensity: 0.1
      }
    }),
    []
  );

  // Memoize OrbitControls props
  const orbitControlsProps = useMemo(
    () => ({
      enableRotate: !isRocketView && !isStarlinkView,
      rotateSpeed: 0.5,
      enableZoom: !isRocketView && !isStarlinkView,
      zoomSpeed: 0.6,
      enablePan: false
    }),
    [isRocketView, isStarlinkView]
  );

  if (!serverDateTime) {
    return null;
  }

  return (
    <div className="relative w-screen h-screen">
      <div className="absolute top-1 md:top-4 left-4 md:left-10 z-10 flex-col select-none">
        <span className="text-[30px] md:text-[40px] font-thin font-sans text-[#209ce9]">
          ӾNO {/*This is where the title is*/}
        </span> 
        <span className="text-[30px] md:text-[40px] text-gray-200">Hub</span>
      </div>

      <div className="absolute top-4 right-4 z-10 flex flex-col gap-2"> {/*Get ride of */}
        <div className="flex flex-row gap-2">
          {/* New button to reset to Earth view */}
          {distanceFromEarth > 10 && (
            <Button
              onClick={resetToEarthView}
              variant="outline"
              size="sm"
              className="flex select-none items-center gap-2 bg-transparent hover:bg-transparent hover:text-[#209ce9]"
            >
              Back to Earth
            </Button>
          )}
          
          {isStarlinkView && (
            <Button
              onClick={moveToNextStarlink}
              variant="outline"
              size="sm"
              className="flex select-none items-center gap-2 bg-transparent hover:bg-transparent hover:text-[#209ce9]"
            >
              <Eye className="w-4 h-4" />
              <span className="hidden md:inline">Next StarLink</span>
            </Button>
          )}
          {isRocketView && (
            <Button
              onClick={moveToNextRocket}
              variant="outline"
              size="sm"
              className="flex select-none items-center gap-2 bg-transparent hover:bg-transparent hover:text-[#209ce9]"
            >
              <Eye className="w-4 h-4" />
              <span className="hidden md:inline">Next Rocket</span>
            </Button>
          )}
        </div>
        <div className="flex items-center gap-2 text-white">
          Active <Rocket className="w-4 h-4 text-red-600" /> {rocketCount}
        </div>
        <ConfirmationHistoryTable />
      </div> {/*Get ride of */}

      <Canvas
        camera={cameraSettings}
        className="w-full h-full cursor-move pointer-events-auto"
        performance={{ min: 0.5 }} // Add performance optimization
        dpr={[1, 2]} // Limit pixel ratio for better performance
        gl={{
          antialias: true,
          powerPreference: 'high-performance',
          alpha: false // Disable alpha for better performance
        }}
      >
        {APP_CONFIG.debug.frameRateDisplay && <Stats />}
        <PerspectiveCamera makeDefault ref={cameraRef} {...cameraSettings} />
        <OrbitControls {...orbitControlsProps} />

        {/* Use memo'd Stars props */}
        <Stars {...starsProps} />

        {/* Use memo'd light settings */}
        <directionalLight
          ref={lightRef}
          color={lightSettings.directional.color}
          intensity={lightSettings.directional.intensity}
        />
        <ambientLight intensity={lightSettings.ambient.intensity} />

        {/* Conditionally render components based on view state */}
        <ThreeMesh
          lightRefs={[lightRef]}
          repsGeoInfo={repsGeoInfo}
          manualTime={simulationTime}
          onNodeHover={setHoveredNode}
        />
        <CloudMesh />
        
        {/* Always render StarlinkMesh 
        <StarlinkMesh
          count={6}
          isStarlinkView={isStarlinkView}
          activeStarlinkIndex={activeStarlinkIndex}
          cameraRef={cameraRef}
        />*/}

        {/*<DonationAnimation />*/}

        {/*<RocketAnimationManager
          ref={rocketManagerRef}
          cameraRef={cameraRef}
          onRocketComplete={handleRocketComplete}
          onRocketCountChange={handleRocketCountChange}
          isRocketView={isRocketView}
          activeRocketIndex={activeRocketIndex}
          setActiveRocketIndex={setActiveRocketIndex}
          setDistanceFromEarth={setDistanceFromEarth}
        />*/}
      </Canvas>
      {/* Node Info */}
      <div className="absolute bottom-1/2 left-4 z-10">
        {cameraRef.current && (
          <div className="bg-transparent text-white p-4 rounded-lg shadow-lg max-w-sm">
            <h3 className="text-lg font-bold mb-2"> Node Position Cart:</h3>
            <p>X: {NodePos.x}</p>
            <p>Y: {NodePos.y}</p>
            <p>Z: {NodePos.z}</p>
            {/*<p>{hoveredNode.latitude}</p>*/}
          </div>
        )}
      </div>

      {/* Node Info */}
      <div className="absolute bottom-1/3 left-4 z-10">
        {cameraRef.current && (
          <div className="bg-transparent text-white p-4 rounded-lg shadow-lg max-w-sm">
            <h3 className="text-lg font-bold mb-2"> Node Position Polar:</h3>
            <p>Radians: {NodePosPolar.x}</p>
            <p>Theta: {NodePosPolar.y}</p>
            <p>Psi: {NodePosPolar.z}</p>
            {/*<p>{hoveredNode.latitude}</p>*/}
          </div>
        )}
      </div>

      {/* Node Info */}
      <div className="absolute bottom-40 left-4 z-10">
        {cameraRef.current && (
          <div className="bg-transparent text-white p-4 rounded-lg shadow-lg max-w-sm">
            <h3 className="text-lg font-bold mb-2"> Camera Position Polar:</h3>
            <p>Radians: {hoverNodePol.x}</p>
            <p>Theta: {hoverNodePol.y}</p>
            <p>Psi: {hoverNodePol.z}</p>
            {/*<p>{hoveredNode.latitude}</p>*/}
          </div>
        )}
      </div>

      {/* Node Info */}
      <div className="absolute bottom-4 left-4 z-10">
        {cameraRef.current && (
          <div className="bg-transparent text-white p-4 rounded-lg shadow-lg max-w-sm">
            <h3 className="text-lg font-bold mb-2"> Camera Position Cart:</h3>
            <p>X: {cameraRef.current.position.x}</p>
            <p>Y: {cameraRef.current.position.y}</p>
            <p>Z: {cameraRef.current.position.z}</p>
            {/*<p>{hoveredNode.latitude}</p>*/}
          </div>
        )}
      </div>
      
      
    </div>
  );
};

export default ThreeSceneClient;
