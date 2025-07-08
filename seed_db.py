from app import app
from models import db, Room, MenuItem

def seed_rooms():
  rooms = [
    Room(
      name="Executive Suite",
      description="Spacious executive suite with panoramic city views, marble bathroom, and premium amenities for the discerning business traveler.",
      price=450.00,
      image_url="images/rooms/executive_suite.jpg",
      capacity=4,
      size="75 sqm",
      amenities="King Bed,City View,Marble Bathroom,Work Desk,Mini Bar,Premium WiFi",
        featured=True
    ),
    Room(
      name="Luxury Ocean View",
      description="Elegant oceanfront suite featuring floor-to-ceiling windows, private balcony, and world-class spa amenities.",
      price=650.00,
      image_url="images/rooms/luxury_ocean_view.jpg",
      capacity=2,
      size="85 sqm",
      amenities="Ocean View,Private Balcony,Jacuzzi,Butler Service,Premium Minibar",
      featured=True
    ),
    Room(
      name="Presidential Suite",
      description="Our crown jewel offering unmatched luxury with separate living areas, private dining room, and dedicated concierge service.",
      price=1200.00,
      image_url="images/rooms/presidential_suite.jpg",
      capacity=6,
      size="150 sqm",
      amenities="Separate Living Room,Private Dining,Concierge Service,Premium Bar,City Panorama",
      featured=True
    )
  ]
  db.session.bulk_save_objects(rooms)
  db.session.commit()

def seed_menu():
  menu_items = [
    MenuItem(
      name="Park Palace Signature Breakfast",
      description="Traditional breakfast with eggs benedict, artisan breads, fresh fruits, and premium coffee",
      price=28.00,
      category="breakfast",
      image_url="images/menu/breakfast_signature.jpg",
      dietary="vegetarian",
      available=True
    ),
    MenuItem(
      name="Healthy Power Bowl",
      description="Quinoa, avocado, fresh berries, nuts, and organic honey drizzle",
      price=24.00,
      category="breakfast",
      image_url="images/menu/power_bowl.jpg",
      dietary="vegan,gluten-free",
      available=True
    ),
    MenuItem(
      name="Mediterranean Grilled Salmon",
      description="Fresh Atlantic salmon with roasted vegetables, quinoa, and lemon herb sauce",
      price=42.00,
      category="lunch",
      image_url="images/menu/grilled_salmon.jpg",
      dietary="gluten-free",
      available=True
    ),
    MenuItem(
      name="Truffle Pasta Primavera",
      description="House-made pasta with seasonal vegetables, truffle oil, and parmesan",
      price=38.00,
      category="lunch",
      image_url="images/menu/truffle_pasta.jpg",
      dietary="vegetarian",
      available=True
    ),
    MenuItem(
      name="Park Palace Wagyu Steak",
      description="Premium A5 Wagyu beef with roasted potatoes, seasonal vegetables, and red wine reduction",
      price=85.00,
      category="dinner",
      image_url="images/menu/wagyu_steak.jpg",
      dietary="",
      available=True
    ),
    MenuItem(
      name="Lobster Thermidor",
      description="Fresh lobster in cognac cream sauce, gruyere cheese, served with herb rice",
      price=68.00,
      category="dinner",
      image_url="images/menu/lobster_thermidor.jpg",
      dietary="gluten-free",
      available=True
    ),
    MenuItem(
      name="Park Palace Signature Cocktail",
      description="Premium gin, elderflower, fresh cucumber, and lime with a touch of rosemary",
      price=18.00,
      category="beverages",
      image_url="images/menu/signature_cocktail.jpg",
      dietary="vegan",
      available=True
    ),
    MenuItem(
      name="Vintage Wine Selection",
      description="Curated selection of premium wines from our cellar, paired with artisan cheeses",
      price=65.00,
      category="beverages",
      image_url="images/menu/vintage_wine.jpg",
      dietary="vegetarian",
      available=True
    ),
    MenuItem(
      name="Chocolate Lava Cake",
      description="Warm chocolate cake with molten center, vanilla ice cream, and berry compote",
      price=16.00,
      category="desserts",
      image_url="images/menu/chocolate_lava_cake.jpg",
      dietary="vegetarian",
      available=True
    ),
    MenuItem(
      name="Tiramisu Royale",
      description="Classic Italian tiramisu with ladyfingers, mascarpone, and espresso",
      price=14.00,
      category="desserts",
      image_url="images/menu/tiramisu_royale.jpg",
      dietary="vegetarian",
      available=True
    ),
    # ...add more as needed
  ]
  db.session.bulk_save_objects(menu_items)
  db.session.commit()

def seed_all():
  with app.app_context():
    seed_rooms()
    seed_menu()
    print("✅ Seeded rooms and menu items.")

if __name__ == "__main__":
  seed_all()