from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from api.limiter import limiter
from api.routes import router as api_router

app = FastAPI()

# Attach limiter to app state
app.state.limiter = limiter

# Register exception handler
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "RAG API is live"}
