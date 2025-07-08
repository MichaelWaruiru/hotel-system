from flask import Flask, request, jsonify, render_template
from datetime import datetime
from config import Config
from flask_migrate import Migrate
from models import db, Booking, MenuItem, Room


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

@app.cli.command("init-db")
def init_db():
    """Create database tables."""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created!")


@app.route("/")
def index():
  return render_template("index.html")

@app.route("/api/rooms/featured")
def get_featured_rooms():
  featured_rooms = Room.query.filter_by(featured=True).all()
  return jsonify([serialize_room(room) for room in featured_rooms])

@app.route("/api/rooms")
def get_all_rooms():
  rooms = Room.query.all()
  return jsonify([serialize_room(room) for room in rooms])

@app.route("/api/rooms/<int:room_id>")
def get_room(room_id):
  room = Room.query.get(room_id)
  if room:
    return jsonify(serialize_room(room))
  return jsonify({"error": "Room not found"}), 404

@app.route("/api/menu")
def get_menu():
  menu_items = MenuItem.query.all()
  return jsonify([serialize_menu_item(item) for item in menu_items])

@app.route("/api/menu/category/<category>")
def get_menu_by_category(category):
  items = MenuItem.query.filter_by(category=category).all()
  return jsonify([serialize_menu_item(item) for item in items])

# @app.route("/api/hotel")
# def get_hotel_info():
#     return jsonify(hotel_info)

@app.route("/api/bookings", methods=["POST"])
def create_booking():
  try:
    data = request.get_json()
    required_fields = ["roomId", "firstName", "lastName", "email", "phone", "checkIn", "checkOut", "guests"]
    for field in required_fields:
      if field not in data:
        return jsonify({"error": f"Missing required field {field}"}), 400

      room = Room.query.get(data["roomId"])
      if not room:
        return jsonify({"error": "Room not found"}), 404

      booking = Booking(
        room_id=room.id,
        first_name=data["firstName"],
        last_name=data["lastName"],
        email=data["email"],
        phone=data["phone"],
        check_in=datetime.strptime(data["checkIn"], "%Y-%m-%d"),
        check_out=datetime.strptime(data["checkOut"], "%Y-%m-%d"),
        guests=int(data["guests"]),
        payment_method=data.get("paymentMethod"),
        total_amount=room.price,
        payment_status="pending"
      )
      db.session.add(booking)
      db.session.commit()

      return jsonify(serialize_booking(booking)), 201
  except Exception as e:
      return jsonify({"error": f"Failed to create booking: {str(e)}"})
    
@app.route("/api/bookings/<int:booking_id>")
def get_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
      return jsonify(serialize_booking(booking))
    return jsonify({'error': 'Booking not found'}), 404
  
# Serialization helpers
def serialize_room(room):
  return {
    "id": room.id,
    "name": room.name,
    "description": room.description,
    "price": f"{room.price:.2f}",
    "imageUrl": room.image_url,
    "capacity": room.capacity,
    "size": room.size,
    "amenities": room.amenities.split(",") if room.amenities else [],
    "featured": room.featured
  }

def serialize_booking(booking):
  return {
    "id": booking.id,
    "roomId": booking.room_id,
    "firstName": booking.first_name,
    "lastName": booking.last_name,
    "email": booking.email,
    "phone": booking.phone,
    "checkIn": booking.check_in.strftime("%Y-%m-%d"),
    "checkOut": booking.check_out.strftime("%Y-%m-%d"),
    "guests": booking.guests,
    "paymentMethod": booking.payment_method,
    "paymentStatus": booking.payment_status,
    "createdAt": booking.created_at.isoformat(),
    "totalAmount": f"{booking.total_amount:.2f}"
  }

def serialize_menu_item(item):
  return {
    "id": item.id,
    "name": item.name,
    "description": item.description,
    "price": f"{item.price:.2f}",
    "category": item.category,
    "imageUrl": item.image_url,
    "dietary": item.dietary.split(",") if item.dietary else [],
    "available": item.available
  }

if __name__ == "main":
    app.run(port=5000, debug=True)