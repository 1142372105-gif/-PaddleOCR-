# 数据库连接配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'paddleocr_text_recognition_system_v1',
    'charset': 'utf8mb4'
}

# 上传文件存储根目录
UPLOAD_FOLDER = 'uploads'

# 允许上传的图片格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff', 'webp'}

# Flask密钥（用于session）
SECRET_KEY = 'paddleocr-secret-2026'

