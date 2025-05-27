import { useState, useRef, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMapMarkerAlt, faClock, faGlobe } from '@fortawesome/free-solid-svg-icons';
import "/node_modules/flag-icons/css/flag-icons.min.css";
import './Table.css'
import countryData from "flag-icons/country.json";
import { formatLatitude, formatLongitude } from '@/lib/parseCoords';

import { ExperimentalEventData, tableEventData, ExtendedEvent } from '@/types/customTypes';
import { exampleExpData } from '@/data/experimentalData';
import { tableExtendedData } from '@/data/countryData';
import GatewayComponent from './Gateway';

interface TableProps {
    activeUid: number | null;
    isFocused: boolean;
}

const getCountryCode = (countryName: string): string => {
    const country = countryData.find((country) => country.name === countryName);
    return country ? country.code : 'us';
}

const Table: React.FC<TableProps> = ({activeUid, isFocused}) => {
    const [storedEvents, setStoredEvents] = useState<tableEventData[]>([]);
    const originalSourceUidRef = useRef<number | null>(null);
    const firstEventRef = useRef<tableEventData | null>(null);

    const convertMainToTableEvent = (event: ExperimentalEventData): tableEventData => {
        const { country, latitude, longitude, description, city } = event;
        return { country, latitude, longitude, description, city};
    }

    const convertExtendedToTableEvent = (event: ExtendedEvent): tableEventData => {
        const { country, description } = event;
        const fetchedData = tableExtendedData.find(data => data.countryName === country)
        if(!fetchedData){
            return { country, latitude: 0, longitude: 0, description, city: "Unknown" }; 
        }
        return { country, 
            latitude: fetchedData.latitude, 
            longitude: fetchedData.longitude, 
            description, 
            city: fetchedData.capitol};
    }

    

    //Load Data on UID change
    useEffect(() => {
        let fetchedData: ExperimentalEventData | null = null;
        let newEvents: tableEventData[] = [];

        if (activeUid !== null) {
            fetchedData = exampleExpData.find(event => event.uid === activeUid) || null;
            if(fetchedData) {
                newEvents.push(convertMainToTableEvent(fetchedData))
                fetchedData?.extendedDescription?.forEach(extEvent =>{ 
                newEvents.push(convertExtendedToTableEvent(extEvent))
            });
        }
        setStoredEvents(prevEvents => newEvents);
        } else {
            console.log("UID is null.");
        }
    }, [activeUid]); 

    
    //console.log(storedEvents)

    useEffect(() => {
        if (storedEvents.length > 0) {
            firstEventRef.current = storedEvents[0];
            console.log(firstEventRef.current)
        }
    }, [storedEvents])

    const firstEvent = storedEvents.length > 0 ? storedEvents[0] : null;


    const renderGatewayEvents = () => {
        const gatewayEvents = storedEvents.slice(1); // Skipping the first event
        return gatewayEvents.map((event, index) => {
            // Ensure the component is returned
            return <GatewayComponent key={index} country={event.country} swap={swap}/>;
        });
    };

    const swap = (country: string) => {
        setStoredEvents((prevEvents) => {
            const index = prevEvents.findIndex(event => event.country === country);
            
            if (index > 0) { // Ensure we are not swapping with the first element or an invalid index
                const newEvents = [...prevEvents]; // Create a shallow copy of the array
                [newEvents[0], newEvents[index]] = [newEvents[index], newEvents[0]]; // Swap elements
                return newEvents;
            }
    
            return prevEvents; // If no valid swap, return the previous state unchanged
        });
    };
    

    if (activeUid === null) {return null};
    return (
        isFocused &&(<div className="table">
        <div className="header">
            <div className="joinedInfo">
                <div className="topInfo">
                    <div className="leftIcon">
                        <FontAwesomeIcon icon={faGlobe} className="circularIcon"></FontAwesomeIcon>
                        <FontAwesomeIcon icon={faMapMarkerAlt} className="pinIcon"></FontAwesomeIcon>
                    </div>
                    <div className="rightDescription">
                        <span className="headerContent">{firstEvent?.city}, {firstEvent?.country}</span>
                        <span className="headerContent">{formatLatitude(firstEvent?.latitude ?? 0)}, {formatLongitude(firstEvent?.longitude ?? 0)}</span>
                    </div>
                </div>
                <div className="bottomInfo">
                    <FontAwesomeIcon icon={faClock} className="circularIcon"></FontAwesomeIcon>
                    <div className="time">
                        <span className="headerContent">3:23pm (EST)</span>
                        <span className="headerContent">March 8, 2025</span>
                        <span className="headerContent">Saturday</span>
                    </div>
                </div>
            </div>
            <span className={`fi fi-${(getCountryCode(firstEvent?.country || '')?.toLowerCase())} mainFlag`}></span>
        </div>
        <div className="title">
            <h3>Local Boy works on WebApp</h3>
        </div>
        <div className="content">{firstEvent?.description}</div>
        <div className="gateway">
            <span className='related'>Related Countries</span>
            <div className="flags">
                {renderGatewayEvents()}
            </div>

        </div>
      </div>)
    );
  }

export default Table;
