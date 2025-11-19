//Create a function to check for the JWT token in cookies and redirect unauthenticated users.
function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

function getCookie(name) {
    // Function to get a cookie value by its name
    // Your code here
}

//Create a function to extract the place ID from the query parameters.
function getPlaceIdFromURL() {
    // Extract the place ID from window.location.search
    // Your code here
}

//Add an event listener for the form submission to handle the review data.
document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Get review text from form
            // Make AJAX request to submit review
            // Handle the response
        });
    }
});

//Use the Fetch API to send a POST request with the review data.
async function submitReview(token, placeId, reviewText) {
    // Make a POST request to submit review data
    // Include the token in the Authorization header
    // Send placeId and reviewText in the request body
    // Handle the response
}

//Display a success message if the submission is successful and clear the form.
//Display an error message if the submission fails.
function handleResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');
        // Clear the form
    } else {
        alert('Failed to submit review');
    }
}