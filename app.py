from flask import Flask
from datetime import datetime
import json
from routes import main_routes, file_routes, latency_routes, report_routes
from config import DEBUG, SECRET_KEY

# Tạo ứng dụng Flask
app = Flask(__name__, 
            template_folder='views/templates',
            static_folder='views/static')

# Cấu hình ứng dụng
app.config['DEBUG'] = DEBUG
app.config['SECRET_KEY'] = SECRET_KEY

# Custom JSON encoder để hỗ trợ datetime
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

app.json_encoder = DateTimeEncoder

# Đăng ký các route
app.register_blueprint(main_routes.blueprint)
app.register_blueprint(file_routes.blueprint)
app.register_blueprint(latency_routes.blueprint)
app.register_blueprint(report_routes.blueprint)

# CORS handling
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001) 