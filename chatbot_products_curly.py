import pandas as pd
import numpy as np
from selenium import webdriver  # pip install selenium
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from quart import jsonify
import asyncio
import httpx
import requests
from gpt_question import send_response
import json


#뷰티컬리 제품 실시간 크롤링
async def oliveyoung_crawling(user_request):
    print('user_request : ',user_request)
    skin_type = user_request.get('action', {}).get('params', {}).get('skin_type')# 파라미터로 넘어온 변수명 주의
    product = user_request.get('action', {}).get('params', {}).get('product')
    search = skin_type + ' ' + product
    print('search : ', search)
    callback_url = user_request.get('userRequest', {}).get('callbackUrl')
    print('callback_url : ', callback_url)
    
    driver = webdriver.Chrome()
    url = f'https://www.kurly.com/search?sword={search}&site=beauty&page=2'
    driver.get(url)
    driver.implicitly_wait(time_to_wait=5)

    #brand, name, price 가져오기
    brands = driver.find_elements(By.CLASS_NAME, 'css-1dry2r1.e1c07x488')

    print("brands 확인", brands)
    if len(brands) == 0: #검색 결과가 없을 경우 
        response = {
        "version": "2.0",
        "template": {
            "outputs": [
                 {
                "simpleText": {
                    "text": "마켓 컬리에서 해당 검색으로 수집된 정보가 없습니다. 다시 시도하시려면 '다시 추천'을 처음으로 돌아가시려면 '처음으로' 버튼을 눌러주세요!"
                }
            }
                ],
                "quickReplies": [  
                        {
                            "messageText": "제품 추천",
                            "action": "message",
                            "label": "다시 추천"
                        },
                        {
                            "messageText": "처음",
                            "action": "message",
                            "label": "처음으로"
                        }
                    ]
            }
        }
        return response
    else: 
        names = driver.find_elements(By.CLASS_NAME, 'css-1wejlc3.e1c07x486')
        links = driver.find_elements(By.CLASS_NAME, 'css-1xyd46f.e1c07x4814')

        #판매가격, 현재가격 가져오기
        price_elements = driver.find_elements(By.CLASS_NAME, 'e1c07x487.css-1t4zbyd.ei5rudb2')
        price_org = [] #판매가격
        price_cur = [] #현재가격
        for i in range(len(price_elements)):
            temp = price_elements[i].text.split("\n")
            if len(temp) == 1: #세일 안할 때 
                price_org .append(price_elements[i].text) #판매가격
                price_cur.append(price_elements[i].text) #현재가격
            else:
                price_org .append(price_elements[i].find_element(By.CLASS_NAME,'dimmed-price.css-18tpqqq.ei5rudb1').text) #판매가격
                price_cur.append(price_elements[i].find_element(By.CLASS_NAME, 'sales-price.css-18tpqqq.ei5rudb1').text) #현재가격

        
        #img url가져오기
        images_url = []
        for i in range(1, len(brands)+1):    
            image = driver.find_element(By.XPATH, f'//*[@id="container"]/div/div[2]/div[2]/a[{i}]/div[1]/div/span/img')
            image = image.get_attribute('src')
            images_url.append(image)
        
        #상품수 5개로 제한
        brands = brands[:5]
        names = names[:5]
        price_org = price_org[:5]
        price_cur = price_cur[:5]
        links = links[:5]
        images_url = images_url[:5]


        #카카오톡 itemcard json형식
        itemcard = []
        for i in range(len(brands)):
            item = {
                    "thumbnail": {
                        "imageUrl": images_url[i],
                        "width": 700,
                        "height": 700
                    },
                    "itemList": [
                        {
                            "title": "브랜드·제품",
                            "description": brands[i].text
                        },
                        {
                            "title": "한줄설명",
                            "description": names[i].text
                        },
                        {
                            "title": "판매가격",
                            "description": price_org[i]
                        }, 
                        {
                            "title": "현재가격",
                            "description": price_cur[i]
                        }
                    ],
                    "buttons": [
                        {
                            "label": "자세히 보러가기",
                            "action": "webLink",
                            "webLinkUrl":links[i].get_attribute('href')
                        },
                    ],
                    "buttonLayout" : "vertical"
                }
            itemcard.append(item)


        response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "itemCard",
                        "items": itemcard
                        }
                    },
                                {
                    "textCard": {
                    "text": " 더 많은 마켓 컬리 제품을 보기 원하신다면 아래 버튼을 눌러주세요! 🙂",
                    "buttons": [
                        {
                        "action": "webLink",
                        "label": "마켓컬리로 이동하기",
                        "webLinkUrl": url
                        },
                    ]
                    }
                }
            ],
            "quickReplies": [  
                    {
                        "messageText": "올리브영 제품 추천",
                        "action": "message",
                        "label": "올리브영 제품 추천"
                    }, 
                    {
                        "messageText": "뷰티컬리 제품 추천",
                        "action": "message",
                        "label": "다시 추천"
                    },
                    {
                        "messageText": "처음",
                        "action": "message",
                        "label": "처음으로"
                    }
                    ]
                }
            }

        print('response 내용 확인', response)

        return response



async def call_crawl_and_send_response(user_request, callback_url, user_id):

    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(None, asyncio.run, oliveyoung_crawling(user_request) )  # 크롤링함수는 response를 리턴할것 

    await send_response(callback_url, response)  # 콜백 URL에 결과를 비동기적으로 전송



async def question_products_curly(user_request):
    # 플러스친구인지 확인해서, 친구가 아니면 친구요청 response
    if user_request.get('userRequest',{}).get('user',{}).get('properties',{}).get('isFriend') is not True:
        fail_response = {
            "version": "2.0",
            "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "채널 추가 후 이용 부탁드립니다."
                    }
                }
            ]
            }
        }
        return jsonify(fail_response)

    user_id = user_request.get('userRequest', {}).get('user', {}).get('id')
    callback_url = user_request.get('userRequest', {}).get('callbackUrl')
    # print("callback_url: ", callback_url)
  

    initial_response = {
        "version": "2.0",
        "useCallback": True,
    }

    # 비동기 함수를 직접 호출하지 않고, asyncio.create_task를 사용하여 백그라운드에서 실행
    asyncio.create_task(call_crawl_and_send_response(user_request, callback_url, user_id))

    return jsonify(initial_response)


# 셀레니움은 비동기 작업을 지원하지 않음. 비동기 작업을 강제로 생성한다음 그 작업 내에서 셀레니움을 실행하는 방식으로 진행되어야함
# 따라서 수정 방법은

# 컨트롤러로부터 요청을 받는 함수 생성할것 ex : async def get_request(user_request):
# question 함수와 동일한 구조로 작성, 단  asyncio.create_task를 호출할 때 매개변수로 전달하는 함수가 크롤링 함수가 아니고 비동기 작업을 생성하는 매개함수가 될 것.


# 아래는 해당 함수의 모양 
# asyncio.create_task(call_crawl_and_send_response(user_request, callback_url, user_id))
# Easyocr 비동기 수행을 위해 개별 루프를 얻는 함수
# async def call_crawl_and_send_response(user_request, callback_url, user_id):

#     loop = asyncio.get_running_loop()
#     response = await loop.run_in_executor(None, 크롤링함수, 매개변수1, 매개변수2, ...)  # 크롤링함수는 response를 리턴할것 
#     await send_response(callback_url, response)  # 콜백 URL에 결과를 비동기적으로 전송

