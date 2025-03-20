from flask import Blueprint, request, jsonify, render_template
from controllers.latency_controller import LatencyController

# Tạo blueprint cho tác vụ liên quan đến dữ liệu độ trễ
blueprint = Blueprint('latency', __name__)

@blueprint.route('/set_result/<string:table>/<string:suite_id>/<string:set_id>')
@blueprint.route('/set_result/<string:table>/<string:suite_id>/<string:set_id>/<int:_id>')
def set_result(table, suite_id, set_id, _id=None):
    """Hiển thị kết quả của một set"""
    device_type = LatencyController.get_device_type(table, suite_id, set_id)
    latency_data = LatencyController.get_latency_data(table, suite_id, set_id, _id)
    
    if request.headers.get('accept') == 'application/json':
        return jsonify({
            'device_type': device_type,
            'latency_data': latency_data
        })
    else:
        return render_template('set_result.html', 
                              table=table,
                              suite_id=suite_id, 
                              set_id=set_id,
                              _id=_id,
                              device_type=device_type,
                              latency_data=latency_data)

@blueprint.route('/set_result/<string:table>/<string:_id>')
def set_result_only_in_id(table, _id):
    """Hiển thị kết quả dựa trên ID"""
    latency_data = LatencyController.get_latency_by_id(table, _id)
    
    if not latency_data:
        return "Không tìm thấy dữ liệu", 404
    
    return set_result(table, latency_data['suite_id'], latency_data['set_id'], _id)

@blueprint.route('/adjust_latency_values', methods=['POST'])
def adjust_latency_values():
    """API để điều chỉnh giá trị độ trễ"""
    data = request.json
    result = LatencyController.update_latency_values(data, data.get('table', 'bixby_latency'))
    return jsonify({"success": result}) 