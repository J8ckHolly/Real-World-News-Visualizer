export interface eventData {
    uid: number;
    city: string;
    country: string;
    latitude: number,
    longitude: number,
    time: string,
    title: string,
    mainDesc: string;
    relatedCountries: string[];
    relatedDescriptions: string[];
}

export interface countryEvent {
  country: string;
  title: string;
  time: number
}

export interface ExperimentalEventData {
  uid: number;
  country: string;
  latitude: number;
  longitude: number;
  description: string;
  city: string;
  extendedDescription: ExtendedEvent[] | null;
}

export interface ExtendedEvent {
  country: string;
  description: string;
}

export interface CountryNameCords {
  countryName: string;
  capitol: string;
  latitude: number;
  longitude: number;
}

export interface tableEventData {
  country: string;
  latitude: number;
  longitude: number;
  description: string;
  city: string;
}

