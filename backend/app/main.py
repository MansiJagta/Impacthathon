from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, user_routes
from app.database import user_collection

app = FastAPI(
    title="Authentication Service",
    description="FastAPI Authentication & Authorization with MongoDB",
    version="1.0.0"
)

# -----------------------------
# CORS Configuration
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Include Routers
# -----------------------------
app.include_router(auth_routes.router, tags=["Authentication"])
app.include_router(user_routes.router, tags=["Users"])


# -----------------------------
# Root Route
# -----------------------------
@app.get("/")
async def root():
    return {"message": "Auth Service Running 🚀"}


# -----------------------------
# Create Unique Email Index
# -----------------------------
@app.on_event("startup")
async def startup_db():
    await user_collection.create_index("email", unique=True)