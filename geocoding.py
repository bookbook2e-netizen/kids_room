"""
지오코딩 모듈 - 주소를 좌표로 변환
"""
import re
import requests
import streamlit as st
from geopy.geocoders import Nominatim
from config import KAKAO_API_KEY


def geocode_with_kakao_keyword(address, headers):
    """카카오 키워드 검색 API"""
    try:
        url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        params = {"query": address}
        response = requests.get(url, headers=headers, params=params, timeout=5)

        st.info(f"카카오 키워드 검색 API 호출 - 상태 코드: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if result.get('documents'):
                doc = result['documents'][0]
                lat = float(doc['y'])
                lon = float(doc['x'])
                place_name = doc.get('place_name', '')
                found_address = doc.get('address_name', address)
                st.success(f"✅ 카카오 키워드 검색 성공: {place_name if place_name else found_address}")
                return lat, lon, found_address, place_name
            else:
                st.warning("카카오 키워드 검색: 결과 없음")
        elif response.status_code == 403:
            st.error(f"❌ 카카오 API 인증 오류 (403): API 키를 확인해주세요")
        else:
            st.warning(f"카카오 키워드 검색 실패 - 상태: {response.status_code}")
    except Exception as e:
        st.error(f"카카오 키워드 검색 오류: {str(e)}")

    return None, None, None, None


def geocode_with_kakao_address(address, headers):
    """카카오 주소 검색 API"""
    try:
        url = "https://dapi.kakao.com/v2/local/search/address.json"
        params = {"query": address}
        response = requests.get(url, headers=headers, params=params, timeout=5)

        st.info(f"카카오 주소 검색 API 호출 - 상태 코드: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if result.get('documents'):
                doc = result['documents'][0]
                lat = float(doc['y'])
                lon = float(doc['x'])
                st.success(f"✅ 카카오 주소 검색 성공!")
                return lat, lon, address, ""
            else:
                st.warning("카카오 주소 검색: 결과 없음")
        elif response.status_code == 403:
            st.error(f"❌ 카카오 API 인증 오류 (403): API 키를 확인해주세요")
            st.code(f"응답: {response.text[:200]}")
        else:
            st.warning(f"카카오 주소 검색 실패 - 상태: {response.status_code}")
            st.code(f"응답: {response.text[:200]}")
    except Exception as e:
        st.error(f"카카오 주소 검색 오류: {str(e)}")

    return None, None, None, None


def geocode_with_nominatim(address):
    """Nominatim 지오코더"""
    st.info("Nominatim 지오코더로 시도 중...")
    try:
        geolocator = Nominatim(user_agent="seongnam_kidsroom_app")
        location = geolocator.geocode(address, timeout=10)
        if location:
            st.success(f"✅ Nominatim 검색 성공")
            return location.latitude, location.longitude, address, ""
    except:
        pass

    return None, None, None, None


def geocode_address(address):
    """
    주소로 좌표 찾기 함수 (카카오 API 우선, Nominatim 백업)
    반환값: (위도, 경도, 주소, 장소명)
    """
    headers = {
        "Authorization": f"KakaoAK {KAKAO_API_KEY}",
        "KA": "sdk/1.0 os/javascript lang/ko-KR device/Win32 origin/http://localhost:8501"
    }

    # 1. 카카오 키워드 검색 API 우선 시도 (장소명 추출을 위해)
    lat, lon, found_address, place_name = geocode_with_kakao_keyword(address, headers)
    if lat and lon:
        return lat, lon, found_address, place_name

    # 2. 카카오 주소 검색 API 시도
    lat, lon, found_address, place_name = geocode_with_kakao_address(address, headers)
    if lat and lon:
        return lat, lon, found_address, place_name

    # 3. 층/호수 정보 제거한 주소로 재시도
    simplified_address = re.sub(r'\s*\d+층.*|\s*\d+호.*', '', address)
    if simplified_address != address:
        lat, lon, found_address, place_name = geocode_with_kakao_address(simplified_address, headers)
        if lat and lon:
            st.success(f"✅ 간소화된 주소로 성공: {simplified_address}")
            return lat, lon, found_address, place_name

    # 4. Nominatim으로 백업 시도
    lat, lon, found_address, place_name = geocode_with_nominatim(address)
    if lat and lon:
        return lat, lon, found_address, place_name

    return None, None, None, None

