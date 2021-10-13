from typing import Optional
from fastapi import APIRouter, status, Response
from playhouse.shortcuts import model_to_dict


from modules.streams.models import Stream

router = APIRouter()


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
        streams = [model_to_dict(stream) for stream in streams]
        response.status_code = status.HTTP_200_OK
        return {"streams": streams}
    except Exception as ex:
        print(ex)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
