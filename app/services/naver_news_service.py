import asyncio
import httpx
from datetime import datetime
from bs4 import BeautifulSoup
from app.config import logger

nowtime = datetime.now().strftime("%Y%m%d")


async def get_naver_news_urls(code=101, page_num=1, date=nowtime):
    naver_news_category_code = code
    page_number = page_num
    set_date = date
    url_list = []

    try:
        logger.info(
            f"🔔 뉴스 URL 수집 시작 - 카테고리: {naver_news_category_code}, 페이지: {page_number}, 날짜: {set_date}"
        )

        async with httpx.AsyncClient(follow_redirects=True) as client:
            for i in range(1, page_number + 1):
                try:
                    # 구 네이버 경제 경로
                    # url = f'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1={naver_news_category_code}&date={set_date}&page={i}'
                    # 새 네이버 글로벌 경제 속보 경로 (262 = 글로벌 경제 코드)
                    url = f"https://news.naver.com/breakingnews/section/{naver_news_category_code}/262?date={set_date}"
                    headers = {
                        "User-Agent": (
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/91.0.4472.124 Safari/537.36"
                        )
                    }

                    logger.info(
                        f"📝 요청 URL: {url}, 페이지: {i}/{page_number}"
                    )
                    response = await client.get(url, headers=headers)
                    if response.status_code != 200:
                        logger.error(
                            f"❌ 페이지 {i} 요청 실패: HTTP {response.status_code}"
                        )
                        continue

                    soup = BeautifulSoup(response.content, "html.parser")
                    # 구 네이버 DOM 구조
                    # news_list = soup.select('.newsflash_body .type06_headline li dl')
                    # news_list.extend(soup.select('.newsflash_body .type06 li dl'))

                    news_list = soup.select(
                        ".section_article .sa_list .sa_item .sa_item_inner .sa_item_flex .sa_text"
                    )
                    logger.debug(
                        f"📝 페이지 {i}에서 {len(news_list)}개의 뉴스 항목 발견"
                    )

                    for line in news_list:
                        a_tag = line.find("a")
                        if a_tag:
                            news_url = a_tag.get("href")
                            url_list.append(news_url)

                    # 요청 간에 약간의 지연
                    await asyncio.sleep(1)

                except Exception as e:
                    logger.error(f"❌ 페이지 {i} 처리 중 오류 발생: {e}")
                    continue

        logger.info(
            f"✅ 뉴스 URL 수집 완료 - 총 {len(url_list)}개의 URL 수집됨"
        )
        return url_list

    except Exception as e:
        logger.error(f"❌ 뉴스 URL 수집 중 예외 발생: {e}")
        return url_list


# 뉴스 URL 내부의 상세 내용을 가져오는 함수
async def get_naver_news_content(url: str, client: httpx.AsyncClient):
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
        # 제목 추출: h2 태그 내부의 span 태그 선택 (양쪽 공백 제거)
        title_tag = soup.select_one("h2 > span")
        title = title_tag.get_text(strip=True) if title_tag else "제목 없음"

        article = soup.find("article", {"id": "dic_area"})
        content = article.get_text(strip=True) if article else "본문 없음"

        news_data = {
            "url": url,
            "title": title,
            "content": content,
        }
        logger.debug(f"📝 뉴스 상세 내용 추출 성공: {url}")
        return news_data

    except Exception as e:
        logger.error(f"❌ 뉴스 내용 요청 중 오류 발생: {url} - {e}")
        return None


async def get_naver_news_contents():
    news_urls = await get_naver_news_urls()
    news_contents = []
    async with httpx.AsyncClient() as client:
        tasks = [get_naver_news_content(url, client) for url in news_urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                logger.error(
                    f"❌ get_naver_news_content 작업에서 예외 발생: {result}"
                )
            elif result:
                news_contents.append(result)
    logger.info(
        f"✅ 뉴스 상세 내용 수집 완료 - 총 {len(news_contents)}개의 뉴스 내용 수집됨"
    )
    return news_contents
