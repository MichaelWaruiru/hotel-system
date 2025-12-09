class ParkPalaceApp {
  constructor() {
      this.currentRoom = null;
      this.currentMenuCategory = 'breakfast';
      this.init();
  }

  init() {
      this.setupEventListeners();
      this.loadInitialData();
  }

  setupEventListeners() {
      // Menu category navigation
      document.querySelectorAll('#menuTabs .nav-link').forEach(tab => {
          tab.addEventListener('click', (e) => {
              e.preventDefault();
              this.switchMenuCategory(e.target.dataset.category);
          });
      });

      // Booking form submission
      document.getElementById('submitBooking')?.addEventListener('click', (e) => {
          e.preventDefault();
          this.submitBooking();
      });

      // Smooth scrolling for navigation links
      document.querySelectorAll('a[href^="#"]').forEach(link => {
          link.addEventListener('click', (e) => {
              e.preventDefault();
              const target = document.querySelector(link.getAttribute('href'));
              if (target) {
                  target.scrollIntoView({ behavior: 'smooth' });
              }
          });
      });
  }

  async loadInitialData() {
      await Promise.all([
          this.loadRooms(),
          this.loadMenu('breakfast'),
          this.loadHotelInfo()
      ]);
  }

  async loadRooms() {
      try {
          const response = await fetch('/api/rooms/featured');
          const rooms = await response.json();
          this.renderRooms(rooms);
      } catch (error) {
          console.error('Error loading rooms:', error);
          this.showError('rooms-container', 'Failed to load rooms');
      }
  }

  renderRooms(rooms) {
      const container = document.getElementById('rooms-container');
      
      if (!rooms || rooms.length === 0) {
          container.innerHTML = '<div class="col-12 text-center"><p class="text-muted">No rooms available</p></div>';
          return;
      }

      container.innerHTML = rooms.map(room => `
          <div class="col-lg-4 col-md-6 mb-4">
              <div class="card room-card h-100 fade-in">
                  <img src="/static/${room.imageUrl}" class="card-img-top" alt="${room.name}">
                  <div class="card-body d-flex flex-column">
                      <div class="d-flex justify-content-between align-items-start mb-2">
                          <h5 class="card-title">${room.name}</h5>
                          <span class="price-display">$${room.price}</span>
                      </div>
                      <p class="card-text text-muted flex-grow-1">${room.description}</p>
                      
                      <div class="room-details mb-3">
                          <small class="text-muted">
                              <i class="bi bi-people me-1"></i>Up to ${room.capacity} guests
                              <span class="ms-3"><i class="bi bi-arrows-fullscreen me-1"></i>${room.size}</span>
                          </small>
                      </div>
                      
                      <div class="room-amenities mb-3">
                          ${room.amenities.map(amenity => `
                              <span class="amenity-badge">${amenity}</span>
                          `).join('')}
                      </div>
                      
                      <button class="btn btn-primary w-100 mt-auto" onclick="app.openBookingModal(${room.id}, '${room.name}', '${room.price}')">
                          <i class="bi bi-calendar-check me-2"></i>Book Now
                      </button>
                  </div>
              </div>
          </div>
      `).join('');
  }

  async loadMenu(category) {
      try {
          const response = await fetch(`/api/menu/category/${category}`);
          const menuItems = await response.json();
          this.renderMenu(menuItems);
      } catch (error) {
          console.error('Error loading menu:', error);
          this.showError('menu-container', 'Failed to load menu');
      }
  }

  renderMenu(menuItems) {
      const container = document.getElementById('menu-container');
      
      if (!menuItems || menuItems.length === 0) {
          container.innerHTML = `
              <div class="col-12 text-center py-5">
                  <i class="bi bi-cup-hot fs-1 text-muted mb-3"></i>
                  <p class="text-muted">No items available in this category</p>
              </div>
          `;
          return;
      }

      container.innerHTML = menuItems.map(item => `
          <div class="col-lg-4 col-md-6 mb-4">
              <div class="card menu-item-card fade-in">
                  <img src="/static/${item.imageUrl}" class="card-img-top" alt="${item.name}">
                  <div class="card-body">
                      <div class="d-flex justify-content-between align-items-start mb-2">
                          <h6 class="card-title">${item.name}</h6>
                          <span class="price-display">$${item.price}</span>
                      </div>
                      <p class="card-text text-muted small">${item.description}</p>
                      
                      <div class="d-flex flex-wrap align-items-center">
                          ${item.dietary.map(diet => `
                              <span class="dietary-badge dietary-${diet}">${diet}</span>
                          `).join('')}
                          ${item.available ? '<span class="dietary-badge" style="background-color: #e8f5e8; color: #2e7d32;">Available</span>' : ''}
                      </div>
                  </div>
              </div>
          </div>
      `).join('');
  }

  async loadHotelInfo() {
      try {
          const response = await fetch('/api/hotel');
          const hotelInfo = await response.json();
          this.renderHotelInfo(hotelInfo);
      } catch (error) {
          console.error('Error loading hotel info:', error);
          this.showError('hotel-info-container', 'Failed to load hotel information');
      }
  }

  renderHotelInfo(info) {
      const container = document.getElementById('hotel-info-container');
      
      container.innerHTML = `
          <div class="text-center mb-5">
              <h2 class="display-5 fw-bold mb-3">About ${info.name}</h2>
              <p class="lead text-muted">${info.description}</p>
          </div>

          <div class="row mb-5">
              <div class="col-lg-6 mb-4">
                  <div class="card hotel-info-card h-100">
                      <div class="card-header bg-primary text-white">
                          <h5 class="mb-0"><i class="bi bi-geo-alt me-2"></i>Location & Contact</h5>
                      </div>
                      <div class="card-body">
                          <div class="mb-3">
                              <strong><i class="bi bi-geo-alt text-primary me-2"></i>Address</strong>
                              <p class="text-muted mb-0">${info.address}</p>
                          </div>
                          <div class="mb-3">
                              <strong><i class="bi bi-telephone text-primary me-2"></i>Phone</strong>
                              <p class="text-muted mb-0">${info.phone}</p>
                          </div>
                          <div class="mb-3">
                              <strong><i class="bi bi-envelope text-primary me-2"></i>Email</strong>
                              <p class="text-muted mb-0">${info.email}</p>
                          </div>
                          <div>
                              <strong><i class="bi bi-clock text-primary me-2"></i>Check-in / Check-out</strong>
                              <p class="text-muted mb-0">
                                  Check-in: ${info.checkInTime}<br>
                                  Check-out: ${info.checkOutTime}
                              </p>
                          </div>
                      </div>
                  </div>
              </div>
              
              <div class="col-lg-6 mb-4">
                  <div class="card hotel-info-card h-100">
                      <div class="card-header bg-primary text-white">
                          <h5 class="mb-0"><i class="bi bi-star me-2"></i>Hotel Amenities</h5>
                      </div>
                      <div class="card-body">
                          <div class="amenity-list">
                              ${info.amenities.map(amenity => `
                                  <div class="amenity-item">${amenity}</div>
                              `).join('')}
                          </div>
                      </div>
                  </div>
              </div>
          </div>

          <div class="card hotel-info-card mb-5">
              <div class="card-header bg-primary text-white">
                  <h5 class="mb-0"><i class="bi bi-shield-check me-2"></i>Hotel Policies</h5>
              </div>
              <div class="card-body">
                  ${info.policies.map(policy => `
                      <div class="policy-item">${policy}</div>
                  `).join('')}
              </div>
          </div>

          <div class="text-center bg-light p-5 rounded">
              <h3 class="fw-bold mb-3">Ready to Experience Park Palace?</h3>
              <p class="text-muted mb-4">
                  Book your stay with us and discover the perfect blend of luxury, comfort, and exceptional service. 
                  Our dedicated team is ready to make your visit unforgettable.
              </p>
              <div class="d-flex flex-column flex-sm-row gap-3 justify-content-center">
                  <a href="tel:+211-712-345-678" class="btn btn-primary">
                      <i class="bi bi-telephone me-2"></i>Call Now
                  </a>
                  <a href="mailto:reservations@parkpalace.com" class="btn btn-outline-primary">
                      <i class="bi bi-envelope me-2"></i>Email Us
                  </a>
              </div>
          </div>
      `;
  }

  switchMenuCategory(category) {
      // Update active tab
      document.querySelectorAll('#menuTabs .nav-link').forEach(tab => {
          tab.classList.remove('active');
      });
      document.querySelector(`#menuTabs .nav-link[data-category="${category}"]`).classList.add('active');
      
      // Load menu for selected category
      this.currentMenuCategory = category;
      this.loadMenu(category);
  }

  openBookingModal(roomId, roomName, roomPrice) {
      this.currentRoom = { id: roomId, name: roomName, price: roomPrice };
      
      // Set room ID in hidden field
      document.getElementById('roomId').value = roomId;
      
      // Update modal title
      document.getElementById('bookingModalLabel').textContent = `Book ${roomName}`;
      
      // Set minimum date to today
      const today = new Date().toISOString().split('T')[0];
      document.getElementById('checkIn').min = today;
      document.getElementById('checkOut').min = today;
      
      // Show modal
      const modal = new bootstrap.Modal(document.getElementById('bookingModal'));
      modal.show();
  }

  async submitBooking() {
      const form = document.getElementById('bookingForm');
      const formData = new FormData(form);
      
      // Validate form
      if (!form.checkValidity()) {
          form.classList.add('was-validated');
          return;
      }

      // Prepare booking data
      const bookingData = {
          roomId: parseInt(document.getElementById('roomId').value),
          firstName: formData.get('firstName') || document.getElementById('firstName').value,
          lastName: formData.get('lastName') || document.getElementById('lastName').value,
          email: formData.get('email') || document.getElementById('email').value,
          phone: formData.get('phone') || document.getElementById('phone').value,
          checkIn: formData.get('checkIn') || document.getElementById('checkIn').value,
          checkOut: formData.get('checkOut') || document.getElementById('checkOut').value,
          guests: parseInt(formData.get('guests') || document.getElementById('guests').value),
          paymentMethod: formData.get('paymentMethod') || document.getElementById('paymentMethod').value
      };

      try {
          const response = await fetch('/api/bookings', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify(bookingData)
          });

          if (response.ok) {
              const booking = await response.json();
              this.showBookingSuccess(booking);
              
              // Close modal and reset form
              bootstrap.Modal.getInstance(document.getElementById('bookingModal')).hide();
              form.reset();
              form.classList.remove('was-validated');
          } else {
              const error = await response.json();
              this.showBookingError(error.error || 'Failed to create booking');
          }
      } catch (error) {
          console.error('Error submitting booking:', error);
          this.showBookingError('Network error occurred');
      }
  }

  showBookingSuccess(booking) {
      const alert = document.createElement('div');
      alert.className = 'alert alert-success alert-dismissible fade show position-fixed';
      alert.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
      alert.innerHTML = `
          <strong>Booking Confirmed!</strong><br>
          Booking ID: ${booking.id}<br>
          Room: ${this.currentRoom.name}<br>
          Check-in: ${booking.checkIn}
          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      document.body.appendChild(alert);
      
      // Auto remove after 5 seconds
      setTimeout(() => {
          if (alert.parentNode) {
              alert.parentNode.removeChild(alert);
          }
      }, 5000);
  }

  showBookingError(message) {
      const alert = document.createElement('div');
      alert.className = 'alert alert-danger alert-dismissible fade show position-fixed';
      alert.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
      alert.innerHTML = `
          <strong>Booking Failed!</strong><br>
          ${message}
          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      document.body.appendChild(alert);
      
      // Auto remove after 5 seconds
      setTimeout(() => {
          if (alert.parentNode) {
              alert.parentNode.removeChild(alert);
          }
      }, 5000);
  }

  showError(containerId, message) {
      const container = document.getElementById(containerId);
      container.innerHTML = `
          <div class="col-12 text-center py-5">
              <i class="bi bi-exclamation-triangle fs-1 text-warning mb-3"></i>
              <p class="text-muted">${message}</p>
              <button class="btn btn-outline-primary" onclick="location.reload()">Retry</button>
          </div>
      `;
  }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.app = new ParkPalaceApp();
});

// Update check-out date when check-in changes
document.addEventListener('DOMContentLoaded', () => {
  const checkInInput = document.getElementById('checkIn');
  const checkOutInput = document.getElementById('checkOut');
  
  if (checkInInput && checkOutInput) {
      checkInInput.addEventListener('change', () => {
          const checkInDate = new Date(checkInInput.value);
          const nextDay = new Date(checkInDate);
          nextDay.setDate(nextDay.getDate() + 1);
          
          checkOutInput.min = nextDay.toISOString().split('T')[0];
          if (checkOutInput.value && checkOutInput.value <= checkInInput.value) {
              checkOutInput.value = nextDay.toISOString().split('T')[0];
          }
      });
  }
});

// Updates year range automatically
const startYear = 2021;
const currentYear = new Date().getFullYear();
document.getElementById("year-range").textContent = startYear === currentYear ? `${startYear}` : `${startYear} - ${currentYear}`;