from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
import requests
import pandas as pd

siDoFullName = {
    "서울":"서울특별시", "서울시":"서울특별시", "서울특별시":"서울특별시",
    "부산":"부산광역시", "부산시":"부산광역시", "부산광역시":"부산광역시",
    "대구":"대구광역시", "대구시":"대구광역시", "대구광역시":"대구광역시",
    "인천":"인천광역시", "인천시":"인천광역시", "인천광역시":"인천광역시",
    "광주":"광주광역시", "광주시":"광주광역시", "광주광역시":"광주광역시",
    "대전":"대전광역시", "대전시":"대전광역시", "대전광역시":"대전광역시",
    "울산":"울산광역시", "울산시":"울산광역시", "울산광역시":"울산광역시",
    "경기":"경기도", "경기도":"경기도",
    "강원":"강원도", "강원도":"강원도",
    "충북":"충청북도", "충청북도":"충청북도",
    "충남":"충청남도", "충청남도":"충청남도",
    "전북":"전라북도", "전라북도":"전라북도",
    "전남":"전라남도", "전라남도":"전라남도",
    "경북":"경상북도", "경상북도":"경상북도",
    "경남":"경상남도", "경상남도":"경상남도",
    "제주":"제주특별자치도", "제주도":"제주특별자치도", "제주특별자치도":"제주특별자치도",
    "세종":"세종특별자치시", "세종시":"세종특별자치시", "세종특별자치시":"세종특별자치시"
}

URL_DETAIL = "https://www.kweather.co.kr/forecast/forecast_lifestyle_detail.html"
URL_ROUGH = "https://www.kweather.co.kr/forecast/forecast_lifestyle.html"
EXCEL_PATH = './resource/sido.xlsx'
CHROME_DRIVER_PATH = './resource/chromedriver.exe'
global driver

# 크롬 페이지 띄우기
# with selenium
def getDriverByUrl(x_url):
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    driver.get(x_url)
    return driver
#

# 시/도 선택
# with selenium
def selectSi_do(x_driver, name):
    select_element = x_driver.find_element_by_xpath(f'//select[@class="lifestyle_select_do"]')
    select_object = Select(select_element)#('/option[text()="{si_do}"]')
    select_object.select_by_visible_text(name)
#

# 시/군/구 선택
# with selenium
def selectSi_gun_gu(x_driver, name):
    select_element = x_driver.find_element_by_xpath(f'//select[@class="lifestyle_select_si"]')
    select_object = Select(select_element)  # ('/option[text()="{si_do}"]')
    select_object.select_by_visible_text(name)
#

# 선택 후 클릭하여 페이지 정보 변환
# with selenium
def clickSelectOption(x_driver):
    x_driver.find_element_by_xpath('//*[@id="Container"]/div[3]/div[2]/ul/li[2]/img').click()
#

# 해당 페이지에 대한 정보 가져오기
# with bs4
def getCurPageSourse(x_driver):
    html = x_driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup
#

# # 해당 페이지에 대한 시/도 시/군/구 이름 가져오기
# # with bs4
# def getAreaName(x_soup):
#     text = x_soup.select_one('#Container > div:nth-child(7) > div.lifestyle_present_forecast > ul.lifestyle_present_forecast_title > li > span').text
#     text = text.strip()
#     return text.split(" ")
#

# # 해당 페이지에서 오늘/내일/모레 예보 선택
# #//*[@id="day1"]/table/tbody/tr/td[1]  오늘
# #//*[@id="day0"]/table/tbody/tr/td[2]  내일
# #//*[@id="day0"]/table/tbody/tr/td[3]  모레
# def clickDate(x_driver, x_date="오늘"):
#     path = ""
#     if x_date == "오늘":
#         path = '//*[@id="day1"]/table/tbody/tr/td[1]'
#     elif x_date == "내일":
#         path = '//*[@id="day0"]/table/tbody/tr/td[2]'
#     else:
#         path = '//*[@id="day0"]/table/tbody/tr/td[3]'
#     x_driver.find_element_by_xpath(path).click()
# #

# 크롬 페이지 종료
# with selenium
def closeDriver(x_driver):
    x_driver.close()
#

# 현재 날씨 가져오기
# with bs4
# 하늘 상태(ex 구름많음), 기온, 체감, 풍향, 풍속, 강수, 습도
def getWeatherBySoup(x_soup):
    soup = x_soup.select_one('#Container > div:nth-child(7) > div.lifestyle_present_forecast > ul.lifestyle_present_forecast_content')
    lis = soup.select('li')

    area = str(lis[0].select('span')[0])
    area = area.split("<br/>")
    area = area[0].split(">")[1] + " " + area[1].split("<")[0]

    time = lis[0].select('span')[1].text

    st_sky = lis[1].select_one('span').text

    info = lis[2].select('table > tbody > tr > td')

    arr = [area, time, st_sky]
    for data in info:
        arr.append(str(data)[4:-5])

    return arr
#


# 날씨 가져오기
def getDetailWeather(driver, siDo, siGunGu):
    if siDo not in siDoFullName.keys():
        return 2, "지역을 정확히 입력해주세요.\n사용법을 모르시면 \'도움\'을 입력해주세요."
    siDo = siDoFullName[siDo]

    err = 0

    try:
        selectSi_do(driver, siDo)
    except:
        err = 1
        return err, "지역을 정확히 입력해주세요.\n사용법을 모르시면 \'도움\'을 입력해주세요."

    temp = ["", "시", "군", "구"]
    for i in range(4):
        temp_siGunGu = siGunGu + temp[i]

        try:
            selectSi_gun_gu(driver, temp_siGunGu)
            err = 0
        except:
            err = 2
            if i == 3:
                return err, "지역을 정확히 입력해주세요.\n사용법을 모르시면 \'도움\'을 입력해주세요."

        if err == 0:
            break

    clickSelectOption(driver)

    soup = getCurPageSourse(driver)

    arr = getWeatherBySoup(soup)

    info = printWeather(arr)

    return err, info
#

# 날씨 가져오기 (ex: 중구만 입력시,  서울, 부산, 인천, ... 모두)
def getDetailWeatherAll(driver, siGunGu):
    df = pd.read_excel(EXCEL_PATH)

    if siGunGu not in df['시군구'].values:
        return 2, "지역을 정확히 입력해주세요.\n사용법을 모르시면 \'도움\'을 입력해주세요."

    arr = df[df['시군구'] == siGunGu].values[0][1:]
    print(arr)
    info = ""
    for si_do in arr:
        if type(si_do) is float:
            break
        print(si_do)
        err, temp = getDetailWeather(driver, siDoFullName[si_do], siGunGu)
        info += temp + '\n\n'

    return err, info
#

# 위치, 시간, 하늘상태, 기온, 체감, 풍향, 풍속, 강수, 습도
def printWeather(info):
    message = info[0] + '\n'
    message += info[1] + ' ' + info[2]
    message += '\n----------------------\n'
    message += "\n기온: " + info[3]
    message += "\n체감: " + info[4]
    message += "\n풍향: " + info[5]
    message += "\n풍속: " + info[6]
    message += "\n강수: " + info[7]
    message += "\n습도: " + info[8]
    return message
#

rough_area = ["서해5도", "서울/경기", "강원영서", "강원영동", "충남", "충북", "경북", "울릉", "전남", "전북", "경남", "제주"]

def getRoughWeatherAll():
    resp = requests.get(URL_ROUGH)
    soup = BeautifulSoup(resp.text, "html5lib")
    lis = soup.select('.lifestyle_present_map > li')
    print("------")
    info = "---------------------------\n"
    for area, elem in zip(rough_area, lis):
        info += f'{area}: {elem.text}\n'
        info += '---------------------------\n'

    return info

areaId = {
    "서울":[1], "서울시":[1], "서울특별시":[1],
    "경기":[1], "경기도":[1],
    "강원":[2,3], "강원도":[2,3], "영서":[2], "영동":[3],
    "충청도":[4,5], "충남":[4], "충북":[5],
    "경상도":[6,10], "경북":[6], "경남":[10],
    "울릉":[7], "울릉도":[7],
    "전라도":[8,9], "전남":[8], "전북":[9],
    "제주도":[11], "제주":[11]
}

def getRoughWeather(area):
    resp = requests.get(URL_ROUGH)
    soup = BeautifulSoup(resp.text, "html5lib")
    lis = soup.select('.lifestyle_present_map > li')

    info = ""
    for id_ in areaId[area]:
        info += f'{rough_area[id_]}: {lis[id_].text}\n'

    return info

def getSiDo(siGunGu):
    siGunGu = pd.read_excel('./sido.xlsx')