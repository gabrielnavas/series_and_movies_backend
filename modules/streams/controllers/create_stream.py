from datetime import datetime
from fastapi import APIRouter, status, Response
from pydantic import BaseModel
from playhouse.shortcuts import model_to_dict


from modules.streams.models import Stream, Platform

router = APIRouter()


class StreamBody(BaseModel):
    name: str
    time_paused: str
    platform_id: int


@router.post("/api/stream")
async def create_stream(stream_body: StreamBody, response: Response):
    def str_to_time(time_paused: str) -> datetime.time:
        time_paused = time_paused.replace(':', '-')
        return datetime.strptime(time_paused, '%H-%M-%S').time()

    def get_platform(platform_id: int):
        try:
            return Platform.get(Platform.id == platform_id)
        except Exception as ex:
            print(ex)
            return None

    def get_stream(stream_body: StreamBody) -> bool:
        try:
            return Stream.get((Stream.name == stream_body.name) &
                              (Stream.platform == stream_body.platform_id))
        except Exception as ex:
            print(ex)
            return None

    try:
        platform_found = get_platform(
            platform_id=stream_body.platform_id
        )
        if platform_found == None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'platform does not exist'}

        if get_stream(stream_body=stream_body) != None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'Stream já existe na plataforma.'}

        stream = Stream.create(
            name=stream_body.name,
            time_paused=str_to_time(stream_body.time_paused),
            platform=platform_found
        )
        stream = model_to_dict(stream)
        response.status_code = status.HTTP_201_CREATED
        return {"stream": stream}
    except Exception as ex:
        print(ex)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
