from fastapi import APIRouter
from app.services import get_naver_news_contents

router = APIRouter()


@router.get("/get-naver-news")
async def get_naver_news_api():
    naver_news_result = await get_naver_news_contents()

    return {"message": naver_news_result}
