import React, {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect
} from 'react';
import useEventWebsocket from '@/hooks/event-websocket';
import { countryEvent } from '../types';

interface EventProviderContext {
  eventHistory: countryEvent[];
  addEvent: (event: countryEvent) => void;
}

const EventContext = createContext<EventProviderContext | undefined>(undefined);

export const EventProvider: React.FC<{ children: React.ReactNode }> = ({
  children
}) => {
  const [eventHistory, setEventHistory] = useState<countryEvent[]>([]);
  const { subscriptions } = useEventWebsocket();

  const addEvent = useCallback((event: countryEvent) => {
    setEventHistory((prev) => {
      const newEventList = [event, ...prev].slice(0, 100); // Keep only the latest 100 events
      return newEventList;
    });
  }, []);

  useEffect(() => {
    if (subscriptions) {
      const eventSubscription = subscriptions.subscribe({
        next: (event: countryEvent) => {
          addEvent(event); // Add the event to the event history
        },
        error: (err) =>
          console.error('Error in event subscription:', err.message),
        complete: () => console.log('Event subscription completed')
      });

      // Clean up the subscription on component unmount
      return () => {
        eventSubscription.unsubscribe();
      };
    }
  }, [subscriptions, addEvent]);

  return (
    <EventContext.Provider value={{ eventHistory, addEvent }}>
      {children}
    </EventContext.Provider>
  );
};

export const useEvents = () => {
  const context = useContext(EventContext);
  if (context === undefined) {
    throw new Error('useEvents must be used within an EventProvider');
  }
  return context;
};
