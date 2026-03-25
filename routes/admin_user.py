# 管理员：用户管理接口
from flask import Blueprint, request, jsonify
from utils import query_one, query_all, execute, insert_get_id, ok, fail
import datetime

admin_user_bp = Blueprint('admin_user', __name__, url_prefix='/api/admin/user')


@admin_user_bp.route('/list', methods=['GET'])
def user_list():
    """查询用户列表，支持关键词搜索和分页"""
    keyword = request.args.get('keyword', '').strip()
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    offset = (page - 1) * size

    if keyword:
        sql = ('SELECT id,username,role,email,nickname,status,createdat FROM usr '
               'WHERE username LIKE %s OR nickname LIKE %s ORDER BY id DESC LIMIT %s OFFSET %s')
        like = f'%{keyword}%'
        rows = query_all(sql, (like, like, size, offset))
        count_row = query_one('SELECT COUNT(*) as cnt FROM usr WHERE username LIKE %s OR nickname LIKE %s',
                              (like, like))
    else:
        rows = query_all('SELECT id,username,role,email,nickname,status,createdat FROM usr '
                         'ORDER BY id DESC LIMIT %s OFFSET %s', (size, offset))
        count_row = query_one('SELECT COUNT(*) as cnt FROM usr', None)

    # 时间格式转字符串
    for r in rows:
        if r.get('createdat'):
            r['createdat'] = str(r['createdat'])
    return jsonify(ok({'list': rows, 'total': count_row['cnt']}))


@admin_user_bp.route('/add', methods=['POST'])
def add_user():
    """添加新用户"""
    data = request.json
    username = data.get('username', '').strip()
    passwd = data.get('passwd', '123456').strip()
    role = int(data.get('role', 0))
    email = data.get('email', '').strip()
    nickname = data.get('nickname', '').strip()
    question = data.get('question', '').strip()
    answer = data.get('answer', '').strip()

    if not username:
        return jsonify(fail('用户名不能为空'))
    exist = query_one('SELECT id FROM usr WHERE username=%s', (username,))
    if exist:
        return jsonify(fail('用户名已存在'))

    sql = ('INSERT INTO usr (username,passwd,role,email,nickname,question,answer,status,createdat) '
           'VALUES (%s,%s,%s,%s,%s,%s,%s,1,%s)')
    uid = insert_get_id(sql, (username, passwd, role, email, nickname, question, answer,
                               datetime.datetime.now()))
    return jsonify(ok({'id': uid}, '用户添加成功'))


@admin_user_bp.route('/update', methods=['POST'])
def update_user():
    """修改用户信息"""
    data = request.json
    uid = data.get('id')
    if not uid:
        return jsonify(fail('缺少用户ID'))

    email = data.get('email', '').strip()
    nickname = data.get('nickname', '').strip()
    role = data.get('role')
    status = data.get('status')
    passwd = data.get('passwd', '').strip()
    question = data.get('question', '').strip()
    answer = data.get('answer', '').strip()

    fields, vals = [], []
    if email != '':
        fields.append('email=%s'); vals.append(email)
    if nickname != '':
        fields.append('nickname=%s'); vals.append(nickname)
    if role is not None:
        fields.append('role=%s'); vals.append(role)
    if status is not None:
        fields.append('status=%s'); vals.append(status)
    if passwd:
        fields.append('passwd=%s'); vals.append(passwd)
    if question:
        fields.append('question=%s'); vals.append(question)
    if answer:
        fields.append('answer=%s'); vals.append(answer)

    if not fields:
        return jsonify(fail('没有要更新的字段'))

    vals.append(uid)
    execute(f"UPDATE usr SET {','.join(fields)} WHERE id=%s", vals)
    return jsonify(ok(None, '用户信息已更新'))


@admin_user_bp.route('/delete', methods=['POST'])
def delete_user():
    """删除用户"""
    data = request.json
    uid = data.get('id')
    if not uid:
        return jsonify(fail('缺少用户ID'))
    # 同步删除该用户的识别记录
    execute('DELETE FROM record WHERE uid=%s', (uid,))
    execute('DELETE FROM usr WHERE id=%s', (uid,))
    return jsonify(ok(None, '用户已删除'))


@admin_user_bp.route('/assign_role', methods=['POST'])
def assign_role():
    """分配用户角色"""
    data = request.json
    uid = data.get('id')
    role = data.get('role')
    if uid is None or role is None:
        return jsonify(fail('参数不完整'))
    execute('UPDATE usr SET role=%s WHERE id=%s', (role, uid))
    return jsonify(ok(None, '角色已更新'))

