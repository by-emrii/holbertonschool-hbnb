// Place Details displayed dynamically

// ============== 1. Get Place ID from URL ==============
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("place_id");
}

// ============== 2. Get Cookie Function ==============
function getCookie(name) {
  // Function to get a cookie value by its name
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

// ============== 3. Check User Authentication ==============
function checkAuthentication() {
  // Function to check for the JWT token in cookies and store it in a variable.
  const token = getCookie("token");
  const addReviewSection = document.getElementById("add-review-btn-section");

  if (!token) {
    // User is not authenticated, hide the add review button
    if (addReviewSection) {
      addReviewSection.style.display = "none";
    }
  } else {
    // User is authenticated, show the add review button
    if (addReviewSection) {
      addReviewSection.style.display = "block";
    }
  }

  return token;
}

// ============== 4. Fetch Place Details ==============
async function fetchPlaceDetails(token, placeId) {
  try {
    const headers = {
      "Content-Type": "application/json",
    };

    // Add authorization header if token is available
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(
      `http://127.0.0.1:5000/api/v1/places/${placeId}`,
      {
        method: "GET",
        headers: headers,
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch place details: ${response.statusText}`);
    }

    const data = await response.json();
    return data.result; // API returns {result: {...}, message: ...}
  } catch (error) {
    console.error("Error fetching place details:", error);
    alert("Failed to load place details. Please try again later.");
    return null;
  }
}

// ============== 5. Fetch Reviews for Place ==============
async function fetchPlaceReviews(placeId) {
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/v1/reviews/place/${placeId}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      // If no reviews found, return empty array
      if (response.status === 404) {
        return [];
      }
      throw new Error(`Failed to fetch reviews: ${response.statusText}`);
    }

    const reviews = await response.json();
    return reviews; // API returns array of reviews
  } catch (error) {
    console.error("Error fetching reviews:", error);
    return [];
  }
}

// ============== 6. Display Place Details ==============
function displayPlaceDetails(place) {
  // Update place title
  const titleElement = document.getElementById("place-title");
  if (titleElement) {
    titleElement.textContent = place.title || "Untitled Place";
  }

  // Update host name
  const hostElement = document.getElementById("place-host");
  if (hostElement && place.owner) {
    hostElement.textContent = `${place.owner.first_name} ${place.owner.last_name}`;
  }

  // Update price
  const priceElement = document.getElementById("place-price");
  if (priceElement) {
    priceElement.textContent = place.price ? place.price.toFixed(2) : "0.00";
  }

  // Update description
  const descriptionElement = document.getElementById("place-description");
  if (descriptionElement) {
    descriptionElement.textContent =
      place.description || "No description available.";
  }

  // Update amenities
  const amenitiesElement = document.getElementById("place-amenities");
  if (amenitiesElement) {
    if (place.amenities && place.amenities.length > 0) {
      const amenityNames = place.amenities
        .map((amenity) => amenity.name)
        .join(", ");
      amenitiesElement.textContent = amenityNames;
    } else {
      amenitiesElement.textContent = "No amenities listed.";
    }
  }
}

// ============== 7. Display Reviews ==============
function displayReviews(reviews) {
  const reviewsSection = document.getElementById("reviews");
  if (!reviewsSection) return;

  // Clear existing reviews (except the title)
  const title = reviewsSection.querySelector("h2");
  reviewsSection.innerHTML = "";
  if (title) {
    reviewsSection.appendChild(title);
  } else {
    const newTitle = document.createElement("h2");
    newTitle.textContent = "Reviews";
    reviewsSection.appendChild(newTitle);
  }

  // If no reviews, display a message
  if (!reviews || reviews.length === 0) {
    const noReviewsMsg = document.createElement("p");
    noReviewsMsg.textContent = "No reviews yet. Be the first to review!";
    noReviewsMsg.style.color = "#666";
    noReviewsMsg.style.fontStyle = "italic";
    reviewsSection.appendChild(noReviewsMsg);
    return;
  }

  // Create review cards for each review
  reviews.forEach((review) => {
    const reviewCard = document.createElement("article");
    reviewCard.className = "review-card";

    // Create reviewer name
    const reviewerName = document.createElement("p");
    reviewerName.innerHTML = `<strong>${
      review.user
        ? review.user.first_name + " " + review.user.last_name
        : "Anonymous"
    }:</strong>`;
    reviewCard.appendChild(reviewerName);

    // Create review text
    const reviewText = document.createElement("p");
    reviewText.textContent = review.text || "";
    reviewCard.appendChild(reviewText);

    // Create rating with stars
    const rating = document.createElement("p");
    const stars =
      "★".repeat(review.rating || 0) + "☆".repeat(5 - (review.rating || 0));
    rating.textContent = `Rating: ${stars}`;
    reviewCard.appendChild(rating);

    reviewsSection.appendChild(reviewCard);
  });
}

// ============== 8. Initialize Page ==============
async function initializePage() {
  // Get place ID from URL
  const placeId = getPlaceIdFromURL();

  if (!placeId) {
    alert("No place ID provided in URL.");
    // Optionally redirect to home page
    // window.location.href = '/';
    return;
  }

  // Check authentication
  const token = checkAuthentication();

  // Fetch and display place details
  const place = await fetchPlaceDetails(placeId, token);
  if (place) {
    displayPlaceDetails(place);
  }

  // Fetch and display reviews
  const reviews = await fetchPlaceReviews(placeId);
  displayReviews(reviews);

  // Update the add review button link to include place_id
  const addReviewBtn = document.getElementById("go-to-add-review");
  if (addReviewBtn) {
    addReviewBtn.onclick = function () {
      location.href = `add_review.html?place_id=${placeId}`;
    };
  }
}

// ============== 9. Run on Page Load ==============
document.addEventListener("DOMContentLoaded", initializePage);
