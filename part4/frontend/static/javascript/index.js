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
        const response = await fetch('https://api.example.com/data', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}` // Add token to GET request
            }
        });
        if (!response.ok) {
            throw new Error(`Failed to load places from API`);
        } else {
            const placesData = await response.json(); // parse JSOn response body to JS object
        }
        displayPlaces(placesData); 
    }
    catch (error) {
        console.error('Error:', error);
    }
}

// Populate places list
function displayPlaces(places) {
    // Clear the current content of the places list
    // Iterate over the places data
    // For each place, create a div element and set its content
    // Append the created element to the places list
}

// Implement Client side filtering
document.getElementById('price-filter').addEventListener('change', (event) => {
    // Get the selected price value
    // Iterate over the places and show/hide them based on the selected price
});