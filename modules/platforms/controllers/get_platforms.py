from typing import Optional
from fastapi import APIRouter, status, Response

from modules.platforms.models import Platform

router = APIRouter()


@router.get("/api/platform")
async def get_platforms(response: Response, page: Optional[int] = 0, count_of_page: Optional[int] = 10):

    def get_all_platform(page: Optional[int] = 0, count_of_page: Optional[int] = 10):
        platfoms = (
            Platform
            .select()
            .order_by(Platform.name.desc())
            .paginate(page, count_of_page)
        )
        return platfoms

    try:
        platforms = get_all_platform(page=page, count_of_page=count_of_page)
        platforms = [platform.__data__ for platform in platforms]
        return {"platforms": platforms}
    except Exception as ex:
        print(ex)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
