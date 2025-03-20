from flask import Blueprint, render_template

# Tạo blueprint cho trang chính
blueprint = Blueprint('main', __name__)

@blueprint.route('/')
def root_page():
    """Trang chủ của ứng dụng"""
    return render_template('index.html') 