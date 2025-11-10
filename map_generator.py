"""
지도 생성 모듈
"""
import folium
import pandas as pd
from config import MAP_CENTER, MAP_ZOOM_START


def extract_dong_name(adm_nm):
    """행정동 이름에서 동 이름만 추출"""
    parts = adm_nm.split()
    if len(parts) > 1:
        return parts[-1]
    else:
        return adm_nm.split('구')[-1] if '구' in adm_nm else adm_nm


def create_base_map():
    """기본 지도 생성"""
    return folium.Map(location=MAP_CENTER, zoom_start=MAP_ZOOM_START)


def _build_feature_collection(gdf: pd.DataFrame, value_cols: list[str]):
    """GeoDataFrame으로부터 안전한 FeatureCollection(dict) 생성.
    모든 행에 geometry.__geo_interface__와 필요한 속성(adm_nm + value_cols)을 포함.
    Folium.Choropleth가 기대하는 feature.properties 구조를 강제로 맞춘다."""
    features = []
    for _, row in gdf.iterrows():
        geom = None
        try:
            geom = row['geometry'].__geo_interface__
        except Exception:
            continue  # geometry 없으면 스킵
        props = {'adm_nm': row.get('adm_nm', '')}
        for c in value_cols:
            if c in row:
                v = row[c]
                try:
                    v = float(v)
                except Exception:
                    pass
                props[c] = v
        features.append({'type': 'Feature', 'geometry': geom, 'properties': props})
    return {'type': 'FeatureCollection', 'features': features}


def add_choropleth_layer(m, merged, opacity=0.7, map_type='총인구', mix_weight=None):
    """Choropleth 레이어 추가 (총인구 또는 인구밀도 시각화) - 안전한 FeatureCollection 사용"""

    # 시각화 기준에 따라 컬럼과 색상 맵 선택
    if map_type == '인구밀도':
        columns = ["adm_nm", "인구밀도"]
        fill_color = "PuBuGn"
        legend_name = "인구밀도 (명/km²)"
    else:
        columns = ["adm_nm", "총인구"]
        fill_color = "YlOrRd"
        legend_name = "총인구수"

    # 안전한 FeatureCollection 구성
    geojson_fc = _build_feature_collection(merged, [columns[1]])
    if not geojson_fc['features']:
        folium.map.CustomPane('warning').add_to(m)
        folium.Marker(MAP_CENTER, icon=folium.DivIcon(html="""
        <div style='background:white;border:1px solid #999;padding:6px;border-radius:4px;font-size:12px;'>
        ⚠ 데이터 매칭된 행정동이 없습니다.
        </div>"""))
        return m

    folium.Choropleth(
        geo_data=geojson_fc,
        data=merged,
        columns=columns,
        key_on="feature.properties.adm_nm",
        fill_color=fill_color,
        fill_opacity=opacity,
        line_opacity=0.5,
        legend_name=legend_name,
        nan_fill_color="white",
        highlight=False
    ).add_to(m)

    return m


def add_dong_layers(m, merged):
    """동별 GeoJson 레이어 추가 (마우스 오버 효과 및 라벨)"""
    style_function = lambda x: {
        'fillColor': 'transparent',
        'color': 'transparent',
        'weight': 0,
        'fillOpacity': 0
    }

    highlight_function = lambda x: {
        'fillColor': '#ffff00',
        'color': '#ff6600',
        'weight': 3,
        'fillOpacity': 0.4,
        'dashArray': '5, 5'
    }

    for _, row in merged.iterrows():
        if pd.notnull(row.get("총인구")):
            dong_name = extract_dong_name(row['adm_nm'])

            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px;">
                <b>{row['adm_nm']}</b><br>
                총인구: <b>{int(row.get('총인구',0)):,}명</b><br>
                인구밀도: <b>{int(row.get('인구밀도',0)):,}명/km²</b>
            </div>
            """

            tooltip_html = f"""
            <div style="font-family: Arial; font-size: 11px;">
                <b>{dong_name}</b><br>
                {int(row.get('총인구',0)):,}명
            </div>
            """

            folium.GeoJson(
                row['geometry'].__geo_interface__,
                style_function=style_function,
                highlight_function=highlight_function,
                tooltip=folium.Tooltip(tooltip_html),
                popup=folium.Popup(popup_html, max_width=250),
                smooth_factor=1.0
            ).add_to(m)

            # 동 이름 라벨
            centroid = row['geometry'].centroid
            folium.Marker(
                location=[centroid.y, centroid.x],
                icon=folium.DivIcon(html=f"""
                    <div style="
                        font-size: 9px;
                        color: rgba(0, 0, 0, 0.4);
                        font-weight: bold;
                        text-align: center;
                        white-space: nowrap;
                        text-shadow: 1px 1px 1px white, -1px -1px 1px white, 1px -1px 1px white, -1px 1px 1px white;
                    ">{dong_name}</div>
                """)
            ).add_to(m)

    return m


def add_kidsroom_markers(m, kidsroom_list):
    """키즈룸 마커 추가"""
    for kr in kidsroom_list:
        folium.Marker(
            location=[kr["lat"], kr["lon"]],
            popup=folium.Popup(f"<b>🎪 {kr['name']}</b><br>{kr['address']}", max_width=250),
            tooltip=kr["name"],
            icon=folium.Icon(color="red", icon="child", prefix="fa")
        ).add_to(m)

    return m


def create_population_map(merged, kidsroom_list, opacity=0.7, map_type='총인구', mix_weight=None):
    """전체 인구 지도 생성 (map_type: '총인구' 또는 '인구밀도')"""
    m = create_base_map()
    m = add_choropleth_layer(m, merged, opacity, map_type, mix_weight)
    m = add_dong_layers(m, merged)
    m = add_kidsroom_markers(m, kidsroom_list)
    return m
