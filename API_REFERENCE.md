# Krishi-Setu Backend API Reference

This document serves as the exact API contract for the Front-End team to integrate the location, marketplace, and AI intelligence systems.

## 📍 1. Location Intelligence System

### Update User Location
Send the user's current GPS coordinates.
- **Endpoint**: `POST /location/update`
- **Body**:
  ```json
  {
    "latitude": 12.9716,
    "longitude": 77.5946
  }
  ```
- **Response**:
  ```json
  {
    "message": "Location updated successfully"
  }
  ```

### Get Market Map (Full Region)
Retrieves all grouped map point data within a given radius. Use this to render all markers at once on Leaflet.
- **Endpoint**: `GET /location/market-map?lat=12.97&lng=77.59&radius=20`
- **Response**:
  ```json
  {
    "farmers": [
      {
        "id": "uuid",
        "name": "Ramesh",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "distance_km": 3.2
      }
    ],
    "vendors": [...],
    "harvests": [
      {
        "farmer_id": "uuid",
        "farmer_name": "Ramesh",
        "crop_type": "tomato",
        "quantity": 200,
        "price_per_kg": 22.0,
        "latitude": 12.9716,
        "longitude": 77.5946,
        "distance_km": 3.2
      }
    ],
    "demands": [
      {
        "vendor_id": "uuid",
        "vendor_name": "Suresh Stores",
        "crop_type": "tomato",
        "required_quantity": 500,
        "offered_price": 25.0,
        "latitude": 12.9750,
        "longitude": 77.5910,
        "distance_km": 4.1
      }
    ]
  }
  ```

---

## 🧠 2. AI Intelligence System

### Crop Demand Prediction
Provides forecasted demand scores, insights, and expected price calculations based on live supply vs demand. Display this when a user selects a specific crop.
- **Endpoint**: `GET /ai/crop-demand?crop=tomato`
- **Response**:
  ```json
  {
    "crop": "tomato",
    "demand_score": 1,
    "demand_posts": 1,
    "harvest_supply": 1,
    "transactions_completed": 0,
    "current_avg_price": 22.0,
    "expected_price": 22.44,
    "trend": "Low demand",
    "recommendation": "Hold harvest if possible"
  }
  ```

### Regional Crop Heatmap
Aggregates exact coordinates into ~1.1km grid cells with calculated heatmap intensity scores. Pass this data directly to `L.heatLayer()`.
- **Endpoint**: `GET /ai/heatmap?crop=tomato`
- **Response**:
  ```json
  {
    "crop": "tomato",
    "heatmap": [
      {
        "lat": 12.97,
        "lng": 77.59,
        "demand_score": 1,
        "demand_count": 1,
        "harvest_count": 1
      }
    ]
  }
  ```
