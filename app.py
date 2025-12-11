from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from datetime import datetime
from config import Config
from flask_migrate import Migrate
from models import db, Booking, MenuItem, Room, User
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from werkzeug.security import check_password_hash
from wtforms.fields import PasswordField
import os


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = "admin_login"


@app.cli.command("init-db")
def init_db():
    """Create database tables."""
    with app.app_context():
        db.create_all()
        print("Database tables created!")


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


# Admin auth
class MyAdminIndexView(AdminIndexView):
  @expose("/")
  def index(self):
    if not current_user.is_authenticated:
      return redirect(url_for("admin_login"))
    return super().index()
  
  def is_accessible(self):
    return current_user.is_authenticated
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for("admin_login"))
  
class SecureModelView(ModelView):
  def is_accessible(self):
    return current_user.is_authenticated
  
  def inaccessible_callback(self):
    return redirect(url_for("admin_login"))
  
class UserModelView(SecureModelView):
  form_extra_fields = {
    "password": PasswordField("Password")
  }
  
  form_columns = ["username", "password"] # Only show username and password fields
  
  def on_model_change(self, form, model, is_created):
    # Hash only if admin entered a password
    if form.password.data:
      model.set_password(form.password.data)
  
  
# Image upload helpers
def room_image_path(file_data):
  return f"images/rooms/{file_data.filename}"

def menu_image_path(file_data):
  return f"images/menu/{file_data.filename}"


class RoomModelView(SecureModelView):
  column_searchable_list = ["name", "description"]
  column_filters = ["featured"]
  form_overrides = dict(image_url=ImageUploadField)
  form_args = dict(
    image_url=dict(
      label="Room Image",
      base_path=os.path.join(os.path.dirname(__file__), "static/images/rooms"),
      relative_path="images/rooms/",
      allow_overwrite=False,
      max_size=(800, 600, True)
    )
  )
  form_columns = ["name", "description", "price", "image_url", "capacity", "size", "amenities", "featured"]


class MenuItemModelView(SecureModelView):
  column_searchable_list = ["name", "description", "category"]
  column_filters = ["category", "available"]
  form_overrides = dict(image_url=ImageUploadField)
  form_args = dict(
    image_url=dict(
      label="Menu Image",
      base_path=os.path.join(os.path.dirname(__file__), "static/images/menu"),
      relative_path="images/menu",
      allow_overwrite=False,
      max_size=(800, 600, True)
    )
  )
  form_columns = ["name", "description", "price", "category", "image_url", "dietary", "available"]
  
admin = Admin(
  app,
  name="Park Palace Admin",
  # template_mode="bootstrap4",
  index_view=MyAdminIndexView()
)
admin.add_view(RoomModelView(Room, db.session, category="Hotel"))
admin.add_view(MenuItemModelView(MenuItem, db.session, category="Hotel"))
admin.add_view(SecureModelView(Booking, db.session, category="Hotel"))
admin.add_view(UserModelView(User, db.session, category="Users"))

# Admin login/logout routes
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
  if current_user.is_authenticated:
    return redirect("/admin")
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
      login_user(user)
      flash("Logged in successfully", "success")
      return redirect("/admin")
    else:
      flash("Invalid username or password", "danger")
      return render_template("admin.html")
  return render_template("admin.html")

@app.route("/admin/logout")
def admin_logout():
  logout_user()
  flash("Logged out.", "info")
  return redirect(url_for("admin_login"))

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

@app.route("/api/hotel")
def get_hotel_info():
    hotel_info = {
        "name": "Park Palace Hotel",
        "address": "123 Bor, Jonglei State, South Sudan",
        "phone": "+211-712-345-678",
        "email": "info@parkpalacehotel.com",
        "description": "A luxurious hotel offering the best amenities and services.",
        
        # Add fields frontend requires
        "checkInTime": "2:00 PM",
        "checkOutTime": "11:00 AM",
        "amenities": [
            "Free Wi-Fi",
            "Swimming Pool",
            "Spa & Wellness Center",
            "Fitness Center",
            "24/7 Room Service",
            "Restaurant & Bar",
            "Airport Shuttle"
        ],
        "policies": [
            "No smoking inside the rooms",
            "Pets allowed upon request",
            "Valid ID required at check-in",
            "Early check-in subject to availability"
        ]
    }
    return jsonify(hotel_info)

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

if __name__ == "__main__":
    app.run(port=5000, debug=True)