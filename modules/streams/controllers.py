from datetime import datetime
from typing import Optional
from fastapi import APIRouter, status, Response, status
from pydantic import BaseModel

from modules.streams.models import Stream

router = APIRouter()


class StreamBody(BaseModel):
    name: str
    time_paused: datetime.time


@router.post("/api/streams")
async def create_stream(stream_body: StreamBody, response: Response):
    try:
        stream = Stream.create(
            name=stream_body.name
        )
        return {"my stream": stream.__data__}
    except Exception as ex:
        print(ex)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}


@router.get("/api/streams")
async def get_streams(page: Optional[int] = 0, count_of_page: Optional[int] = 10):
    try:
        streams = (
            Stream
            .select()
            .order_by(Stream.name.desc())
            .paginate(page, count_of_page)
            .dicts()
        )
        return {"streams": streams}
    except Exception as ex:
        print(ex)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
