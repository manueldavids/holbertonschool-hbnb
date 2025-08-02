// ============================================================================
// HBnB - Main JavaScript functionality
// ============================================================================

// ============================================================================
// CONFIGURATION
// ============================================================================

// HBnB Frontend Configuration
const CONFIG = {
    // API Configuration - URLs en crudo
    API_BASE_URL: 'http://127.0.0.1:5000/api/v1',
    
    // Frontend Configuration
    FRONTEND_PORT: 8000,
    FRONTEND_URL: 'http://127.0.0.1:8000',
    
    // Endpoints
    ENDPOINTS: {
        LOGIN: '/auth/login',
        REGISTER: '/users/register',
        PLACES: '/places/',
        REVIEWS: '/reviews/',
        USERS: '/users/'
    }
};

// Helper function to get full API URL
function getApiUrl(endpoint) {
    return `${CONFIG.API_BASE_URL}${endpoint}`;
}

// ============================================================================
// INITIALIZATION
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const logoutLink = document.getElementById('logout-link');
    const reviewForm = document.getElementById('review-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    } else if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    } else if (reviewForm) {
        reviewForm.addEventListener('submit', handleReviewSubmit);
        setupReviewForm();
    } else {
        checkAuthentication();
    }

    // Add logout functionality
    if (logoutLink) {
        logoutLink.addEventListener('click', handleLogout);
    }

    // Add filter functionality
    const maxPriceSelect = document.getElementById('max-price');
    if (maxPriceSelect) {
        maxPriceSelect.addEventListener('change', filterPlaces);
    }
    
    // STRICT AUTHENTICATION CHECK - Redirect to login if no token
    const currentPage = window.location.pathname.split('/').pop();
    const publicPages = ['login.html', 'register.html'];
    
    // If not a public page, check for token
    if (!publicPages.includes(currentPage)) {
        const token = getAuthToken();
        if (!token) {
            console.log('No token found, redirecting to login...');
            window.location.href = 'login.html';
            return;
        }
    }
});

// ============================================================================
// AUTHENTICATION FUNCTIONS
// ============================================================================

async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(getApiUrl(CONFIG.ENDPOINTS.LOGIN), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            
            // Save user data and token
            saveUserData(data.user || {}, data.access_token);
            
            window.location.href = 'index.html';
        } else {
            const errorData = await response.json();
            alert(`Login failed: ${errorData.error || 'Invalid credentials'}`);
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Network error.');
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const first_name = document.getElementById('first_name').value;
    const last_name = document.getElementById('last_name').value;
    
    try {
        const response = await fetch(getApiUrl(CONFIG.ENDPOINTS.REGISTER), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                email, 
                password, 
                first_name, 
                last_name 
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            alert('Registration successful! Please login with your new account.');
            window.location.href = 'login.html';
        } else {
            const errorData = await response.json();
            alert(`Registration failed: ${errorData.error || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Network error. Please try again.');
    }
}

function handleLogout(event) {
    event.preventDefault();
    
    // Remove the token cookie
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    
    // Clear localStorage
    localStorage.removeItem('user');
    localStorage.removeItem('authToken');
    
    // Redirect to login page
    window.location.href = 'login.html';
}

function checkAuthentication() {
    const token = getAuthToken();
    const loginLink = document.getElementById('login-link');
    const registerLink = document.getElementById('register-link');
    const logoutLink = document.getElementById('logout-link');

    if (!token) {
        // User not authenticated - redirect to login
        console.log('No token found in checkAuthentication, redirecting to login...');
        window.location.href = 'login.html';
        return;
    } else {
        // User authenticated
        if (loginLink) loginLink.style.display = 'none';
        if (registerLink) registerLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'inline';
        fetchPlaces(token);
    }
}

// ============================================================================
// REVIEW FUNCTIONS
// ============================================================================

function setupReviewForm() {
    const reviewText = document.getElementById('review-text');
    const ratingSelect = document.getElementById('rating');

    // Add character counter for review text
    if (reviewText) {
        reviewText.addEventListener('input', function() {
            const maxLength = 500;
            const currentLength = this.value.length;
            
            // Update character counter if it exists, or create it
            let counter = document.getElementById('char-counter');
            if (!counter) {
                counter = document.createElement('div');
                counter.id = 'char-counter';
                counter.style.cssText = 'text-align: right; font-size: 0.8rem; color: #666; margin-top: 0.25rem;';
                reviewText.parentNode.appendChild(counter);
            }
            
            counter.textContent = `${currentLength}/${maxLength} characters`;
            
            if (currentLength > maxLength) {
                counter.style.color = '#dc3545';
            } else {
                counter.style.color = '#666';
            }
        });
    }

    // Add rating preview
    if (ratingSelect) {
        ratingSelect.addEventListener('change', function() {
            const rating = parseInt(this.value);
            const stars = '⭐'.repeat(rating) + '☆'.repeat(5 - rating);
            
            // Update rating preview if it exists, or create it
            let preview = document.getElementById('rating-preview');
            if (!preview) {
                preview = document.createElement('div');
                preview.id = 'rating-preview';
                preview.style.cssText = 'margin-top: 0.5rem; font-size: 1.2rem; color: #FFD700;';
                ratingSelect.parentNode.appendChild(preview);
            }
            
            preview.textContent = `Rating: ${stars}`;
        });
    }
}

async function handleReviewSubmit(event) {
    event.preventDefault();
    
    const reviewText = document.getElementById('review-text');
    const ratingSelect = document.getElementById('rating');
    const token = getAuthToken();

    if (!token) {
        alert('Please login to submit a review.');
        window.location.href = 'login.html';
        return;
    }

    const reviewData = {
        text: reviewText.value.trim(),
        rating: parseInt(ratingSelect.value),
        placeName: 'Beautiful Beach House',
        timestamp: new Date().toISOString()
    };

    // Validate form data
    if (!reviewData.text) {
        alert('Please enter your review text.');
        return;
    }

    if (reviewData.rating < 1 || reviewData.rating > 5) {
        alert('Please select a valid rating.');
        return;
    }

    // Submit review to API
    await submitReview(reviewData, token);
}

async function submitReview(reviewData, token) {
    // Show loading state
    const submitBtn = document.querySelector('.submit-review-btn');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Submitting...';
    submitBtn.disabled = true;

    try {
        // Get place ID from URL or use default
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('place_id') || 'bd76aaf7-9a01-41ef-9513-312aaed9f7f3';

        const response = await fetch(getApiUrl(CONFIG.ENDPOINTS.REVIEWS), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                rating: reviewData.rating,
                comment: reviewData.text
            })
        });

        if (response.ok) {
            const result = await response.json();
            showSuccessMessage();
            
            // Reset form
            document.getElementById('review-form').reset();
            
            // Store review in localStorage for demo purposes
            const existingReviews = JSON.parse(localStorage.getItem('hbnb_reviews') || '[]');
            existingReviews.push(reviewData);
            localStorage.setItem('hbnb_reviews', JSON.stringify(existingReviews));
            
        } else {
            const errorData = await response.json();
            alert(`Failed to submit review: ${errorData.error || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('Network error. Please try again.');
    } finally {
        // Reset button
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

function showSuccessMessage() {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `
        <div style="
            background-color: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 6px;
            margin-bottom: 1rem;
            text-align: center;
            border: 1px solid #c3e6cb;
        ">
            <strong>Success!</strong> Your review has been submitted successfully.
        </div>
    `;
    
    const formCard = document.querySelector('.review-form-card');
    const reviewForm = document.getElementById('review-form');
    if (formCard && reviewForm) {
        formCard.insertBefore(successDiv, reviewForm);
    }

    // Remove success message after 3 seconds
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Enhanced token getter that checks both cookie and localStorage
function getAuthToken() {
    return getCookie('token') || localStorage.getItem('authToken');
}

// Function to save user data to localStorage after successful login
function saveUserData(userData, token) {
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('authToken', token);
    document.cookie = `token=${token}; path=/`;
}

// Function to get current user data
function getCurrentUser() {
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
}

// Function to check if user is authenticated
function isAuthenticated() {
    const token = getAuthToken();
    return !!token;
}

// ============================================================================
// API FUNCTIONS
// ============================================================================

async function fetchPlaces(token) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Add authorization header if token is provided
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(getApiUrl(CONFIG.ENDPOINTS.PLACES), {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const data = await response.json();
            // Handle the new response format with places array and count
            const places = data.places || data;
            displayPlaces(places);
        } else {
            console.error('Failed to load places:', response.status);
            alert('Failed to load places');
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        alert('Failed to load places');
    }
}

// ============================================================================
// UI FUNCTIONS
// ============================================================================

function displayPlaces(places) {
    const placesContainer = document.querySelector('.places-container');

    if (!placesContainer) return;

    placesContainer.innerHTML = '';

    places.forEach(place => {
        const placeCard = createPlaceCard(place);
        placesContainer.appendChild(placeCard);
    });
}

function displayDemoPlaces() {
    const placesContainer = document.querySelector('.places-container');
    
    if (!placesContainer) return;

    placesContainer.innerHTML = '<p>Please log in to view available places.</p>';
}

function createPlaceCard(place) {
    const article = document.createElement('article');
    article.className = 'place-card';
    article.dataset.price = place.price_per_night || place.price || 0;

    article.innerHTML = `
        <h3>${place.name || 'Unnamed Place'}</h3>
        <p class="price">Price per night: $${place.price_per_night || place.price || 0}</p>
        <button class="view-details-btn" onclick="viewPlaceDetails('${place.id || 'demo'}')">View Details</button>
    `;

    return article;
}

function viewPlaceDetails(placeId) {
    window.location.href = `place.html?id=${placeId}`;
}

function filterPlaces() {
    const maxPrice = document.getElementById('max-price').value;
    const placeCards = document.querySelectorAll('.place-card');
    
    placeCards.forEach(card => {
        const price = parseInt(card.dataset.price);
        
        if (maxPrice === 'all' || price <= parseInt(maxPrice)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// ============================================================================
// AUTHENTICATION PROTECTION
// ============================================================================

// STRICT AUTHENTICATION CHECK - Redirect to login if no token
function checkProtectedPages() {
    const currentPage = window.location.pathname.split('/').pop();
    const publicPages = ['login.html', 'register.html'];
    
    // If not a public page, check for token
    if (!publicPages.includes(currentPage)) {
        const token = getAuthToken();
        if (!token) {
            console.log('No token found in checkProtectedPages, redirecting to login...');
            window.location.href = 'login.html';
            return;
        }
    }
}

// Update navigation based on authentication status
function updateNavigation() {
    const token = getAuthToken();
    const loginLink = document.getElementById('login-link');
    const registerLink = document.getElementById('register-link');
    const logoutLink = document.getElementById('logout-link');

    if (!token) {
        // User not authenticated - redirect to login
        console.log('No token found in updateNavigation, redirecting to login...');
        window.location.href = 'login.html';
        return;
    } else {
        // User authenticated
        if (loginLink) loginLink.style.display = 'none';
        if (registerLink) registerLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'inline';
    }
}

// ============================================================================
// STYLES FOR SUCCESS MESSAGE
// ============================================================================

// Add styles for success message
const style = document.createElement('style');
style.textContent = `
    .success-message {
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);

