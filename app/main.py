from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI()

# Allow CORS for the frontend
origins = [
    "http://localhost:3000",
    "https://2024-messidepaul-front.vercel.app",
    "https://2024-huidobro-front.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    # Allow all headers (Authorization, Content-Type, etc.)
    allow_headers=["*"],
)

# Your routes here...
app.include_router(router)
