// Display/hide loginLink depending on Auth
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        // Fetch places data if the user is authenticated
        fetchPlaces(token);
    }
}

// Get value of cookie by name
function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (let cookie of cookies) {
        let [key, value] = cookie.split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}

// Fetch places data
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) {
            throw new Error(`Failed to load places from API`);
        } else {
            const placesData = await response.json(); // parse JSON response body to JS object
        }
        displayPlaces(placesData); 
    }
    catch (error) {
        console.error('Error:', error);
    }
}

// Populate places list dynamically
function displayPlaces(places) {
    const placeCard = document.querySelector('.places-list');
    placeCard.innerHTML = '';
    for (const place of places) {
        const placeDiv = document.createElement('div');
        placeDiv.setAttribute('class', 'place-card');
        placeDiv.innerHTML = `
            <div>
                <h2 class="card-title">${place.title}</h2>
            </div>
            <div class="price">Price per night:$${place.price}</div>
            <button id="details-button">View Details</button>`;
        placeCard.appendChild(placeDiv);
    }
}

// Implement Client side filtering
document.getElementById('price-filter').addEventListener('change', (event) => {
    const filteredPrice = this.value; // this refers to the drop-down element
    const places = document.getElementById('places-list');
    
    for (const place of places) {
        const placePrice = parseFloat(place.price);
        if (filteredPrice === 'All' || placePrice <= filteredPrice) {
            place.style.display ='block';
        } else {
            place.style.display ='none';
        }
    }
    //     Getting a reference to all the place elements on your page.
    // Iterating through these place elements.
    // For each place, checking if its price falls within the selectedPrice range.
    // Showing or hiding the place elements accordingly (e.g., by changing their style.display property).
});