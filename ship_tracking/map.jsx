import mapboxgl from 'mapbox-gl';

// Initialize map
useEffect(() => {
  const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/navigation-day-v1',
    center: [initialLng, initialLat],
    zoom: 9
  });
  
}, []);