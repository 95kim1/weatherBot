from weather.getWeather import *
from telepot.loop import MessageLoop
import telepot

def parse(text):
    text = text.strip().split(" ")
    print(text)
    if text[0] == text[-1]:
        text = [text[0].strip(), ""]
    else:
        # '천안시 동남구/서북구'에 대한 예외처리
        if len(text) > 2 and (text[-1] == "동남구" or text[-1] == "서북구"):
            length = len(text)
            temp = text[-1]
            for i in range(1, length):
                if text[i] != "":
                    text[-1] = text[i]
            text[-1] += " " + temp
        text = [text[0].strip(), text[-1].strip()]
    return text

def help():
    return """
    사용법: 
    1. 기본 :  "날씨"
        - 서해5도, 서울/경기, 강원영서, 강원영동, 충남, 충북, 경북, 울릉, 전남, 전북, 경남, 제주
    
    2. 기본 :  "시/도"
        "시/도"만 입력하는 경우 아래의 지역만 확인할 수 있습니다.
        - 서울, 경기, 강원, 영서, 영동
        - 충북, 충남, 충청도, 경북, 경남, 경상도 
        - 전남, 전북, 전라도, 울릉도, 제주도
    
    3. 자세히 :  "시/도 시/군/구"
        단, 세종특별자치시의 경우 "시/도"만 입력하시면 됩니다.
    
    4. 자세히 :  "시/군/구"
        중구와 같이 시/도가 겹치는(서울, 부산, 인천, ...) 지역은 모든 지역이 출력됩니다.   

    - "시/도"는 '서울', '서울시' 와 같이 줄여도 가능합니다.
    - "시/군/구"는  '강남구'->'강남', '청주시'->'청주' 와 같이 줄여도 가능합니다.

    예시) 
    1. 날씨
    2. 서울
    3. 서울 강남구
    4. 강남구
    """

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(f'content_type: {content_type}')
    print(f'chat_type: {chat_type}')
    print(f'chat_id: {chat_id}')
    print(f'msg: {msg}')

    if content_type == 'text':
        text = msg['text'].strip()
        # 도움말 출력
        if text == "도움" or text == "도움말":
            message = help()
            bot.sendMessage(chat_id, message)
            return

        # 대강의 날씨 출력
        if text == "날씨" or text == "날씨" or text == "ㄴㅆ" or text == "ㄴㅅ":
            info = getRoughWeatherAll()
            bot.sendMessage(chat_id, info)
            return

        text = parse(msg['text'])
        # 시/도 날씨
        if text[1] == "" and text[0] in areaId.keys():
            print('시/도 날씨')
            info = getRoughWeather(text[0])
            bot.sendMessage(chat_id, info)
            return


        if (text[0] == "세종" or text[0] == "세종시" or text[0] == "세종특별자치시"):
            text[1] = "세종특별자치시"

        # 시/군/구 날씨 # text[0] == 시/군/구
        if text[1] == "":
            err, info = getDetailWeatherAll(driver, text[0])
            bot.sendMessage(chat_id, info)
            print(f'error: {err}')
            return

        # 시/군/구 날씨 # text[1] == 시/군/구
        # 천안시: 동남구, 서북구 in kweather.co.kr
        if text[1] == "천안시":
            err, info = getDetailWeather(driver, text[0], "천안시 동남구")
            bot.sendMessage(chat_id, info)
            text[1] = "천안시 서북구"

        err, info = getDetailWeather(driver, text[0], text[1])
        bot.sendMessage(chat_id, info)
        print(f'error: {err}')
    print()

# main

driver = getDriverByUrl(URL_DETAIL)
TOKEN = "change this: get TOKEN from telegram's BotFather"
bot = telepot.Bot(TOKEN)
MessageLoop(bot=bot, handle=handle).run_forever()

