import sys
import os

# Ensure the root directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine
from sqlalchemy import text
from app.models.user import User
from app.models.harvest import Harvest
from app.models.demand import Demand
from app.models.location_model import UserLocation
from app.core.security import hash_password
from app.ai.services.prediction_service import calculate_crop_demand
from app.services.location_service import (
    find_nearby_users, find_nearby_harvests, find_nearby_demands
)

def run_verification():
    db = SessionLocal()
    
    print("--- 1. ADDING DATABASE INDEXES ---")
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_user_locations_coords ON user_locations(latitude, longitude);"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_harvest_status ON harvests(status);"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_demand_status ON demands(status);"))
            conn.commit()
            print("✅ Database indexes added successfully.")
    except Exception as e:
        print(f"⚠️ Index warning: {e}")

    print("\n--- 2. CREATING TEST DATA ---")
    # Clean previous test data if exists
    test_email_farmer = "farmer_ai_test@example.com"
    test_email_vendor = "vendor_ai_test@example.com"
    
    farmer = db.query(User).filter(User.email == test_email_farmer).first()
    if not farmer:
        farmer = User(name="Test Farmer", email=test_email_farmer, password_hash="dummy_hash", role="farmer", verified=True)
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
        
        loc_f = UserLocation(user_id=farmer.id, latitude=12.9716, longitude=77.5946)
        harvest = Harvest(farmer_id=farmer.id, crop_type="tomato", category="vegetables", quantity=200, price_per_kg=22.0)
        db.add(loc_f)
        db.add(harvest)
        db.commit()

    vendor = db.query(User).filter(User.email == test_email_vendor).first()
    if not vendor:
        vendor = User(name="Test Vendor", email=test_email_vendor, password_hash="dummy_hash", role="vendor", verified=True)
        db.add(vendor)
        db.commit()
        db.refresh(vendor)
        
        loc_v = UserLocation(user_id=vendor.id, latitude=12.9750, longitude=77.5910)
        demand = Demand(vendor_id=vendor.id, crop_type="tomato", category="vegetables", required_quantity=500, offered_price=25.0)
        db.add(loc_v)
        db.add(demand)
        db.commit()
        
    print("✅ Test data created (Farmer, Vendor, Location, Harvest, Demand).")

    print("\n--- 3. VERIFYING MARKET MAP ENDPOINT (INTERNAL) ---")
    market_map = {
        "farmers": find_nearby_users(db, "farmer", 12.97, 77.59, 20.0),
        "vendors": find_nearby_users(db, "vendor", 12.97, 77.59, 20.0),
        "harvests": find_nearby_harvests(db, 12.97, 77.59, 20.0),
        "demands": find_nearby_demands(db, 12.97, 77.59, 20.0)
    }
    print(f"Market Map Farmers: {len(market_map['farmers'])}")
    print(f"Market Map Vendors: {len(market_map['vendors'])}")
    print(f"Market Map Harvests: {len(market_map['harvests'])}")
    print(f"Market Map Demands: {len(market_map['demands'])}")
    if all(isinstance(market_map[k], list) for k in market_map):
        print("✅ Market Map structured data confirmed.")

    print("\n--- 4. VERIFYING AI PREDICTION ENGINE ---")
    ai_result = calculate_crop_demand(db, "tomato")
    print(f"Crop: {ai_result['crop']}")
    print(f"Demand Score: {ai_result['demand_score']}")
    print(f"Trend: {ai_result['trend']}")
    print(f"Expected Price: {ai_result['expected_price']}")
    
    if ai_result['demand_score'] > 0:
        print("✅ AI Prediction engine successfully updated based on test data.")
    else:
        print("⚠️ AI Prediction engine score is still 0.")

if __name__ == "__main__":
    run_verification()
