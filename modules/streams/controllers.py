from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, status, Response, status
from pydantic import BaseModel


from modules.streams.models import Stream

router = APIRouter()


class StreamBody(BaseModel):
    name: str
    time_paused: str


@router.post("/api/stream")
async def create_stream(stream_body: StreamBody, response: Response):

    # TODO
    # Reafactory to class
    def str_to_time(time_paused: str) -> datetime.time:
        return datetime.strptime(time_paused, '%H-%M-%S').time()

    def stream_already_exists(stream_body: StreamBody) -> bool:
        stream_found = Stream.select().where(Stream.name == stream_body.name)
        if len(stream_found) > 0:
            return True
        return False

    def stream_create(stream_body: StreamBody):
        stream_created = Stream.create(
            name=stream_body.name,
            time_paused=str_to_time(stream_body.time_paused)
        )
        return stream_created

    try:
        if stream_already_exists(stream_body=stream_body):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'stream has exists'}

        stream = stream_create(stream_body=stream_body)
        response.status_code = status.HTTP_201_CREATED
        return {"stream": stream.__data__}
    except Exception as ex:
        print(ex)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}


@router.get("/api/stream")
async def get_streams(response: Response, page: Optional[int] = 0, count_of_page: Optional[int] = 10):

    def get_all_streams(page: Optional[int] = 0, count_of_page: Optional[int] = 10):
        streams = (
            Stream
            .select()
            .order_by(Stream.name.desc())
            .paginate(page, count_of_page)
        )
        return streams

    try:
        streams = get_all_streams(page=page, count_of_page=count_of_page)
        streams = [stream.__data__ for stream in streams]
        return {"streams": streams}
    except Exception as ex:
        print(ex)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}


@router.put("/api/stream/{stream_id}")
async def get_streams(response: Response, stream_body: StreamBody, stream_id: int):

    def get_stream(stream_id: int):
        stream_found = (
            Stream
            .select()
            .where(Stream.id == stream_id)
        )
        if len(stream_found) > 0:
            return stream_found[0]
        return None

    def update_stream(stream: Stream, stream_id: int) -> int:
        stream_count_updated = (
            Stream
            .update(
                name=stream.name,
                time_paused=stream.time_paused
            )
            .where(Stream.id == stream_id)
        ).execute()
        return stream_count_updated

    try:
        stream_found = get_stream(stream_id)
        if not stream_found:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'stream not exists'}

        count_update = update_stream(stream_body, stream_id)
        if count_update == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'stream not updated'}

        response.status_code = status.HTTP_204_NO_CONTENT
    except Exception as ex:
        print(ex)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}


@router.delete("/api/stream/{stream_id}")
async def get_streams(response: Response, stream_id: int):

    def get_stream(stream_id: int):
        stream_found = (
            Stream
            .select()
            .where(Stream.id == stream_id)
        )
        if len(stream_found) > 0:
            return stream_found[0]
        return None

    def delete_stream(stream_id: int) -> int:
        count_deleted = (
            Stream
            .delete()
            .where(Stream.id == stream_id)
        ).execute()
        return count_deleted

    try:
        stream_found = get_stream(stream_id)
        if not stream_found:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'stream not exists'}

        count_deleted = delete_stream(stream_id)
        if count_deleted == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'stream not deleted'}

        response.status_code = status.HTTP_204_NO_CONTENT
    except Exception as ex:
        print(ex)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
