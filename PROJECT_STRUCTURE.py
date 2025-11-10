"""
프로젝트 구조 요약 및 모듈 의존성
"""

# 모듈 의존성 그래프
"""
app.py (메인)
├── config.py
├── data_loader.py
│   └── config (간접)
├── kidsroom_manager.py
│   └── config
├── map_generator.py
│   └── config
├── ui_components.py
│   ├── config
│   ├── geocoding
│   └── kidsroom_manager
└── geocoding.py
    └── config
"""

# 각 모듈의 책임
MODULES = {
    "app.py": "메인 애플리케이션 - 전체 흐름 제어",
    "config.py": "설정 관리 - API 키, 경로, 상수",
    "data_loader.py": "데이터 I/O - CSV/GeoJSON 로드 및 처리",
    "geocoding.py": "지오코딩 - 주소를 좌표로 변환",
    "kidsroom_manager.py": "키즈룸 데이터 관리 - CRUD 작업",
    "map_generator.py": "지도 생성 - Folium 지도 렌더링",
    "ui_components.py": "UI 컴포넌트 - Streamlit 인터페이스"
}

# 주요 함수 목록
FUNCTIONS = {
    "data_loader.py": [
        "load_csv_file(file_path)",
        "load_geojson_file(file_path)",
        "process_population_data(df)",
        "process_geodata(gdf, city_name)",
        "merge_data(gdf_filtered, df)"
    ],
    "geocoding.py": [
        "geocode_address(address) -> (lat, lon, address, place_name)",
        "geocode_with_kakao_keyword(address, headers)",
        "geocode_with_kakao_address(address, headers)",
        "geocode_with_nominatim(address)"
    ],
    "kidsroom_manager.py": [
        "load_kidsroom_data()",
        "save_kidsroom_data(data)",
        "add_kidsroom(list, name, address, lat, lon)",
        "remove_kidsroom(list, index)"
    ],
    "map_generator.py": [
        "create_population_map(merged, kidsroom_list)",
        "create_base_map()",
        "add_choropleth_layer(m, merged)",
        "add_dong_layers(m, merged)",
        "add_kidsroom_markers(m, kidsroom_list)"
    ],
    "ui_components.py": [
        "render_file_upload_section()",
        "render_kidsroom_input_section()",
        "render_kidsroom_auto_search_tab()",
        "render_kidsroom_manual_input_tab()",
        "render_kidsroom_list()"
    ]
}

# 리팩토링 이점
BENEFITS = """
1. 유지보수성 향상
   - 각 모듈이 단일 책임을 가짐
   - 버그 수정 시 해당 모듈만 확인

2. 코드 재사용성
   - 함수 단위로 분리되어 다른 프로젝트에서 재사용 가능
   - 예: geocoding.py는 다른 지도 앱에서도 사용 가능

3. 테스트 용이성
   - 각 모듈을 독립적으로 테스트 가능
   - 단위 테스트 작성이 쉬워짐

4. 협업 효율성
   - 여러 개발자가 다른 모듈을 동시에 작업 가능
   - Git conflict 발생 확률 감소

5. 확장성
   - 새로운 기능 추가 시 새로운 모듈 생성
   - 기존 코드 수정 최소화
"""

