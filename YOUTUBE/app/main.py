from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.router import router
from app.db import initialize_database, close_mongo_connection
import os

async def lifespan(app: FastAPI):
    print("Starting up...")
    await initialize_database()
    yield
    print("Shutting down...")
    await close_mongo_connection()

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Add a root endpoint to redirect to the frontend
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/static/index.html")

# Optional: Health check endpoint
@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}

# Serve static files from an absolute path
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")