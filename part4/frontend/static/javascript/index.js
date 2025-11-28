// Display/hide loginLink depending on Auth
window.addEventListener("load", function checkAuthentication() {
  const token = getCookie("token");
  const loginLink = document.getElementsByClassName("login-button")[0];
  const logoutLink = document.getElementsByClassName("logout-button")[0];

  if (!token) {
    // User NOT logged in
    loginLink.style.display = "block";
    logoutLink.style.display = "none";
  } else {
    // User IS logged in
    loginLink.style.display = "none";
    logoutLink.style.display = "block";
  }
  fetchPlaces(token);
});

// Get value of cookie by name
function getCookie(name) {
  const cookies = document.cookie.split("; ");
  for (let cookie of cookies) {
    let [key, value] = cookie.split("=");
    if (key === name) {
      return value;
    }
  }
  return null;
}

// Fetch places data
async function fetchPlaces(token) {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/v1/places/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      throw new Error(`Failed to load places from API`);
    } else {
      const placesData = await response.json();
      const placesResult = placesData.result;
      displayPlaces(placesResult);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

// Fetch average rating
async function fetchRating(place_id) {
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/v1/places/average/${place_id}`,
      {
        method: "GET",
      }
    );
    if (!response.ok) {
      throw new Error("Failed to fetch average rating");
    } else {
      const ratingData = await response.json();
      return ratingData;
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

// Populate places list dynamically
async function displayPlaces(places) {
  const placeCard = document.querySelector("#places-list");
  placeCard.innerHTML = "";
  for (const place of places) {
    const placeDiv = document.createElement("div");
    placeDiv.setAttribute("class", "place-card");
    placeDiv.setAttribute("data-price", place.price);
    const rating = await fetchRating(place.id);
    placeDiv.innerHTML = `<div>
          <h2 class="card-title">${place.title}</h2>
      </div>
      <div class="image-wrapper">
        <img class="img" src="${place.image_url}">
      </div>
      <div class="price-box">
        <div class="price">
          <span class="price-value">$${place.price}</span>
          <span class="price-label">per night</span>
        </div>

        <div class="rating">
          <span class="rating-value"> ${rating.average_rating}</span>
          <span class="rating-label">Rating</span>
        </div>
      </div>
      <button class="details-button">View Details</button>`;

    placeCard.appendChild(placeDiv);

    const detailsButton = placeDiv.querySelector(".details-button");

    detailsButton.addEventListener("click", () => {
      window.location.href = `http://127.0.0.1:5000/place_details?place_id=${place.id}`;
    });
  }
}

// Implement Client side filtering
document.getElementById("price-filter").addEventListener("change", (event) => {
  const myFilters = document.getElementById("price-filter");
  const filteredPrice = myFilters.value;
  const places = document.getElementById("places-list");

  for (const place of places.children) {
    const placePrice = place.getAttribute("data-price");
    if (filteredPrice === "All" || placePrice <= parseFloat(filteredPrice)) {
      place.style.display = "block";
    } else {
      place.style.display = "none";
    }
  }
});
