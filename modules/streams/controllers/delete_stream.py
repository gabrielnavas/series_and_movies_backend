from fastapi import APIRouter, status, Response, Request


from modules.shared.infra.errors_handler import LogHttpErrorHandler
from modules.streams.models import Stream

router = APIRouter()


@router.delete("/api/stream/{stream_id}")
async def delete_stream(request: Request, response: Response, stream_id: int):

    def get_stream(stream_id: int):
        try:
            stream = Stream.select().where(Stream.id == stream_id)
            return stream[0]
        except:
            return None

    def delete_stream(stream_id: int) -> int:
        try:
            Stream.delete().where(Stream.id == stream_id).execute()
        except:
            raise Exception('stream not deleted')

    try:
        stream_found = get_stream(stream_id)
        if stream_found == None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'stream not exists'}

        count_deleted = delete_stream(stream_id)
        if count_deleted == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": 'stream not deleted'}

        response.status_code = status.HTTP_204_NO_CONTENT
    except Exception as ex:
        error_handler = LogHttpErrorHandler()
        error_handler.handle(
            request=request,
            response=response,
            error=e
        )
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
