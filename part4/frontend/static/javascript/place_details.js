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
  // Base path for amenity icons (not used for SVGs, but kept)
  const iconBasePath = "../../static/images/";

  // Map amenity names to icon filenames
  const amenityIconFiles = {
    wifi: `<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-wifi" viewBox="0 0 16 16">
  <path d="M15.384 6.115a.485.485 0 0 0-.047-.736A12.44 12.44 0 0 0 8 3C5.259 3 2.723 3.882.663 5.379a.485.485 0 0 0-.048.736.52.52 0 0 0 .668.05A11.45 11.45 0 0 1 8 4c2.507 0 4.827.802 6.716 2.164.205.148.49.13.668-.049"/>
  <path d="M13.229 8.271a.482.482 0 0 0-.063-.745A9.46 9.46 0 0 0 8 6c-1.905 0-3.68.56-5.166 1.526a.48.48 0 0 0-.063.745.525.525 0 0 0 .652.065A8.46 8.46 0 0 1 8 7a8.46 8.46 0 0 1 4.576 1.336c.206.132.48.108.653-.065m-2.183 2.183c.226-.226.185-.605-.1-.75A6.5 6.5 0 0 0 8 9c-1.06 0-2.062.254-2.946.704-.285.145-.326.524-.1.75l.015.015c.16.16.407.19.611.09A5.5 5.5 0 0 1 8 10c.868 0 1.69.201 2.42.56.203.1.45.07.61-.091zM9.06 12.44c.196-.196.198-.52-.04-.66A2 2 0 0 0 8 11.5a2 2 0 0 0-1.02.28c-.238.14-.236.464-.04.66l.706.706a.5.5 0 0 0 .707 0l.707-.707z"/>
</svg>`,

    pool: `<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-water" viewBox="0 0 16 16">
  <path d="M.036 3.314a.5.5 0 0 1 .65-.278l1.757.703a1.5 1.5 0 0 0 1.114 0l1.014-.406a2.5 2.5 0 0 1 1.857 0l1.015.406a1.5 1.5 0 0 0 1.114 0l1.014-.406a2.5 2.5 0 0 1 1.857 0l1.015.406a1.5 1.5 0 0 0 1.114 0l1.757-.703a.5.5 0 1 1 .372.928l-1.758.703a2.5 2.5 0 0 1-1.857 0l-1.014-.406a1.5 1.5 0 0 0-1.114 0l-1.015.406a2.5 2.5 0 0 1-1.857 0l-1.014-.406a1.5 1.5 0 0 0-1.114 0l-1.015.406a2.5 2.5 0 0 1-1.857 0L.314 3.964a.5.5 0 0 1-.278-.65m0 3a.5.5 0 0 1 .65-.278l1.757.703a1.5 1.5 0 0 0 1.114 0l1.014-.406a2.5 2.5 0 0 1 1.857 0l1.015.406a1.5 1.5 0 0 0 1.114 0l1.014-.406a2.5 2.5 0 0 1 1.857 0l1.015.406a1.5 1.5 0 0 0 1.114 0l1.757-.703a.5.5 0 1 1 .372.928l-1.758.703a2.5 2.5 0 0 1-1.857 0l-1.014-.406a1.5 1.5 0 0 0-1.114 0l-1.015.406a2.5 2.5 0 0 1-1.857 0l-1.014-.406a1.5 1.5 0 0 0-1.114 0l-1.015.406a2.5 2.5 0 0 1-1.857 0L.314 6.964a.5.5 0 0 1-.278-.65m0 3a.5.5 0 0 1 .65-.278l1.757.703a1.5 1.5 0 0 0 1.114 0l1.014-.406a2.5 2.5 0 0 1 1.857 0l1.015.406a1.5 1.5 0 0 0 1.114 0l1.014-.406a2.5 2.5 0 0 1 1.857 0l1.015.406a1.5 1.5 0 0 0 1.114 0l1.757-.703a.5.5 0 1 1 .372.928l-1.758.703a2.5 2.5 0 0 1-1.857 0l-1.014-.406a1.5 1.5 0 0 0-1.114 0l-1.015.406a2.5 2.5 0 0 1-1.857 0l-1.014-.406a1.5 1.5 0 0 0-1.114 0l-1.015.406a2.5 2.5 0 0 1-1.857 0L.314 9.964a.5.5 0 0 1-.278-.65m0 3a.5.5 0 0 1 .65-.278l1.757.703a1.5 1.5 0 0 0 1.114 0l1.014-.406a2.5 2.5 0 0 1 1.857 0l1.015.406a1.5 1.5 0 0 0 1.114 0l1.014-.406a2.5 2.5 0 0 1 1.857 0l1.015.406a1.5 1.5 0 0 0 1.114 0l1.757-.703a.5.5 0 1 1 .372.928l-1.758.703a2.5 2.5 0 0 1-1.857 0l-1.014-.406a1.5 1.5 0 0 0-1.114 0l-1.015.406a2.5 2.5 0 0 1-1.857 0l-1.014-.406a1.5 1.5 0 0 0-1.114 0l-1.015.406a2.5 2.5 0 0 1-1.857 0l-1.757-.703a.5.5 0 0 1-.278-.65"/>
</svg>`,

    bath: `<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-droplet" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M7.21.8C7.69.295 8 0 8 0q.164.544.371 1.038c.812 1.946 2.073 3.35 3.197 4.6C12.878 7.096 14 8.345 14 10a6 6 0 0 1-12 0C2 6.668 5.58 2.517 7.21.8m.413 1.021A31 31 0 0 0 5.794 3.99c-.726.95-1.436 2.008-1.96 3.07C3.304 8.133 3 9.138 3 10a5 5 0 0 0 10 0c0-1.201-.796-2.157-2.181-3.7l-.03-.032C9.75 5.11 8.5 3.72 7.623 1.82z"/>
  <path fill-rule="evenodd" d="M4.553 7.776c.82-1.641 1.717-2.753 2.093-3.13l.708.708c-.29.29-1.128 1.311-1.907 2.87z"/>
</sv"g>`,

    parking: `<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-car-front" viewBox="0 0 16 16">
  <path d="M4 9a1 1 0 1 1-2 0 1 1 0 0 1 2 0m10 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0M6 8a1 1 0 0 0 0 2h4a1 1 0 1 0 0-2zM4.862 4.276 3.906 6.19a.51.51 0 0 0 .497.731c.91-.073 2.35-.17 3.597-.17s2.688.097 3.597.17a.51.51 0 0 0 .497-.731l-.956-1.913A.5.5 0 0 0 10.691 4H5.309a.5.5 0 0 0-.447.276"/>
  <path d="M2.52 3.515A2.5 2.5 0 0 1 4.82 2h6.362c1 0 1.904.596 2.298 1.515l.792 1.848c.075.175.21.319.38.404.5.25.855.715.965 1.262l.335 1.679q.05.242.049.49v.413c0 .814-.39 1.543-1 1.997V13.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-1.338c-1.292.048-2.745.088-4 .088s-2.708-.04-4-.088V13.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-1.892c-.61-.454-1-1.183-1-1.997v-.413a2.5 2.5 0 0 1 .049-.49l.335-1.68c.11-.546.465-1.012.964-1.261a.8.8 0 0 0 .381-.404l.792-1.848ZM4.82 3a1.5 1.5 0 0 0-1.379.91l-.792 1.847a1.8 1.8 0 0 1-.853.904.8.8 0 0 0-.43.564L1.03 8.904a1.5 1.5 0 0 0-.03.294v.413c0 .796.62 1.448 1.408 1.484 1.555.07 3.786.155 5.592.155s4.037-.084 5.592-.155A1.48 1.48 0 0 0 15 9.611v-.413q0-.148-.03-.294l-.335-1.68a.8.8 0 0 0-.43-.563 1.8 1.8 0 0 1-.853-.904l-.792-1.848A1.5 1.5 0 0 0 11.18 3z"/>
</svg>`,

    kitchen: `<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-fork-knife" viewBox="0 0 16 16">
  <path d="M13 .5c0-.276-.226-.506-.498-.465-1.703.257-2.94 2.012-3 8.462a.5.5 0 0 0 .498.5c.56.01 1 .13 1 1.003v5.5a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5zM4.25 0a.25.25 0 0 1 .25.25v5.122a.128.128 0 0 0 .256.006l.233-5.14A.25.25 0 0 1 5.24 0h.522a.25.25 0 0 1 .25.238l.233 5.14a.128.128 0 0 0 .256-.006V.25A.25.25 0 0 1 6.75 0h.29a.5.5 0 0 1 .498.458l.423 5.07a1.69 1.69 0 0 1-1.059 1.711l-.053.022a.92.92 0 0 0-.58.884L6.47 15a.971.971 0 1 1-1.942 0l.202-6.855a.92.92 0 0 0-.58-.884l-.053-.022a1.69 1.69 0 0 1-1.059-1.712L3.462.458A.5.5 0 0 1 3.96 0z"/>
</svg>`,

    tv: `<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-tv" viewBox="0 0 16 16">
  <path d="M2.5 13.5A.5.5 0 0 1 3 13h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5M13.991 3l.024.001a1.5 1.5 0 0 1 .538.143.76.76 0 0 1 .302.254c.067.1.145.277.145.602v5.991l-.001.024a1.5 1.5 0 0 1-.143.538.76.76 0 0 1-.254.302c-.1.067-.277.145-.602.145H2.009l-.024-.001a1.5 1.5 0 0 1-.538-.143.76.76 0 0 1-.302-.254C1.078 10.502 1 10.325 1 10V4.009l.001-.024a1.5 1.5 0 0 1 .143-.538.76.76 0 0 1 .254-.302C1.498 3.078 1.675 3 2 3zM14 2H2C0 2 0 4 0 4v6c0 2 2 2 2 2h12c2 0 2-2 2-2V4c0-2-2-2-2-2"/>
</svg>`,

    "air conditioning": `<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-fan" viewBox="0 0 16 16">
  <path d="M10 3c0 1.313-.304 2.508-.8 3.4a2 2 0 0 0-1.484-.38c-.28-.982-.91-2.04-1.838-2.969a8 8 0 0 0-.491-.454A6 6 0 0 1 8 2c.691 0 1.355.117 1.973.332Q10 2.661 10 3m0 5q0 .11-.012.217c1.018-.019 2.2-.353 3.331-1.006a8 8 0 0 0 .57-.361 6 6 0 0 0-2.53-3.823 9 9 0 0 1-.145.64c-.34 1.269-.944 2.346-1.656 3.079.277.343.442.78.442 1.254m-.137.728a2 2 0 0 1-1.07 1.109c.525.87 1.405 1.725 2.535 2.377q.3.174.605.317a6 6 0 0 0 2.053-4.111q-.311.11-.641.199c-1.264.339-2.493.356-3.482.11ZM8 10c-.45 0-.866-.149-1.2-.4-.494.89-.796 2.082-.796 3.391q0 .346.027.678A6 6 0 0 0 8 14c.94 0 1.83-.216 2.623-.602a8 8 0 0 1-.497-.458c-.925-.926-1.555-1.981-1.836-2.96Q8.149 10 8 10M6 8q0-.12.014-.239c-1.02.017-2.205.351-3.34 1.007a8 8 0 0 0-.568.359 6 6 0 0 0 2.525 3.839 8 8 0 0 1 .148-.653c.34-1.267.94-2.342 1.65-3.075A2 2 0 0 1 6 8m-3.347-.632c1.267-.34 2.498-.355 3.488-.107.196-.494.583-.89 1.07-1.1-.524-.874-1.406-1.733-2.541-2.388a8 8 0 0 0-.594-.312 6 6 0 0 0-2.06 4.106q.309-.11.637-.199M8 9a1 1 0 1 0 0-2 1 1 0 0 0 0 2"/>
  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
</svg>`,

    heating: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-fire" viewBox="0 0 16 16">
  <path d="M8 16c3.314 0 6-2 6-5.5 0-1.5-.5-4-2.5-6 .25 1.5-1.25 2-1.25 2C11 4 9 .5 6 0c.357 2 .5 4-2 6-1.25 1-2 2.729-2 4.5C2 14 4.686 16 8 16m0-1c-1.657 0-3-1-3-2.75 0-.75.25-2 1.25-3C6.125 10 7 10.5 7 10.5c-.375-1.25.5-3.25 2-3.5-.179 1-.25 2 1 3 .625.5 1 1.364 1 2.25C11 14 9.657 15 8 15"/>
</svg>`,
  };

  // return img tag for amenity icon
  const normalizedName = amenityName.toLowerCase().trim();
  const svg =
    amenityIconFiles[normalizedName] ||
    `<svg fill="currentColor" viewBox="0 0 16 16"><rect width="50" height="50"/></svg>`;

  // wrap the SVG in a div with the CSS class
  return `<div class="amenity-icon">${svg}</div>`;
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
  if (hasHalfStar) starsHTML += '<span class="half-star">★</span>';
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
        <p><span class="dollar-sign">$</span>${
          place.price ? place.price.toFixed(2) : "0"
        }</p>
        <p class="per-night-text">Per night</p>
      </div>
      <div class="star-rating">
        <p>${stars}</p>
      </div>
      <div class="rating">
        <p class="average-rating">${averageRating}</p>
        <p class="rating-title">Rating</p>
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
    }</strong>`;
    reviewCard.appendChild(reviewerName);

    // Create review text
    const reviewText = document.createElement("p");
    reviewText.textContent = review.text || "";
    reviewCard.appendChild(reviewText);

    // Create rating with stars
    const rating = document.createElement("p");

    // label text node
    rating.appendChild(document.createTextNode("Rating: "));

    const starsSpan = document.createElement("span");
    starsSpan.className = "stars";
    starsSpan.textContent =
      (review.rating ? "★".repeat(review.rating) : "") +
      "☆".repeat(5 - (review.rating || 0));

    rating.appendChild(starsSpan);
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
