from models.latency_model import LatencyModel
from datetime import datetime

class LatencyController:
    @staticmethod
    def create_data_dummy(audio_offset, listening_start_ms, capsule_result_ms,
                          suite_id, set_id, set_timestamp,
                          utterance_id, utterance_timestamp,
                          run_id, raw_data_path):
        """
        Tạo dữ liệu latency giả lập
        """
        # Tính toán các độ trễ
        is_voice_wakeup = True
        
        wakeup_latency_ms = listening_start_ms - audio_offset[1]
        e2e_latency_ms = capsule_result_ms - audio_offset[3]
        
        if wakeup_latency_ms < 0:
            wakeup_latency_ms = -1
        
        if e2e_latency_ms < 0:
            e2e_latency_ms = -1
        
        # Chuẩn bị dữ liệu để lưu
        data_dict = {
            "device_type": "mobile",
            "is_voice_wakeup": is_voice_wakeup,
            "wakeup_latency": wakeup_latency_ms,
            "e2e_latency": e2e_latency_ms,
            "on_create_latency": 0,
            "timestamp": datetime.now(),
            "suite_id": suite_id,
            "set_id": set_id,
            "set_timestamp": set_timestamp,
            "utterance_id": utterance_id,
            "utterance_timestamp": utterance_timestamp,
            "run_id": run_id,
            "raw_data_path": raw_data_path
        }
        
        # Lưu vào CSDL
        return LatencyModel.save_data(data_dict)
    
    @staticmethod
    def save_log_info(data, table='bixby_latency', db_id=None):
        """
        Lưu thông tin log latency
        """
        return LatencyModel.save_log_info(data, table, db_id)
    
    @staticmethod
    def update_running(suite_id, set_id, is_running, table='bixby_latency'):
        """
        Cập nhật trạng thái đang chạy của một set
        """
        return LatencyModel.update_running(suite_id, set_id, is_running, table)
    
    @staticmethod
    def get_device_type(table, suite_id, set_id):
        """
        Lấy loại thiết bị
        """
        return LatencyModel.query_device_type(table, suite_id, set_id)
    
    @staticmethod
    def get_latency_by_id(table, _id):
        """
        Lấy dữ liệu latency theo ID
        """
        return LatencyModel.query_latency_with_id(table, _id)
    
    @staticmethod
    def get_latency_data(table, suite_id, set_id, _id=None):
        """
        Lấy dữ liệu latency của một set
        """
        if _id:
            return LatencyModel.query_latency_table(table, suite_id, set_id, _id)
        else:
            return LatencyModel.query_latency_table(table, suite_id, set_id)
    
    @staticmethod
    def update_latency_values(data_dict, table):
        """
        Cập nhật giá trị latency
        """
        return LatencyModel.update_latency_values(data_dict, table)
    
    @staticmethod
    def insert_dummy_data():
        """
        Chèn dữ liệu giả lập để kiểm thử
        """
        # Tạo các dữ liệu giả lập cho việc kiểm thử
        audio_offset = [0, 100, 200, 300]
        listening_start_ms = 500
        capsule_result_ms = 2000
        suite_id = "test_suite"
        set_id = f"test_set_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        set_timestamp = datetime.now()
        utterance_id = "test_utterance"
        utterance_timestamp = datetime.now()
        run_id = "test_run_1"
        raw_data_path = "test/path"
        
        # Chèn dữ liệu giả lập
        return LatencyController.create_data_dummy(
            audio_offset, listening_start_ms, capsule_result_ms,
            suite_id, set_id, set_timestamp,
            utterance_id, utterance_timestamp,
            run_id, raw_data_path
        ) 