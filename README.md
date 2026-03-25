# PaddleOCR 文本识别系统

基于 PaddleOCR 的全栈文字识别 Web 应用，支持单张/批量图片上传识别，提供用户管理与管理员后台。

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3 + Flask 3.0 |
| OCR 引擎 | PaddleOCR 2.7 + PaddlePaddle 2.6（PP-OCRv3 模型） |
| 前端 | Vue 3 + Vite |
| 数据库 | MySQL（PyMySQL） |

---

## 项目结构

```
code/
├── app.py              # Flask 入口，注册蓝图
├── config.py           # 数据库、上传目录等配置
├── ocr_engine.py       # OCR 核心模块（模型加载与识别）
├── utils.py            # 数据库工具函数
├── log_writer.py       # 操作日志写入
├── routes/
│   ├── user.py         # 用户注册/登录/找回密码
│   ├── admin_user.py   # 管理员用户管理
│   ├── admin.py        # 系统配置/日志/统计
│   └── record.py       # 图片上传与 OCR 识别记录
├── models/             # 本地 PP-OCRv3 模型文件
├── uploads/            # 上传图片存储（按年月分组）
└── frontend/           # Vue 3 前端
    └── src/views/
        ├── Login / Register / FindPwd
        ├── user/       # 普通用户页面
        └── admin/      # 管理员后台页面
```

---

## 核心功能

**用户端**
- 注册 / 登录 / 安全问题找回密码
- 单张图片上传识别，支持 10 种语言（中、英、日、韩、法、德等）
- 批量图片上传识别（数量上限可配置）
- 识别历史分页查看、手动修正结果、删除记录

**管理员后台**
- 用户管理（启用/禁用账号）
- 系统参数配置（识别阈值、批量上限、方向分类开关）
- 操作日志分页查询、关键词搜索、CSV 导出、定期清理
- 统计分析：总览数据、按月识别趋势、各语言准确率

---

## 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 准备模型

将以下模型解压后放入 `C:/ocr_models/`（或修改 `ocr_engine.py` 中的 `MODEL_DIR`）：

```
ch_PP-OCRv3_det_infer/
ch_PP-OCRv3_rec_infer/
ch_ppocr_mobile_v2.0_cls_infer/
```

### 3. 初始化数据库

```bash
mysql -u root -p < paddleocr_text_recognition_system_v1.sql
```

### 4. 启动后端

```bash
python app.py
# 默认运行在 http://localhost:5000
```

### 5. 启动前端

```bash
cd frontend
npm install
npm run dev
```

---

## 接口一览

| 模块 | 前缀 | 说明 |
|------|------|------|
| 用户 | `/api/user` | 注册、登录、找回密码、修改信息 |
| 识别记录 | `/api/record` | 上传识别、历史查询、结果编辑 |
| 管理-用户 | `/api/admin/user` | 用户列表、启用/禁用 |
| 管理-配置 | `/api/admin/config` | 系统参数读写 |
| 管理-日志 | `/api/admin/log` | 日志查询、导出、清理 |
| 管理-统计 | `/api/admin/stat` | 总览、月报、语言准确率 |

