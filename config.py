"""
설정 파일
"""

import streamlit as st
import os

# 카카오 API 키 (Streamlit Secrets 또는 환경변수에서 로드)
# 우선순위: st.secrets -> 환경변수 -> 빈 문자열
_kakao_secret = st.secrets.get("KAKAO_API_KEY") if hasattr(st, 'secrets') else None
_env_key = os.environ.get("KAKAO_API_KEY")

if _kakao_secret:
    KAKAO_API_KEY = _kakao_secret
elif _env_key:
    KAKAO_API_KEY = _env_key
    st.info("환경변수 KAKAO_API_KEY 사용 중")
else:
    KAKAO_API_KEY = ""
    st.warning("KAKAO_API_KEY가 설정되지 않았습니다. .streamlit/secrets.toml 또는 환경변수로 설정하세요.")

# 기본 데이터 파일 경로
DEFAULT_CSV_FILE = "data/202510_202510_연령별인구현황_월간.csv"
DEFAULT_GEO_FILE = "data/HangJeongDong_ver20250401.geojson"
KIDSROOM_DATA_FILE = "data/kidsroom_data.json"

# 지도 설정
MAP_CENTER = [37.4, 127.13]
MAP_ZOOM_START = 12
