from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from starlette.middleware.cors import CORSMiddleware

from app.api.users import user
from app.api.rules import router as rules
from app.api.sender import router as senders
import threading
from app.core.db import engine, Base
from app.service.worker import start_worker

app = FastAPI(title="Email Forwarder")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://v0-next-js-frontend-seven-flame.vercel.app",
        "http://localhost:3000",
    "https://v0.app",
        "https://*.v0.app"

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    try:
        # Test DB connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # <-- wrap string with text()
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        print("✅ Database connected and tables ready")
    except OperationalError as e:
        print("❌ Failed to connect to database:", e)
        raise e  # Fail startup if DB is not reachable

# Include routes
app.include_router(user, prefix="/api")
app.include_router(rules, prefix="/api")
app.include_router(senders, prefix="/api")

# Start worker in background
threading.Thread(target=start_worker, daemon=True).start()
