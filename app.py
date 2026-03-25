# Flask主入口文件：基于PaddleOCR的文本识别系统后端
import os
from flask import Flask
from config import UPLOAD_FOLDER, SECRET_KEY

# 注册蓝图
from routes.user import user_bp
from routes.admin_user import admin_user_bp
from routes.admin import admin_bp
from routes.record import record_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 注册所有蓝图
app.register_blueprint(user_bp)
app.register_blueprint(admin_user_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(record_bp)


# 健康检测接口
@app.route('/api/ping', methods=['GET'])
def ping():
    return {'code': 200, 'msg': 'pong', 'data': 'PaddleOCR系统运行正常'}


if __name__ == '__main__':
    # 开发模式运行，端口5000
    app.run(host='0.0.0.0', port=5000, debug=True)

