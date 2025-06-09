// Pin Detail Modal Functionality

function openPinDetailModal(pin) {
    // Set modal title
    const modalTitle = document.getElementById('modalPinTitle');
    if (modalTitle) modalTitle.textContent = pin.title;
    
    // Set image or show placeholder
    const imageContainer = document.getElementById('modalPinImage');
    const noImagePlaceholder = document.getElementById('modalNoImage');
    
    if (imageContainer && noImagePlaceholder) {
        if (pin.image) {
            imageContainer.src = pin.image;
            imageContainer.style.display = 'block';
            noImagePlaceholder.style.display = 'none';
        } else {
            imageContainer.style.display = 'none';
            noImagePlaceholder.style.display = 'flex';
        }
    }
    
    // Set directions link
    const directionsLink = document.getElementById('modalDirectionsLink');
    if (directionsLink) {
        directionsLink.href = `https://www.google.com/maps/dir/?api=1&destination=${pin.latitude},${pin.longitude}`;
    }
    
    // Set category badge
    const categoryBadge = document.getElementById('modalCategoryBadge');
    if (categoryBadge) {
        if (pin.category === 'dispensary') {
            categoryBadge.className = 'badge bg-success';
            categoryBadge.innerHTML = '<i class="bi bi-shop"></i> Dispensary';
        } else {
            categoryBadge.className = 'badge bg-primary';
            categoryBadge.innerHTML = '<i class="bi bi-emoji-smile"></i> Smoke Spot';
        }
    }
    
    // Set author
    const authorLink = document.getElementById('modalPinAuthor');
    if (authorLink) {
        authorLink.textContent = pin.username;
        authorLink.href = `/profile/${pin.username}/`;
    }
    
    // Set rating stars
    const starsDisplay = document.getElementById('modalStarsDisplay');
    if (starsDisplay) {
        starsDisplay.innerHTML = getStarsHtml(pin.average_rating);
    }
    
    const reviewCount = document.getElementById('modalReviewCount');
    if (reviewCount) {
        reviewCount.textContent = `(${pin.rating_count} ${pin.rating_count === 1 ? 'review' : 'reviews'})`;
    }
    
    // Set description
    const pinDescription = document.getElementById('modalPinDescription');
    if (pinDescription) {
        pinDescription.textContent = pin.description;
    }
    
    // Set feature badges
    const features = document.getElementById('modalFeaturesList');
    if (features) {
        features.innerHTML = '';
        
        // Security level
        if (pin.security_level > 1) {
            const securityLabels = ['', 'Low', 'Medium', 'High'];
            features.innerHTML += `<div class="feature-badge">
                <i class="bi bi-shield-fill"></i> ${securityLabels[pin.security_level]} discretion
            </div>`;
        }
        
        // Has seating
        if (pin.has_seating === true || pin.has_seating === 'true' || pin.has_seating === 'on') {
            features.innerHTML += `<div class="feature-badge">
                <i class="bi bi-chair"></i> Seating
            </div>`;
        }
        
        // Is scenic
        if (pin.is_scenic === true || pin.is_scenic === 'true' || pin.is_scenic === 'on') {
            features.innerHTML += `<div class="feature-badge">
                <i class="bi bi-image"></i> Scenic
            </div>`;
        }
        
        // Is sheltered
        if (pin.is_sheltered === true || pin.is_sheltered === 'true' || pin.is_sheltered === 'on') {
            features.innerHTML += `<div class="feature-badge">
                <i class="bi bi-umbrella"></i> Sheltered
            </div>`;
        }
        
        // Is private
        if (pin.is_private === true || pin.is_private === 'true' || pin.is_private === 'on') {
            features.innerHTML += `<div class="feature-badge">
                <i class="bi bi-eye-slash"></i> Private
            </div>`;
        }
        
        // Is accessible
        if (pin.is_accessible === true || pin.is_accessible === 'true' || pin.is_accessible === 'on') {
            features.innerHTML += `<div class="feature-badge">
                <i class="bi bi-universal-access"></i> Accessible
            </div>`;
        } else if (pin.is_accessible === false || pin.is_accessible === 'false' || pin.is_accessible === 'off') {
            features.innerHTML += `<div class="feature-badge">
                <i class="bi bi-universal-access-circle"></i> Limited access
            </div>`;
        }
    }
    
    // Set up favorite button
    const isAuthenticated = document.body.dataset.userAuthenticated === 'true';
    const currentUsername = document.body.dataset.username;
    const favoriteBtn = document.getElementById('modalFavoriteBtn');
    
    if (favoriteBtn) {
        if (isAuthenticated) {
            favoriteBtn.style.display = 'inline-block';
            favoriteBtn.dataset.pinId = pin.id;
            
            if (pin.is_favorite) {
                favoriteBtn.className = 'btn btn-danger me-2 mb-2';
                favoriteBtn.innerHTML = '<i class="bi bi-heart-fill"></i>';
            } else {
                favoriteBtn.className = 'btn btn-outline-danger me-2 mb-2';
                favoriteBtn.innerHTML = '<i class="bi bi-heart"></i>';
            }
        } else {
            favoriteBtn.style.display = 'none';
        }
    }
    
    // Set up delete button
    const deleteBtn = document.getElementById('modalDeleteBtn');
    if (deleteBtn) {
        if (isAuthenticated && pin.username === currentUsername) {
            deleteBtn.style.display = 'inline-block';
            deleteBtn.dataset.pinId = pin.id;
        } else {
            deleteBtn.style.display = 'none';
        }
    }
    
    // Setup review form
    const reviewForm = document.getElementById('modalReviewFormContainer');
    const loginPrompt = document.getElementById('modalLoginPrompt');
    const submitBtn = document.getElementById('modalSubmitReview');
    
    if (reviewForm && loginPrompt && submitBtn) {
        if (isAuthenticated) {
            reviewForm.style.display = 'block';
            loginPrompt.style.display = 'none';
            submitBtn.dataset.pinId = pin.id;
            
            // Reset review form
            const ratingValue = document.getElementById('modalRatingValue');
            const reviewComment = document.getElementById('modalReviewComment');
            const stars = document.querySelectorAll('#modalStarsInput .star i');
            
            if (ratingValue) ratingValue.value = '0';
            if (reviewComment) reviewComment.value = '';
            if (stars) {
                stars.forEach(star => {
                    star.className = 'bi bi-star';
                });
            }
        } else {
            reviewForm.style.display = 'none';
            loginPrompt.style.display = 'block';
        }
    }
    
    // Load reviews
    loadReviewsForModal(pin.id);
    
    // Show the modal
    try {
        const pinDetailModal = document.getElementById('pinDetailModal');
        if (pinDetailModal) {
            const modal = new bootstrap.Modal(pinDetailModal);
            modal.show();
        }
    } catch (e) {
        console.error('Error showing modal:', e);
    }
}

// Function to load reviews for a pin
function loadReviewsForModal(pinId) {
  const reviewsList = document.getElementById('modalReviewsList');
  const noReviews = document.getElementById('modalNoReviews');
  
  if (!reviewsList || !noReviews) return;
  
  // Add error handling and prevent connection issues
  fetch(`/api/pins/${pinId}/reviews/`, { 
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest'
    },
    // Add a timeout to prevent hanging requests
    signal: AbortSignal.timeout(5000)
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.reviews && data.reviews.length > 0) {
        reviewsList.innerHTML = '';
        noReviews.style.display = 'none';
        
        data.reviews.forEach(review => {
          try {
            reviewsList.innerHTML += `
              <div class="review-item">
                <div class="stars-display">
                  ${typeof getStarsHtml === 'function' ? getStarsHtml(review.rating) : ''}
                  <span style="color: #cbff78; font-weight: 500;">${review.username || 'Anonymous'}</span>
                </div>
                ${review.comment ? `<p class="mt-2">${review.comment}</p>` : ''}
              </div>`;
          } catch (error) {
            console.warn('Error rendering review:', error);
          }
        });
        reviewsList.style.display = 'block';
      } else {
        noReviews.style.display = 'block';
        reviewsList.style.display = 'none';
      }
    })
    .catch(error => {
      console.error('Error loading reviews:', error);
      if (reviewsList) {
        reviewsList.innerHTML = '<div class="alert alert-danger">Error loading reviews. Please try again later.</div>';
      }
      noReviews.style.display = 'none';
    });
}

// This function should be defined in the main JS but we'll add it here as a fallback
if (typeof getStarsHtml !== 'function') {
    function getStarsHtml(rating) {
        const fullStars = Math.floor(rating);
        const halfStar = rating % 1 >= 0.5;
        const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
        
        let html = '';
        // Full stars
        for (let i = 0; i < fullStars; i++) {
            html += '<i class="bi bi-star-fill"></i>';
        }
        // Half star if needed
        if (halfStar) {
            html += '<i class="bi bi-star-half"></i>';
        }
        // Empty stars
        for (let i = 0; i < emptyStars; i++) {
            html += '<i class="bi bi-star"></i>';
        }
        return html;
    }
}

// Add event listeners once DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    try {
        // Star rating functionality
        const starsInput = document.querySelector('#modalStarsInput');
        if (starsInput) {
            starsInput.addEventListener('click', function(e) {
                if (e.target.closest('.star')) {
                    const star = e.target.closest('.star');
                    const rating = parseInt(star.dataset.value);
                    
                    // Update stars display
                    const stars = this.querySelectorAll('.star');
                    stars.forEach((s, index) => {
                        const starIcon = s.querySelector('i');
                        if (index < rating) {
                            starIcon.className = 'bi bi-star-fill';
                        } else {
                            starIcon.className = 'bi bi-star';
                        }
                    });
                    
                    // Store rating value
                    const ratingValue = document.getElementById('modalRatingValue');
                    if (ratingValue) ratingValue.value = rating;
                }
            });
        }
        
        // Submit review button
        const submitReviewBtn = document.getElementById('modalSubmitReview');
        if (submitReviewBtn) {
            submitReviewBtn.addEventListener('click', function() {
                const pinId = this.dataset.pinId;
                const ratingValue = document.getElementById('modalRatingValue');
                const reviewComment = document.getElementById('modalReviewComment');
                
                if (!ratingValue || !reviewComment) return;
                
                const rating = parseInt(ratingValue.value);
                const comment = reviewComment.value.trim();
                
                if (rating === 0) {
                    alert('Please select a rating before submitting.');
                    return;
                }
                
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
                if (!csrfToken) {
                    alert('CSRF token not found. Please refresh the page and try again.');
                    return;
                }
                
                fetch(`/api/pins/${pinId}/reviews/create/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken.value
                    },
                    body: JSON.stringify({
                        rating: rating,
                        comment: comment
                    })
                })
                .then(response => response.json())
                .then(data => {
                    // Update displays
                    const starsDisplay = document.getElementById('modalStarsDisplay');
                    if (starsDisplay) starsDisplay.innerHTML = getStarsHtml(data.average_rating);
                    
                    const reviewCount = document.getElementById('modalReviewCount');
                    if (reviewCount) {
                        reviewCount.textContent = `(${data.rating_count} ${data.rating_count === 1 ? 'review' : 'reviews'})`;
                    }
                    
                    // Reset form
                    if (ratingValue) ratingValue.value = '0';
                    if (reviewComment) reviewComment.value = '';
                    
                    const stars = document.querySelectorAll('#modalStarsInput .star i');
                    stars.forEach(star => {
                        star.className = 'bi bi-star';
                    });
                    
                    // Reload reviews
                    loadReviewsForModal(pinId);
                    
                    // Update marker data if the window function exists
                    if (typeof window.updateMarkerRating === 'function') {
                        window.updateMarkerRating(pinId, data.average_rating, data.rating_count);
                    }
                    
                    alert('Thank you for your review!');
                })
                .catch(error => {
                    console.error('Error submitting review:', error);
                    alert('Failed to submit review. Please try again.');
                });
            });
        }
        
        // Favorite button
        const favoriteBtn = document.getElementById('modalFavoriteBtn');
        if (favoriteBtn) {
            favoriteBtn.addEventListener('click', function() {
                const pinId = this.dataset.pinId;
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
                
                if (!csrfToken) {
                    alert('CSRF token not found. Please refresh the page and try again.');
                    return;
                }
                
                fetch(`/api/pins/${pinId}/favorite/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken.value
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'added') {
                        this.className = 'btn btn-danger me-2 mb-2';
                        this.innerHTML = '<i class="bi bi-heart-fill"></i>';
                    } else {
                        this.className = 'btn btn-outline-danger me-2 mb-2';
                        this.innerHTML = '<i class="bi bi-heart"></i>';
                    }
                    
                    // Update marker data if the window function exists
                    if (typeof window.updateMarkerFavorite === 'function') {
                        window.updateMarkerFavorite(pinId, data.status === 'added');
                    }
                })
                .catch(error => {
                    console.error('Error toggling favorite:', error);
                    alert('Failed to update favorite. Please try again.');
                });
            });
        }
        
        // Delete button
        const deleteBtn = document.getElementById('modalDeleteBtn');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', function() {
                const pinId = this.dataset.pinId;
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
                
                if (!csrfToken) {
                    alert('CSRF token not found. Please refresh the page and try again.');
                    return;
                }
                
                if (confirm('Are you sure you want to delete this pin? This action cannot be undone.')) {
                    fetch(`/api/pins/${pinId}/delete/`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': csrfToken.value
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Close modal
                        const pinDetailModal = document.getElementById('pinDetailModal');
                        if (pinDetailModal) {
                            const modal = bootstrap.Modal.getInstance(pinDetailModal);
                            if (modal) modal.hide();
                        }
                        
                        // Remove marker from map if the window function exists
                        if (typeof window.removeMarkerFromMap === 'function') {
                            window.removeMarkerFromMap(pinId);
                        }
                        
                        alert('Pin deleted successfully');
                    })
                    .catch(error => {
                        console.error('Error deleting pin:', error);
                        alert('Failed to delete pin. Please try again.');
                    });
                }
            });
        }
    } catch (e) {
        console.error('Error setting up modal event listeners:', e);
    }
});