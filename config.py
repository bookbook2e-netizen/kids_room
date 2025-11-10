"""
설정 파일
"""

import streamlit as st

# 카카오 API 키 (Streamlit Secrets에서 로드)
try:
    KAKAO_API_KEY = st.secrets["KAKAO_API_KEY"]
except FileNotFoundError:
    # 로컬 환경에서 secrets.toml 파일이 없을 경우를 대비
    KAKAO_API_KEY = "cc95b8fce354c33266491ac0e040b376"
except KeyError:
    # secrets.toml 파일에 키가 없을 경우를 대비
    st.error("Streamlit Secrets에 KAKAO_API_KEY가 설정되지 않았습니다.")
    KAKAO_API_KEY = ""

# 기본 데이터 파일 경로
DEFAULT_CSV_FILE = "data/202510_202510_연령별인구현황_월간.csv"
DEFAULT_GEO_FILE = "data/HangJeongDong_ver20250401.geojson"
KIDSROOM_DATA_FILE = "data/kidsroom_data.json"

# 지도 설정
MAP_CENTER = [37.4, 127.13]
MAP_ZOOM_START = 12

