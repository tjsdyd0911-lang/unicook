<div align="center">
  <img src="./images/unicook_main.png" width="80%">
  <h3>AI를 활용한 개인 맞춤형 상품 추천</h3>
</div>

## ⌨️ 기간

- **2026.03.24 ~ 2026.04.27(5주)**

<a name="tableContents"></a>

<br/>

## 🔎 목차

1. <a href="#subject">🎯 주제</a>
1. <a href="#mainContents">⭐️ 주요 분석</a>
1. <a href="#systemArchitecture">⚙ 시스템 아키텍쳐</a>
1. <a href="#skills">🛠️ 기술 스택</a>
1. <a href="#erd">💾 ERD</a>
1. <a href="#contents">🖥️ 화면 소개</a>
1. <a href="#developers">👥 팀원 소개</a>

<br/>

<!------- 주제 시작 -------->

## 🎯 주제

<a name="subject"></a>

**빅데이터 분석**과 **AI**를 활용한 식품 커머스 프로젝트로 개인 맞춤형 추천 상품을 보여줍니다.<br />
각 페이지마다 다른 **알고리즘**을 이용하여 데이터를 분석합니다.

<br />
**주요 기능**


- **Numpy**, **Pandas**를 이용한 전처리
- **Scikit-learn(SVD)**, **협업 필터링**의 **코사인 유사도 분석** 이용
- 분석한 내용과 시간대별 추천과 아이템 카테고리 결합
  
<div align="right"><a href="#tableContents">목차로 이동</a></div>

<br/>

<!------- 주요 기능 시작 -------->

## ⭐️ 주요 분석

<a name="mainContents"></a>

### 메인 페이지

#### 메인 페이지 상단과 하단에 상품별 분석 내용을 제공합니다.

- 상단 분석
  - 회원 : 시간대별 분석 + 사용자 구매내역(SVD) + 아이템 카테고리를 결합하여 분석합니다.
  - 비회원 : 시간대별 가장 많은 구매내역을 가진 상품 4가지를 표시합니다.

- 하단 분석
  - 회원 : 로그인한 사용자와 같은 성별, 비슷한 나이대의 유사도를 통해 도출한 가중치를 아이템으로 도출했습니다.
  - 비회원 : 전체 회원을 대상으로 구매내역에 대한 가중치를 부여하여 분석 후 화면에 표시합니다.


---


### 상세 페이지

#### 현재 상품 기준의 분석 내용을 제공합니다.

- 현재 상품과 가장 유사도가 높은 상품들을 도출하여 화면에 표시합니다.


---


### 장바구니

<h4>장바구니에 담긴 상품과 전체 사용자의 구매내역을 통해 분석합니다.</h4>

- 장바구니에 담긴 상품들을 토대로 아이템 간 코사인 유사도를 계산합니다.
- 구매내역 + 구매수량(로그화)을 합산하여 유사도를 계산합니다.


---


### 구매내역

#### 현재 사용자가 지금까지 구매한 내용을 바탕으로 상품을 추천할 수 있도록 분석합니다.

- 현재 사용자가 구매한 상품의 구매빈도와 구매수량에 대한 가중치를 계산하여 최애 상품을 분석합니다.
- 가중치 점수: (빈도 * 0.7) + (수량 * 0.3)


---


<div align="right"><a href="#tableContents">목차로 이동</a></div>

<br/>


<!------- 시스템 아키텍쳐 시작 -------->

## ⚙ 시스템 아키텍쳐

<a name="systemArchitecture"></a>

<img src="./images/unicook_System Architecture.png">

- Frontend: HTML5, CSS3, JavaScript를 활용하여 깔끔하고 가독성 좋은 UI와 Ajax를 이용한 비동기 통신 환경을 구축 
- Backend & DB: Flask 프레임워크를 사용하여 서버를 구현하였으며, MySQL을 통해 사용자 정보 및 구매 이력 데이터를 관리
- AI Engine: Pandas와 NumPy로 전처리된 데이터를 바탕으로, Scikit-learn의 SVD(특이값 분해) 및 코사인 유사도 알고리즘을 활용해 고도화된 개인화 추천 로직을 수행

본 프로젝트는 Flask 기반의 웹 서버와 Scikit-learn 기반의 AI 추천 엔진을 결합한 지능형 커머스 플랫폼입니다. 사용자 구매 데이터를 분석하여 개인 맞춤형 상품을 추천하는 시스템 아키텍처를 구축하였습니다.

<div align="right"><a href="#tableContents">목차로 이동</a></div>

<br/>

<!------- 기술 스택 시작 -------->

## 🛠️ 기술 스택

<a name="skills"></a>

### 💻 FrontEnd

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Ajax](https://img.shields.io/badge/Ajax-%23ffffff.svg?style=for-the-badge&logo=jquery&logoColor=black)
![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)
---

### ⚙️ BackEnd

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Mysql](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mariadb&logoColor=white)
---

### 📊 Data Analysis

![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
---

### 📈 Visualization

![Chart.js](https://img.shields.io/badge/chart.js-F5788D?style=for-the-badge&logo=chart.js&logoColor=white)
![ApexCharts](https://img.shields.io/badge/ApexCharts-008FFB?style=for-the-badge&logo=apexcharts&logoColor=white)
---

### 🤝 Collaboration

![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
---

<div align="right"><a href="#tableContents">목차로 이동</a></div>

<br/>

<!------- ERD 시작 -------->

## 💾 ERD
<a name="erd"></a>
<img src="./images/unicook_ERD.png">

<div align="right"><a href="#tableContents">목차로 이동</a></div>

<br/>

<!------- 화면 소개 시작 -------->

<a name="contents"></a>

<br/>

## 🖥️ 화면 소개

### 1. 메인 페이지 상단

<table>
    <tr>
        <td align="center" width="200">
            <h5>메인 페이지 상단</h5>
            <img src="./images/main_1.png" alt="main_1" width="100%" />  
        </td>
        <td align="center" width="200">
            <h5>시간대별 분석</h5>
            <img src="./images/main_1_recommend.png" alt="시간대별 분석" width="100%" />  
        </td> 
    </tr>
    <tr>
      <td align="center">
        <div>✔ 시간대별 추천 상품 화면에 표시</div>
      </td>
      <td align="center">
        <div>✔ 비회원은 시간대별 분석</div>
        <div>✔ 회원은 시간대별 + 사용자 구매이력(SVD) + 아이템 카테고리 결합 분석</div>
      </td>
    </tr>
</table>

### 2. 메인 페이지 하단

<table>
    <tr>
        <td align="center" width="200">
            <h5>메인 페이지 하단</h5>
            <img src="./images/main_2.png" alt="메인하단" width="100%" />
        </td>
        <td align="center" width="200">
            <h5>하단 비회원 분석</h5>
            <img src="./images/main_2_recommend1.png" alt="비회원 분석" width="100%" />
        </td>
        <td align="center" width="200">
            <h5>하단 회원 분석</h5>
            <img src="./images/main_2_recommend2.png" alt="회원 분석" width="100%" />
        </td>
    </tr>
    <tr>
      <td align="center">
        <div>✔ 구매 빈도와 수량으로 가중치를 계산하여 화면에 표시</div>
      </td>
      <td align="center">
        <div>✔ 전체회원을 대상으로 가중치 점수가 높은 상품 분석</div>
      </td>
      <td align="center">
        <div>✔ 로그인한 회원 대상으로 비슷한 성별, 나이대 회원의 유사도 분석</div>
      </td>
    </tr>
</table>

### 3. 상세 페이지

<table>
    <tr>
        <td align="center" width="200">
            <h5>상세 페이지 화면</h5>
            <img src="./images/view.png" alt="상세 페이지" width="200" />  
        </td>
        <td align="center" width="200">
            <h5>상세 페이지 분석 및 시각화</h5>
            <img src="./images/view_recommend.png" alt="상세 페이지 분석" width="200" />  
        </td>
    </tr>
    <tr>
      <td align="center">
        <div>✔ 현재 페이지의 제품과 유사한 상품 화면에 표시</div>
      </td>
      <td align="center">
        <div>✔ 현재 페이지 상품과 유사한 제품을 분석 및 Heatmap으로 시각화</div>
      </td>
    </tr>
</table>

### 4. 장바구니

<table>
    <tr>
        <td align="center" width="200">
            <h5>장바구니 화면</h5>
            <img src="./images/cart.png" alt="" width="200" />  
        </td>
        <td align="center" width="200">
            <h5>장바구니 분석</h5>
            <img src="./images/cart_recommend.png" alt="" width="200" />  
        </td>
    </tr>
    <tr>
      <td align="center">
        <div>✔ 장바구니 담은 상품 비동기 통신(AJAX)을 통한수량 및 가격 변경</div>
      </td>
      <td align="center">
        <div>✔ 장바구니에 담은 상품과 유사한 상품을 분석 및 시각화</div>
      </td>
    </tr>
</table>

### 5. 구매내역

<table>
    <tr>
        <td align="center" width="200">
            <h5>구매내역 화면</h5>
            <img src="./images/purchase.png" alt="" width="200" />  
        </td>
        <td align="center" width="200">
            <h5>구매내역 분석</h5>
            <img src="./images/purchase_recommend.png" alt="" width="200" />  
        </td>
    </tr>
    <tr>
      <td align="center">
        <div>✔ 구매내역을 전체, 1개월, 3개월 필터화</div>
      </td>
      <td align="center">
        <div>✔ 구매한 상품과 유사한 상품을 분석 및 시각화</div>
      </td>
    </tr>
</table>

<div align="right"><a href="#tableContents">목차로 이동</a></div>

<br/>

### ✔ 프로젝트 결과물

---

<!-- - [포팅메뉴얼] -->
<!-- - [발표자료] -->
- [중간발표자료](./ppt/중간발표_unicook.pdf)
- [최종발표자료](./ppt/최종발표_unicook.pdf)


<!------- 팀원 소개 시작 -------->

## 👥 팀원 소개

<a name="developers"></a>
<table>
    <tr>
        <td align="center" width="200">
            <h5>Name</h5>
        </td>
        <td align="center" width="200">
            <h5>박윤희</h5>
        </td>
        <td align="center" width="200">
            <h5>박세연</h5>
        </td>
        <td align="center" width="200">
            <h5>박정희</h5>
        </td>
        <td align="center" width="200">
            <h5>백세원</h5>
        </td>
        <td align="center" width="200">
            <h5>진선용</h5>
        </td>
        <td align="center" width="200">
            <h5>정정원</h5>
        </td>
    </tr>
    <tr>
        <td align="center" width="200">
            <h5>역할</h5>
        </td>
        <td align="center" width="200">
            <h5>풀스택</h5>
        </td>
        <td align="center" width="200">
            <h5>프론트엔드</h5>
        </td>
        <td align="center" width="200">
            <h5>프론트엔드</h5>
        </td>
        <td align="center" width="200">
            <h5>풀스택</h5>
        </td>
        <td align="center" width="200">
            <h5>풀스택</h5>
        </td>
        <td align="center" width="200">
            <h5>프론트엔드</h5>
        </td>
    </tr>
</table>

<div align="right"><a href="#tableContents">목차로 이동</a></div>
