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
            return pd.read_csv(file_path, encoding="utf-8")
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

    # 행정구역에서 동 이름만 추출
    # 예: "경기도 성남시 중원구 도촌동(4113101000)" -> "도촌동"
    # 방법: split()으로 마지막 단어를 추출한 후 괄호 제거
    df["정규화된_동명"] = df["행정구역"].apply(
        lambda x: x.split()[-1].split('(')[0] if isinstance(x, str) and '동' in x else None
    )

    return df


def process_geodata(gdf, city_name="성남시"):
    """GeoJSON 데이터 처리"""
    # 특정 도시만 필터링
    gdf_filtered = gdf[gdf["sggnm"].str.contains(city_name, na=False)].copy()

    # adm_nm에서 동 이름만 추출
    # 예: "경기도 성남시중원구 도촌동" -> "도촌동"
    # 방법: split()으로 마지막 단어를 추출
    gdf_filtered['dong_nm'] = gdf_filtered['adm_nm'].apply(
        lambda x: x.strip().split()[-1] if isinstance(x, str) and '동' in x else None
    )

    return gdf_filtered


def merge_data(gdf_filtered, df):
    """인구 데이터와 지리 데이터 병합 및 인구밀도 계산"""
    # 동 이름을 기준으로 병합
    merged = gdf_filtered.merge(df, left_on="dong_nm", right_on="정규화된_동명", how="left")

    # 면적 계산 (CRS를 EPSG:5186으로 변환하여 제곱미터 단위로 계산)
    # to_crs(5186)을 사용하면 정확한 면적 계산이 가능
    merged['면적'] = merged['geometry'].to_crs(epsg=5186).area

    # 인구밀도 계산 (명/km²)
    # 면적이 0보다 클 경우에만 계산
    merged['인구밀도'] = merged.apply(
        lambda row: (row['총인구'] / (row['면적'] / 1_000_000)) if row['면적'] > 0 else 0,
        axis=1
    )

    return merged
