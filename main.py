"""
TradeScope — FastAPI Backend
Run with: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from routes.analyze import router as analyze_router
from routes.watchlist import router as watchlist_router
from routes.zerodha import router as zerodha_router

app = FastAPI(
    title="TradeScope API",
    description="Technical signal analyzer for NSE/BSE stocks",
    version="1.0.0"
)

# ── CORS: allow your frontend to call this API ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://keen-hamster-2193ed.netlify.app",   # your live Netlify site
        "http://localhost:5500",                      # local dev
        "http://localhost:3000",                      # local dev alt
        "null",                                       # file:// opened locally
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register route groups ──
app.include_router(analyze_router, prefix="/api")
app.include_router(watchlist_router, prefix="/api")
app.include_router(zerodha_router, prefix="/api")


@app.get("/")
def root():
    return {"status": "ok", "message": "TradeScope API is running"}


@app.get("/api/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)def root():
    return {"status": "ok", "message": "TradeScope API is running"}


@app.get("/api/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
