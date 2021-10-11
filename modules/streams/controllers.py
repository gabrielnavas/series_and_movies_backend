from typing import Optional
from fastapi import APIRouter, status, Response
from pydantic import BaseModel

from modules.streams.models import Stream

router = APIRouter()


@router.get("/api/streams")
async def get_streams(page: Optional[int] = 0, count_of_page: Optional[int] = 10):
    streams = (
        Stream
        .select()
        .order_by(Stream.name.desc())
        .paginate(page, count_of_page)
        .dicts()
    )
    return {"streams": streams}


class StreamBody(BaseModel):
    name: str


@router.post("/api/streams")
async def create_stream(stream_body: StreamBody):
    stream = Stream.create(
        name=stream_body.name
    )
    return {"my stream": stream.__data__}
