"""
키즈룸 데이터 관리 모듈
"""
import json
import os
from config import KIDSROOM_DATA_FILE


def load_kidsroom_data():
    """키즈룸 데이터 로드"""
    if os.path.exists(KIDSROOM_DATA_FILE):
        try:
            with open(KIDSROOM_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_kidsroom_data(data):
    """키즈룸 데이터 저장"""
    with open(KIDSROOM_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_kidsroom(kidsroom_list, name, address, lat, lon):
    """키즈룸 추가"""
    kidsroom_list.append({
        "name": name,
        "address": address,
        "lat": lat,
        "lon": lon
    })
    save_kidsroom_data(kidsroom_list)
    return kidsroom_list


def remove_kidsroom(kidsroom_list, index):
    """키즈룸 삭제"""
    kidsroom_list.pop(index)
    save_kidsroom_data(kidsroom_list)
    return kidsroom_list

