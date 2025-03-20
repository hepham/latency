from models.latency_model import LatencyModel
from models.comment_model import CommentModel
from models.utterance_model import UtteranceModel
from datetime import datetime, timedelta
import calendar

class ReportController:
    @staticmethod
    def get_data_monthly_report(table, suite_id, year, month):
        """
        Lấy báo cáo hàng tháng
        """
        # Tính tuần đầu và cuối của tháng
        first_day = datetime(year, month, 1)
        if month == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)
        
        first_week = int(first_day.strftime('%U'))
        last_week = int(last_day.strftime('%U'))
        
        # Lấy dữ liệu tổng hợp
        summary = ReportController.query_overal_summary_by_month(
            table, suite_id, year, first_week, last_week
        )
        
        log_summary = ReportController.query_overal_log_sumary_by_month(
            table, suite_id, year, first_week, last_week
        )
        
        # Định dạng dữ liệu
        return ReportController.format_data_overall_avg_log(summary, log_summary)
    
    @staticmethod
    def get_outlier_list(table, suite_id, year, month):
        """
        Lấy danh sách ngoại lai
        """
        # Tính tuần đầu và cuối của tháng
        first_day = datetime(year, month, 1)
        if month == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)
        
        first_week = int(first_day.strftime('%U'))
        last_week = int(last_day.strftime('%U'))
        
        # Lấy thông tin tổng thể
        overall_summary = ReportController.query_overall_summary(table, suite_id)
        
        if not overall_summary:
            return []
        
        # Tính ngưỡng để xác định ngoại lai
        avg_wakeup = overall_summary['avg_wakeup']
        avg_e2e = overall_summary['avg_e2e']
        std_wakeup = overall_summary['std_wakeup']
        std_e2e = overall_summary['std_e2e']
        
        threshold_wakeup_min = avg_wakeup - 3 * std_wakeup
        threshold_wakeup_max = avg_wakeup + 3 * std_wakeup
        threshold_e2e_min = avg_e2e - 3 * std_e2e
        threshold_e2e_max = avg_e2e + 3 * std_e2e
        
        # Lấy dữ liệu của tháng
        sql = f"""
            SELECT _id, timestamp, utterance_id, wakeup_latency, e2e_latency, raw_data_path
            FROM {table}
            WHERE suite_id=%s AND YEAR(timestamp)=%s AND MONTH(timestamp)=%s
              AND ((wakeup_latency < %s OR wakeup_latency > %s) OR (e2e_latency < %s OR e2e_latency > %s))
              AND (is_excluded=FALSE OR is_excluded IS NULL)
            ORDER BY timestamp DESC
        """
        params = (
            suite_id, year, month, 
            threshold_wakeup_min, threshold_wakeup_max, 
            threshold_e2e_min, threshold_e2e_max
        )
        
        outliers = LatencyModel.execute_raw_query(sql, params)
        
        # Thêm thông tin về ngưỡng và điểm chuẩn
        for outlier in outliers:
            outlier['avg_wakeup'] = avg_wakeup
            outlier['avg_e2e'] = avg_e2e
            outlier['std_wakeup'] = std_wakeup
            outlier['std_e2e'] = std_e2e
        
        return outliers
    
    @staticmethod
    def get_comment_month(table, suite_id, year, month):
        """
        Lấy comment của tháng
        """
        return CommentModel.query_comment_month(table, suite_id, year, month)
    
    @staticmethod
    def set_comment_month(table, suite_id, year, month, comment_launch, comment_e2e):
        """
        Thiết lập comment của tháng
        """
        return CommentModel.set_comment(table, suite_id, year, month, comment_launch, comment_e2e)
    
    @staticmethod
    def get_monthly_latency(table, year, first_week, last_week):
        """
        Lấy độ trễ theo tháng
        """
        return LatencyModel.query_monthly_latency(table, year, first_week, last_week)
    
    @staticmethod
    def get_monthly_latency_by_utterance(table, suite_id, year, first_week, last_week, utterance_id):
        """
        Lấy độ trễ theo tháng cho một utterance cụ thể
        """
        return LatencyModel.query_monthly_latency_by_utterance(table, suite_id, year, first_week, last_week, utterance_id)
    
    @staticmethod
    def get_avg_log_by_month(table, suite_id, year, first_week, last_week, utterance_id=None):
        """
        Lấy giá trị trung bình log theo tháng
        """
        return LatencyModel.query_avg_log_by_month(table, suite_id, year, first_week, last_week, utterance_id)
    
    @staticmethod
    def query_log_latency_by_week(table, suite_id, year, first_week, last_week):
        """
        Truy vấn độ trễ log theo tuần
        """
        return LatencyModel.query_log_latency_by_week(table, suite_id, year, first_week, last_week)
    
    @staticmethod
    def query_log_latency_by_week_by_utterance(table, suite_id, year, first_week, last_week, utterance_id):
        """
        Truy vấn độ trễ log theo tuần cho một utterance cụ thể
        """
        return LatencyModel.query_log_latency_by_week_by_utterance(table, suite_id, year, first_week, last_week, utterance_id)
    
    @staticmethod
    def query_overal_summary_by_week(table, suite_id, year, first_week, last_week, utterance_id=None):
        """
        Truy vấn tổng hợp tổng thể theo tuần
        """
        return LatencyModel.query_overal_summary_by_week(table, suite_id, year, first_week, last_week, utterance_id)
    
    @staticmethod
    def query_overal_summary_by_month(table, suite_id, year, first_week, last_week, utterance_id=None):
        """
        Truy vấn tổng hợp tổng thể theo tháng
        """
        return LatencyModel.query_overal_summary_by_month(table, suite_id, year, first_week, last_week, utterance_id)
    
    @staticmethod
    def query_overal_log_sumary_by_month(table, suite_id, year, first_week, last_week, utterance_id=None):
        """
        Truy vấn tổng hợp log tổng thể theo tháng
        """
        return LatencyModel.query_overal_log_sumary_by_month(table, suite_id, year, first_week, last_week, utterance_id)
    
    @staticmethod
    def query_overall_summary(table, suite_id, utterance_id=None):
        """
        Truy vấn tổng hợp tổng thể
        """
        return LatencyModel.query_overall_summary(table, suite_id, utterance_id)
    
    @staticmethod
    def get_exclude_data(table, suite_id, year, first_week, last_week):
        """
        Lấy dữ liệu bị loại trừ
        """
        return LatencyModel.query_exclude_data(table, suite_id, year, first_week, last_week)
    
    @staticmethod
    def update_exclude_status(table, id, reason):
        """
        Cập nhật trạng thái loại trừ của một bản ghi
        """
        return LatencyModel.update_exclude_status_by_id(table, id, reason)
    
    @staticmethod
    def format_data_graph(week_latencies, log_latencies, first_week, last_week):
        """
        Định dạng dữ liệu cho biểu đồ
        """
        weeks = []
        wakeup_data = []
        e2e_data = []
        log_wakeup_data = []
        log_e2e_data = []
        
        # Khởi tạo mảng tuần
        for week_num in range(first_week, last_week + 1):
            weeks.append(f"Week {week_num}")
            wakeup_data.append(None)
            e2e_data.append(None)
            log_wakeup_data.append(None)
            log_e2e_data.append(None)
        
        # Điền dữ liệu wakeup và e2e
        for latency in week_latencies:
            if first_week <= latency["week_num"] <= last_week:
                index = latency["week_num"] - first_week
                wakeup_data[index] = round(latency["avg_wakeup"], 2)
                e2e_data[index] = round(latency["avg_e2e"], 2)
        
        # Điền dữ liệu log
        for log in log_latencies:
            if first_week <= log["week_num"] <= last_week:
                index = log["week_num"] - first_week
                log_wakeup_data[index] = round(log["avg_wakeup"], 2)
                log_e2e_data[index] = round(log["avg_e2e"], 2)
        
        return {
            "weeks": weeks,
            "wakeup": wakeup_data,
            "e2e": e2e_data,
            "log_wakeup": log_wakeup_data,
            "log_e2e": log_e2e_data
        }
    
    @staticmethod
    def format_data_overall_avg_log(month_overal_summary, month_overall_log_summary):
        """
        Định dạng dữ liệu tổng thể trung bình log
        """
        categories = []
        wakeup_data = []
        e2e_data = []
        log_wakeup_data = []
        log_e2e_data = []
        count_data = []
        
        # Điền dữ liệu từ tổng hợp tổng thể
        for summary in month_overal_summary:
            categories.append(summary["utterance_id"])
            wakeup_data.append(round(summary["avg_wakeup"], 2))
            e2e_data.append(round(summary["avg_e2e"], 2))
            count_data.append(summary["count"])
        
        # Điền dữ liệu từ tổng hợp log
        for i, cat in enumerate(categories):
            found = False
            for log in month_overall_log_summary:
                if log["utterance_id"] == cat:
                    log_wakeup_data.append(round(log["avg_wakeup"], 2))
                    log_e2e_data.append(round(log["avg_e2e"], 2))
                    found = True
                    break
            
            if not found:
                log_wakeup_data.append(None)
                log_e2e_data.append(None)
        
        return {
            "categories": categories,
            "wakeup": wakeup_data,
            "e2e": e2e_data,
            "log_wakeup": log_wakeup_data,
            "log_e2e": log_e2e_data,
            "count": count_data
        }
    
    @staticmethod
    def format_suite_year_month(table):
        """
        Định dạng dữ liệu suite-year-month
        """
        data = LatencyModel.get_suite_year_month(table)
        result = {}
        
        for item in data:
            suite_id = item["suite_id"]
            year = item["year"]
            month = item["month"]
            
            if suite_id not in result:
                result[suite_id] = {}
            
            if year not in result[suite_id]:
                result[suite_id][year] = []
            
            if month not in result[suite_id][year]:
                result[suite_id][year].append(month)
        
        return result 