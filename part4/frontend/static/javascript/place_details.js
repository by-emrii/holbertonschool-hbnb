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

// ============== 3. Toggle Login/Logout Buttons ==============
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

  return token;
}

// ============== 4. Check User Authentication ==============
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

// ============== 5. Fetch Place Details ==============
async function fetchPlaceDetails(placeId, token) {
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

// ============== 6. Fetch Reviews for Place ==============
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

// ============== 7. Amenity Icon Mapping ==============
function getAmenityIcon(amenityName) {
  // Base path for amenity icons
  const iconBasePath = "../../static/images/";

  // Map amenity names to icon filenames
  const amenityIconFiles = {
    wifi: "icon_wifi.png",
    pool: "icon_bath.png",
    bath: "icon_bath.png",
    // "air conditioning": "icon_ac.png",
    // parking: "icon_parking.png",
    // kitchen: "icon_kitchen.png",
    // tv: "icon_tv.png"
  };

  const normalizedName = amenityName.toLowerCase().trim();
  const iconFile = amenityIconFiles[normalizedName] || "icon.png"; // default icon

  // return img tag for amenity icon
  return `<img src="${iconBasePath}${iconFile}" alt="${amenityName}" class="amenity-icon" width="50" height="50">`;
}

// ============== 8. Calculate Average Rating ==============
function calculateAverageRating(reviews) {
  if (!reviews || reviews.length === 0) return 0;
  const totalRating = reviews.reduce(
    (sum, review) => sum + (review.rating || 0),
    0
  );
  return (totalRating / reviews.length).toFixed(1);
}

// ============== 9. Generate Star Rating HTML ==============
function generateStarRating(rating) {
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 >= 0.5;
  const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

  let starsHTML = "★".repeat(fullStars);
  if (hasHalfStar) starsHTML += "⯨";
  starsHTML += "☆".repeat(emptyStars);

  return starsHTML;
}

// ============== 10. Display Place Details ==============
function displayPlaceDetails(place, reviews) {
  const placeDetailsSection = document.getElementById("place-details");
  if (!placeDetailsSection) return;

  // Update place title
  const titleElement = document.getElementById("place-title");
  if (titleElement) {
    titleElement.textContent = place.title || "Untitled Place";
  }

  // Create and insert image container (after title, before place-info)
  const existingImage = placeDetailsSection.querySelector(
    ".listing-image-container"
  );
  if (!existingImage && place.image_url) {
    const imageContainer = document.createElement("div");
    imageContainer.className = "listing-image-container";
    imageContainer.innerHTML = `
      <img class="hero-img" src="${place.image_url}" alt="${
      place.title || "Place Image"
    }">
    `;
    // Insert after title
    const placeInfo = placeDetailsSection.querySelector(".place-info");
    if (placeInfo) {
      placeDetailsSection.insertBefore(imageContainer, placeInfo);
    } else {
      placeDetailsSection.appendChild(imageContainer);
    }
  }

  // Create and insert price/rating card (after image, before place-info)
  const existingCard = document.getElementById("listing-info-card");
  if (!existingCard) {
    const averageRating = calculateAverageRating(reviews);
    const stars = generateStarRating(parseFloat(averageRating));

    const priceRatingCard = document.createElement("section");
    priceRatingCard.id = "listing-info-card";
    priceRatingCard.innerHTML = `
      <div class="price-container">
        <p><strong><span class="dollar-sign">$</span>${
          place.price ? place.price.toFixed(2) : "0"
        }</strong></p>
        <p class="per-night-text">Per night</p>
      </div>
      <div class="star-rating">
        <p>${stars}</p>
      </div>
      <div class="rating">
        <p class="average-rating">${averageRating}</p>
        <p class="rating-title"><strong>Rating</strong></p>
      </div>
    `;

    // Insert after image container
    const imageContainer = placeDetailsSection.querySelector(
      ".listing-image-container"
    );
    const placeInfo = placeDetailsSection.querySelector(".place-info");
    if (imageContainer && placeInfo) {
      placeDetailsSection.insertBefore(priceRatingCard, placeInfo);
    } else if (placeInfo) {
      placeDetailsSection.insertBefore(priceRatingCard, placeInfo);
    }
  }

  // Update host name
  const hostElement = document.getElementById("place-host");
  if (hostElement && place.owner) {
    hostElement.textContent = `${place.owner.first_name} ${place.owner.last_name}`;
  }

  // Update price (in the existing text info)
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

  // ✨ Create Amenities section with icons (replace the text)
  const amenitiesElement = document.getElementById("place-amenities");
  if (amenitiesElement && place.amenities) {
    // Check if we already created the grid
    const existingGrid = document.querySelector(".amenities-grid");
    if (!existingGrid) {
      // Create amenities section after place-info
      const amenitiesSection = document.createElement("section");
      amenitiesSection.id = "amenities";
      amenitiesSection.innerHTML = `
        <h2 class="amenities-title">Amenities</h2>
        <div class="amenities-grid"></div>
      `;

      // Insert after place-details section
      const reviewsSection = document.getElementById("reviews");
      if (reviewsSection && reviewsSection.parentNode) {
        reviewsSection.parentNode.insertBefore(
          amenitiesSection,
          reviewsSection
        );
      }

      // Now populate the grid
      const amenitiesGrid = amenitiesSection.querySelector(".amenities-grid");
      if (place.amenities.length > 0) {
        place.amenities.forEach((amenity) => {
          const amenityBox = document.createElement("div");
          amenityBox.className = "amenity-box";
          amenityBox.innerHTML = getAmenityIcon(amenity.name);

          const amenityName = document.createElement("p");
          amenityName.innerHTML = `<span>${amenity.name}</span>`;
          amenityBox.appendChild(amenityName);

          amenitiesGrid.appendChild(amenityBox);
        });
      } else {
        amenitiesGrid.innerHTML =
          '<p style="color: #666; font-style: italic">No amenities listed.</p>';
      }
    }

    // Hide the original text amenities
    amenitiesElement.parentElement.style.display = "none";
  }
}

// ============== 11. Display Reviews ==============
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

// ============== 12. Initialize Page ==============
async function initializePage() {
  // Get place ID from URL
  const placeId = getPlaceIdFromURL();

  if (!placeId) {
    alert("No place ID provided in URL.");
    // Optionally redirect to home page
    // window.location.href = '/';
    return;
  }

  // Toggle header login/logout buttons
  const token = checkAuthUI();

  // Check authentication for add review section
  checkAuthentication();

  // Fetch place details and reviews
  const place = await fetchPlaceDetails(placeId, token);
  const reviews = await fetchPlaceReviews(placeId);

  // Display place details with reviews (for calculating rating)
  if (place) {
    displayPlaceDetails(place, reviews);
  }

  // Display reviews
  displayReviews(reviews);

  // Update the add review button link to include place_id
  const addReviewBtn = document.getElementById("go-to-add-review");
  if (addReviewBtn) {
    addReviewBtn.onclick = function () {
      location.href = `add_review?place_id=${placeId}`;
    };
  }
}

// ============== 13. Run on Page Load ==============
document.addEventListener("DOMContentLoaded", initializePage);
