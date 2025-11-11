"""
Streamlit UI 컴포넌트 모듈
"""
import streamlit as st
import os
from config import DEFAULT_CSV_FILE, DEFAULT_GEO_FILE
from geocoding import geocode_address
from kidsroom_manager import add_kidsroom, remove_kidsroom, update_kidsroom


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

        st.success("✅ 카카오 지도 API를 사용하여 정확한 한국 주소 검��� 및 장소명 자동 추출이 가능합니다!")
        st.info("💡 주소를 입력하면 카카오 지도에서 장소명을 자동����로 찾아 키즈룸 이름으로 사용합니다.")
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
                    1. 주소를 정확히 입력���는지 확인하세요
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
    """등록된 키즈룸 목록 렌더링 (수정/삭제 지원 + 페이징 + 검색)"""
    if 'kidsroom_page' not in st.session_state:
        st.session_state.kidsroom_page = 0
    if 'kidsroom_page_size' not in st.session_state:
        st.session_state.kidsroom_page_size = 5

    kids = st.session_state.kidsroom_list
    if not kids:
        st.info("등록된 키즈룸이 없습니다")
        return

    st.write("**등록된 키즈룸 목록:**")

    # 검색 필터
    keyword = st.text_input("🔍 이름/주소 검색", value="", placeholder="키워드 입력")
    if keyword.strip():
        filtered = [k for k in kids if keyword.lower() in k['name'].lower() or keyword.lower() in k['address'].lower()]
    else:
        filtered = kids

    total = len(filtered)

    # 페이지 크기 선택
    col_ps, col_info = st.columns([1,3])
    with col_ps:
        page_size = st.selectbox("페이지 크기", [5,10,15,20], index=[5,10,15,20].index(st.session_state.kidsroom_page_size) if st.session_state.kidsroom_page_size in [5,10,15,20] else 0)
        if page_size != st.session_state.kidsroom_page_size:
            st.session_state.kidsroom_page_size = page_size
            st.session_state.kidsroom_page = 0
    with col_info:
        st.caption(f"총 {total}개 항목")

    # 총 페이지 계산
    page_size = st.session_state.kidsroom_page_size
    total_pages = max(1, (total + page_size - 1) // page_size)

    # 현재 페이지 보정
    if st.session_state.kidsroom_page >= total_pages:
        st.session_state.kidsroom_page = total_pages - 1

    page = st.session_state.kidsroom_page
    start = page * page_size
    end = start + page_size
    page_items = filtered[start:end]

    # 페이지 네비게이션
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1,1,2,4])
    with nav_col1:
        if st.button("⬅ 이전", disabled=page==0):
            st.session_state.kidsroom_page -= 1
            st.rerun()
    with nav_col2:
        if st.button("다음 ➡", disabled=page >= total_pages-1):
            st.session_state.kidsroom_page += 1
            st.rerun()
    with nav_col3:
        st.caption(f"페이지 {page+1} / {total_pages}")
    with nav_col4:
        jump = st.number_input("페이지 이동", min_value=1, max_value=total_pages, value=page+1, step=1)
        if jump-1 != page:
            st.session_state.kidsroom_page = jump-1
            st.rerun()

    # 스크롤 가능한 영역
    st.markdown("""
    <style>
    .kidsroom-scroll-wrapper {max-height:420px; overflow-y:auto; border:1px solid #ddd; padding:6px 10px; border-radius:6px; background:#fafafa;}
    .kidsroom-scroll-wrapper .streamlit-expanderHeader {font-size:0.9rem;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="kidsroom-scroll-wrapper">', unsafe_allow_html=True)
    if not page_items:
        st.warning("검색 결과 없음")
    for idx, kr in enumerate(page_items):
        global_index = filtered.index(kr)  # 원본 인덱스 (삭제/수정 반영 위해)
        with st.expander(f"{global_index+1}. {kr['name']} - {kr['address']}"):
            col1, col2, col3, col4, col5 = st.columns([2,2,1.5,1.5,1])
            new_name = col1.text_input("이름", value=kr['name'], key=f"name_{global_index}")
            new_addr = col2.text_input("주소", value=kr['address'], key=f"addr_{global_index}")
            new_lat = col3.number_input("위도", value=float(kr['lat']), format="%.6f", key=f"lat_{global_index}")
            new_lon = col4.number_input("경도", value=float(kr['lon']), format="%.6f", key=f"lon_{global_index}")

            if col5.button("💾 저장", key=f"save_{global_index}"):
                st.session_state.kidsroom_list = update_kidsroom(
                    st.session_state.kidsroom_list,
                    global_index,
                    name=new_name,
                    address=new_addr,
                    lat=new_lat,
                    lon=new_lon
                )
                st.success("저장되었습니다")
                st.rerun()

            del_col, info_col = st.columns([1,4])
            if del_col.button("🗑️ 삭제", key=f"del_{global_index}"):
                st.session_state.kidsroom_list = remove_kidsroom(st.session_state.kidsroom_list, global_index)
                st.warning("삭제되었습니다")
                # 삭제 후 페이지 재조정
                if (total-1) <= page*page_size and page>0:
                    st.session_state.kidsroom_page -= 1
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 페이지 요약
    st.caption(f"현재 표시: {start+1 if total else 0} - {min(end, total)} / {total}")


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
