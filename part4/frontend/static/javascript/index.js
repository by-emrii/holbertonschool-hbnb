// import { fetchPlaceReviews } from "./place_details";

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
      const placesData = await response.json(); // parse JSON response body to JS object
      const placesResult = placesData.result;
      displayPlaces(placesResult);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

// // fetch review data for place
// async function fetchPlaceReviews(placeId) {
//   try {
//     const response = await fetch(
//       `http://127.0.0.1:5000/api/v1/reviews/place/${placeId}`,
//       {
//         method: "GET",
//         headers: {
//           "Content-Type": "application/json",
//         },
//       }
//     );

//     if (!response.ok) {
//       // If no reviews found, return empty array
//       if (response.status === 404) {
//         return [];
//       }
//       throw new Error(`Failed to fetch reviews: ${response.statusText}`);
//     }

//     const reviews = await response.json();
//     return reviews; // API returns array of reviews
//   } catch (error) {
//     console.error("Error fetching reviews:", error);
//     return [];
//   }
// }

// Populate places list dynamically
async function displayPlaces(places) {
  const placeCard = document.querySelector("#places-list");
  placeCard.innerHTML = "";
  for (const place of places) {
    console.log(place);
    // const reviewData = await fetchPlaceReviews(place.id);
    // // console.log("Place_id:", place.id);
    // console.log("place review data:", reviewData);
    const placeDiv = document.createElement("div");
    placeDiv.setAttribute("class", "place-card");
    placeDiv.setAttribute("data-price", place.price);
    placeDiv.innerHTML = `<div>
          <h2 class="card-title">${place.title}</h2>
      </div>
      <div class="image-wrapper">
        <img class="img" src="${place.image_url}">
      </div>
      <div class="price">Price per night: $${place.price}</div>
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
  const filteredPrice = myFilters.value; // this refers to the selected price
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
