# 操作日志写入工具：供其他模块调用记录关键操作
from utils import execute
import datetime


def write_log(uid, action, detail='', ip=''):
    """
    写入操作日志
    uid: 操作用户ID（0=系统）
    action: 操作类型描述
    detail: 操作详情
    ip: 操作者IP
    """
    try:
        execute(
            'INSERT INTO oplog (uid,action,detail,ip,createdat) VALUES (%s,%s,%s,%s,%s)',
            (uid, action, detail, ip, datetime.datetime.now())
        )
    except Exception as e:
        # 日志写入失败不影响主业务
        print(f'[日志写入失败] {e}')

