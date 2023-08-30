# 💻 Project-KakaoChatbot-GPTSkinManager
카카오톡 챗봇 + ChatGPT + Oliveyoung&Beautycurly제품 추천
## 🧴 프로젝트 소개
ChatGPT와 크롤링을 활용하여 피부 고민 상담 및 기초 제품을 추천해주는 카카오톡 챗봇입니다. 
## 📅 개발 기간
- 2023.07.17 ~ 2023.08.06
## ⚒️ 개발 환경
- Visual Studio Code: 코드 작성
- ngrok

<주요 라이브러리 및 프레임워크>
- Quart 0.18.4
- [Asycgpt](https://github.com/Just1z/asyncgpt)
- selenium 4.11.2
  
## 🧩 주요 기능
### 1. 피부상담
- 챗봇 사용자의 발화를 받아 prompt engineering이 적용된 입력값을 Chatgpt에게 전달 및 답변 제공 
### 2. 제품추천: 올리브영, 뷰티컬리
- 사용자가 스킨 타입 선택, 올리브영과 뷰티 컬리 중 선택
- selenium을 이용하여 실시간으로 인기 제품 검색 결과를 추천 상품으로 제공
### 3. 내 주변 피부과 찾기
- '주변 피부과'로 검색되어 있는 네이버 지도 링크로 이동하여 자신 주변의 피부과 위치 제공
### 4. 내 피부 타입 알아보기 
- 단순히 피부 타입 별 특징을 써 넣은 텍스트로 간략하게 자신의 피부 타입을 찾아볼 수 있도록 함
