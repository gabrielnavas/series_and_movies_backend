from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, status, Response
from pydantic import BaseModel


from modules.streams.models import Stream, Platform

router = APIRouter()


class StreamBody(BaseModel):
    name: str
    time_paused: str
    platform_id: int


@router.post("/api/stream")
async def create_stream(stream_body: StreamBody, response: Response):

    def str_to_time(time_paused: str) -> datetime.time:
        return datetime.strptime(time_paused, '%H-%M-%S').time()

    def fetch_platform_exists(platform_id: int):
        platform_founds = Platform.select().where(Platform.id == platform_id)
        return platform_founds[0] if len(platform_founds) > 0 else None

    def stream_already_exists(stream_body: StreamBody) -> bool:
        stream_founds = Stream.select().where(Stream.name == stream_body.name)
        return len(stream_founds) > 0

    def stream_create(stream_body: StreamBody, platform_name):
        return stream_created

    try:
        platform_found = fetch_platform_exists(
            platform_id=stream_body.platform_id
        )
        if platform_found == None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'platform does not exist'}

        if stream_already_exists(stream_body=stream_body):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'stream already exists'}

        stream = stream_created = Stream.create(
            name=stream_body.name,
            time_paused=str_to_time(stream_body.time_paused),
            platform=platform_found
        )
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
async def get_stream(response: Response, stream_body: StreamBody, stream_id: int):
    def fetch_stream_exists(stream_id: int):
        stream_found = (
            Stream
            .select()
            .where(Stream.id == stream_id)
        )
        return stream_found[0] if len(stream_found) > 0 else None

    def update_stream(stream_found: Stream, stream_update: StreamBody, stream_id: int) -> int:
        stream_found.name = stream_update.name
        stream_found.time_paused = stream_update.time_paused
        stream_found.platform = Platform.get(stream_update.platform_id)
        stream_count_updated = stream_found.save()
        return stream_count_updated

    try:
        stream_found = fetch_stream_exists(stream_id=stream_id)
        if not stream_found:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'stream not exists'}

        count_update = update_stream(
            stream_found=stream_found, stream_update=stream_body, stream_id=stream_id)
        if count_update == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'stream not updated'}

        response.status_code = status.HTTP_204_NO_CONTENT
    except Exception as ex:
        print(ex)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}


@router.delete("/api/stream/{stream_id}")
async def get_stream(response: Response, stream_id: int):

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
