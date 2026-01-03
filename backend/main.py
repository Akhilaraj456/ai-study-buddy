from fastapi import FastAPI
from routes.health import router as health_router
from routes.upload import router as upload_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI Study Buddy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health server checker
app.include_router(health_router)

# Extraction router
app.include_router(upload_router)

