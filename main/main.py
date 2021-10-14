from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from main.database_config import DatabaseConfig

from modules.streams.controllers.create_stream import router as router_create_stream
from modules.streams.controllers.get_streams import router as router_get_streams
from modules.streams.controllers.update_stream import router as router_update_stream
from modules.streams.controllers.delete_stream import router as router_delete_stream

from modules.platforms.controllers.get_platforms import router as router_get_platforms

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
app.include_router(router_create_stream)
app.include_router(router_get_streams)
app.include_router(router_update_stream)
app.include_router(router_delete_stream)


# platforms router
app.include_router(router_get_platforms)


@app.on_event("startup")
async def startup_event():
    database_config = DatabaseConfig()
    database_config.handle()


@app.get("/")
async def root():
    return {
        "hello": "world2",
    }
