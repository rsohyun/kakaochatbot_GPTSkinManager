import asyncio
from asyncgpt import asyncgpt
import sys
from quart import Quart, request
from gpt_question import question
from chatbot_products_oliveyoung import question_products
from chatbot_products_curly import question_products_curly
from quart import jsonify

application = Quart(__name__)


# GPT 호출 함수
@application.route("/question", methods=["POST"])
async def call_gpt():
    user_request = await request.json
    print('user_request : ',user_request)

    return await question(user_request)


# 올리브영 크롤링 호출 함수
@application.route("/products_oliveyoung", methods=["POST"])
async def call_crawling():
    user_request = await request.json
    print('user_request : ',user_request)

    callback_url = user_request.get('userRequest', {}).get('callbackUrl')
    print('callback_url : ', callback_url)


    return await question_products(user_request)

# 뷰티컬리 크롤링 호출 함수
@application.route("/products_curly", methods=["POST"])
async def call_crawling_curly():
    user_request = await request.json
    print('user_request : ',user_request)

    callback_url = user_request.get('userRequest', {}).get('callbackUrl')
    print('callback_url : ', callback_url)


    return await question_products_curly(user_request)


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80)
