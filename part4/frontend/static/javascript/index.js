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
    const placeCard = document.getElementByClassName('places-list');
    placeCard.innerHTML = '';
    for (let place in places) {
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
    // Get the selected price value
    // Iterate over the places and show/hide them based on the selected price
});