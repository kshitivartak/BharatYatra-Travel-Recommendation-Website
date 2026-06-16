import React, { useState, useEffect, createContext } from 'react';
import { getPlacesByBounds, getPlacesByLatLng } from "../api";
import axios from "axios";

export const MainContext = createContext();

export const MainContextProvider = ({ children }) => {
    const [places, setPlaces] = useState([]);
    const [filteredPlaces, setFilteredPlaces] = useState([]);
    const [coordinates, setCoordinates] = useState({});
    const [bounds, setBounds] = useState(null);

    const [rating, setRating] = useState(0);
    const [type, setType] = useState('restaurants');
    const [isLoading, setIsLoading] = useState(false);
    
    const [restaurants, setRestaurants] = useState([]);
    const [hotels, setHotels] = useState([]);
    const [attractions, setAttractions] = useState([]);

    // 1. Get Current User Location on Mount
    useEffect(() => {
        navigator.geolocation.getCurrentPosition(
            ({ coords: { latitude, longitude } }) => {
                setCoordinates({ lat: latitude, lng: longitude });
            },
            (error) => console.error("Error getting location:", error)
        );
    }, []);

    // 2. Fetch Places for Map View (Runs when map moves or type changes)
    useEffect(() => {
        const source = axios.CancelToken.source();

        if (bounds?.sw && bounds?.ne) {
            setIsLoading(true);
            
            const fetchMapData = async () => {
                try {
                    const data = await getPlacesByBounds(type, bounds.sw, bounds.ne, source);
                    setPlaces(data?.filter((place) => place.name));
                    setRating(0); // Reset rating filter when map changes
                    setIsLoading(false);
                } catch (error) {
                    if (axios.isCancel(error)) return;
                    console.error("Map Fetch Error:", error);
                    setIsLoading(false);
                }
            };

            fetchMapData();
        }

        return () => source.cancel("Operation canceled by the user.");
    }, [type, bounds]);

    // 3. Fetch Data for Homepage (Runs once coordinates are found)
    useEffect(() => {
        const source = axios.CancelToken.source();

        if (coordinates.lat && coordinates.lng) {
            setIsLoading(true);

            const fetchHomepageData = async () => {
                try {
                    // Fetch all categories simultaneously
                    const [resData, attrData, hotelData] = await Promise.all([
                        getPlacesByLatLng('restaurants', coordinates.lat, coordinates.lng, { limit: 15, min_rating: 4 }, source),
                        getPlacesByLatLng('attractions', coordinates.lat, coordinates.lng, { limit: 15, min_rating: 4 }, source),
                        getPlacesByLatLng('hotels', coordinates.lat, coordinates.lng, { limit: 15, min_rating: 4 }, source)
                    ]);

                    setRestaurants(resData?.filter(p => p.name && p.location_id !== "0"));
                    setAttractions(attrData?.filter(p => p.name && p.location_id !== "0" && p.rating > 0));
                    setHotels(hotelData?.filter(p => p.name && p.location_id !== "0" && p.rating > 0));
                    
                    setIsLoading(false);
                } catch (error) {
                    if (axios.isCancel(error)) return;
                    console.error("Homepage Fetch Error:", error);
                    setIsLoading(false);
                }
            };

            fetchHomepageData();
        }

        return () => source.cancel();
    }, [coordinates]);

    // 4. Handle Filtering by Rating
    useEffect(() => {
        const filtered = places?.filter((place) => Number(place.rating) >= rating);
        setFilteredPlaces(filtered);
    }, [rating, places]);

    return (
        <MainContext.Provider value={{ 
            places, setPlaces, 
            coordinates, setCoordinates, 
            bounds, setBounds, 
            rating, setRating, 
            type, setType, 
            isLoading, setIsLoading, 
            filteredPlaces, 
            attractions, restaurants, hotels 
        }}>
            {children}
        </MainContext.Provider>
    );
};
