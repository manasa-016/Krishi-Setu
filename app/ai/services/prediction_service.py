from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Harvest, Demand, Transaction

def calculate_crop_demand(db: Session, crop_type: str):
    # 1. Gather raw data from the DB
    demand_posts = db.query(Demand).filter(Demand.crop_type.ilike(f"%{crop_type}%")).filter(Demand.status == "open").count()
    harvest_supply = db.query(Harvest).filter(Harvest.crop_type.ilike(f"%{crop_type}%")).filter(Harvest.status == "available").count()
    transactions_count = db.query(Transaction).join(Harvest, Transaction.harvest_id == Harvest.id).filter(Harvest.crop_type.ilike(f"%{crop_type}%")).count()
    
    # Calculate Average Transaction Price to predict future price
    avg_price_query = db.query(func.avg(Harvest.price_per_kg)).join(Transaction, Harvest.id == Transaction.harvest_id).filter(Harvest.crop_type.ilike(f"%{crop_type}%")).scalar()
    
    # If no past transactions exist for this crop, fallback to current supply average pricing
    if not avg_price_query:
        avg_price_query = db.query(func.avg(Harvest.price_per_kg)).filter(Harvest.crop_type.ilike(f"%{crop_type}%")).filter(Harvest.status == "available").scalar()
    
    base_price = float(avg_price_query) if avg_price_query else 0.0

    # 2. Demand Score Formula
    demand_score = (demand_posts * 2) + transactions_count - harvest_supply
    
    # Floor the score at 0
    demand_score = max(0, demand_score)

    # 3. Market Insight Labels
    if demand_score < 10:
        trend = "Low demand"
        recommendation = "Hold harvest if possible"
    elif demand_score < 20:
        trend = "Medium demand"
        recommendation = "Steady market, sell at average price"
    else:
        trend = "High demand"
        recommendation = "Strong market, sell within next 3 days for premium"

    # 4. Expected Price
    # Expected price goes up as demand score gets higher. 
    expected_price = base_price * (1 + (demand_score / 50))

    return {
        "crop": crop_type,
        "demand_score": demand_score,
        "demand_posts": demand_posts,
        "harvest_supply": harvest_supply,
        "transactions_completed": transactions_count,
        "current_avg_price": round(base_price, 2),
        "expected_price": round(expected_price, 2),
        "trend": trend,
        "recommendation": recommendation
    }
