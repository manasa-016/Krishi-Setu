from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.core.database import engine
from app.api.routes.auth import router as auth_router
from app.api.routes.harvest import router as harvest_router
from app.api.routes.demand import router as demand_router
from app.api.routes.transactions import router as transaction_router
from app.api.routes.prices import router as price_router

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(harvest_router)
app.include_router(demand_router)
app.include_router(transaction_router)
app.include_router(price_router)

@app.get("/")
def health_check():
    return {"status": "Agri Tech Backend Running"}