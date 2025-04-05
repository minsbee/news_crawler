from fastapi import APIRouter
from app.services import get_yh_finance_news_contents

router = APIRouter()


@router.get("/get-yh-finance-news")
async def get_yh_finance_news_api():
    yh_finance_news_result = await get_yh_finance_news_contents()

    return {"message": yh_finance_news_result}
