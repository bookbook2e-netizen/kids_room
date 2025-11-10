# kids_room (성남시 동별 인구 & 키즈룸 시각화)

Streamlit 기반으로 성남시 행정동 별 인구(총인구 / 인구밀도)와 키즈룸(키즈카페 등) 위치를 지도 위에 시각화하는 애플리케이션입니다.

## 1. 로컬 실행
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 2. GitHub 업로드
```bash
git init
git add .
git commit -m "init: kids_room app"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/kids_room.git
git push -u origin main
```

## 3. 카카오 API Key 분리 (.streamlit/secrets.toml)
`.streamlit/secrets.toml` 파일을 만들고:
```toml
KAKAO_REST_API_KEY = "your_rest_key"
```
`geocoding.py`에서 `st.secrets["KAKAO_REST_API_KEY"]`로 참조하도록 수정 가능.

## 4. Streamlit Cloud 배포
1. https://streamlit.io → Sign in (Google 계정 가능)
2. New app 선택 → GitHub repo 연결
3. Branch: `main`, File: `app.py`
4. Advanced settings → Secrets 입력:
```toml
KAKAO_REST_API_KEY = "your_rest_key"
```
5. Deploy

## 5. 문제 해결 체크리스트
- KeyError: 'properties' → Folium.Choropleth에 안전한 FeatureCollection 전달 완료
- 인구/인구밀도 토글 → 사이드바 라디오 버튼
- 투명도 조절 → 슬라이더 (`opacity`)
- 키즈룸 데이터 지속성 → `kidsroom_manager.py` (JSON 저장 구현 필요 시 추가)

## 6. 향후 개선 아이디어
- 연령대별 선택 필터 추가
- 혼합 지표(총인구 vs 밀도 가중) 재도입 (안정화 후)
- 키즈룸 DB/Google Sheet 연동
- Mobile UI 최적화

## 7. 라이선스
개인 학습/포트폴리오 용도.

