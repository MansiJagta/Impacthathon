from fastapi import FastAPI
from services.model import train_model
from routers import claims, reviewer

app = FastAPI(title="Claims AI System")

# Global ML model
model = None


@app.on_event("startup")
def startup_event():
    global model
    model = train_model()


# Make model accessible inside routers
claims.set_model_reference(lambda: model)

# Include routers
app.include_router(claims.router)
app.include_router(reviewer.router)
