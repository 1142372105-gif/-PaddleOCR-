# 用户相关接口：注册、登录、找回密码、修改个人信息
from flask import Blueprint, request, jsonify, session
from utils import query_one, execute, insert_get_id, ok, fail
import datetime

user_bp = Blueprint('user', __name__, url_prefix='/api/user')


@user_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.json
    username = data.get('username', '').strip()
    passwd = data.get('passwd', '').strip()
    email = data.get('email', '').strip()
    nickname = data.get('nickname', '').strip()
    question = data.get('question', '').strip()
    answer = data.get('answer', '').strip()

    if not username or not passwd:
        return jsonify(fail('用户名和密码不能为空'))
    if len(username) < 3 or len(username) > 50:
        return jsonify(fail('用户名长度3~50位'))
    if len(passwd) < 6:
        return jsonify(fail('密码不能少于6位'))

    # 检查用户名是否已存在
    exist = query_one('SELECT id FROM usr WHERE username=%s', (username,))
    if exist:
        return jsonify(fail('用户名已存在'))

    sql = ('INSERT INTO usr (username,passwd,role,email,nickname,question,answer,status,createdat) '
           'VALUES (%s,%s,0,%s,%s,%s,%s,1,%s)')
    uid = insert_get_id(sql, (username, passwd, email, nickname, question, answer,
                              datetime.datetime.now()))
    return jsonify(ok({'id': uid}, '注册成功'))


@user_bp.route('/login', methods=['POST'])
def login():
    """用户登录：校验密码"""
    data = request.json
    username = data.get('username', '').strip()
    passwd = data.get('passwd', '').strip()

    if not username or not passwd:
        return jsonify(fail('用户名和密码不能为空'))

    row = query_one('SELECT id,username,passwd,role,email,nickname,status FROM usr WHERE username=%s',
                    (username,))
    if not row:
        return jsonify(fail('用户不存在'))
    if row['status'] == 0:
        return jsonify(fail('账号已被禁用，请联系管理员'))
    if row['passwd'] != passwd:
        return jsonify(fail('密码错误'))

    # 写session
    session['uid'] = row['id']
    session['role'] = row['role']

    return jsonify(ok({
        'id': row['id'],
        'username': row['username'],
        'role': row['role'],
        'email': row['email'],
        'nickname': row['nickname']
    }, '登录成功'))


@user_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    session.clear()
    return jsonify(ok(None, '已退出登录'))


@user_bp.route('/find_password', methods=['POST'])
def find_password():
    """通过安全问题找回密码"""
    data = request.json
    username = data.get('username', '').strip()
    answer = data.get('answer', '').strip()
    newpasswd = data.get('newpasswd', '').strip()

    if not username or not answer or not newpasswd:
        return jsonify(fail('参数不完整'))

    row = query_one('SELECT id,question,answer FROM usr WHERE username=%s', (username,))
    if not row:
        return jsonify(fail('用户不存在'))
    if row['answer'] != answer:
        return jsonify(fail('安全问题答案错误'))
    if len(newpasswd) < 6:
        return jsonify(fail('新密码不能少于6位'))

    execute('UPDATE usr SET passwd=%s WHERE id=%s', (newpasswd, row['id']))
    return jsonify(ok(None, '密码已重置'))


@user_bp.route('/get_question', methods=['GET'])
def get_question():
    """获取安全问题（用于找回密码页面展示）"""
    username = request.args.get('username', '').strip()
    if not username:
        return jsonify(fail('请输入用户名'))
    row = query_one('SELECT question FROM usr WHERE username=%s', (username,))
    if not row:
        return jsonify(fail('用户不存在'))
    return jsonify(ok({'question': row['question']}))


@user_bp.route('/update_info', methods=['POST'])
def update_info():
    """修改个人信息（邮箱、昵称、密码）"""
    data = request.json
    uid = data.get('uid')
    email = data.get('email', '').strip()
    nickname = data.get('nickname', '').strip()
    passwd = data.get('passwd', '').strip()

    if not uid:
        return jsonify(fail('缺少用户ID'))

    fields, vals = [], []
    if email:
        fields.append('email=%s'); vals.append(email)
    if nickname:
        fields.append('nickname=%s'); vals.append(nickname)
    if passwd:
        if len(passwd) < 6:
            return jsonify(fail('密码不能少于6位'))
        fields.append('passwd=%s'); vals.append(passwd)

    if not fields:
        return jsonify(fail('没有需要更新的内容'))

    vals.append(uid)
    execute(f"UPDATE usr SET {','.join(fields)} WHERE id=%s", vals)
    return jsonify(ok(None, '个人信息已更新'))


@user_bp.route('/info', methods=['GET'])
def get_info():
    """获取单个用户详情"""
    uid = request.args.get('uid')
    if not uid:
        return jsonify(fail('缺少uid'))
    row = query_one('SELECT id,username,role,email,nickname,question,status,createdat FROM usr WHERE id=%s',
                    (uid,))
    if not row:
        return jsonify(fail('用户不存在'))
    if row.get('createdat'):
        row['createdat'] = str(row['createdat'])
    return jsonify(ok(row))

