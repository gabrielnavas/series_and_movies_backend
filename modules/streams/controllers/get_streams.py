from typing import Optional
from fastapi import APIRouter, status, Response, Request
from playhouse.shortcuts import model_to_dict


from modules.shared.infra.errors_handler import LogHttpErrorHandler
from modules.streams.models import Stream

router = APIRouter()


@router.get("/api/stream")
async def get_streams(request: Request, response: Response, platform_id: int, platform_name: Optional[str] = '', page: Optional[int] = 0, count_of_page: Optional[int] = 10):
    def get_all_streams_from_platform(platform_id: int, platform_name: Optional[str] = '', page: Optional[int] = 0, count_of_page: Optional[int] = 10):
        try:
            if len(platform_name) == 0:
                streams = (
                    Stream
                    .select()
                    .order_by(Stream.name.desc())
                    .paginate(page, count_of_page)
                    .where(Stream.platform == platform_id)
                )
            else:
                streams = (
                    Stream
                    .select()
                    .order_by(Stream.name.desc())
                    .paginate(page, count_of_page)
                    .where(
                        (Stream.platform == platform_id) &
                        (Stream.name.contains(platform_name))
                    )
                )
            return streams
        except Exception as ex:
            return []

    try:
        streams = get_all_streams_from_platform(platform_id=platform_id, platform_name=platform_name,
                                                page=page, count_of_page=count_of_page)
        response.status_code = status.HTTP_200_OK
        if len(streams) == 0:
            return {"streams": []}
        streams = [model_to_dict(stream) for stream in streams]
        return {"streams": streams}
    except Exception as ex:
        error_handler = LogHttpErrorHandler()
        error_handler.handle(
            request=request,
            response=response,
            error=e
        )
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
