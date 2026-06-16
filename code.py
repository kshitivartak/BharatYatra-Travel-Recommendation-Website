import React, { useState, useEffect } from &#39;react&#39;;
import { getPlacesByBounds, getPlacesByLatLng,
getTransportOptionsByLatLng} from &quot;../api&quot;;
import axios from &quot;axios&quot;;
export const MainContext = React.createContext();
export const MainContextProvider = ({ children }) =&gt; {
const [places, setPlaces] = useState();
const [filteredPlaces, setFilteredPlaces] = useState();
const [coordinates, setCoordinates] = useState({});
const [bounds, setBounds] = useState({});

const [rating, setRating] = useState(0);
const [type, setType] = useState(&#39;restaurants&#39;);
const [isLoading, setIsLoading] = useState(false);
const [restaurants, setRestaurants] = useState();
const [hotels, setHotels] = useState();
const [attractions, setAttractions] = useState();
const [transportOptions, setTransportOptions] = useState();
// Get Current User Location
useEffect(() =&gt; {
// Getting the current position corrdinates from browsers naviagtor
sensor
navigator.geolocation.getCurrentPosition(({ coords: {latitude,
longitude} }) =&gt; {
// setting coordinates latitude and longitude to the state
setCoordinates({lat: latitude, lng: longitude})
})
}, [])
// Get Places for Map View
useEffect(() =&gt; {
let source = axios.CancelToken.source();
// Setting loading state to true while data is being fetched
setIsLoading(true);
// If bounds state value of southwest - &#39;sw&#39; and northeast &#39;ne&#39; is
available then the try-catch block is fired
if (bounds.sw &amp;&amp; bounds.ne) {
try {
// Calling on the getPlacesByBounds endpoint passing in the
type (hotels || attractions || restaurant), bounds and &#39;source&#39; for error
handling and effect cleanup
getPlacesByBounds(type, bounds.sw, bounds.ne, source)
.then(data =&gt; {
// Response &#39;data&#39; is ready and set to the places state
setPlaces(data?.filter(place =&gt; place.name))
// Loading state set back to false - to stop loading, after
data is fetched
setIsLoading(false);
})
console.log(&#39;All set! &#39;, bounds.sw, bounds.ne);
} catch (error) {
console.error(error)

}
}
// Effect Cleanup
return () =&gt; {
source.cancel();
}
}, [type, bounds])
// Get Places for Homepage
useEffect(() =&gt; {
let source = axios.CancelToken.source();
// Setting loading state to true while data is being fetched
setIsLoading(true);
// if coordinates state value latitude &#39;lat&#39; and longitude &#39;lng&#39; is found,
the try-catch block is fired
if (coordinates.lat &amp;&amp; coordinates.lng) {
try {
// Calling on getPlacesByLatLng for &#39;restaurants&#39; type, passing
in parameter for &#39;limits&#39; &amp; &#39;min_rating&#39;; and &#39;source&#39; for error handling and
effect cleanup
getPlacesByLatLng(&#39;restaurants&#39;, coordinates.lat,
coordinates.lng, { limit: 20, min_rating: 4 }, source)
.then(data =&gt; {
// Response &#39;data&#39; received and set to restaurants state
filtering out data without &#39;name&#39; property, &#39;location_id&#39; === 0
setRestaurants(data?.filter(restaurant =&gt; restaurant.name
&amp;&amp; restaurant.location_id != 0))
});
// Calling on getPlacesByLatLng for &#39;attractions&#39; type, passing
in parameter for &#39;limits&#39; &amp; &#39;min_rating&#39;; and &#39;source&#39; for error handling and
effect cleanup
getPlacesByLatLng(&#39;attractions&#39;, coordinates.lat,
coordinates.lng, { limit: 20, min_rating: 4 }, source)
.then(data =&gt; {
// Response &#39;data&#39; received and set to attractions state
filtering out data without &#39;name&#39; property, &#39;location_id&#39; === 0
setAttractions(data?.filter(attraction =&gt; attraction.name
&amp;&amp; attraction.location_id != 0 &amp;&amp; attraction.rating &gt; 0))
});

// Calling on getPlacesByLatLng for &#39;restaurants&#39; type, passing
in parameter for &#39;limits&#39; &amp; &#39;min_rating&#39;; and &#39;source&#39; for error handling and
effect cleanup
getPlacesByLatLng(&#39;hotels&#39;, coordinates.lat, coordinates.lng, {
limit: 20, min_rating: 4 }, source)
.then(data =&gt; {
// Response &#39;data&#39; received and set to hotels state filtering
out data without &#39;name&#39; property, &#39;location_id&#39; === 0
setHotels(data?.filter(hotel =&gt; hotel.name &amp;&amp;
hotel.location_id != 0 &amp;&amp; hotel.rating &gt; 0))
});
} catch (error) {
console.error(error)
}
}
// Effect Cleanup
return () =&gt; {
source.cancel()
}
}, [coordinates]);
// Get Filtered Places by Rating
useEffect(() =&gt; {
// Places filter by rating for Map view
// Set new filteredPlaces on change of &#39;rating&#39; state
// filter in only data with &#39;rating&#39; proper greater than or equal to the
selcted rating value
setFilteredPlaces(places?.filter(place =&gt; Number(place.rating) &gt;=
rating))
}, [rating])
return (
// Passing State value through main context to children for access
&lt;MainContext.Provider value={{ places, setPlaces, coordinates,
setCoordinates, bounds, setBounds, rating, setRating, type, setType,
isLoading, setIsLoading, filteredPlaces, attractions, restaurants, hotels
}}&gt;
{ children }
&lt;/MainContext.Provider&gt;
)
}
