from models.utterance_model import UtteranceModel

class UtteranceController:
    @staticmethod
    def setup_utterance_table():
        """
        Thiết lập bảng utterance
        """
        return UtteranceModel.setup_utterance_table()
    
    @staticmethod
    def query_utterance_ids(table, year, first_week, last_week):
        """
        Truy vấn danh sách utterance ID
        """
        return UtteranceModel.query_utterance_ids(table, year, first_week, last_week)
    
    @staticmethod
    def query_utterance_id(table, year, first_week, last_week, utterance_id):
        """
        Truy vấn thông tin về một utterance cụ thể
        """
        return UtteranceModel.query_utterance_id(table, year, first_week, last_week, utterance_id)
    
    @staticmethod
    def query_utterance_specific_data(table, utterance_id, year, first_week, last_week, suite_id=None):
        """
        Truy vấn dữ liệu cụ thể cho một utterance
        """
        return UtteranceModel.query_utterance_specific_data(table, utterance_id, year, first_week, last_week, suite_id) 