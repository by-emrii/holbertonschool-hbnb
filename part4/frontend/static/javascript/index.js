// Display/hide loginLink depending on Auth
function checkAuthentication() {
  const token = getCookie("token");
  const loginLink = document.getElementsByClassName("login-button");

  if (!token) {
    loginLink[0].style.display = "block";
  } else {
    loginLink[0].style.display = "none";
    // Fetch places data if the user is authenticated
    fetchPlaces(token);
  }
}

checkAuthentication();

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

// Populate places list dynamically
function displayPlaces(places) {
  const placeCard = document.querySelector("#places-list");
  placeCard.innerHTML = "";
  for (const place of places) {
    // console.log(place);
    const placeDiv = document.createElement("div");
    placeDiv.setAttribute("class", "place-card");
    placeDiv.setAttribute("data-price", place.price);
    placeDiv.innerHTML = `
              <div>
                  <h2 class="card-title">${place.title}</h2>
              </div>
              <div class="price">Price per night: $${place.price}</div>
              <button id="details-button">View Details</button>`;
    placeCard.appendChild(placeDiv);
  }
}

// Implement Client side filtering
document.getElementById("price-filter").addEventListener("change", (event) => {
  const myFilters = document.getElementById("price-filter");
  const filteredPrice = myFilters.value; // this refers to the selected price
  const places = document.getElementById("places-list");
  //   console.log(places);

  for (const place of places.children) {
    // console.log(places.children);
    // console.log(place);
    // break;
    const placePrice = place.getAttribute("data-price");
    // console.log(placePrice);
    if (filteredPrice === "All" || placePrice <= parseFloat(filteredPrice)) {
      place.style.display = "block";
    } else {
      place.style.display = "none";
    }
  }
});
