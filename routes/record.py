# 图片上传与OCR识别接口
import os
import uuid
import datetime
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from utils import query_one, query_all, execute, insert_get_id, ok, fail
from ocr_engine import do_ocr, get_supported_langs

record_bp = Blueprint('record', __name__, url_prefix='/api/record')


def allowed_file(filename):
    """检查文件扩展名是否合法"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_save_path():
    """生成按年月分组的上传目录"""
    now = datetime.datetime.now()
    folder = os.path.join(UPLOAD_FOLDER, str(now.year), f'{now.month:02d}')
    os.makedirs(folder, exist_ok=True)
    return folder


@record_bp.route('/upload', methods=['POST'])
def upload():
    """单张图片上传并立即识别"""
    uid = request.form.get('uid')
    lang = request.form.get('lang', 'ch')

    if not uid:
        return jsonify(fail('缺少用户ID'))
    if 'file' not in request.files:
        return jsonify(fail('未选择文件'))

    file = request.files['file']
    if file.filename == '':
        return jsonify(fail('文件名为空'))
    if not allowed_file(file.filename):
        return jsonify(fail('不支持的文件格式'))

    # 读取OCR参数配置
    threshold_cfg = query_one("SELECT cfgval FROM config WHERE cfgkey='ocr.threshold'", None)
    angle_cfg = query_one("SELECT cfgval FROM config WHERE cfgkey='ocr.useangle'", None)
    threshold = float(threshold_cfg['cfgval']) if threshold_cfg else 0.5
    use_angle = angle_cfg['cfgval'] == '1' if angle_cfg else True

    # 保存文件
    original_name = file.filename
    ext = original_name.rsplit('.', 1)[1].lower()
    save_folder = get_save_path()
    new_name = f'{uuid.uuid4().hex}.{ext}'
    save_path = os.path.join(save_folder, new_name)
    file.save(save_path)

    # 数据库路径用正斜杠
    db_path = save_path.replace('\\', '/')

    # 先插入处理中记录
    sql = ('INSERT INTO record (uid,imgpath,imgname,lang,result,confidence,status,createdat) '
           'VALUES (%s,%s,%s,%s,NULL,0,0,%s)')
    rec_id = insert_get_id(sql, (uid, db_path, original_name, lang, datetime.datetime.now()))

    # 调用OCR识别
    try:
        result_text, avg_conf = do_ocr(save_path, lang=lang, use_angle=use_angle, threshold=threshold)
        execute('UPDATE record SET result=%s,confidence=%s,status=1 WHERE id=%s',
                (result_text, avg_conf, rec_id))
        return jsonify(ok({'id': rec_id, 'result': result_text, 'confidence': avg_conf}, '识别成功'))
    except Exception as e:
        execute('UPDATE record SET status=2 WHERE id=%s', (rec_id,))
        return jsonify(fail(f'识别失败：{str(e)}'))


@record_bp.route('/batch_upload', methods=['POST'])
def batch_upload():
    """批量图片上传并识别"""
    uid = request.form.get('uid')
    lang = request.form.get('lang', 'ch')

    if not uid:
        return jsonify(fail('缺少用户ID'))

    # 批量数量限制
    batch_cfg = query_one("SELECT cfgval FROM config WHERE cfgkey='ocr.batchmax'", None)
    batch_max = int(batch_cfg['cfgval']) if batch_cfg else 20
    threshold_cfg = query_one("SELECT cfgval FROM config WHERE cfgkey='ocr.threshold'", None)
    angle_cfg = query_one("SELECT cfgval FROM config WHERE cfgkey='ocr.useangle'", None)
    threshold = float(threshold_cfg['cfgval']) if threshold_cfg else 0.5
    use_angle = angle_cfg['cfgval'] == '1' if angle_cfg else True

    files = request.files.getlist('files')
    if not files:
        return jsonify(fail('未选择文件'))
    if len(files) > batch_max:
        return jsonify(fail(f'批量上传最多{batch_max}张'))

    results = []
    for file in files:
        if not allowed_file(file.filename):
            results.append({'filename': file.filename, 'status': 'error', 'msg': '格式不支持'})
            continue
        original_name = file.filename
        ext = original_name.rsplit('.', 1)[1].lower()
        save_folder = get_save_path()
        new_name = f'{uuid.uuid4().hex}.{ext}'
        save_path = os.path.join(save_folder, new_name)
        file.save(save_path)
        db_path = save_path.replace('\\', '/')
        sql = ('INSERT INTO record (uid,imgpath,imgname,lang,result,confidence,status,createdat) '
               'VALUES (%s,%s,%s,%s,NULL,0,0,%s)')
        rec_id = insert_get_id(sql, (uid, db_path, original_name, lang, datetime.datetime.now()))
        try:
            result_text, avg_conf = do_ocr(save_path, lang=lang, use_angle=use_angle, threshold=threshold)
            execute('UPDATE record SET result=%s,confidence=%s,status=1 WHERE id=%s',
                    (result_text, avg_conf, rec_id))
            results.append({'id': rec_id, 'filename': original_name, 'status': 'ok',
                            'result': result_text, 'confidence': avg_conf})
        except Exception as e:
            execute('UPDATE record SET status=2 WHERE id=%s', (rec_id,))
            results.append({'id': rec_id, 'filename': original_name, 'status': 'error', 'msg': str(e)})

    return jsonify(ok(results, '批量识别完成'))


@record_bp.route('/list', methods=['GET'])
def record_list():
    """查询当前用户的识别历史（分页）"""
    uid = request.args.get('uid')
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    offset = (page - 1) * size

    if not uid:
        return jsonify(fail('缺少uid'))

    rows = query_all('SELECT id,imgname,lang,result,confidence,status,createdat '
                     'FROM record WHERE uid=%s ORDER BY id DESC LIMIT %s OFFSET %s',
                     (uid, size, offset))
    cnt = query_one('SELECT COUNT(*) as cnt FROM record WHERE uid=%s', (uid,))
    for r in rows:
        if r.get('createdat'):
            r['createdat'] = str(r['createdat'])
    return jsonify(ok({'list': rows, 'total': cnt['cnt']}))


@record_bp.route('/detail', methods=['GET'])
def record_detail():
    """获取单条识别记录详情"""
    rid = request.args.get('id')
    row = query_one('SELECT id,uid,imgpath,imgname,lang,result,confidence,status,createdat '
                    'FROM record WHERE id=%s', (rid,))
    if not row:
        return jsonify(fail('记录不存在'))
    if row.get('createdat'):
        row['createdat'] = str(row['createdat'])
    return jsonify(ok(row))


@record_bp.route('/update', methods=['POST'])
def record_update():
    """编辑识别结果（用户手动修正）"""
    data = request.json
    rid = data.get('id')
    result = data.get('result', '')
    if not rid:
        return jsonify(fail('缺少记录ID'))
    execute('UPDATE record SET result=%s WHERE id=%s', (result, rid))
    return jsonify(ok(None, '识别结果已更新'))


@record_bp.route('/delete', methods=['POST'])
def record_delete():
    """删除识别记录"""
    data = request.json
    rid = data.get('id')
    if not rid:
        return jsonify(fail('缺少记录ID'))
    # 删除前查出图片路径（可选：删除本地文件）
    row = query_one('SELECT imgpath FROM record WHERE id=%s', (rid,))
    if row and os.path.exists(row['imgpath']):
        try:
            os.remove(row['imgpath'])
        except Exception:
            pass
    execute('DELETE FROM record WHERE id=%s', (rid,))
    return jsonify(ok(None, '记录已删除'))


@record_bp.route('/langs', methods=['GET'])
def langs():
    """获取支持的识别语言列表"""
    return jsonify(ok(get_supported_langs()))


@record_bp.route('/image/<path:imgpath>', methods=['GET'])
def get_image(imgpath):
    """提供上传图片的访问"""
    return send_from_directory('.', imgpath)

