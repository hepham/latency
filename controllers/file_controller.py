from flask import send_from_directory, current_app
import os
from utils.file_helpers import get_raw_filename, get_raw_file_url, find_file
from config import LATENCY_DATA_FOLDER

class FileController:
    @staticmethod
    def get_file(filename):
        """
        Phục vụ tệp từ thư mục dữ liệu
        """
        try:
            # Kiểm tra path traversal
            if ".." in filename or filename.startswith('/'):
                return "Truy cập bị từ chối", 403
            
            download = 'download' in request.args
            return send_from_directory(LATENCY_DATA_FOLDER, filename, as_attachment=download)
        except Exception as e:
            current_app.logger.error(f"Lỗi khi tải tệp {filename}: {str(e)}")
            return "Không tìm thấy tệp", 404
    
    @staticmethod
    def get_image(filename):
        """
        Phục vụ hình ảnh tĩnh từ thư mục images
        """
        try:
            return send_from_directory('views/static/images', filename)
        except Exception as e:
            current_app.logger.error(f"Lỗi khi tải hình ảnh {filename}: {str(e)}")
            return "Không tìm thấy hình ảnh", 404
    
    @staticmethod
    def get_raw_filename_api(raw_data_path, clue):
        """
        API để lấy tên tệp raw
        """
        return {
            "filename": get_raw_filename(raw_data_path, clue)
        }
    
    @staticmethod
    def get_raw_file_url_api(raw_data_path, clue, download=False):
        """
        API để lấy URL cho tệp raw
        """
        return {
            "url": get_raw_file_url(raw_data_path, clue, download)
        }
    
    @staticmethod
    def show_video(filename, raw_data_path):
        """
        Hiển thị video
        """
        from config import LATENCY_DATA_FOLDER, LATENCY_DATA_NAME
        
        full_path = os.path.join(LATENCY_DATA_FOLDER, raw_data_path, filename)
        
        if os.path.exists(full_path):
            file_url = f"/{LATENCY_DATA_NAME}/{raw_data_path}/{filename}"
            return {
                "video_url": file_url,
                "success": True
            }
        
        return {
            "success": False,
            "message": "Không tìm thấy video"
        } 