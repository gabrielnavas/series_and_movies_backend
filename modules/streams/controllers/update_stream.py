from datetime import datetime
from fastapi import APIRouter, status, Response
from pydantic import BaseModel


from modules.streams.models import Stream, Platform

router = APIRouter()


class StreamBody(BaseModel):
    name: str
    time_paused: str
    platform_id: int


@router.put("/api/stream/{stream_id}")
async def get_stream(response: Response, stream_body: StreamBody, stream_id: int):

    def str_to_time(time_paused: str) -> datetime.time:
        time_paused = time_paused.replace(':', '-')
        return datetime.strptime(time_paused, '%H-%M-%S').time()

    def fetch_stream_exists(stream_id: int):
        try:
            streams = Stream.select().where(Stream.id == stream_id)
            return streams[0]
        except:
            return None

    def fetch_platform(platform_id: int):
        try:
            platforms = Platform.select().where(Platform.id == platform_id)
            return platforms[0]
        except:
            return None

    def update_stream(stream_found: Stream, platform_found: Platform, stream_update: StreamBody) -> int:
        stream_found.name = stream_update.name
        stream_found.time_paused = str_to_time(stream_update.time_paused)
        stream_found.platform = Platform.get(stream_update.platform_id)
        stream_count_updated = stream_found.save()
        return stream_count_updated

    try:
        platform_found = fetch_platform(stream_body.platform_id)
        if platform_found == None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'platform not exist'}

        stream_found = fetch_stream_exists(stream_id=stream_id)
        if stream_found == None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'stream not exist'}

        count_update = update_stream(
            stream_found=stream_found, platform_found=platform_found, stream_update=stream_body)
        if count_update == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'stream not updated'}

        response.status_code = status.HTTP_204_NO_CONTENT
    except Exception as ex:
        print(ex)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
