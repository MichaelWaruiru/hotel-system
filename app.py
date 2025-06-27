from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "park-palace-hotel-secret-key")


rooms_data = [
    {
        "id": 1,
        "name": "Executive Suite",
        "description": "Spacious executive suite with panoramic city views, marble bathroom, and premium amenities for the discerning business traveler.",
        "price": "450.00",
        "imageUrl": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600",
        "capacity": 4,
        "size": "75 sqm",
        "amenities": ["King Bed", "City View", "Marble Bathroom", "Work Desk", "Mini Bar", "Premium WiFi"],
        "featured": True
    },
    {
        "id": 2,
        "name": "Luxury Ocean View",
        "description": "Elegant oceanfront suite featuring floor-to-ceiling windows, private balcony, and world-class spa amenities.",
        "price": "650.00",
        "imageUrl": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600",
        "capacity": 2,
        "size": "85 sqm",
        "amenities": ["Ocean View", "Private Balcony", "Jacuzzi", "Butler Service", "Premium Minibar"],
        "featured": True
    },
    {
        "id": 3,
        "name": "Presidential Suite",
        "description": "Our crown jewel offering unmatched luxury with separate living areas, private dining room, and dedicated concierge service.",
        "price": "1200.00",
        "imageUrl": "https://images.unsplash.com/photo-1590490360182-c33d57733427?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600",
        "capacity": 6,
        "size": "150 sqm",
        "amenities": ["Separate Living Room", "Private Dining", "Concierge Service", "Premium Bar", "City Panorama"],
        "featured": True
    }
]

menu_items = [
    {
        "id": 1,
        "name": "Gloria Signature Breakfast",
        "description": "Traditional breakfast with eggs benedict, artisan breads, fresh fruits, and premium coffee",
        "price": "28.00",
        "category": "breakfast",
        "imageUrl": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600",
        "dietary": ["vegetarian"],
        "available": True
    },
    {
        "id": 2,
        "name": "Healthy Power Bowl",
        "description": "Quinoa, avocado, fresh berries, nuts, and organic honey drizzle",
        "price": "24.00",
        "category": "breakfast",
        "imageUrl": "https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600",
        "dietary": ["vegan", "gluten-free"],
        "available": True
    },
    {
        "id": 3,
        "name": "Mediterranean Grilled Salmon",
        "description": "Fresh Atlantic salmon with roasted vegetables, quinoa, and lemon herb sauce",
        "price": "42.00",
        "category": "lunch",
        "imageUrl": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600",
        "dietary": ["gluten-free"],
        "available": True
    },
    {
        "id": 4,
        "name": "Truffle Pasta Primavera",
        "description": "House-made pasta with seasonal vegetables, truffle oil, and parmesan",
        "price": "38.00",
        "category": "lunch",
        "imageUrl": "https://images.unsplash.com/photo-1563379091339-03246963d7d3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600",
        "dietary": ["vegetarian"],
        "available": True
    },
    {
        "id": 5,
        "name": "Gloria Wagyu Steak",
        "description": "Premium A5 Wagyu beef with roasted potatoes, seasonal vegetables, and red wine reduction",
        "price": "85.00",
        "category": "dinner",
        "imageUrl": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600",
        "dietary": [],
        "available": True
    },
    {
        "id": 6,
        "name": "Lobster Thermidor",
        "description": "Fresh lobster in cognac cream sauce, gruyere cheese, served with herb rice",
        "price": "68.00",
        "category": "dinner",
        "imageUrl": "https://images.unsplash.com/photo-1559847844-d98a29d0c27f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600",
        "dietary": ["gluten-free"],
        "available": True
    },
    {
        "id": 7,
        "name": "Gloria Signature Cocktail",
        "description": "Premium gin, elderflower, fresh cucumber, and lime with a touch of rosemary",
        "price": "18.00",
        "category": "beverages",
        "imageUrl": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600",
        "dietary": ["vegan"],
        "available": True
    },
    {
        "id": 8,
        "name": "Vintage Wine Selection",
        "description": "Curated selection of premium wines from our cellar, paired with artisan cheeses",
        "price": "65.00",
        "category": "beverages",
        "imageUrl": "https://images.unsplash.com/photo-1474722883778-792e7990302f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600",
        "dietary": ["vegetarian"],
        "available": True
    },
    {
        "id": 9,
        "name": "Chocolate Lava Cake",
        "description": "Warm chocolate cake with molten center, vanilla ice cream, and berry compote",
        "price": "16.00",
        "category": "desserts",
        "imageUrl": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600",
        "dietary": ["vegetarian"],
        "available": True
    },
    {
        "id": 10,
        "name": "Tiramisu Royale",
        "description": "Classic Italian tiramisu with ladyfingers, mascarpone, and espresso",
        "price": "14.00",
        "category": "desserts",
        "imageUrl": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600",
        "dietary": ["vegetarian"],
        "available": True
    }
]

hotel_info = {
    "id": 1,
    "name": "Gloria Regency Hotel",
    "description": "Experience unparalleled luxury and elegance at Gloria Regency Hotel, where sophisticated accommodations meet world-class service. Located in the heart of the city, our hotel offers breathtaking views, exquisite dining, and premium amenities for the discerning traveler.",
    "address": "123 Luxury Boulevard, Metropolitan District, MC 10001",
    "phone": "+1 (555) 123-4567",
    "email": "reservations@gloriaregency.com",
    "checkInTime": "3:00 PM",
    "checkOutTime": "12:00 PM",
    "amenities": [
        "24/7 Concierge Service",
        "Luxury Spa & Wellness Center",
        "Rooftop Infinity Pool",
        "State-of-the-Art Fitness Center",
        "Fine Dining Restaurant",
        "Business Center",
        "Valet Parking",
        "Room Service",
        "Laundry & Dry Cleaning",
        "Airport Transfer Service",
        "Meeting & Event Facilities",
        "Complimentary WiFi"
    ],
    "policies": [
        "Check-in: 3:00 PM | Check-out: 12:00 PM",
        "Cancellation: Free cancellation up to 24 hours before arrival",
        "Pet Policy: Pets welcome with advance notice (additional fees apply)",
        "Smoking: Designated smoking areas only - all rooms are non-smoking",
        "Age Requirement: Guests must be 18+ to check in",
        "Additional Guests: Maximum occupancy as specified per room type",
        "Damage Policy: Guests are responsible for any damages to hotel property"
    ]
}

bookings = []

@app.route("/")
def index():
  return render_template("index.html")

app.route("/api/rooms/featured")
def get_featured_rooms():
  featured_rooms = [room for room in rooms_data if room.get("featured", False)]
  return jsonify(featured_rooms)