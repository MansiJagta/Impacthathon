from fastapi import FastAPI

from app.api.routes.underwriter import router as underwriter_router

app = FastAPI(title="Insurance Claims Backend")

app.include_router(underwriter_router)


@app.get("/")
async def health_check() -> dict:
    return {"status": "ok"}
