"""
키즈룸 데이터 관리 모듈
"""
import json
import os
import datetime
import hashlib
from config import KIDSROOM_DATA_FILE


BACKUP_DIR = os.path.join(os.path.dirname(KIDSROOM_DATA_FILE), 'backups')


def load_kidsroom_data():
    """키즈룸 데이터 로드"""
    if os.path.exists(KIDSROOM_DATA_FILE):
        try:
            with open(KIDSROOM_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def _backup_current(data):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(BACKUP_DIR, f'kidsroom_data_{ts}.json')
    try:
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def save_kidsroom_data(data):
    try:
        if os.path.exists(KIDSROOM_DATA_FILE):
            # 기존 내용 로드하여 백업
            try:
                with open(KIDSROOM_DATA_FILE, 'r', encoding='utf-8') as f:
                    old = json.load(f)
            except Exception:
                old = []
            _backup_current(old)
    except Exception:
        pass
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


def update_kidsroom(kidsroom_list, index, name=None, address=None, lat=None, lon=None):
    """기존 키즈룸 정보 수정 후 저장"""
    if 0 <= index < len(kidsroom_list):
        item = kidsroom_list[index]
        if name is not None and name.strip():
            item['name'] = name.strip()
        if address is not None and address.strip():
            item['address'] = address.strip()
        if lat is not None:
            try:
                item['lat'] = float(lat)
            except ValueError:
                pass
        if lon is not None:
            try:
                item['lon'] = float(lon)
            except ValueError:
                pass
        save_kidsroom_data(kidsroom_list)
    return kidsroom_list


def get_kidsroom_file_hash():
    """kidsroom_data.json 파일 내용 SHA256 해시 반환 (없으면 None)"""
    if os.path.exists(KIDSROOM_DATA_FILE):
        try:
            with open(KIDSROOM_DATA_FILE, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return None
    return None
