from fastapi import FastAPI
from app.config import envs, logger, setup_exception_handlers
from app.routers import (
    authorize_b2_router,
    get_upload_url_b2_router,
    get_naver_news_router,
    get_yh_finance_news_router,
)


def create_app():
    app = FastAPI(title="Fast API")

    logger.info(f"Environment: {envs.CURRENT_ENV}")
    logger.info(f"Log level: {envs.LOG_LEVEL}")

    app.include_router(
        authorize_b2_router,
        prefix="/api",
        tags=["Authorize_b2"],
    )

    app.include_router(
        get_upload_url_b2_router,
        prefix="/api",
        tags=["Get_upload_url_b2"],
    )

    app.include_router(
        get_naver_news_router,
        prefix="/api",
        tags=["Get_naver_news"],
    )
    
    app.include_router(
        get_yh_finance_news_router,
        prefix="/api",
        tags=["Get_yh_finance_news"],
    )

    setup_exception_handlers(app)

    @app.get("/")
    async def root():
        return {"message": "Welcome to Fast API!"}

    return app


app = create_app()

__all__ = [
    "app",
    "envs",
    "logger",
    "setup_exception_handlers",
]
