"""
지도 생성 모듈
"""
import folium
import pandas as pd
from config import MAP_CENTER, MAP_ZOOM_START


def extract_dong_name(adm_nm):
    """행정동 이름에서 동 이름만 추출"""
    if ' ' in adm_nm:
        return adm_nm.split()[-1]
    else:
        return adm_nm.replace('경기도성남시', '').replace('수정구', '').replace('중원구', '').replace('분당구', '')


def create_base_map():
    """기본 지도 생성"""
    return folium.Map(location=MAP_CENTER, zoom_start=MAP_ZOOM_START)


def add_choropleth_layer(m, merged, opacity=0.7):
    """Choropleth 레이어 추가 (총인구 시각화)"""
    folium.Choropleth(
        geo_data=merged,
        data=merged,
        columns=["adm_nm", "총인구"],
        key_on="feature.properties.adm_nm",
        fill_color="YlOrRd",
        fill_opacity=opacity,
        line_opacity=0.5,
        legend_name="총인구수",
        nan_fill_color="white",
        highlight=False  # 파란색 직사각형 비활성화
    ).add_to(m)

    return m


def add_dong_layers(m, merged):
    """동별 GeoJson 레이어 추가 (마우스 오버 효과 및 라벨)"""
    # 기본 스타일 (투명)
    style_function = lambda x: {
        'fillColor': 'transparent',
        'color': 'transparent',
        'weight': 0,
        'fillOpacity': 0
    }

    # 하이라이트 스타일 (동 경계를 따라 강조)
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
                총인구: <b>{int(row['총인구']):,}명</b>
            </div>
            """

            tooltip_html = f"""
            <div style="font-family: Arial; font-size: 11px;">
                <b>{dong_name}</b><br>
                {int(row['총인구']):,}명
            </div>
            """

            # GeoJson 레이어 (마우스 오버 시 동 경계를 따라 강조)
            folium.GeoJson(
                row['geometry'],
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


def create_population_map(merged, kidsroom_list, opacity=0.7):
    """전체 인구 지도 생성"""
    m = create_base_map()
    m = add_choropleth_layer(m, merged, opacity)
    m = add_dong_layers(m, merged)
    m = add_kidsroom_markers(m, kidsroom_list)
    return m

