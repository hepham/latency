import os
import glob
from flask import url_for
from config import LATENCY_DATA_FOLDER, LATENCY_DATA_NAME, SERVER_URL

def get_set_result_id_url(table, suite_id, set_id, _id):
    """
    Tạo URL cho trang kết quả set cụ thể
    """
    return f"{SERVER_URL}/set_result/{table}/{suite_id}/{set_id}/{_id}"

def get_raw_file_url(raw_data_path, clue, download=False):
    """
    Tạo URL cho tệp raw data
    """
    filename = get_raw_filename(raw_data_path, clue)
    if filename:
        file_url = f"/{LATENCY_DATA_NAME}/{raw_data_path}/{filename}"
        if download:
            file_url += "?download=true"
        return file_url
    return ""

def get_raw_filename(raw_data_path, clue):
    """
    Lấy tên tệp raw data dựa trên đường dẫn và từ khóa
    """
    file_path = find_file(os.path.join(LATENCY_DATA_FOLDER, raw_data_path, clue))
    if file_path:
        filename = os.path.basename(file_path)
        return filename
    return ""

def find_file(path):
    """
    Tìm tệp dựa trên pattern
    """
    files = glob.glob(path)
    return files[0] if files and len(files) > 0 else None

def get_graph_url(raw_data_path):
    """
    Tạo URL cho biểu đồ
    """
    return get_raw_file_url(raw_data_path, "*.png")

def get_dashboard_url(table, suite_id, set_id):
    """
    Tạo URL cho dashboard
    """
    return f"{SERVER_URL}/set_result/{table}/{suite_id}/{set_id}" 