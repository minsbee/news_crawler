import requests
import time
from bs4 import BeautifulSoup

def get_news_urls(code, page_num, date):
    url_list = []

    for i in range(1, page_num + 1):
        url = f'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1={code}&date={date}&page={i}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        news = requests.get(url, headers=headers)
        soup = BeautifulSoup(news.content, 'html.parser')

        # 선택자 확인
        news_list = soup.select('.newsflash_body .type06_headline li dl')
        news_list.extend(soup.select('.newsflash_body .type06 li dl'))

        # 요소 확인 및 URL 추출
        for line in news_list:
            a_tag = line.find('a')  # <a> 태그 찾기
            if a_tag:  # <a> 태그가 존재할 때만 실행
                url_list.append(a_tag.get('href'))

        time.sleep(1)

    return url_list


news_result = get_news_urls('001', 1, '20241212')
print(news_result)
