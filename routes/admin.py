# 管理员：系统配置、日志管理、统计分析接口
from flask import Blueprint, request, jsonify, make_response
from utils import query_one, query_all, execute, ok, fail
import datetime, csv, io

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


# =================== 系统配置 ===================

@admin_bp.route('/config/list', methods=['GET'])
def config_list():
    """获取所有系统配置"""
    rows = query_all('SELECT id,cfgkey,cfgval,remark,updatedat FROM config ORDER BY id', None)
    for r in rows:
        if r.get('updatedat'):
            r['updatedat'] = str(r['updatedat'])
    return jsonify(ok(rows))


@admin_bp.route('/config/update', methods=['POST'])
def config_update():
    """更新系统配置项"""
    data = request.json
    cfg_id = data.get('id')
    cfgval = data.get('cfgval', '').strip()
    remark = data.get('remark', '').strip()

    if not cfg_id:
        return jsonify(fail('缺少配置ID'))

    fields, vals = [], []
    fields.append('cfgval=%s'); vals.append(cfgval)
    if remark:
        fields.append('remark=%s'); vals.append(remark)
    vals.append(cfg_id)
    execute(f"UPDATE config SET {','.join(fields)} WHERE id=%s", vals)
    return jsonify(ok(None, '配置已更新'))


# =================== 日志管理 ===================

@admin_bp.route('/log/list', methods=['GET'])
def log_list():
    """分页查询操作日志"""
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 20))
    keyword = request.args.get('keyword', '').strip()
    offset = (page - 1) * size

    if keyword:
        sql = ('SELECT o.id,o.uid,u.username,o.action,o.detail,o.ip,o.createdat '
               'FROM oplog o LEFT JOIN usr u ON o.uid=u.id '
               'WHERE o.action LIKE %s OR o.detail LIKE %s '
               'ORDER BY o.id DESC LIMIT %s OFFSET %s')
        like = f'%{keyword}%'
        rows = query_all(sql, (like, like, size, offset))
        cnt = query_one('SELECT COUNT(*) as cnt FROM oplog WHERE action LIKE %s OR detail LIKE %s',
                        (like, like))
    else:
        rows = query_all('SELECT o.id,o.uid,u.username,o.action,o.detail,o.ip,o.createdat '
                         'FROM oplog o LEFT JOIN usr u ON o.uid=u.id '
                         'ORDER BY o.id DESC LIMIT %s OFFSET %s', (size, offset))
        cnt = query_one('SELECT COUNT(*) as cnt FROM oplog', None)

    for r in rows:
        if r.get('createdat'):
            r['createdat'] = str(r['createdat'])
    return jsonify(ok({'list': rows, 'total': cnt['cnt']}))


@admin_bp.route('/log/export', methods=['GET'])
def log_export():
    """导出日志为CSV"""
    rows = query_all('SELECT o.id,u.username,o.action,o.detail,o.ip,o.createdat '
                     'FROM oplog o LEFT JOIN usr u ON o.uid=u.id ORDER BY o.id DESC', None)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', '操作用户', '操作动作', '操作详情', 'IP地址', '操作时间'])
    for r in rows:
        writer.writerow([r['id'], r.get('username', '系统'), r['action'],
                         r['detail'], r['ip'], str(r['createdat'])])
    resp = make_response(output.getvalue())
    resp.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
    resp.headers['Content-Disposition'] = 'attachment; filename=oplog.csv'
    return resp


@admin_bp.route('/log/clear', methods=['POST'])
def log_clear():
    """清空历史日志（保留最近30天）"""
    cutoff = datetime.datetime.now() - datetime.timedelta(days=30)
    execute('DELETE FROM oplog WHERE createdat < %s', (cutoff,))
    return jsonify(ok(None, '历史日志已清空'))


# =================== 统计分析 ===================

@admin_bp.route('/stat/overview', methods=['GET'])
def stat_overview():
    """识别统计总览"""
    total_user = query_one('SELECT COUNT(*) as cnt FROM usr WHERE role=0', None)
    total_record = query_one('SELECT COUNT(*) as cnt FROM record', None)
    success_record = query_one("SELECT COUNT(*) as cnt FROM record WHERE status=1", None)
    avg_conf = query_one("SELECT ROUND(AVG(confidence),4) as avg FROM record WHERE status=1", None)

    return jsonify(ok({
        'totalUser': total_user['cnt'],
        'totalRecord': total_record['cnt'],
        'successRecord': success_record['cnt'],
        'avgConfidence': float(avg_conf['avg']) if avg_conf['avg'] else 0
    }))


@admin_bp.route('/stat/monthly', methods=['GET'])
def stat_monthly():
    """按月统计识别数量（用于报表）"""
    rows = query_all(
        "SELECT DATE_FORMAT(createdat,'%Y-%m') as mon, COUNT(*) as cnt, "
        "SUM(status=1) as success, SUM(status=2) as fail "
        "FROM record GROUP BY mon ORDER BY mon",
        None
    )
    return jsonify(ok(rows))


@admin_bp.route('/stat/accuracy', methods=['GET'])
def stat_accuracy():
    """各语言识别准确率分析"""
    rows = query_all(
        "SELECT lang, COUNT(*) as total, SUM(status=1) as success, "
        "ROUND(AVG(CASE WHEN status=1 THEN confidence ELSE 0 END),4) as avgconf "
        "FROM record GROUP BY lang",
        None
    )
    return jsonify(ok(rows))

