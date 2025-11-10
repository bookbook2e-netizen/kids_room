"""
성남시 인구 현황 및 키즈룸 분석 애플리케이션
"""
import streamlit as st
from streamlit_folium import st_folium

# 모듈 임포트
from data_loader import load_csv_file, load_geojson_file, process_population_data, process_geodata, merge_data
from kidsroom_manager import load_kidsroom_data
from map_generator import create_population_map
from ui_components import render_file_upload_section, render_kidsroom_input_section


def initialize_session_state():
    """세션 스테이트 초기화"""
    if 'kidsroom_list' not in st.session_state:
        st.session_state.kidsroom_list = load_kidsroom_data()


def show_data_matching_info(merged):
    """데이터 매칭 결과 표시"""
    matched_count = merged['총인구'].notna().sum()
    total_count = len(merged)

    st.write(f"**매칭된 동 개수:** {matched_count} / {total_count}")

    if matched_count == 0:
        st.warning("⚠️ 행정구역 매칭이 되지 않았습니다. 데이터를 확인해��세요.")


def main():
    """메인 애플리케이션"""
    # 페이지 설정
    st.set_page_config(page_title="성남시 인구 현황 및 키즈룸 분석", layout="wide")

    # 제목
    st.title("🧒 성남시 동별 인구 현황 및 키즈룸 지도")
    st.markdown("행정동별 총인구 데이터와 키즈룸 위치를 결합한 지도 기반 상권 분석 시각화")

    # 세션 스테이트 초기화
    initialize_session_state()

    # 파일 업로드 섹션
    csv_file_path, geo_file_path, use_files, map_type, mix_weight, opacity = render_file_upload_section()

    if use_files:
        # 데이터 로드
        df = load_csv_file(csv_file_path)
        gdf = load_geojson_file(geo_file_path)

        # 데이터 처리
        df = process_population_data(df)
        gdf_filtered = process_geodata(gdf, city_name="성남시")

        # 데이터 병합
        merged = merge_data(gdf_filtered, df)

        # 매칭 정보 표시
        show_data_matching_info(merged)

        # 키즈룸 입력 섹션
        render_kidsroom_input_section()

        st.divider()

        # 지도 생성 및 표시
        st.subheader("📊 성남시 동별 인구 분포 지도")
        population_map = create_population_map(merged, st.session_state.kidsroom_list, opacity, map_type, mix_weight)
        st_folium(population_map, width=1200, height=600)
    else:
        st.info("📁 CSV와 GeoJSON 파일을 모두 업로드해주세요.")


if __name__ == "__main__":
    main()
