# OCR识别核心模块：调用PaddleOCR进行真实文字识别
import os
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR

# ============================================================
# 本地模型目录配置
# 模型文件统一放在项目根目录的 models/ 文件夹下
# 目录结构：
#   models/
#     ch_PP-OCRv3_det_infer/          <- 中文检测模型
#     ch_PP-OCRv3_rec_infer/          <- 中文识别模型
#     ch_ppocr_mobile_v2.0_cls_infer/ <- 方向分类模型
# ============================================================

# 模型放在纯英文路径下，避免PaddleOCR在Windows上解析中文路径时截断
# 模型已复制到 C:\ocr_models\
MODEL_DIR = 'D:/2613PaddleOCR/2613PaddleOCR/model'

# 各模型路径（中文 PP-OCRv3）
DET_MODEL_DIR = MODEL_DIR + '/ch_PP-OCRv3_det_infer'
REC_MODEL_DIR = MODEL_DIR + '/ch_PP-OCRv3_rec_infer'
CLS_MODEL_DIR = MODEL_DIR + '/ch_ppocr_mobile_v2.0_cls_infer'

# 检查模型文件是否存在
def _check_model():
    """检查本地模型是否已放置，缺失时给出提示"""
    missing = []
    for d in [DET_MODEL_DIR, REC_MODEL_DIR, CLS_MODEL_DIR]:
        if not os.path.isdir(d):
            missing.append(d)
    if missing:
        print('=' * 60)
        print('[OCR引擎] ⚠️  以下模型目录不存在，请先下载模型：')
        for m in missing:
            print(f'   缺失：{m}')
        print('下载地址：')
        print('  检测模型: https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar')
        print('  识别模型: https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar')
        print('  分类模型: https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar')
        print('  解压后放入项目根目录 models/ 文件夹下')
        print('=' * 60)
        return False
    return True

# 各语言OCR实例缓存（避免重复初始化）
_ocr_cache = {}
# 启动时检查一次模型
_model_ok = _check_model()


def get_ocr(lang='ch', use_angle=True, threshold=0.5):
    """
    获取指定语言的OCR实例（带缓存）
    中文使用本地模型；其他语言若无本地模型则自动下载到 models/ 目录
    lang: 语言代码，支持 ch/en/japan/korean/french/german 等
    use_angle: 是否启用文字方向分类
    threshold: 文本检测置信度阈值
    """
    key = f'{lang}_{use_angle}_{threshold}'
    if key not in _ocr_cache:
        if lang == 'ch' and _model_ok:
            # 中文：使用本地指定路径的模型，完全离线
            _ocr_cache[key] = PaddleOCR(
                use_angle_cls=use_angle,
                lang=lang,
                det_model_dir=DET_MODEL_DIR,   # 本地检测模型路径
                rec_model_dir=REC_MODEL_DIR,   # 本地识别模型路径
                cls_model_dir=CLS_MODEL_DIR,   # 本地分类模型路径
                det_db_thresh=threshold,
                show_log=False
            )
        else:
            # 其他语言：由PaddleOCR自动下载到 models/ 子目录
            _ocr_cache[key] = PaddleOCR(
                use_angle_cls=use_angle,
                lang=lang,
                det_db_thresh=threshold,
                show_log=False
            )
    return _ocr_cache[key]


def do_ocr(img_path, lang='ch', use_angle=True, threshold=0.5):
    """
    对图片执行OCR识别
    返回: (result_text: str, avg_confidence: float)
    """
    ocr = get_ocr(lang, use_angle, threshold)

    # 读取图片
    img = Image.open(img_path).convert('RGB')
    img_array = np.array(img)

    # 执行识别，result结构: [行, 行, ...]
    # 每行: [[[x1,y1],...], (文本, 置信度)]
    result = ocr.ocr(img_array, cls=use_angle)

    if not result or result[0] is None:
        return '', 0.0

    lines = []
    confidences = []

    for page in result:
        if page is None:
            continue
        for item in page:
            # item: [坐标点列表, (文本, 置信度)]
            text_info = item[1]
            text = text_info[0]
            conf = float(text_info[1])
            lines.append(text)
            confidences.append(conf)

    result_text = '\n'.join(lines)
    avg_conf = round(sum(confidences) / len(confidences), 4) if confidences else 0.0

    return result_text, avg_conf


def get_supported_langs():
    """返回支持的识别语言列表"""
    return [
        {'code': 'ch',      'name': '中文（简体）'},
        {'code': 'en',      'name': '英文'},
        {'code': 'japan',   'name': '日语'},
        {'code': 'korean',  'name': '韩语'},
        {'code': 'french',  'name': '法语'},
        {'code': 'german',  'name': '德语'},
        {'code': 'it',      'name': '意大利语'},
        {'code': 'es',      'name': '西班牙语'},
        {'code': 'ru',      'name': '俄语'},
        {'code': 'ar',      'name': '阿拉伯语'},
    ]

