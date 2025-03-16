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
import { Vector3 } from 'three';
import { Button } from '@/components/ui/button';
import { Rocket, Eye, Globe } from 'lucide-react'; // Understand
import { APP_CONFIG } from '@/constants/config'; //Understand - Keep
import { latLongToVector3 } from './network-arc';

const SLERPZOOM = (start: THREE.Vector3, end: THREE.Vector3, t: number): THREE.Vector3 => {
  const startNormal = start.clone().normalize();
  const endNormal = end.clone().normalize(); 

  const start_magnitude = start.length();
  const end_magnitude = end.length();
  
  const dot = startNormal.dot(endNormal);
  const omega = Math.acos(Math.min(Math.max(dot, -1), 1));
  const sinOmega = Math.sin(omega);

  const liftFactor = Math.sin(t * Math.PI/2) * (end_magnitude - start_magnitude) + start_magnitude; 
  if (sinOmega === 0) {
    return start.clone();
  } else {
    const weight0 = Math.sin((1 - t) * omega) / sinOmega;
    const weight1 = Math.sin(t * omega) / sinOmega;
    const point = new THREE.Vector3()
      .addScaledVector(startNormal, weight0)
      .addScaledVector(endNormal, weight1)
      .normalize()
      .multiplyScalar(liftFactor); //Might be Implemented differently

    return point;
  }
};

function rotatePointAboutX(point: THREE.Vector3): THREE.Vector3 {
  const angleDegrees = 23.5
  
  // Convert degrees to radians
  const angleRadians = THREE.MathUtils.degToRad(angleDegrees);
  
  // Create a rotation matrix around the X axis
  const rotationMatrix = new THREE.Matrix4();
  rotationMatrix.makeRotationX(angleRadians);
  
  // Apply the rotation to the point
  const rotatedPoint = point.clone().applyMatrix4(rotationMatrix);
  
  return rotatedPoint;
}

interface ThreeSceneClientProps {
  repsGeoInfo: IRepData[];
  serverDateTime: Date | null;
}

type ButtonState = "Spin" | "Stop" | "Return";

const ThreeSceneClient: React.FC<ThreeSceneClientProps> = ({
  repsGeoInfo,
  serverDateTime
}) => {
  const lightRef = useRef<THREE.DirectionalLight>(null);
  const [simulationTime, setSimulationTime] = useState<Date>(
    serverDateTime || new Date()
  );
  const [hoveredNode, setHoveredNode] = useState<IRepData | null>(null);
  const [clickedNode, setClickedNode] = useState<IRepData | null>(null);
  const { confirmationHistory: confirmations } = useConfirmations();
  const [trackPoint, setTrackPoint] = useState<THREE.Vector3>(new THREE.Vector3());
  const [cameraState, setCameraState] = useState<ButtonState>("Stop");
  const [zoomedIn, setZoomedIn] = useState(false)
  const [enableRotate, setEnableRotate] = useState(true);
  const cameraRef = useRef<THREE.PerspectiveCamera>(null);
  const animationFrameId = useRef<number>(-1); // Store the animation frame ID in a ref
  const [theta, setTheta] = useState(0);
  const [phi, setPhi] = useState(0);
  
  

  useEffect(() => {
    if (serverDateTime) {
      setSimulationTime(serverDateTime);
    }
  }, [serverDateTime]);

  const cameraStateFSM = () => {
    console.log("Clicked");
    setCameraState((prevCameraState) => {
      if (prevCameraState === "Spin") {
        setEnableRotate((prev) => !prev);
        return "Stop";
      } else if (prevCameraState === "Stop" && !zoomedIn) {
        setEnableRotate((prev) => !prev);
        return "Spin";
      } 
       else if (prevCameraState === "Return") {
        console.log("Here");
        return "Stop";
      }
      return prevCameraState;
    });
  };

  useEffect(() => {
    cameraStateFSM();
  }, [zoomedIn]);
  
  // FSM for the camera
  useEffect(() => {
    //Spinning Actions
    if (cameraState==="Spin") {
      console.log("Rotating");
      rotatingCamera();
    }
    //Zooming from track to zoom plane
    else if(cameraState === "Stop" && clickedNode){
      if (!clickedNode || !cameraRef.current) return;
      console.log("Zoomed In");
      setTrackPoint(cameraRef.current.position.clone())

      let start = cameraRef.current.position.clone()
      let eventExtendedPoint = latLongToVector3(clickedNode.latitude, clickedNode.longitude, 2); 
      eventExtendedPoint = rotatePointAboutX(eventExtendedPoint);
      setZoomedIn((prevZoomDone) => !prevZoomDone);
      zoomFunc(start,eventExtendedPoint)
    }
    // On Zoom plane switching from one node to another
    else if(cameraState === "Return" && clickedNode){
      if (!clickedNode || !cameraRef.current) return;
      console.log("Point Switching");

      let start = cameraRef.current.position.clone()
      let eventExtendedPoint = latLongToVector3(clickedNode.latitude, clickedNode.longitude, 2); 
      eventExtendedPoint = rotatePointAboutX(eventExtendedPoint);
      zoomFunc(start,eventExtendedPoint)
    }

    else if(cameraState === "Return" && zoomedIn){
      if(!cameraRef.current) return;
      let start = cameraRef.current.position.clone()
      zoomFunc(start,trackPoint)
    }
    
    else {
      console.log("Not Moving");
      // Cleanup the animation if rotation is disabled
      cancelAnimationFrame(animationFrameId.current);
    }

    // Cleanup on component unmount or when effect is cleaned up
    return () => cancelAnimationFrame(animationFrameId.current);
  }, [clickedNode, cameraState]);


  const rotatingCamera = () => {
    const radius = 3;
    const speed = 0.005;

    const animateCamera = () => {
      if (cameraRef.current) {
        setTheta((prevTheta) => {
          const newTheta = prevTheta + speed;
          cameraRef.current!.position.x = radius * Math.cos(newTheta);
          cameraRef.current!.position.z = radius * Math.sin(newTheta);
          cameraRef.current!.lookAt(0, 0, 0);
          return newTheta;  // Return the new Theta to update the state
        });
        animationFrameId.current = requestAnimationFrame(animateCamera);
      }
    };

    // Cancel any previous animation frame before starting a new one
    cancelAnimationFrame(animationFrameId.current);

    // Start the new animation loop
    animationFrameId.current = requestAnimationFrame(animateCamera);
  };
  
  const zoomFunc = (start: THREE.Vector3, end: THREE.Vector3) => {
    console.log("hi")
    console.log(cameraState)
    console.log(start)
    console.log(end)
    const numPoints = 100;
    let t = 0; // Local interpolation state instead of using React state
    const animate = () => {
      if (t > 1) {
        console.log('Done')
        setClickedNode(null);
        return;
      }
  
      const interpolatedPoint = SLERPZOOM(start, end, t);  //Change start and end
      cameraRef.current!.position.copy(interpolatedPoint);
  
      t += 1 / numPoints;
      animationFrameId.current = requestAnimationFrame(animate);
    };
  
    cancelAnimationFrame(animationFrameId.current); // Ensure previous animation is stopped
    animationFrameId.current = requestAnimationFrame(animate);
  };

  
  // Memoize camera settings
  const cameraSettings = useMemo(
    () => ({
      fov: 45,
      position: [3, 2, 0] as [number, number, number]
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
      enableRotate: !enableRotate,
      rotateSpeed: 0.5,
      enableZoom: true,
      zoomSpeed: 0.6,
      enablePan: false
    }),
    []
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
        <ConfirmationHistoryTable 
        cameraStateFSM={cameraStateFSM}
        cameraState={cameraState}/>
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
          onNodeClick={setClickedNode}
        /> {/* for repsGeoInfo put null to cut the connections */}
        <CloudMesh />
        
      </Canvas>
      <div className="absolute bottom-2 left-4 z-10">
        {hoveredNode && (
          <div className="bg-transparent text-white p-4 rounded-lg shadow-lg max-w-sm">
            <h3 className="text-lg font-bold mb-2">
            </h3>
            <p>Latitude: {hoveredNode.latitude}</p>
            <p>Longitude: {hoveredNode.longitude}</p>
          </div>
        )}
      </div>
      {/* Node Info */}
      <div className="absolute bottom-20 left-4 z-10">
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
