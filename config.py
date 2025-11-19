"""
설정 파일
"""

import streamlit as st
import os
import unicodedata

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
    st.warning("KAKAO_API_KEY가 설정되지 않았습니다. .streamlit/secrets.toml 또는 환경변수로 설정해주세요.")

# ===== 도시별 기본 CSV 파일 매핑 추가 =====
DEFAULT_CITY = "성남시"
CITY_FILE_MAP = {
    "성남시": "data/202510_202510_연령별인구현황_월간_성남시.csv",
    # 광주시 / 용인시 파일이 NFD(분해형)으로 저장된 환경 대응: 기존 파일명이 분해형이라도 그대로 사용
    "광주시": "data/202510_202510_연령별인구현황_월간_광주시.csv",
    "용인시": "data/202510_202510_연령별인구현황_월간_용인시.csv",
}
CITIES = list(CITY_FILE_MAP.keys())

# 기본 CSV 파일 (도시 postfix 적용)
DEFAULT_CSV_FILE = CITY_FILE_MAP.get(DEFAULT_CITY)
DEFAULT_GEO_FILE = "data/HangJeongDong_ver20250401.geojson"
KIDSROOM_DATA_FILE = "data/kidsroom_data.json"

# 지도 설정
MAP_CENTER = [37.4, 127.13]
MAP_ZOOM_START = 12


def _normalize_existing(path: str) -> str:
    """경로를 NFC/NFD 두 형태로 시도하여 실제 존재하는 파일 경로를 반환"""
    if os.path.exists(path):
        return path
    # 두 가지 Unicode 정규화 폼 모두 검사
    for form in ("NFC", "NFD"):
        candidate = unicodedata.normalize(form, path)
        if os.path.exists(candidate):
            return candidate
    return path  # 마지막으로 원본 반환 (실패 시 상위 로직에서 존재 여부 다시 판단)


def get_city_csv_path(city_name: str) -> str | None:
    """도시명을 받아 해당 CSV 경로 반환 (없으면 None), Unicode 정규화 처리 포함"""
    raw = CITY_FILE_MAP.get(city_name)
    if not raw:
        return None
    return _normalize_existing(raw)
