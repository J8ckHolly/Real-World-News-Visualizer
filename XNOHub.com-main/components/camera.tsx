'use client';
import React from 'react';
import { PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';

interface CameraProps {
    cameraRef : React.RefObject<THREE.PerspectiveCamera>;
}
{/*
const camera: React.FC<CameraProps> = ({ cameraRef }) => {

};*/}