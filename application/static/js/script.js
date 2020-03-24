console.log(`Javascript enabled`);

/*
(function getLocation() {
    const geoLocation = document.querySelector('.location');
    const status = document.querySelector('.status');
    
    const success = (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        status.textContent = '';
        geoLocation.textContent = `lat: ${lat}° lon: ${lon}°`;
    }
    
    const error = () => {
        status.textContent = 'Unable to get location';
    }
    
    if (!navigator.geolocation) {
        status.textContent = 'Geolocation not supported.';
    } else {
        status.textContent = 'Locating...';
        navigator.geolocation.getCurrentPosition(success, error);
    }
})();
*/
