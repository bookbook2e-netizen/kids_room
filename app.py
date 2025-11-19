"""
성남시 인구 현황 및 키즈룸 분석 애플리케이션
"""
import streamlit as st
from streamlit_folium import st_folium

# 모듈 임포트
from data_loader import load_csv_file, load_geojson_file, process_population_data, process_geodata, merge_data
from kidsroom_manager import load_kidsroom_data, get_kidsroom_file_hash
from map_generator import create_population_map
from ui_components import render_file_upload_section, render_kidsroom_input_section


def initialize_session_state():
    """세션 스테이트 초기화"""
    if 'kidsroom_list' not in st.session_state:
        st.session_state.kidsroom_list = load_kidsroom_data()
    if 'kidsroom_file_hash' not in st.session_state:
        st.session_state.kidsroom_file_hash = get_kidsroom_file_hash()


def show_data_matching_info(merged):
    """데이터 매칭 결과 표시"""
    matched_count = merged['총인구'].notna().sum()
    total_count = len(merged)

    st.write(f"**매칭된 동 개수:** {matched_count} / {total_count}")

    if matched_count == 0:
        st.warning("⚠️ 행정구역 매칭이 되지 않았습니다. 데이터를 확인해��세요.")


def main():
    """메인 애플리케이션"""
    st.set_page_config(page_title="도시별 인구 현황 및 키즈룸 분석", layout="wide")

    st.title("🧒 도시별 동별 인구 현황 및 키즈룸 지도")
    st.markdown("행정동별 총인구 데이터와 키즈룸 위치를 결합한 지도 기반 상권 분석 시각화")

    initialize_session_state()

    csv_file_path, geo_file_path, use_files, map_type, mix_weight, opacity, city_name = render_file_upload_section()

    # ==== 사이드바 디버그 / 동기화 기능 추가 ====
    with st.sidebar.expander("데이터 동기화 & 디버그", expanded=False):
        st.caption(f"현재 kidsroom 파일 해시: {st.session_state.get('kidsroom_file_hash')}")
        always_reload = st.checkbox("매 실행마다 kidsroom_data.json 강제 재로딩", value=st.session_state.get('always_reload', False))
        st.session_state.always_reload = always_reload
        if st.button("🔄 세션 초기화"):
            st.session_state.clear()
            st.success("세션 스테이트 초기화 완료 (페이지 자동 새로고됨)")
            st.rerun()
        if st.button("📥 파일에서 강제 재로딩"):
            st.session_state.kidsroom_list = load_kidsroom_data()
            st.session_state.kidsroom_file_hash = get_kidsroom_file_hash()
            st.success("파일 재로딩 완료")
            st.rerun()
        # 데이터 요약
        kr_list = st.session_state.get('kidsroom_list', [])
        st.write(f"키즈룸 개수: {len(kr_list)}")
        if kr_list:
            preview_names = ', '.join(k['name'] for k in kr_list[:5])
            st.write(f"미리보기: {preview_names}{' ...' if len(kr_list)>5 else ''}")

    # 파일 변경 감지 또는 항상 재로딩 옵션 적용
    current_hash = get_kidsroom_file_hash()
    if st.session_state.get('always_reload'):
        st.session_state.kidsroom_list = load_kidsroom_data()
        st.session_state.kidsroom_file_hash = current_hash
    elif current_hash and current_hash != st.session_state.get('kidsroom_file_hash'):
        st.info("🔁 파일 내용 변경 감지 → 자동 재로딩")
        st.session_state.kidsroom_list = load_kidsroom_data()
        st.session_state.kidsroom_file_hash = current_hash

    # ===== 상단 지도 우선 렌더링 =====
    if use_files:
        df = load_csv_file(csv_file_path)
        gdf = load_geojson_file(geo_file_path)
        df = process_population_data(df)
        gdf_filtered = process_geodata(gdf, city_name=city_name)
        merged = merge_data(gdf_filtered, df)

        # 데이터 매칭 정보 & kidsroom ���약 상단 표시
        info_col1, info_col2 = st.columns([2,1])
        with info_col1:
            show_data_matching_info(merged)
        with info_col2:
            st.markdown("### 키즈룸 데이터")
            st.write(f"개수: {len(st.session_state.kidsroom_list)}")
            if st.session_state.kidsroom_list:
                st.caption(', '.join(k['name'] for k in st.session_state.kidsroom_list[:3]) + (" ..." if len(st.session_state.kidsroom_list)>3 else ""))

        st.subheader(f"📊 {city_name} 동별 인구 분포 지도")
        population_map = create_population_map(merged, st.session_state.kidsroom_list, opacity, map_type, mix_weight)
        st_folium(population_map, width=1200, height=600)

        st.divider()
        st.subheader("🎪 키즈룸 위치 추가 / 관리")
        render_kidsroom_input_section()
    else:
        st.info("📁 CSV와 GeoJSON 파일을 모두 업로드하거나 기본 파일을 사용해주세요.")


if __name__ == "__main__":
    main()
