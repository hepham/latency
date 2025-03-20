from flask import Blueprint, request, jsonify, render_template
from controllers.file_controller import FileController

# Tạo blueprint cho tác vụ liên quan đến tệp
blueprint = Blueprint('files', __name__)

@blueprint.route('/files/<path:filename>')
def files(filename):
    """Phục vụ tệp từ thư mục dữ liệu"""
    return FileController.get_file(filename)

@blueprint.route('/images/<path:filename>')
def get_images(filename):
    """Phục vụ hình ảnh tĩnh"""
    return FileController.get_image(filename)

@blueprint.route("/get_raw_filename", methods=['POST'])
def get_filename():
    """API để lấy tên tệp raw"""
    data = request.json
    return jsonify(FileController.get_raw_filename_api(
        data.get('raw_data_path'), 
        data.get('clue')
    ))

@blueprint.route("/get_raw_file_url", methods=['POST'])
def get_file_url():
    """API để lấy URL cho tệp raw"""
    data = request.json
    return jsonify(FileController.get_raw_file_url_api(
        data.get('raw_data_path'), 
        data.get('clue'),
        data.get('download', False)
    ))

@blueprint.route('/video', methods=['POST'])
def show_video():
    """API để hiển thị video từ request POST"""
    data = request.json
    return jsonify(FileController.show_video(
        data.get('filename'), 
        data.get('raw_data_path')
    ))

@blueprint.route('/video', methods=['GET'])
def show_video_get():
    """Trang hiển thị video từ request GET"""
    filename = request.args.get('filename')
    raw_data_path = request.args.get('raw_data_path')
    result = FileController.show_video(filename, raw_data_path)
    
    if result['success']:
        return render_template('video_player.html', video_url=result['video_url'])
    return result['message'], 404 