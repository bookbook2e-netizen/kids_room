"""
Streamlit UI 컴포넌트 모듈
"""
import streamlit as st
import os
from config import DEFAULT_CSV_FILE, DEFAULT_GEO_FILE
from geocoding import geocode_address
from kidsroom_manager import add_kidsroom, remove_kidsroom


def render_file_upload_section():
    """파일 업로드 섹션 렌더링"""
    st.sidebar.header("📂 데이터 파일 설정")
    use_default = st.sidebar.checkbox("기본 파일 사용", value=True, help="data 디렉토리의 기본 파일을 사용합니다")

    if use_default:
        if os.path.exists(DEFAULT_CSV_FILE) and os.path.exists(DEFAULT_GEO_FILE):
            st.sidebar.success(f"✅ 기본 파일 로드됨")
            st.sidebar.text(f"CSV: {DEFAULT_CSV_FILE}")
            st.sidebar.text(f"GeoJSON: {DEFAULT_GEO_FILE}")
            csv_file, geo_file, use_files = DEFAULT_CSV_FILE, DEFAULT_GEO_FILE, True
        else:
            st.sidebar.error("❌ 기본 파일을 찾을 수 없습니다")
            st.sidebar.info("파일 업로드 옵션을 사용하세요")
            csv_file, geo_file, use_files = None, None, False
    else:
        st.sidebar.info("📤 파일을 업로드하세요")
        uploaded_csv = st.sidebar.file_uploader("인구 데이터 CSV", type=["csv"])
        uploaded_geo = st.sidebar.file_uploader("GeoJSON 파일", type=["geojson", "json"])

        if uploaded_csv and uploaded_geo:
            csv_file, geo_file, use_files = uploaded_csv, uploaded_geo, True
        else:
            csv_file, geo_file, use_files = None, None, False

    # 지도 설정 섹션
    st.sidebar.header("🗺️ 지도 설정")

    # 시각화 기준 선택
    map_type = st.sidebar.radio(
        "시각화 기준",
        ('총인구', '인구밀도'),
        help="지도에 표시할 데이터 기준을 선택하세요. 인구밀도는 면적 대비 인구수입니다."
    )

    opacity = st.sidebar.slider(
        "지도 투명도",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="값이 낮을수록 배경 지도가 잘 보입니다"
    )

    return csv_file, geo_file, use_files, map_type, None, opacity


def render_kidsroom_auto_search_tab():
    """키즈룸 자동 검색 탭 렌더링"""
    with st.form("키즈룸_자동추가"):
        kr_address = st.text_input("주소 또는 장소명", placeholder="예: 경기 성남시 수정구 위례광장로 45 또는 플레이포레키즈룸")

        st.success("✅ 카카오 지도 API를 사용하여 정확한 한국 주소 검색 및 장소명 자동 추출이 가능합니다!")
        st.info("💡 주소를 입력하면 카카오 지도에서 장소명을 자동으로 찾아 키즈룸 이름으로 사용합니다.")
        submitted = st.form_submit_button("🔍 검색하여 추가")

        if submitted and kr_address:
            with st.spinner("카카오 API로 주소를 검색하는 중..."):
                lat, lon, used_address, place_name = geocode_address(kr_address)

                if lat and lon:
                    # 장소명이 있으면 장소명 사용, 없으면 주소에서 추출
                    kr_name = place_name if place_name else (kr_address.split()[-1] if kr_address else "키즈룸")

                    st.session_state.kidsroom_list = add_kidsroom(
                        st.session_state.kidsroom_list,
                        kr_name, used_address, lat, lon
                    )
                    st.success(f"✅ {kr_name} 추가됨!\n- 주소: {used_address}\n- 좌표: ({lat:.6f}, {lon:.6f})")
                    st.rerun()
                else:
                    st.error(f"""
                    ❌ 주소를 찾을 수 없습니다.
                    
                    **해결 방법:**
                    1. 주소를 정확히 입력했는지 확인하세요
                    2. '📍 좌표 직접 입력' 탭으로 이동
                    3. [네이버 지도에서 '{kr_address}' 검색](https://map.naver.com/v5/search/{kr_address})
                    4. 좌표를 확인하여 직접 입력
                    """)


def render_kidsroom_manual_input_tab():
    """키즈룸 수동 입력 탭 렌더링"""
    with st.form("키즈룸_수동추가"):
        kr_name_manual = st.text_input("키즈룸 이름", placeholder="예: 플레이포레키즈룸", key="manual_name")
        kr_address_manual = st.text_input("주소", placeholder="예: 경기 성남시 수정구 위례광장로 45", key="manual_addr")

        col_lat, col_lon = st.columns(2)
        with col_lat:
            kr_lat = st.number_input("위도 (Latitude)", min_value=37.0, max_value=38.0, value=37.4741, format="%.6f", step=0.0001)
        with col_lon:
            kr_lon = st.number_input("경도 (Longitude)", min_value=127.0, max_value=128.0, value=127.1453, format="%.6f", step=0.0001)

        st.markdown("""
        **🔍 좌표 찾는 방법:**
        1. [네이버 지도](https://map.naver.com)에서 주소 검색
        2. 해당 위치 클릭 → 우측 정보창 또는 하단에 좌표 표시
        3. 좌표를 복사하여 위 입력칸에 붙여넣기
        """)

        submitted_manual = st.form_submit_button("➕ 키즈룸 추가")

        if submitted_manual and kr_name_manual and kr_address_manual:
            st.session_state.kidsroom_list = add_kidsroom(
                st.session_state.kidsroom_list,
                kr_name_manual, kr_address_manual, kr_lat, kr_lon
            )
            st.success(f"✅ {kr_name_manual} 추가됨! (위도: {kr_lat:.6f}, 경도: {kr_lon:.6f})")
            st.rerun()


def render_kidsroom_list():
    """등록된 키즈룸 목록 렌더링"""
    if st.session_state.kidsroom_list:
        st.write("**등록된 키즈룸 목록:**")

        # 스크롤 가능한 컨테이너로 목록 표시
        list_container = st.container()
        with list_container:
            # 최대 높이를 설정한 스크롤 영역
            st.markdown("""
            <style>
            .kidsroom-list {
                max-height: 300px;
                overflow-y: auto;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            </style>
            """, unsafe_allow_html=True)

            for idx, kr in enumerate(st.session_state.kidsroom_list):
                col_info, col_del = st.columns([5, 1])
                with col_info:
                    st.text(f"• {kr['name']} - {kr['address']}")
                with col_del:
                    if st.button("🗑️", key=f"del_{idx}"):
                        st.session_state.kidsroom_list = remove_kidsroom(st.session_state.kidsroom_list, idx)
                        st.rerun()


def render_kidsroom_input_section():
    """키즈룸 입력 섹션 렌더링"""
    st.subheader("🎪 키즈룸 위치 추가")

    st.info("""
    💡 **주소 입력 방법:**
    - 🔍 **주소로 자동 검색**: 카카오 API를 사용하여 한국 주소를 정확하게 찾습니다 (권장)
    - 📍 **좌표 직접 입력**: 네이버 지도에서 찾은 좌표를 직접 입력
    """)

    tab1, tab2 = st.tabs(["🔍 주소로 자동 검색 (카카오 API)", "📍 좌표 직접 입력"])

    with tab1:
        render_kidsroom_auto_search_tab()

    with tab2:
        render_kidsroom_manual_input_tab()

    render_kidsroom_list()
