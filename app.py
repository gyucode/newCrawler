import requests
from bs4 import BeautifulSoup
import pandas as pd
from src.searchNaver import SearchNaver
import re
import time
import datetime
 

링크수 = 10
검색어 = '출산율'
searchNaver = SearchNaver(검색어)
news_urls = []
titles = []
contents = []
data = []

# part1 네이버뉴스 링크 조회
while len(news_urls) < 링크수:
    url = searchNaver.url
    print(url)

    # requests 모듈을 사용하여 HTML 소스코드 가져오기
    response = requests.get(url)
    html = response.text

    # BeautifulSoup 모듈을 사용하여 HTML 파싱하기
    soup = BeautifulSoup(html, "html.parser")

    # naver new link만 받아오기
    articles = soup.find_all(class_="info",text=['네이버뉴스'] )


    for i in articles:
        link = i['href']
        # 중복된 URL제거
        if link not in news_urls:
            news_urls.append(link)
            print(news_urls)
        if len(news_urls) >= 링크수:
            break
    print(len(news_urls))
    searchNaver.pageUp()

# part2 네이버 기사에 접근해서 제목과 내용 받아오기.
for link in news_urls:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}
    original_html = requests.get(link, headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")
    # 뉴스 제목 가져오기
    title = html.select("div#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
    # list합치기
    title = ''.join(str(title))
    # html태그제거
    pattern1 = '<[^>]*>'
    title = re.sub(pattern=pattern1, repl='', string=title)
    titles.append(title)

    # 뉴스 본문 가져오기
    content = html.select("div#dic_area")

    # 기사 텍스트만 가져오기
    # list합치기
    content = ''.join(str(content))

    # html태그제거 및 텍스트 다듬기
    content = re.sub(pattern=pattern1, repl='', string=content)
    pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
    content = content.replace(pattern2, '')

    contents.append(content)
    data.append([title,link,content])

# part3 엑셀에 데이터 저장

# 추출한 데이터를 pandas DataFrame으로 변환하기
df = pd.DataFrame(data, columns=["제목", "링크", "내용"])

now = datetime.datetime.now()
nowDatetime = now.strftime('%Y%m%d_%H%M%S')
print(nowDatetime)  # 2015-04-19 12:11:32
# 추출한 데이터를 엑셀 파일로 저장하기
df.to_excel(f"news_{nowDatetime}.xlsx", index=False)