import os

# Cấu hình cơ sở dữ liệu
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'bixby_latency_db')
}

# Cấu hình đường dẫn
LATENCY_DATA_FOLDER = os.environ.get('LATENCY_DATA_FOLDER', '/path/to/latency/data')
LATENCY_DATA_NAME = 'files'

# Cấu hình server
SERVER_URL = os.environ.get('SERVER_URL', 'http://10.253.118.194:6001')

# Cấu hình flask
DEBUG = os.environ.get('DEBUG', True)
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key') 