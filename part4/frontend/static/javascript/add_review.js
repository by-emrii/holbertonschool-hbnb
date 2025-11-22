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
    return document.cookie
        .split("; ")
        .find(row => row.startsWith(name + "="))
        ?.split("=")[1] || null;

}

//Create a function to extract the place ID from the query parameters.f
function getPlaceIdFromURL() {
    // Extract the place ID from window.location.search
    // Your code here
    const params = new URLSearchParams(window.location.search);
    return params.get("place_id");
}

//Add an event listener for the form submission to handle the review data.
document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    if (!placeId) {
        alert("No place ID found in URL.");
        return;
    }

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Get review text from form
            // Make AJAX request to submit review
            // Handle the response
            const reviewText = document.getElementById("review").value;
            const rating = document.querySelector('input[name="rating"]:checked')?.value;

            if (!rating) {
                alert("Please select a star rating.");
                return;
            }

            const response = await submitReview(token, placeId, reviewText, rating);
            if (response) handleResponse(response);
        });
    }
});

//Use the Fetch API to send a POST request with the review data.
async function submitReview(token, placeId, reviewText, rating) {
    // Make a POST request to submit review data
    // Include the token in the Authorization header
    // Send placeId and reviewText in the request body
    
    try {
        const response = await fetch("http://127.0.0.1:5000/api/reviews", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                review_text: reviewText,
                rating: rating
            }),
        });

        return response;
    } catch (error) {
        console.error("Error submitting review:", error);
        alert("Network error — please try again.");
    }
}

//Display a success message if the submission is successful and clear the form.
//Display an error message if the submission fails.
function handleResponse(response) {
    if (response.ok) {
        alert("Review submitted successfully!");
        document.getElementById("review-form").reset();
    } else {
        alert("Failed to submit review.");
    }
}