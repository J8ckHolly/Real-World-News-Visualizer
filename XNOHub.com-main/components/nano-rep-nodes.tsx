import React, { useMemo, useCallback, useRef } from 'react';
import * as THREE from 'three';
import { IRepData,  CountryNameCords} from '@/types/index';
import NetworkArcs from './network-arc';
import { MultipleArcs } from './arcBetweenNodes';
import ArcBetweenNodes from './arcBetweenNodes';

interface NanoRepNodesProps {
  repsGeoInfo: IRepData[];
  earthRadius: number;
  onNodeHover: (nodeRepsGeoInfo: IRepData | null) => void;
  onNodeClick: (nodeRepsGeoInfo: IRepData | null) => void;
}



const representativeData: IRepData = {
  account: "nano_3rep1234567890abcdefghijklmnopqrstuvwx",
  account_formatted: "nano_3rep...tuvwx",
  alias: "MyRepresentative",
  is_known_account: true,
  last_telemetry_report: new Date().toISOString(), // Current timestamp
  node_id: "rep-node-001",
  node_ip: "192.168.1.100",
  node_maker: "NanoNodeMaker",
  node_uptime: "5 days, 4 hours",
  node_version: "V23.2",
  show_weight: true,
  votingweight: 1_500_000_000_000_000_000_000_000_000_000, // Using underscores for readability
  weight_formatted: "1.5 MNANO",
  weight_percent: 2.5,
  latitude: 6.4238,
  longitude: -66.9036,
  assigned_city: true,
};

const yucatanRepresentativeData: IRepData = {
  account: "nano_3yucatan1234567890abcdefghijklmnopqrstuvwx",
  account_formatted: "nano_3yucatan...tuvwx",
  alias: "YucatanRepresentative",
  is_known_account: true,
  last_telemetry_report: new Date().toISOString(), // Current timestamp
  node_id: "rep-node-002",
  node_ip: "192.168.2.200",
  node_maker: "YucatanNodeMaker",
  node_uptime: "10 days, 12 hours",
  node_version: "V23.3",
  show_weight: true,
  votingweight: 2_000_000_000_000_000_000_000_000_000_000, // Adjusted value
  weight_formatted: "2 MNANO",
  weight_percent: 3.1,
  latitude: 20.4,  // Approximate latitude for Yucatán Peninsula
  longitude: -89.1, // Approximate longitude for Yucatán Peninsula
  assigned_city: true,
};

const rioRepresentativeData: IRepData = {
  account: "nano_3rio1234567890abcdefghijklmnopqrstuvwx",
  account_formatted: "nano_3rio...tuvwx",
  alias: "RioRepresentative",
  is_known_account: true,
  last_telemetry_report: new Date().toISOString(), // Current timestamp
  node_id: "rep-node-003",
  node_ip: "192.168.3.100",
  node_maker: "RioNodeMaker",
  node_uptime: "15 days, 8 hours",
  node_version: "V23.3",
  show_weight: true,
  votingweight: 1_800_000_000_000_000_000_000_000_000_000, // Adjusted value
  weight_formatted: "1.8 MNANO",
  weight_percent: 2.9,
  latitude: -22.9068, // Approximate latitude for Rio de Janeiro
  longitude: -43.1729, // Approximate longitude for Rio de Janeiro
  assigned_city: true,
};

const limaRepresentativeData: IRepData = {
  account: "nano_3lima1234567890abcdefghijklmnopqrstuvwx",
  account_formatted: "nano_3lima...tuvwx",
  alias: "LimaRepresentative",
  is_known_account: true,
  last_telemetry_report: new Date().toISOString(), // Current timestamp
  node_id: "rep-node-004",
  node_ip: "192.168.4.150",
  node_maker: "LimaNodeMaker",
  node_uptime: "20 days, 3 hours",
  node_version: "V23.3",
  show_weight: true,
  votingweight: 1_600_000_000_000_000_000_000_000_000_000, // Adjusted value
  weight_formatted: "1.6 MNANO",
  weight_percent: 2.5,
  latitude: -12.0464, // Approximate latitude for Lima, Peru
  longitude: -77.0428, // Approximate longitude for Lima, Peru
  assigned_city: true,
};

const NodeArray = [yucatanRepresentativeData, limaRepresentativeData, rioRepresentativeData]

const NanoRepNodes: React.FC<NanoRepNodesProps> = React.memo(
  ({ repsGeoInfo, earthRadius, onNodeHover, onNodeClick }) => {
    const earthRadiusRef = useRef(earthRadius);

    const nodes = useMemo(() => {
      return repsGeoInfo.map((rep) => ({
        ...rep,
        position: calculatePosition(
          rep.latitude,
          rep.longitude,
          earthRadiusRef.current
        ),
        color: new THREE.Color(0x1a6dd4)
      }));
    }, [repsGeoInfo]);

    const myNodes = useMemo(() => {
      return NodeArray.map((rep) => ({
        ...rep,
        position: calculatePosition(
          rep.latitude,
          rep.longitude,
          earthRadiusRef.current
        ),
        color: new THREE.Color(0x800080)
      }));
    }, [repsGeoInfo]);

    const handleNodeHover = useCallback(
      (node: IRepData | null) => {
        onNodeHover(node);
      },
      [onNodeHover]
    );

    const handleNodeClick = useCallback(
      (node: IRepData | null) => {
        console.log('Node Clicked');
        onNodeClick(node)
      }, []
    )

    return (
      <group>
        {nodes.map((node, index) => (
          <Node
            key={node.account}
            node={node}
            earthRadius={earthRadiusRef.current}
            onHover={handleNodeHover}
            onClick={handleNodeClick}
          />
        ))}
        <NetworkArcs nodes={nodes} earthRadius={earthRadiusRef.current} />

        <Node
          key={representativeData.account}
          node={{
            ...representativeData,
            position: calculatePosition(representativeData.latitude,representativeData.longitude,earthRadiusRef.current),
            color: new THREE.Color(0xff0000)
          }}
          earthRadius={earthRadiusRef.current}
          onHover={handleNodeHover}
          onClick={handleNodeClick}
        />
        {myNodes.map((node, index) => (
          <Node
            key={node.account}
            node={node}
            earthRadius={earthRadiusRef.current}
            onHover={handleNodeHover}
            onClick={handleNodeClick}
          />
        ))}
        {/*
        <MultipleArcs
        startNode={representativeData}
        endNodes={myNodes}
        earthRadius={earthRadiusRef.current}/>
        */}

      </group>
    );
  }
);

NanoRepNodes.displayName = 'NanoRepNodes';

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

interface NodeProps {
  node: IRepData & { position: THREE.Vector3; color: THREE.Color };
  earthRadius: number;
  onHover: (nodeRepsGeoInfo: IRepData | null) => void;
  onClick: (nodeRepsGeoInfo: IRepData | null) => void;
}

const Node: React.FC<NodeProps> = React.memo(
  ({ node, earthRadius, onHover, onClick }) => {
    const [hovered, setHovered] = React.useState(false);

    const barHeight = useMemo(() => {
      const baseHeight = earthRadius * 0.2;
      const variableHeight = (node.weight_percent / 50) * earthRadius;
      const hoverMultiplier = hovered ? 1.3 : 1;
      return (baseHeight + variableHeight) * hoverMultiplier;
    }, [earthRadius, node.weight_percent, hovered]);

    const barGeometry = useMemo(() => {
      const geometry = new THREE.CylinderGeometry(0.0005, 0.006, barHeight, 32);
      geometry.translate(0, barHeight / 2, 0);
      return geometry;
    }, [barHeight]);

    const barPosition = useMemo(() => {
      return node.position.clone().normalize().multiplyScalar(earthRadius);
    }, [node.position, earthRadius]);

    const barQuaternion = useMemo(() => {
      const up = new THREE.Vector3(0, 1, 0);
      const axis = new THREE.Vector3()
        .crossVectors(up, barPosition)
        .normalize();
      const radians = Math.acos(up.dot(barPosition.clone().normalize()));
      return new THREE.Quaternion().setFromAxisAngle(axis, radians);
    }, [barPosition]);

    const handlePointerOver = useCallback(
      (e: THREE.Event) => {
        e.stopPropagation();
        setHovered(true);
        onHover(node);
      },
      [node, onHover]
    );

    const handlePointerOut = useCallback(
      (e: THREE.Event) => {
        e.stopPropagation();
        setHovered(false);
        onHover(null);
      },
      [onHover]
    );

    const handleClick = useCallback(
      (e: THREE.Event) => {
        e.stopPropagation();
        onClick?.(node);  // Call onClick when the node is clicked
      },
      [onClick]
    );

    return (
      <group
        position={barPosition}
        quaternion={barQuaternion}
        onPointerOver={handlePointerOver}
        onPointerOut={handlePointerOut}
        onClick={handleClick}
      >
        <mesh geometry={barGeometry}>
          <meshBasicMaterial
            color={hovered ? 0xffa500 : node.color}
            opacity={hovered ? 1 : 0.7}
            transparent
          />
        </mesh>
      </group>
    );
  }
);

Node.displayName = 'Node';

export default NanoRepNodes;
