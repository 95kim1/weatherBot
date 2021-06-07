# weatherBot
univ. project - to make a little bot - weather bot with telegram
-------

## 1. 사용법

1. weatherBot.py의 TOKEN 변수에 텔레그램으로 부터 받은 token을 적어주세요.
2. weatherBot.py를 실행시킵니다.
3. 이제 본인의 telegram bot과 대화를 하여 날씨 정보를 얻을 수 있습니다.

### 대화 사용법

- "도움", "도움말"을 통해 어떤 방식으로 입력해야 하는 지 알 수 있습니다.
- "날씨"를 입력하여 전국의 날씨를 얻을 수 있습니다.
- "시/도", "시/도 시/군/구", "시/군/구" 3가지의 입력을 통해 해당 지역의 날씨 정보를 얻을 수 있습니다.
- "시/도"의 경우 도움말에 나온 지역만 정보를 얻을 수 있습니다.

## 2. bot을 위해 사용한 것들

1. 텔레그램
2. 파이썬
3. 라이브러리
4. 엑셀
   - "시/군/구"와 "시/도"를 맵핑할 때 사용   
5. 웹페이지
   - https://www.kweather.co.kr/forecast/forecast_lifestyle.html
   - https://www.kweather.co.kr/forecast/forecast_lifestyle_detail.html

## 3. 라이브러리

~~~
- 라이브러리 -
0. telepot
  텔레그램 봇 이용 api
1. selenium
  웹페이지에서 option을 선택하여 원하는 부분만 바꾸어 정보를 얻어야 하는 경우 bs4만으로 정보를 얻을 수 없어서 사용.
2. bs4 (BeautifulSoup)
  웹페이지를 scrapping하기
3. pandas
  엑셀 파일 읽기
~~~

