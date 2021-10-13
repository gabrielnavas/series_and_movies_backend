from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from main.database_config import DatabaseConfig

from modules.streams.controllers import router as router_streams
from modules.platforms.controllers import router as router_platforms

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://series-and-movies-frontend-2ngyhty0p-gabnavas.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# streams router
app.include_router(router_streams)
app.include_router(router_platforms)


@app.on_event("startup")
async def startup_event():
    database_config = DatabaseConfig()
    database_config.handle()


@app.get("/")
async def root():
    return {
        "hello": "world",
    }
