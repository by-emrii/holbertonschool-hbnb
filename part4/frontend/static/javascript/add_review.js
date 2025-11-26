/*-------- Check User Authentication --------*/
function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = '../index/index.html';
    }
    return token;
}

/*-------- Get Cookie --------*/
function getCookie(name) {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith(name + "="))
        ?.split("=")[1] || null;
}

/*-------- Login/logout --------*/
function checkAuthUI() {
    const token = getCookie("token");
    const loginLink = document.querySelector(".login-button");
    const logoutLink = document.querySelector(".logout-button");

    if (!loginLink || !logoutLink) return;

    if (token) {
        loginLink.style.display = "none";
        logoutLink.style.display = "block";
    } else {
        loginLink.style.display = "block";
        logoutLink.style.display = "none";
    }
}

/*-------- Get place ID from URL --------*/
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("place_id");
}

/*-------- Setup event listener for review form --------*/
document.addEventListener("DOMContentLoaded", async () => {
    const token = checkAuthentication();
    checkAuthUI();
    const placeId = getPlaceIdFromURL();

    // Fetch and display the place title (no alert if fails)
    const placeTitle = await fetchPlaceName(placeId, token);
    displayPlaceTitle(placeTitle);

    /* Star rating setup */
    const ratingInputs = document.querySelectorAll('input[name="rating"]');
    const numericalRating = document.getElementById("numerical-rating");

    ratingInputs.forEach(input => {
        input.addEventListener("change", () => {
            numericalRating.textContent = Number(input.value);
        });
    });

    /* Review form submit */
    const reviewForm = document.getElementById("review-form");
    reviewForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const reviewText = document.getElementById("review").value.trim();
        const rating = Number(document.querySelector('input[name="rating"]:checked')?.value);

        if (!reviewText) {
            alert("Please write a review.");
            return;
        }

        if (!rating) {
            alert("Please select a rating.");
            return;
        }

        const response = await submitReview(token, placeId, reviewText, rating);
        await handleResponse(response, placeId);
    });
});

/*-------- Fetch Place Name Only (No alerts on failure) --------*/
async function fetchPlaceName(placeId, token) {
    try {
        const headers = { "Content-Type": "application/json" };
        if (token) headers["Authorization"] = `Bearer ${token}`;

        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: "GET",
            headers
        });

        if (!response.ok) return "Untitled Place";

        const data = await response.json();
        return data.result?.title || "Untitled Place"; 
    } catch {
        return "Untitled Place"; 
    }
}

// Place title
function displayPlaceTitle(title) {
    const titleElement = document.getElementById("place-title");
    if (titleElement) {
        titleElement.textContent = title;
    }
}

/*-------- Make AJAX request to submit review --------*/
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/v1/reviews", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: rating
            })
        });
        return response;
    } catch (err) {
        console.error("Network error:", err);
        alert("Network error — try again.");
    }
}

/*-------- Handle API response --------*/
async function handleResponse(response, placeId) {
    if (!response) return;

    if (response.ok) {
        alert("Review submitted successfully!");
        window.location.href = `../place_details?place_id=${placeId}`;
    } else {
        try {
            // Handle backend error messages
            const data = await response.json(); 
            if (data.error) {
                alert(data.error);  // shows backend messages like "You cannot review your own place" or "You have already reviewed this place"
            } else {
                alert("Failed to submit review."); 
            }
        } catch {
            alert("Failed to submit review."); 
        }
    }
}
