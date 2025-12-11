from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Room(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  description = db.Column(db.Text, nullable=False)
  price = db.Column(db.Float, nullable=False)
  image_url = db.Column(db.String(256))
  capacity = db.Column(db.Integer, nullable=False)
  size = db.Column(db.String(64))
  amenities = db.Column(db.Text) # Store as comma-separated string
  featured = db.Column(db.Boolean, default=False)
  
  bookings = db.relationship("Booking", backref="room", lazy=True)
  
class Booking(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
  first_name = db.Column(db.String(64), nullable=False)
  last_name = db.Column(db.String(64), nullable=False)
  email = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(32), nullable=False)
  check_in = db.Column(db.Date, nullable=False)
  check_out = db.Column(db.Date, nullable=False)
  guests = db.Column(db.Integer, nullable=False)
  payment_method = db.Column(db.String(32))
  payment_status = db.Column(db.String(32), default="pending")
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  total_amount = db.Column(db.Float)

class MenuItem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  description = db.Column(db.Text, nullable=False)
  price = db.Column(db.Float, nullable=False)
  category = db.Column(db.String(32), nullable=False)
  image_url = db.Column(db.String(256))
  dietary = db.Column(db.String(128))  # comma-separated
  available = db.Column(db.Boolean, default=True)
  
class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, nullable=False)
  password_hash = db.Column(db.Text, nullable=False)
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
    
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)