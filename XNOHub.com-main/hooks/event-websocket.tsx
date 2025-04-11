import { useState, useEffect, useCallback, useMemo } from 'react';
import { Subject, interval } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { countryEvent } from '../types';
import { exampleCountryData } from '@/data/exampleCountryData';
import { APP_CONFIG } from '@/constants/config';

const useEventWebsocket = () => {
    const wsUrl = useMemo(() => APP_CONFIG.websocket.urls.nano, []);
    const [subscriptions, setSubscriptions] = useState<Subject<countryEvent> | null>(null);
    const isLocalDevelopment = useMemo(() => {
    return !wsUrl || APP_CONFIG.debug.useSampleData;
    }, [wsUrl]);

    const simulateConfirmations = useCallback(() => {
        if (isLocalDevelopment) {
          const confirmationSubscription = new Subject<countryEvent>();
          let index = 0;
    
          const intervalSubscription = interval(
            APP_CONFIG.simulation.interval).subscribe(() => {
            const confirmation = exampleCountryData[index];
            confirmationSubscription.next(confirmation);
            //console.log(confirmation)
            index = (index + 1) % exampleCountryData.length;
          });

          setSubscriptions(confirmationSubscription)
    
          return () => {
            intervalSubscription.unsubscribe();
          };
        }
      }, [isLocalDevelopment]);


    useEffect(() => {
    if (isLocalDevelopment) {
        console.log('Using sample data for local development');
        return simulateConfirmations();
    } }, [wsUrl, isLocalDevelopment, simulateConfirmations]);
  return {subscriptions}
};

export default useEventWebsocket;