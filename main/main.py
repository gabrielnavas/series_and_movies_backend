from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.streams.controllers import router as router_streams

app = FastAPI()

origins = [
    "http://localhost:3000",
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


@app.on_event("startup")
async def startup_event():
    from main.init_tables_database import init_tables
    # from main.init_dev_data import init_dev_data

    init_tables()


@app.get("/")
async def root():

    import os
    return {
        "01": os.environ['ENV'],
    }
