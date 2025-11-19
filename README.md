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
    ├── 202510_202510_연령별인구현황_월간_성남시.csv
    ├── 202510_202510_연령별인구현황_월간_광주시.csv
    ├── 202510_202510_연령별인구현황_월간_용인시.csv
    ├── HangJeongDong_ver20250401.geojson
    ├── kidsroom_data.json
    └── backups/
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
   - 키즈룸 데이터 JSON 파일 ��장
   - 앱 재시작 시 자동 로드

## 리팩토링 개선 사항

- ✅ 단일 책임 원칙: 각 모듈이 명확한 역할을 가짐
- ✅ 코드 재사용성: 함수 단위로 분리하여 재사용 가능
- ✅ 유지보수성: 기능별 파일 분리로 수정 용이
- ✅ 가독성: 명확한 함수명과 모듈 구조
- ✅ 테스트 용이성: 각 모듈을 독립적으로 테스트 가능

## 다도시 지원 (성남시 · 광주시 · 용인시)

현재 애플리케이션은 `config.py`의 `CITY_FILE_MAP`을 통해 세 도시의 월간 연령별 인구 CSV를 지원합니다.

### 파일명 규칙
```
202510_202510_연령별인구현황_월간_<도시명>.csv
```
예: `202510_202510_연령별인구현황_월간_성남시.csv`

광주시/용인시는 macOS에서 Unicode 분해형(NFD) 파일명이 생성될 수 있어 코드에서 NFC/NFD 정규화를 모두 시도합니다.

### 인코딩 표준화
- 모든 CSV는 UTF-8(BOM 포함, `utf-8-sig`)으로 저장하는 것을 권장
- 로딩 시 `utf-8` → 실패 시 `cp949` 폴백

### 다도시 로드 함수
`data_loader.load_population_for_city(city)` : 단일 도시 처리

`data_loader.load_all_populations()` : `{city: DataFrame}` 반환

### 도시 선택 UI
사이드바에서 도시를 선택하면 해당 도시의 CSV와 공통 GeoJSON을 사용하여 Choropleth를 생성합니다.

## Git 사용 참고
저장소가 초기화되지 않았다면 다음 명령으로 초기화 후 원격 연결:
```bash
git init
git add .
git commit -m "init"
git branch -M main
git remote add origin <YOUR_REPO_URL>
git push -u origin main
```
