# 성남시 인구 현황 및 키즈룸 분석 애플리케이션

## 프로젝트 구조

```
kids_room/
├── app.py                      # 메인 애플리케이션 (실행 파일)
├── config.py                   # 설정 파일 (API 키, 경로 등)
├── data_loader.py              # 데이터 로드 및 처리
├── geocoding.py                # 지오코딩 (주소 → 좌표 변환)
├── kidsroom_manager.py         # 키즈룸 데이터 관리
├── map_generator.py            # 지도 생성
├── ui_components.py            # Streamlit UI 컴포넌트
└── data/                       # 데이터 디렉토리
    ├── 202510_202510_연령별인구현황_월간.csv
    ├── hangjeongdong_경기도.geojson
    └── kidsroom_data.json
```

## 모듈 설명

### 1. `config.py`
- 애플리케이션 전체 설정 관리
- API 키, 파일 경로, 지도 기본 설정 등

### 2. `data_loader.py`
- CSV 및 GeoJSON 파일 로드
- 인구 데이터 처리 (정규화, 컬럼 추출)
- 지리 데이터 처리 및 병합

### 3. `geocoding.py`
- 카카오 API를 이용한 주소 검색
- Nominatim 백업 지오코딩
- 주소 → 좌표 변환 로직

### 4. `kidsroom_manager.py`
- 키즈룸 데이터 CRUD 작업
- JSON 파일 저장/로드

### 5. `map_generator.py`
- Folium 지도 생성
- Choropleth 레이어 추가
- 동별 라벨 및 마커 추가

### 6. `ui_components.py`
- Streamlit UI 컴포넌트
- 파일 업로드, 키즈룸 입력 폼 등

### 7. `app.py`
- 메인 애플리케이션
- 모든 모듈을 통합하여 실행

## 실행 방법

```bash
# 기존 방식 (백업)
streamlit run seongnam_population_app_backup.py

# 새로운 모듈화 버전
streamlit run app.py
```

## 주요 기능

1. **동별 인구 시각화**
   - 성남시 행정동별 총인구 Choropleth 지도
   - 마우스 오버 시 인구 정보 표시

2. **키즈룸 위치 관리**
   - 카카오 API를 통한 자동 주소 검색
   - 수동 좌표 입력
   - 키즈룸 추가/삭제

3. **데이터 영구 저장**
   - 키즈룸 데이터 JSON 파일 저장
   - 앱 재시작 시 자동 로드

## 리팩토링 개선 사항

- ✅ 단일 책임 원칙: 각 모듈이 명확한 역할을 가짐
- ✅ 코드 재사용성: 함수 단위로 분리하여 재사용 가능
- ✅ 유지보수성: 기능별 파일 분리로 수정 용이
- ✅ 가독성: 명확한 함수명과 모듈 구조
- ✅ 테스트 용이성: 각 모듈을 독립적으로 테스트 가능

