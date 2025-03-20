from .base import BaseModel
from ..utils.db_connection import execute_query, query

class CommentModel(BaseModel):
    """
    Model cho dữ liệu comment
    """
    
    @classmethod
    def setup_comment_table(cls):
        """
        Thiết lập bảng comment
        """
        sql = """
            CREATE TABLE IF NOT EXISTS monthly_comments (
              _id INT PRIMARY KEY AUTO_INCREMENT
            , suite_id VARCHAR(50) NOT NULL
            , year INT NOT NULL
            , month INT NOT NULL
            , comment_launch TEXT
            , comment_e2e TEXT
            )
        """
        execute_query(sql)
    
    @classmethod
    def query_comment_month(cls, table, suite_id, year, month):
        """
        Truy vấn comment của tháng
        """
        sql = """
            SELECT comment_launch, comment_e2e
            FROM monthly_comments
            WHERE suite_id=%s AND year=%s AND month=%s
        """
        params = (suite_id, year, month)
        result = query(sql, params)
        
        if result:
            return result[0]
        return {"comment_launch": "", "comment_e2e": ""}
    
    @classmethod
    def set_comment(cls, table, suite_id, year, month, comment_launch, comment_e2e):
        """
        Thiết lập comment của tháng
        """
        # Kiểm tra xem comment đã tồn tại chưa
        check_sql = """
            SELECT _id FROM monthly_comments
            WHERE suite_id=%s AND year=%s AND month=%s
        """
        check_params = (suite_id, year, month)
        existing = query(check_sql, check_params)
        
        if existing:
            # Cập nhật comment hiện có
            update_sql = """
                UPDATE monthly_comments
                SET comment_launch=%s, comment_e2e=%s
                WHERE _id=%s
            """
            update_params = (comment_launch, comment_e2e, existing[0]['_id'])
            execute_query(update_sql, update_params)
        else:
            # Tạo comment mới
            insert_sql = """
                INSERT INTO monthly_comments (suite_id, year, month, comment_launch, comment_e2e)
                VALUES (%s, %s, %s, %s, %s)
            """
            insert_params = (suite_id, year, month, comment_launch, comment_e2e)
            execute_query(insert_sql, insert_params)
        
        return True 