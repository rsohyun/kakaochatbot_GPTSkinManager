# 💻 Project-KakaoChatbot-GPTSkinManager
카카오톡 챗봇 + ChatGPT + Oliveyoung&Beautycurly제품 추천
## 🧴 프로젝트 소개
### 주제
ChatGPT와 크롤링을 활용하여 피부 고민 상담 및 기초 제품을 추천해주는 카카오톡 챗봇입니다. 
### 주제 선정 배경
이 프로젝트의 동기는 제가 피부 관리를 위해 탐색하면서 겪었던 지속적인 문제와 관찰로부터 비롯되었습니다. 이러한 문제들에 기반하여 사용자 경험을 향상시키고 피부 관리 및 화장품 분야에서 실질적인 해결책을 제공하는 프로젝트를 제안하게 하였습니다.

1. **다양한 피부 문제와 정보 과부하**

      다양한 피부 문제에 직면하면 Naver 및 Youtube와 같은 플랫폼에서 관련 정보를 얻기 위해 개별적인 검색을 자주 시도하게 됩니다. 그러나 이러한 방식은 번거로운 작업을 필요로 하며, 종종 유용하지 않은 정보를 찾아내는 데 시간이 소요됩니다. 관련 없는 콘텐츠를 걸러내는 동안 소중한 시간을 낭비하는 경우가 많았습니다.
    
      **<제안된 해결책>**
      - ChatGPT를 활용하여 다양한 피부 문제에 대한 맞춤형 제안과 통찰력을 제공하는 기능 개발
      - Naver 검색 결과와 관련 Youtube 영상으로의 링크를 통합하여 관련 정보에 쉽게 접근
      - 개인 맞춤 피부 관련 도움을 위해 근처 피부과를 찾는 기능 구현

2. **화장품 선택에서의 어려움**

      특정한 피부 유형에 맞는 적합한 스킨케어 제품을 선택하는 것은 상당히 어려운 일이라고 생각합니다. 저 또한 건성 및 아토피 피부에 적합한 화장품을 찾는 것이 매우 어려운 일이었습니다. 
      Naver는 대부분 광고를 보여주며, Youtube는 좋은 영상를 찾더라도 영상의 길이가 길고 광고인 경우가 많았으며, 접할 수 있는 브랜드도 제한적이었습니다.
    
      **<제안된 해결책>**
      - 사용자가 고유한 피부 유형을 식별할 수 있도록 정보 제공
      - Oliveyoung과 Beautycurly와 같은 플랫폼의 다양한 인기 제품을 수집하여 사용자에게 추천

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
[주요기능 - 피부상담 Wiki로 이동](https://github.com/rsohyun/kakaochatbot_GPTSkinManager/wiki/%EC%A3%BC%EC%9A%94-%EA%B8%B0%EB%8A%A5-%EC%86%8C%EA%B0%9C-:-%EB%82%B4-%EC%A3%BC%EB%B3%80-%ED%94%BC%EB%B6%80%EA%B3%BC-%EC%B0%BE%EA%B8%B0)
- 챗봇 사용자의 발화를 받아 prompt engineering이 적용된 입력값을 Chatgpt에게 전달 및 답변 제공 
### 2. 제품추천: 올리브영, 뷰티컬리
[주요기능 - 제품추천 Wiki로 이동](https://github.com/rsohyun/kakaochatbot_GPTSkinManager/wiki/%EC%A3%BC%EC%9A%94-%EA%B8%B0%EB%8A%A5-%EC%86%8C%EA%B0%9C-:-%EC%A0%9C%ED%92%88-%EC%B6%94%EC%B2%9C)
- 사용자가 스킨 타입 선택, 올리브영과 뷰티 컬리 중 선택
- selenium을 이용하여 실시간으로 인기 제품 검색 결과를 추천 상품으로 제공
### 3. 내 주변 피부과 찾기
[주요기능 - 내 주변 피부과 찾기 Wiki로 이동](https://github.com/rsohyun/kakaochatbot_GPTSkinManager/wiki/%EC%A3%BC%EC%9A%94-%EA%B8%B0%EB%8A%A5-%EC%86%8C%EA%B0%9C-:-%EB%82%B4-%EC%A3%BC%EB%B3%80-%ED%94%BC%EB%B6%80%EA%B3%BC-%EC%B0%BE%EA%B8%B0)
- '주변 피부과'로 검색되어 있는 네이버 지도 링크로 이동하여 자신 주변의 피부과 위치 제공
### 4. 내 피부 타입 알아보기 
[주요기능 - 내 피부 타입 알아보기  Wiki로 이동](https://github.com/rsohyun/kakaochatbot_GPTSkinManager/wiki/%EC%A3%BC%EC%9A%94-%EA%B8%B0%EB%8A%A5-%EC%86%8C%EA%B0%9C-:-%ED%94%BC%EB%B6%80-%ED%83%80%EC%9E%85-%EC%95%8C%EC%95%84%EB%B3%B4%EA%B8%B0)
- 단순히 피부 타입 별 특징을 써 넣은 텍스트로 간략하게 자신의 피부 타입을 찾아볼 수 있도록 함
