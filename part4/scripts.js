// HBnB - Main JavaScript functionality
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    } else {
        checkAuthentication();
    }
});

async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            alert('Login failed.');
        }
    } catch (error) {
        alert('Network error.');
    }
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.querySelector('nav a[href="login.html"]');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/places/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            alert('Failed to load places');
        }
    } catch (error) {
        alert('Failed to load places');
    }
}

function displayPlaces(places) {
    const placesContainer = document.querySelector('.places-container');

    if (!placesContainer) return;

    placesContainer.innerHTML = '';

    places.forEach(place => {
        const placeCard = createPlaceCard(place);
        placesContainer.appendChild(placeCard);
    });
}

function createPlaceCard(place) {
    const article = document.createElement('article');
    article.className = 'place-card';
    article.dataset.price = place.price_per_night || 0;

    article.innerHTML = `
        <img src="images/img_place.png" alt="${place.name || 'Place'}">
        <div class="place-info">
            <h2>${place.name || 'Unnamed Place'}</h2>
            <p class="price">$${place.price_per_night || 0} per night</p>
            <button onclick="viewPlaceDetails('${place.id}')">View Details</button>
        </div>
    `;

    return article;
}

function viewPlaceDetails(placeId) {
    window.location.href = `place.html?id=${placeId}`;
}

