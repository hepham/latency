from flask import Blueprint, request, jsonify, render_template
from controllers.report_controller import ReportController
from controllers.utterance_controller import UtteranceController
from datetime import datetime, timedelta
from utils.file_helpers import get_graph_url

# Tạo blueprint cho tác vụ liên quan đến báo cáo
blueprint = Blueprint('report', __name__)

@blueprint.route('/set_result/<string:table>/<string:suite_id>/<string:utterance_id>/<int:year>/<int:month>/<int:week>', methods=['GET'])
def set_result_in_ids(table, suite_id, utterance_id, year, month, week):
    """Hiển thị kết quả dựa trên IDs"""
    # Tính tuần đầu và cuối của tháng
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    first_week = int(first_day.strftime('%U'))
    last_week = int(last_day.strftime('%U'))
    
    # Lấy dữ liệu từ controller
    data = UtteranceController.query_utterance_specific_data(
        table, utterance_id, year, first_week, last_week, suite_id
    )
    
    if request.headers.get('accept') == 'application/json':
        return jsonify(data)
    else:
        return render_template('set_result_ids.html', 
                              table=table,
                              suite_id=suite_id, 
                              utterance_id=utterance_id,
                              year=year,
                              month=month,
                              week=week,
                              data=data)

@blueprint.route('/report_full_data/<string:table>/<string:utterance_id>/<int:year>/<int:first_week>/<int:last_week>', methods=['GET'])
def get_table_report(table, utterance_id, year, first_week, last_week):
    """API lấy báo cáo đầy đủ"""
    suite_ids = UtteranceController.query_utterance_id(
        table, year, first_week, last_week, utterance_id
    )
    
    result = []
    for suite_id in suite_ids:
        data = ReportController.get_monthly_latency_by_utterance(
            table, suite_id, year, first_week, last_week, utterance_id
        )
        
        if data:
            formatted_data = ReportController.format_data_graph(data, [], first_week, last_week)
            result.append({
                "suite_id": suite_id,
                "data": formatted_data
            })
    
    return jsonify(result)

@blueprint.route('/utterance/data', methods=['POST'])
def get_utterance_specific_data():
    """API lấy dữ liệu cụ thể của một utterance"""
    data = request.json
    table = data.get('table')
    utterance_id = data.get('utterance_id')
    year = data.get('year')
    first_week = data.get('first_week')
    last_week = data.get('last_week')
    suite_id = data.get('suite_id')
    
    result = UtteranceController.query_utterance_specific_data(
        table, utterance_id, year, first_week, last_week, suite_id
    )
    
    # Thêm URL biểu đồ cho mỗi bản ghi
    for record in result:
        raw_data_path = record.get('raw_data_path')
        if raw_data_path:
            record['graph_url'] = get_graph_url(raw_data_path)
    
    return jsonify(result)

@blueprint.route("/monthly/<string:table>/<string:suite_id>/<int:year>/<int:month>", methods=["GET"])
def get_monthly_report_detail(table, suite_id, year, month):
    """API lấy chi tiết báo cáo hàng tháng"""
    # Tính tuần đầu và cuối của tháng
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    first_week = int(first_day.strftime('%U'))
    last_week = int(last_day.strftime('%U'))
    
    # Lấy dữ liệu từ controller
    weekly_data = ReportController.get_avg_log_by_month(table, suite_id, year, first_week, last_week)
    log_data = ReportController.query_log_latency_by_week(table, suite_id, year, first_week, last_week)
    
    # Định dạng dữ liệu cho biểu đồ
    graph_data = ReportController.format_data_graph(weekly_data, log_data, first_week, last_week)
    
    return jsonify(graph_data)

@blueprint.route("/monthly/<string:table>/<string:suite_id>/<int:year>/<int:first_week>/<int:last_week>", methods=["GET"])
def get_week_to_week_summary(table, suite_id, year, first_week, last_week):
    """API lấy tổng kết từng tuần"""
    # Lấy dữ liệu từ controller
    weekly_summary = ReportController.query_overal_summary_by_week(
        table, suite_id, year, first_week, last_week
    )
    
    log_summary = ReportController.query_log_latency_by_week(
        table, suite_id, year, first_week, last_week
    )
    
    # Định dạng dữ liệu
    result = {
        "weekly_summary": weekly_summary,
        "log_summary": log_summary,
        "graph_data": ReportController.format_data_graph(weekly_summary, log_summary, first_week, last_week)
    }
    
    return jsonify(result)

@blueprint.route("/monthly/<string:table>/<string:suite_id>/<int:year>/<int:month>", methods=["POST"])
def get_monthly_report_detail_by_utterance(table, suite_id, year, month):
    """API lấy chi tiết báo cáo hàng tháng theo utterance"""
    data = request.json
    utterance_id = data.get('utterance_id')
    
    # Tính tuần đầu và cuối của tháng
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    first_week = int(first_day.strftime('%U'))
    last_week = int(last_day.strftime('%U'))
    
    # Lấy dữ liệu dựa trên utterance
    if utterance_id:
        weekly_data = ReportController.get_monthly_latency_by_utterance(
            table, suite_id, year, first_week, last_week, utterance_id
        )
        log_data = ReportController.query_log_latency_by_week_by_utterance(
            table, suite_id, year, first_week, last_week, utterance_id
        )
    else:
        weekly_data = ReportController.get_avg_log_by_month(table, suite_id, year, first_week, last_week)
        log_data = ReportController.query_log_latency_by_week(table, suite_id, year, first_week, last_week)
    
    # Định dạng dữ liệu
    graph_data = ReportController.format_data_graph(weekly_data, log_data, first_week, last_week)
    
    return jsonify(graph_data)

@blueprint.route('/monthly_report/<string:table>/<string:suite_id>/<int:year>/<int:month>', methods=['GET'])
def get_monthly_report(table, suite_id, year, month):
    """Trang báo cáo hàng tháng"""
    # Tính tuần đầu và cuối của tháng
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    first_week = int(first_day.strftime('%U'))
    last_week = int(last_day.strftime('%U'))
    
    # Lấy dữ liệu từ controller
    report_data = ReportController.get_data_monthly_report(table, suite_id, year, month)
    outliers = ReportController.get_outlier_list(table, suite_id, year, month)
    comments = ReportController.get_comment_month(table, suite_id, year, month)
    
    result = {
        "report_data": report_data,
        "outliers": outliers,
        "comments": comments,
        "first_week": first_week,
        "last_week": last_week
    }
    
    if request.headers.get('accept') == 'application/json':
        return jsonify(result)
    else:
        return render_template('monthly_report.html', data=result)

@blueprint.route('/monthly_report/<string:table>/<int:year>/<int:month>', methods=['POST'])
def get_monthly_suite_report(table, year, month):
    """API lấy báo cáo hàng tháng của suite"""
    data = request.json
    suite_id = data.get('suite_id')
    
    if not suite_id:
        return jsonify({"error": "Missing suite_id"}), 400
    
    return get_monthly_report(table, suite_id, year, month)

@blueprint.route("/comments/<string:suite_id>/<int:year>/<int:month>", methods=['POST'])
def set_comment_month(suite_id, year, month):
    """API đặt comment cho tháng"""
    data = request.json
    comment_launch = data.get('comment_launch', '')
    comment_e2e = data.get('comment_e2e', '')
    
    ReportController.set_comment_month('monthly_comments', suite_id, year, month, comment_launch, comment_e2e)
    
    return jsonify({"success": True})

@blueprint.route('/outliners/<string:table>/<string:suite_id>/<int:year>/<int:month>')
def get_outliners(table, suite_id, year, month):
    """API lấy dữ liệu ngoại lai"""
    outliers = ReportController.get_outlier_list(table, suite_id, year, month)
    return jsonify(outliers)

@blueprint.route('/monthly_report/exclude_data/<string:table>/<string:suite_id>/<int:year>/<int:month>', methods=['GET'])
def get_exclude_data(table, suite_id, year, month):
    """API lấy dữ liệu bị loại trừ"""
    # Tính tuần đầu và cuối của tháng
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    first_week = int(first_day.strftime('%U'))
    last_week = int(last_day.strftime('%U'))
    
    # Lấy dữ liệu bị loại trừ
    exclude_data = ReportController.get_exclude_data(table, suite_id, year, first_week, last_week)
    
    return jsonify(exclude_data)

@blueprint.route('/monthly_report/<string:table>/id/<int:id>', methods=['DELETE'])
def delete_outliner(table, id):
    """API xóa ngoại lai"""
    reason = request.args.get('reason', 'Manual exclusion')
    ReportController.update_exclude_status(table, id, reason)
    
    return jsonify({"success": True}) 