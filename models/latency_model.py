@classmethod
def query_log_latency_by_week(cls, table, suite_id, year, first_week, last_week):
    """
    Truy vấn độ trễ log theo tuần
    """
    sql = f"""
        SELECT 
            WEEK(timestamp, 1) as week_num,
            AVG(wakeup_latency) as avg_wakeup,
            AVG(e2e_latency) as avg_e2e
        FROM {table}
        WHERE suite_id=%s AND YEAR(timestamp)=%s 
          AND WEEK(timestamp, 1) BETWEEN %s AND %s
          AND wakeup_latency > 0 AND e2e_latency > 0
        GROUP BY WEEK(timestamp, 1)
        ORDER BY WEEK(timestamp, 1)
    """
    params = (suite_id, year, first_week, last_week)
    return query(sql, params)

@classmethod
def query_log_latency_by_week_by_utterance(cls, table, suite_id, year, first_week, last_week, utterance_id):
    """
    Truy vấn độ trễ log theo tuần cho một utterance cụ thể
    """
    sql = f"""
        SELECT 
            WEEK(timestamp, 1) as week_num,
            AVG(wakeup_latency) as avg_wakeup,
            AVG(e2e_latency) as avg_e2e
        FROM {table}
        WHERE suite_id=%s AND YEAR(timestamp)=%s 
          AND WEEK(timestamp, 1) BETWEEN %s AND %s
          AND utterance_id=%s
          AND wakeup_latency > 0 AND e2e_latency > 0
        GROUP BY WEEK(timestamp, 1)
        ORDER BY WEEK(timestamp, 1)
    """
    params = (suite_id, year, first_week, last_week, utterance_id)
    return query(sql, params)

@classmethod
def query_overal_summary_by_week(cls, table, suite_id, year, first_week, last_week, utterance_id=None):
    """
    Truy vấn tổng hợp tổng thể theo tuần
    """
    where_clause = "suite_id=%s AND YEAR(timestamp)=%s AND WEEK(timestamp, 1) BETWEEN %s AND %s AND wakeup_latency > 0 AND e2e_latency > 0"
    params = [suite_id, year, first_week, last_week]
    
    if utterance_id:
        where_clause += " AND utterance_id=%s"
        params.append(utterance_id)
    
    sql = f"""
        SELECT 
            WEEK(timestamp, 1) as week_num,
            AVG(wakeup_latency) as avg_wakeup,
            AVG(e2e_latency) as avg_e2e,
            STDDEV(wakeup_latency) as std_wakeup,
            STDDEV(e2e_latency) as std_e2e,
            COUNT(*) as count
        FROM {table}
        WHERE {where_clause}
        GROUP BY WEEK(timestamp, 1)
        ORDER BY WEEK(timestamp, 1)
    """
    
    return query(sql, tuple(params))

@classmethod
def query_overal_summary_by_month(cls, table, suite_id, year, first_week, last_week, utterance_id=None):
    """
    Truy vấn tổng hợp tổng thể theo tháng
    """
    where_clause = "suite_id=%s AND YEAR(timestamp)=%s AND WEEK(timestamp, 1) BETWEEN %s AND %s AND wakeup_latency > 0 AND e2e_latency > 0"
    params = [suite_id, year, first_week, last_week]
    
    if utterance_id:
        where_clause += " AND utterance_id=%s"
        params.append(utterance_id)
    
    sql = f"""
        SELECT 
            utterance_id,
            AVG(wakeup_latency) as avg_wakeup,
            AVG(e2e_latency) as avg_e2e,
            STDDEV(wakeup_latency) as std_wakeup,
            STDDEV(e2e_latency) as std_e2e,
            COUNT(*) as count
        FROM {table}
        WHERE {where_clause}
        GROUP BY utterance_id
        ORDER BY utterance_id
    """
    
    return query(sql, tuple(params))

@classmethod
def query_overal_log_sumary_by_month(cls, table, suite_id, year, first_week, last_week, utterance_id=None):
    """
    Truy vấn tổng hợp log tổng thể theo tháng
    """
    where_clause = "suite_id=%s AND YEAR(timestamp)=%s AND WEEK(timestamp, 1) BETWEEN %s AND %s AND wakeup_latency > 0 AND e2e_latency > 0"
    params = [suite_id, year, first_week, last_week]
    
    if utterance_id:
        where_clause += " AND utterance_id=%s"
        params.append(utterance_id)
    
    sql = f"""
        SELECT 
            utterance_id,
            AVG(wakeup_latency) as avg_wakeup,
            AVG(e2e_latency) as avg_e2e
        FROM {table}
        WHERE {where_clause}
        GROUP BY utterance_id
        ORDER BY utterance_id
    """
    
    return query(sql, tuple(params))

@classmethod
def get_suite_year_month(cls, table):
    """
    Lấy danh sách các suite, năm, tháng có sẵn
    """
    sql = f"""
        SELECT DISTINCT 
            suite_id, 
            YEAR(timestamp) as year, 
            MONTH(timestamp) as month
        FROM {table}
        ORDER BY suite_id, year DESC, month DESC
    """
    
    return query(sql)

@classmethod
def execute_raw_query(cls, sql, params=None):
    """
    Thực thi truy vấn SQL trực tiếp
    """
    return query(sql, params) 