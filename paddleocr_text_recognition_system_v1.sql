-- ============================================================
-- 数据库名：paddleocr_text_recognition_system_v1
-- 编码：UTF-8
-- 说明：基于PaddleOCR的文本识别系统数据库
-- ============================================================

CREATE DATABASE IF NOT EXISTS `paddleocr_text_recognition_system_v1`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE `paddleocr_text_recognition_system_v1`;

-- ============================================================
-- 表1：用户表（存储所有用户信息，含管理员和普通用户）
-- ============================================================
CREATE TABLE `usr` (
  `id`         INT          NOT NULL AUTO_INCREMENT COMMENT '用户主键ID',
  `username`   VARCHAR(50)  NOT NULL                COMMENT '用户名，唯一',
  `passwd`     VARCHAR(50)  NOT NULL                COMMENT '用户密码（明文）',
  `role`       TINYINT      NOT NULL DEFAULT 0      COMMENT '角色：0普通用户 1管理员',
  `email`      VARCHAR(100) NOT NULL DEFAULT ''     COMMENT '邮箱地址',
  `nickname`   VARCHAR(50)  NOT NULL DEFAULT ''     COMMENT '用户昵称',
  `question`   VARCHAR(200) NOT NULL DEFAULT ''     COMMENT '密码找回安全问题',
  `answer`     VARCHAR(200) NOT NULL DEFAULT ''     COMMENT '安全问题答案',
  `status`     TINYINT      NOT NULL DEFAULT 1      COMMENT '账号状态：0禁用 1启用',
  `createdat`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ============================================================
-- 表2：系统配置表（OCR参数配置，管理员维护）
-- ============================================================
CREATE TABLE `config` (
  `id`         INT          NOT NULL AUTO_INCREMENT COMMENT '配置主键ID',
  `cfgkey`     VARCHAR(100) NOT NULL                COMMENT '配置键名',
  `cfgval`     VARCHAR(500) NOT NULL DEFAULT ''     COMMENT '配置值',
  `remark`     VARCHAR(200) NOT NULL DEFAULT ''     COMMENT '配置说明',
  `updatedat`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_cfgkey` (`cfgkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';

-- ============================================================
-- 表3：识别记录表（存储用户上传图片及识别结果）
-- ============================================================
CREATE TABLE `record` (
  `id`         INT          NOT NULL AUTO_INCREMENT COMMENT '记录主键ID',
  `uid`        INT          NOT NULL                COMMENT '所属用户ID，关联usr.id',
  `imgpath`    VARCHAR(500) NOT NULL                COMMENT '图片存储路径',
  `imgname`    VARCHAR(200) NOT NULL DEFAULT ''     COMMENT '原始文件名',
  `lang`       VARCHAR(20)  NOT NULL DEFAULT 'ch'   COMMENT '识别语言',
  `result`     LONGTEXT                             COMMENT '识别结果文本',
  `confidence` FLOAT        NOT NULL DEFAULT 0      COMMENT '平均置信度（0~1）',
  `status`     TINYINT      NOT NULL DEFAULT 0      COMMENT '识别状态：0处理中 1成功 2失败',
  `createdat`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
  PRIMARY KEY (`id`),
  KEY `idx_uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='识别记录表';

-- ============================================================
-- 表4：操作日志表（记录系统关键操作，支持管理员查看导出）
-- ============================================================
CREATE TABLE `oplog` (
  `id`         INT          NOT NULL AUTO_INCREMENT COMMENT '日志主键ID',
  `uid`        INT          NOT NULL DEFAULT 0      COMMENT '操作用户ID，0表示系统',
  `action`     VARCHAR(100) NOT NULL                COMMENT '操作动作描述',
  `detail`     VARCHAR(500) NOT NULL DEFAULT ''     COMMENT '操作详情',
  `ip`         VARCHAR(50)  NOT NULL DEFAULT ''     COMMENT '操作者IP地址',
  `createdat`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  PRIMARY KEY (`id`),
  KEY `idx_uid` (`uid`),
  KEY `idx_createdat` (`createdat`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';

-- ============================================================
-- 初始化数据
-- ============================================================

-- 插入管理员账号（密码明文：123456）
INSERT INTO `usr` (`username`,`passwd`,`role`,`email`,`nickname`,`question`,`answer`,`status`,`createdat`) VALUES
('admin','123456',1,'admin@ocrtest.com','超级管理员','您的出生城市是哪里？','北京','1','2026-01-01 08:00:00'),
('manager','123456',1,'manager@ocrtest.com','运营管理员','您母亲的姓名是什么？','李芳','1','2026-01-05 09:00:00');

-- 插入普通用户（密码明文：123456）
INSERT INTO `usr` (`username`,`passwd`,`role`,`email`,`nickname`,`question`,`answer`,`status`,`createdat`) VALUES
('zhangsan','123456',0,'zhangsan@qq.com','张三','您的小学名称是什么？','朝阳小学','1','2026-01-10 10:00:00'),
('lisi','123456',0,'lisi@163.com','李四','您的第一辆车品牌？','丰田','1','2026-01-12 14:30:00'),
('wangwu','123456',0,'wangwu@gmail.com','王五','您最喜欢的颜色？','蓝色','1','2026-01-15 11:00:00'),
('zhaoliu','123456',0,'zhaoliu@sina.com','赵六','您的毕业大学名称？','清华大学','1','2026-02-01 09:00:00'),
('qianqi','123456',0,'qianqi@qq.com','钱七','您宠物的名字？','小白','1','2026-02-10 16:00:00'),
('sunba','123456',0,'sunba@163.com','孙八','您的身份证前6位？','110101','0','2026-02-15 08:30:00');

-- 插入系统配置
INSERT INTO `config` (`cfgkey`,`cfgval`,`remark`,`updatedat`) VALUES
('ocr.lang','ch','默认识别语言','2026-01-01 08:00:00'),
('ocr.threshold','0.5','文本检测置信度阈值','2026-01-01 08:00:00'),
('ocr.useangle','1','是否启用方向分类（1是 0否）','2026-01-01 08:00:00'),
('ocr.maxsize','10','上传图片最大尺寸(MB)','2026-01-01 08:00:00'),
('ocr.batchmax','20','单次批量上传最大数量','2026-01-01 08:00:00'),
('sys.title','PaddleOCR文本识别系统','系统名称','2026-01-01 08:00:00');

-- 插入识别记录（模拟多用户的识别历史数据）
INSERT INTO `record` (`uid`,`imgpath`,`imgname`,`lang`,`result`,`confidence`,`status`,`createdat`) VALUES
(3,'uploads/2026/01/rec_001.jpg','合同扫描件.jpg','ch','甲方：北京科技有限公司\n乙方：上海信息技术有限公司\n合同金额：人民币壹拾万元整\n签订日期：2026年1月18日',0.92,1,'2026-01-18 10:23:00'),
(3,'uploads/2026/01/rec_002.jpg','身份证正面.jpg','ch','姓名：张三\n性别：男\n民族：汉\n出生：1995年03月12日\n住址：北京市朝阳区',0.95,1,'2026-01-20 14:05:00'),
(4,'uploads/2026/01/rec_003.jpg','英文发票.jpg','en','Invoice No: INV-20260120\nDate: 2026-01-20\nAmount: $2,500.00\nPayment Due: 2026-02-20',0.97,1,'2026-01-20 16:30:00'),
(3,'uploads/2026/02/rec_004.jpg','模糊照片.jpg','ch','识别结果不清晰，请重新上传',0.31,2,'2026-02-05 09:10:00'),
(5,'uploads/2026/02/rec_005.jpg','营业执照.jpg','ch','统一社会信用代码：91110105MA001X0X0X\n名称：王五电子商务有限公司\n类型：有限责任公司\n法定代表人：王五\n注册资本：100万元',0.89,1,'2026-02-08 11:45:00'),
(4,'uploads/2026/02/rec_006.jpg','产品说明书.jpg','ch','产品名称：智能温控器\n型号：TC-2026A\n额定电压：220V\n额定功率：500W\n使用温度：-10℃~60℃',0.91,1,'2026-02-12 15:20:00'),
(6,'uploads/2026/02/rec_007.jpg','会议纪要.jpg','ch','会议时间：2026年2月20日\n会议地点：总公司三楼会议室\n参会人员：部门负责人\n主要议题：2026年度工作规划',0.88,1,'2026-02-20 17:00:00'),
(5,'uploads/2026/03/rec_008.jpg','表格截图.png','ch','序号  姓名  部门  职位\n1  张三  技术部  工程师\n2  李四  市场部  经理\n3  王五  财务部  专员',0.86,1,'2026-03-01 10:00:00'),
(3,'uploads/2026/03/rec_009.jpg','火车票.jpg','ch','始发站：北京南\n终到站：上海虹桥\nG1次  2026年03月05日  07:00开\n二等座 05车08A号\n票价：553.0元',0.94,1,'2026-03-05 08:30:00'),
(7,'uploads/2026/03/rec_010.jpg','快递单.jpg','ch','快递单号：SF1234567890\n寄件人：钱七  手机：138****0000\n收件人：赵六  手机：139****1111\n地址：上海市浦东新区张江高科技园区',0.90,1,'2026-03-10 13:25:00'),
(4,'uploads/2026/03/rec_011.jpg','英文报告.jpg','en','Annual Report 2026\nRevenue: $10.5 Million\nNet Profit: $2.3 Million\nGrowth Rate: 18.5%',0.96,1,'2026-03-15 09:40:00'),
(6,'uploads/2026/04/rec_012.jpg','手写便签.jpg','ch','明天开会记得带资料\n下午3点准时到场\n联系电话13800138000',0.72,1,'2026-04-01 08:50:00'),
(3,'uploads/2026/04/rec_013.jpg','银行流水.jpg','ch','账户：621226****1234\n2026-04-02  转账收入  +50000.00\n2026-04-03  消费支出  -1200.00\n余额：98800.00元',0.93,1,'2026-04-02 10:15:00'),
(5,'uploads/2026/04/rec_014.jpg','毕业证书.jpg','ch','毕业证书\n兹证明张同学于2022年6月\n完成计算机科学与技术专业本科学习\n经审核符合毕业条件，准予毕业',0.91,1,'2026-04-05 14:30:00'),
(7,'uploads/2026/04/rec_015.jpg','处理中示例.png','ch',NULL,0.00,0,'2026-04-10 09:00:00');

-- 插入操作日志
INSERT INTO `oplog` (`uid`,`action`,`detail`,`ip`,`createdat`) VALUES
(1,'用户登录','管理员admin登录系统','192.168.1.1','2026-01-01 08:05:00'),
(1,'修改配置','修改OCR识别阈值为0.5','192.168.1.1','2026-01-01 08:10:00'),
(1,'添加用户','创建普通用户 zhangsan','192.168.1.1','2026-01-10 10:05:00'),
(1,'添加用户','创建普通用户 lisi','192.168.1.1','2026-01-12 14:35:00'),
(3,'用户登录','用户zhangsan登录系统','192.168.1.100','2026-01-18 10:20:00'),
(3,'上传识别','上传图片 合同扫描件.jpg 识别成功','192.168.1.100','2026-01-18 10:23:00'),
(3,'上传识别','上传图片 身份证正面.jpg 识别成功','192.168.1.100','2026-01-20 14:05:00'),
(4,'用户登录','用户lisi登录系统','192.168.1.101','2026-01-20 16:28:00'),
(4,'上传识别','上传图片 英文发票.jpg 识别成功','192.168.1.101','2026-01-20 16:30:00'),
(1,'禁用用户','禁用用户 sunba 账号','192.168.1.1','2026-02-16 09:00:00'),
(5,'上传识别','上传图片 营业执照.jpg 识别成功','192.168.1.102','2026-02-08 11:45:00'),
(3,'上传识别','上传图片 模糊照片.jpg 识别失败，置信度过低','192.168.1.100','2026-02-05 09:10:00'),
(6,'修改信息','用户zhaoliu修改个人邮箱','192.168.1.103','2026-02-20 17:05:00'),
(2,'查看日志','管理员manager查看操作日志列表','192.168.1.2','2026-03-01 09:00:00'),
(2,'导出日志','管理员manager导出2026年1月日志数据','192.168.1.2','2026-03-01 09:10:00'),
(1,'清空日志','管理员清空2025年全部历史日志','192.168.1.1','2026-03-05 10:00:00'),
(3,'删除记录','用户zhangsan删除识别记录ID=4','192.168.1.100','2026-03-06 08:40:00'),
(7,'上传识别','上传图片 快递单.jpg 识别成功','192.168.1.104','2026-03-10 13:25:00'),
(4,'导出结果','用户lisi导出识别结果为TXT','192.168.1.101','2026-03-16 10:00:00'),
(1,'修改配置','修改批量上传数量上限为20','192.168.1.1','2026-04-01 08:00:00'),
(6,'上传识别','上传图片 手写便签.jpg 识别成功','192.168.1.103','2026-04-01 08:50:00'),
(3,'上传识别','上传图片 银行流水.jpg 识别成功','192.168.1.100','2026-04-02 10:15:00'),
(5,'上传识别','上传图片 毕业证书.jpg 识别成功','192.168.1.102','2026-04-05 14:30:00'),
(7,'用户登录','用户qianqi登录系统','192.168.1.104','2026-04-10 08:55:00'),
(7,'上传识别','上传图片 处理中示例.png 等待识别','192.168.1.104','2026-04-10 09:00:00');


