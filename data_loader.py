"""
데이터 로드 및 처리 모듈
"""
import pandas as pd
import geopandas as gpd
import streamlit as st


def load_csv_file(file_path):
    """CSV 파일 로드"""
    try:
        if isinstance(file_path, str):
            # 파일 경로인 경우
            return pd.read_csv(file_path, encoding="cp949")
        else:
            # 업로드된 파일인 경우
            file_path.seek(0)
            try:
                return pd.read_csv(file_path, encoding="utf-8")
            except UnicodeDecodeError:
                file_path.seek(0)
                return pd.read_csv(file_path, encoding="cp949")
    except Exception as e:
        st.error(f"CSV 파일 로드 오류: {e}")
        st.stop()


def load_geojson_file(file_path):
    """GeoJSON 파일 로드"""
    try:
        return gpd.read_file(file_path)
    except Exception as e:
        st.error(f"GeoJSON 파일 로드 오류: {e}")
        st.stop()


def process_population_data(df):
    """인구 데이터 처리"""
    # 총인구 컬럼 찾기
    total_pop_col = [c for c in df.columns if '총인구' in c and '계_' in c][0]
    df['총인구'] = df[total_pop_col].replace(",", "", regex=True).astype(float)

    # 행정동 이름 정리 - 띄어쓰기 제거 및 코드 제거
    df["정규화된_행정구역"] = df["행정구역"].str.replace(r"\s+", "", regex=True).str.replace(r"\(.*\)", "", regex=True)

    return df


def process_geodata(gdf, city_name="성남시"):
    """GeoJSON 데이터 처리"""
    # 특정 도시만 필터링
    gdf_filtered = gdf[gdf["adm_nm"].str.contains(city_name)].copy()

    # GeoJSON도 띄어쓰기 제거하여 정규화
    gdf_filtered["정규화된_adm_nm"] = gdf_filtered["adm_nm"].str.replace(r"\s+", "", regex=True)

    return gdf_filtered


def merge_data(gdf_filtered, df):
    """인구 데이터와 지리 데이터 병합"""
    merged = gdf_filtered.merge(df, left_on="정규화된_adm_nm", right_on="정규화된_행정구역", how="left")
    return merged

