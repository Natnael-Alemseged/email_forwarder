from fastapi import FastAPI
from app.api.users import user
from app.api.rules import router as rules
import threading

from app.core.db import engine,Base
from app.service.worker import start_worker

app = FastAPI(title="Email Forwarder")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(user, prefix="/api")
app.include_router(rules, prefix="/api")

# Start worker in background
threading.Thread(target=start_worker, daemon=True).start()
