import asyncio
import httpx
from datetime import datetime
from bs4 import BeautifulSoup
from app.config import logger


async def get_yh_finance_news_urls():
    url_list = []

    try:
        logger.info("🔔 뉴스 URL 수집 시작")

        async with httpx.AsyncClient(follow_redirects=True) as client:
            url = "https://finance.yahoo.com"
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                )
            }

            logger.info(f"📝 요청 URL: {url}")
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                logger.error(f"❌ 요청 실패: HTTP {response.status_code}")
                return url_list

            soup = BeautifulSoup(response.content, "html.parser")
            news_list = soup.select(
                ".hero-latest-news .story-items .story-item .container .content"
            )
            logger.debug(f"📝 {len(news_list)}개의 뉴스 항목 발견")

            for line in news_list:
                a_tag = line.find("a")
                if a_tag:
                    news_url = a_tag.get("href")
                    url_list.append(news_url)

        logger.info(f"✅ 뉴스 URL 수집 완료 - 총 {len(url_list)}개의 URL 수집됨")
        return url_list

    except Exception as e:
        logger.error(f"❌ 뉴스 URL 수집 중 예외 발생: {e}")
        return url_list



# 뉴스 URL 내부의 상세 내용을 가져오는 함수
async def get_yh_finance_news_content(url: str, client: httpx.AsyncClient):
    contents_list = []  # 각 문단의 텍스트를 담을 리스트

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }
    try:
        logger.debug(f"📝 뉴스 상세 내용 요청: {url}")
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            logger.error(
                f"❌ 뉴스 상세 내용 요청 실패: {url} - HTTP {response.status_code}"
            )
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        title_tag = soup.select_one(".cover-title")
        title = title_tag.get_text(strip=True) if title_tag else "제목 없음"

        article_p_tags = soup.select(".atoms-wrapper > p")
        for p_tag in article_p_tags:
            text = p_tag.get_text(strip=True)
            if text:
                contents_list.append(text)

        joined_content = ", ".join(contents_list)

        news_data = {
            "url": url,
            "title": title,
            "content": joined_content,
        }
        logger.debug(f"📝 뉴스 상세 내용 추출 성공: {url}")
        return news_data

    except Exception as e:
        logger.error(f"❌ 뉴스 내용 요청 중 오류 발생: {url} - {e}")
        return None


async def get_yh_finance_news_contents():
    news_urls = await get_yh_finance_news_urls()
    news_contents = []
    async with httpx.AsyncClient() as client:
        tasks = [get_yh_finance_news_content(url, client) for url in news_urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                logger.error(
                    f"❌ get_yh_finance_news_content 작업에서 예외 발생: {result}"
                )
            elif result:
                news_contents.append(result)
    logger.info(
        f"✅ 뉴스 상세 내용 수집 완료 - 총 {len(news_contents)}개의 뉴스 내용 수집됨"
    )
    return news_contents
