from asyncgpt.asyncgpt.chatgpt import GPT
import asyncio
import httpx
import requests
from transformers import GPT2Tokenizer
from quart import jsonify

sessions = {}

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# 콜백 URL에 GPT에서 얻은 답변을 보내는 함수 
async def send_response(callback_url, response):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    async with httpx.AsyncClient() as client:
        res = await client.post(callback_url, json=response, headers=headers)
    print("response: ", response)

    # 예외처리
    if res.status_code != 200:
        print(f"Failed to send response: {res.status_code}, {res.text}")
    else:
        print("Response successfully sent")


# GPT에서 답변을 얻는 함수 (토큰 관리 로직 포함)  --> 답변을 카톡 서버로 보내는 함수 호출
async def get_answer(skin_question, user_utterance, callback_url, session_id):
    bot = GPT(apikey="<please put your apikey>") # bot 초기화
    if session_id in sessions: # 기존 대화가 있는지 확인해서 발화 정보 가져오기
        messages = sessions[session_id]
    else: # 기존 대화가 없으면 새로운 저장 공간 생성
        messages = [] 
    messages.append({"role": "user", "content": user_utterance}) # 유저 발화 저장
    tokens = tokenizer.encode(str(messages)) # 토큰 수 세기
    if len(tokens) >= 6500 or len(messages) > 20: # 적정한 수준으로 토큰 유지 로직
        messages.pop(0)
        if len(tokens) >= 7500:
            messages.pop(0)

    # 새로온 발화 저장
    sessions[session_id] = messages 
    # print(messages)
    completion = await bot.chat_complete(messages)
    answer = str(completion)
    messages.append({"role": "system", "content": answer})
    tokens = tokenizer.encode(str(messages))

    # 토큰 재확인
    if len(tokens) >= 6500 or len(messages) > 20:
        messages.pop(0)
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                },
                {
        "listCard": {
          "header": {
            "title": "더 많은 정보를 원하시나요?"
          },
          "items": [
            {
              "title": "네이버 검색 결과",
              "description": f"{skin_question}으로 검색한 네이버 결과 확인하기",
              "imageUrl": "https://i.pinimg.com/originals/fb/71/04/fb71048e03a5ada757f70d61b583d0bf.png",
              "link": {
                "web": f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={skin_question}"
              }
            },
            {
              "title": "유튜브 검색 결과",
              "description": f"{skin_question}으로 검색한 유튜브 결과 확인하기",
              "imageUrl": "https://lh3.googleusercontent.com/3g4wDOiAnxbyAflNz4MhGxrkWw4vJ_kEtHTKQyqTx3o9hMBLmTIJha9ZmY87yu9mc8uM-u2OYCz6gPLx4V1o-fuV0ZHGFGenWGKV8tnPR2OvOMqIe2c=v0-s1050",
              "link": {
                "web":f"https://www.youtube.com/results?search_query={skin_question}"
                }
            }
          ]
        }
      }
            ],
        "quickReplies": [  
                    {
                        "messageText": "피부 상담",
                        "action": "message",
                        "label": "다른 질문"
                    },
                    {
                        "messageText": "처음",
                        "action": "message",
                        "label": "처음으로"
                    }
                    ]
                }
        }

    # 답변 보내는 함수 호출
    await send_response(callback_url, response)

# 컨트롤러에서 호출되는 함수로, 콜백 response 
async def question(user_request):
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

    # 폴백, 블록 두개 다 쓰려면 이부분 고치기(if, else)
    
    skin_part = user_request.get('action', {}).get('params', {}).get('skin_part_text')# 파라미터로 넘어온 변수명 주의
    skin_text = user_request.get('action', {}).get('params', {}).get('skin_problem_text')
    skin_question = skin_part + "/" + skin_text
    print(skin_question)
    user_utterance = f"""너는 친절한 피부 상담사이고, 
                질문의 형식은 피부 고민부위/피부 고민내용으로 되어있어
                질문에 대해서 해당 증상의 원인을 리스트 형식으로 설명해준 다음 해결 방안도 리스트 형식으로 제시해줘.
                만약 피부고민이외의 질문이라면 답변하지 말아줘.
                질문: {skin_question} """

    print("user_utterance: ", user_utterance)
  

    initial_response = {
        "version": "2.0",
        "useCallback": True,
    }

    # 비동기 함수를 직접 호출하지 않고, asyncio.create_task를 사용하여 백그라운드에서 실행
    asyncio.create_task(get_answer(skin_question, user_utterance, callback_url, user_id))

    return jsonify(initial_response)