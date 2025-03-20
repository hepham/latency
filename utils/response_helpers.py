from flask import jsonify, render_template

def api_response(data, status=200):
    """
    Tạo response API chuẩn
    """
    return jsonify(data), status

def error_response(message, status=400):
    """
    Tạo response lỗi chuẩn
    """
    return jsonify({"error": message}), status

def template_or_json(template_name, data, accept_json=None):
    """
    Trả về template hoặc JSON dựa trên accept header
    """
    if accept_json is None:
        from flask import request
        accept_json = request.headers.get('accept') == 'application/json'
    
    if accept_json:
        return jsonify(data)
    else:
        return render_template(template_name, data=data) 